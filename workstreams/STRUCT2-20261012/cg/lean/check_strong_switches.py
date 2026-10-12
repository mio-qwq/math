#!/usr/bin/env python3
"""Independent finite checks of the proved strong-switch parameter formula.

The checker uses literal CG canonical-double-cover adjacency and the explicit
coordinate action, but no graph-automorphism search or stored switch list.
Universal necessity and sufficiency remain the responsibility of Lean.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import time


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compose(p, q):
    return tuple(p[q[v]] for v in range(len(p)))


def inverse(p):
    result = [0] * len(p)
    for v, w in enumerate(p):
        result[w] = v
    return tuple(result)


def conjugate(p, g):
    return compose(compose(p, g), inverse(p))


def actually_strong(graph, p):
    return (all(p[p[v]] == v for v in range(len(p))) and
            all((p[v] & 1) != (v & 1) for v in range(len(p))) and
            all(p[v] not in graph[v] for v in range(len(p))))


def predicted(n, a, positive, swap):
    return (positive == 1 and a == 3 * n) or (
        positive == 0 and swap == 1 and a % 2 == 1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    original_path = root.parent / 'independent/check_original_definition.py'
    bridge_path = root / 'check_coordinate_bridge.py'
    actions_path = root / 'check_model_actions.py'
    original = import_path('literal_cg_strong', original_path)
    bridge = import_path('coordinate_bridge_strong', bridge_path)
    actions = import_path('model_actions_strong', actions_path)
    start = time.perf_counter()
    rows = []
    for n in (3, 5, 7, 9, 31, 101):
        graph = original.cdc(original.source_graph(n))
        automorphisms = {}
        strong = {}
        for a in range(6 * n):
            for positive in (0, 1):
                for swap in (0, 1):
                    key = (a, positive, swap)
                    p = actions.actual_mapping(n, a, positive, swap, bridge)
                    assert actions.is_automorphism(graph, p)
                    automorphisms[key] = p
                    observed = actually_strong(graph, p)
                    assert observed == predicted(n, a, positive, swap)
                    if observed:
                        strong[key] = p
        assert len(strong) == 3 * n + 2
        class_sizes = None
        if n <= 9:
            remaining = set(strong.values())
            classes = []
            while remaining:
                g = min(remaining)
                orbit = {conjugate(p, g) for p in automorphisms.values()}
                assert orbit <= set(strong.values())
                classes.append(orbit)
                remaining -= orbit
            class_sizes = sorted(map(len, classes))
            assert class_sizes == [1, 1, 3 * n]
        rows.append({'n': n, 'parameters_checked': 24 * n,
                     'strong_switches': len(strong),
                     'conjugacy_class_sizes': class_sizes,
                     'literal_adjacency_colour_and_involution_checks': True})

    # Three nearby false formulae are detected on the literal cover.
    n = 3
    graph = original.cdc(original.source_graph(n))
    assert not actually_strong(graph, actions.actual_mapping(n, 2, 0, 1, bridge))
    assert not actually_strong(graph, actions.actual_mapping(n, 1, 0, 0, bridge))
    assert not actually_strong(graph, actions.actual_mapping(n, 1, 1, 1, bridge))
    report = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'seconds': round(time.perf_counter() - start, 6),
        'source_sha256': digest(__file__),
        'dependencies': {str(p.name): digest(p) for p in
                         (original_path, bridge_path, actions_path)},
        'lean_source_sha256': digest(root / 'StrongSwitchClassification.lean'),
        'cases': rows,
        'parameters_checked': sum(row['parameters_checked'] for row in rows),
        'damage_controls_detected': 3,
        'success': True,
        'scope': ('Finite checks of the explicit 24n family against literal original CG CDCs. '
                  'Conjugacy was checked at n=3,5,7,9. Universal exhaustion and the iff '
                  'classification are established by Lean, not by this program.')
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS:', len(rows), 'orders;', report['parameters_checked'],
          'parameters; 3 damage controls;', report['seconds'], 'seconds')


if __name__ == '__main__':
    main()
