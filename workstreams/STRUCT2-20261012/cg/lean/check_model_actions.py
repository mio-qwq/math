#!/usr/bin/env python3
"""Check new explicit action/encoding formulas against literal CG CDC edges.

This does not search the full automorphism group. Universal exhaustiveness
and exact cardinality are proved by the supplied Lean inverse maps.
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


def action(n, a, positive, swap, v):
    size, csize = 6 * n, 2 * n
    layer, t = divmod(v, size)
    if layer == 3:
        return 3 * size + ((a + t) if positive else (a - t)) % csize
    u = ((a + t) if positive else (a - t)) % size
    return (layer ^ swap if layer < 2 else layer) * size + u


def actual_mapping(n, a, positive, swap, bridge):
    return tuple(bridge.to_cover(n, action(n, a, positive, swap, bridge.from_cover(n, v)))
                 for v in range(20 * n))


def is_automorphism(graph, mapping):
    return (set(mapping) == set(range(len(graph))) and
            all({mapping[w] for w in graph[v]} == graph[mapping[v]]
                for v in range(len(graph))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    original_path = root.parent / 'independent/check_original_definition.py'
    bridge_path = root / 'check_coordinate_bridge.py'
    original = import_path('literal_cg_definition', original_path)
    bridge = import_path('coordinate_bridge', bridge_path)
    start = time.perf_counter()
    packed = 0
    for n in range(1, 102, 2):
        for code in range(24 * n):
            a, tail = divmod(code, 4)
            positive, swap = divmod(tail, 2)
            assert a < 6 * n
            assert code == 4 * a + 2 * positive + swap
            assert positive == int(code % 4 >= 2)
            assert swap == int(code % 2 == 1)
            packed += 1
    rows = []
    for n in (1, 3, 5, 7, 9, 31, 101):
        graph = original.cdc(original.source_graph(n))
        shifts = range(6 * n) if n <= 9 else sorted({0, 1, 2, 3*n-1, 3*n, 6*n-2, 6*n-1})
        images = set()
        tested = 0
        for a in shifts:
            for positive in (0, 1):
                for swap in (0, 1):
                    mapping = actual_mapping(n, a, positive, swap, bridge)
                    assert is_automorphism(graph, mapping)
                    images.add(mapping)
                    for t in range(6 * n):
                        p = ((a + t) if positive else (a - t)) % (6 * n)
                        centre = ((a % (2 * n) + t % (2 * n)) if positive
                                  else (a % (2 * n) - t % (2 * n))) % (2 * n)
                        assert p % (2 * n) == centre
                    zero = bridge.to_cover(n, 0)
                    one = bridge.to_cover(n, 1)
                    zero_model = bridge.from_cover(n, mapping[zero])
                    one_model = bridge.from_cover(n, mapping[one])
                    ring0, image0 = divmod(zero_model, 6 * n)
                    ring1, image1 = divmod(one_model, 6 * n)
                    assert (image0, int((image0 + 1) % (6 * n) == image1), ring0) == (a, positive, swap)
                    assert ring1 == ring0
                    tested += 1
        assert len(images) == tested
        rows.append({'n': n, 'all_shifts_tested': n <= 9,
                     'shifts_tested': len(shifts), 'distinct_actual_automorphisms': tested,
                     'all_original_adjacencies_and_residue_checks': True})
    # Damaging one image breaks actual original adjacency; no typed model is consulted.
    n = 3
    graph = original.cdc(original.source_graph(n))
    damaged = list(actual_mapping(n, 0, 1, 0, bridge))
    damaged[0], damaged[2] = damaged[2], damaged[0]
    assert not is_automorphism(graph, damaged)
    report = {'utc': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(),
              'seconds': round(time.perf_counter() - start, 6),
              'source_sha256': digest(__file__),
              'original_definition_sha256': digest(original_path),
              'coordinate_bridge_sha256': digest(bridge_path),
              'lean_sources': {s: digest(root / s) for s in ['CycleActions.lean', 'ModelActions.lean']},
              'pack_unpack_codes_checked': packed, 'cases': rows,
              'damage_controls_detected': 1, 'success': True,
              'scope': 'Finite explicit-family checks only; n=1 is a proper subgroup, '
                       'and full automorphism exhaustion/cardinality for odd n>=3 comes from Lean, not this program.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS:', len(rows), 'orders;', sum(r['distinct_actual_automorphisms'] for r in rows),
          'actual actions;', packed, 'numeric codes;', report['seconds'], 'seconds')


if __name__ == '__main__':
    main()
