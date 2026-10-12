#!/usr/bin/env python3
"""Six-cycle checks from literal named CG edges, without a type restriction.

Only the frozen source_graph/cdc constructors are imported. The search
does not import the coordinate model or assume which vertices a cycle may
visit. Its small-depth enumeration is supplementary to the symbolic Lean
proof, not an all-parameter certificate.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import time


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cycles_at(graph, root):
    """Count undirected simple six-cycles containing root; retain a witness."""
    count, witness = 0, None
    path = [root]
    visited = {root}

    def search(v):
        nonlocal count, witness
        if len(path) == 6:
            if root in graph[v]:
                count += 1
                if witness is None:
                    witness = path.copy()
            return
        for w in sorted(graph[v]):
            if w not in visited:
                path.append(w)
                visited.add(w)
                search(w)
                visited.remove(w)
                path.pop()

    search(root)
    assert count % 2 == 0  # two orientations, with root fixed
    return count // 2, witness


def kind(n, v):
    base = v // 2
    return 'ring' if base < 6 * n else ('centre' if base < 7 * n else 'leaf')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--max-n', type=int, default=101)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    original = root.parent / 'independent/check_original_definition.py'
    spec = importlib.util.spec_from_file_location('literal_cg_definition', original)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    start = time.perf_counter()
    rows = []
    exception = None
    for n in range(1, args.max_n + 1, 2):
        graph = module.cdc(module.source_graph(n))
        histograms = {k: Counter() for k in ('ring', 'centre', 'leaf')}
        for v in range(len(graph)):
            count, witness = cycles_at(graph, v)
            histograms[kind(n, v)][count] += 1
            if n >= 3:
                assert (count == 0) == (kind(n, v) == 'centre')
                assert count == (0 if kind(n, v) == 'centre' else 2)
            elif kind(n, v) == 'centre':
                assert count > 0
                if exception is None:
                    assert len(set(witness)) == 6
                    assert all(witness[(i + 1) % 6] in graph[witness[i]] for i in range(6))
                    exception = {'n': 1, 'original_centre_vertex': v, 'six_cycle': witness}
        rows.append({'n': n, 'vertices': len(graph),
                     'six_cycle_incidence_histograms': histograms,
                     'centre_iff_no_six_cycle': n >= 3})
    assert exception is not None
    # A deliberately damaged original graph fails the observed incidence count.
    damaged = module.cdc(module.source_graph(3))
    for w in list(damaged[0]):
        damaged[w].remove(0)
    damaged[0].clear()
    assert cycles_at(damaged, 0)[0] == 0
    assert kind(3, 0) == 'ring'
    report = {'utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(),
              'seconds': round(time.perf_counter() - start, 6),
              'source_sha256': digest(__file__),
              'original_definition_sha256': digest(original),
              'lean_source_sha256': digest(root / 'SixCycleInvariant.lean'),
              'cases': rows, 'n_one_exception': exception,
              'controls_detected': ['n=1 centre exception', 'isolated damaged ring vertex'],
              'success': True,
              'scope': 'Finite original-adjacency cross-check; no automorphism search. '
                       'Exactly two cycle incidences at each noncentre is a finite observation here; '
                       'Lean proves existence/nonexistence and type invariance, not the complete six-cycle catalogue.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS:', len(rows), 'odd parameters; explicit n=1 exception and damage control;',
          report['seconds'], 'seconds')


if __name__ == '__main__':
    main()
