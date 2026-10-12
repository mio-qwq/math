#!/usr/bin/env python3
"""Compare the new universal coordinate definitions to literal named CG edges.

Only source_graph and cdc are reused from the frozen original-definition
checker. The half-split maps, inverses and deck are implemented afresh from
OddCoordinates. No automorphism search or expected group list is run.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import time


def half(a, m):
    return a + m if a < m else a - m


def reduce_half(a, m):
    return a if a < m else a - m


def join_half(a, b, m):
    return a if a % 2 == b else a + m


def to_cover(n, v):
    size, k = 6 * n, 3 * n
    if v < size:
        return 2 * v + v % 2
    if v < 2 * size:
        t = v - size
        return 2 * half(t, k) + t % 2
    if v < 3 * size:
        t = v - 2 * size
        a = reduce_half(t, k)
        leaf = 7 * n + 3 * (a % n) + a // n
        return 2 * leaf + 1 - t % 2
    s = v - 3 * size
    return 2 * (6 * n + reduce_half(s, n)) + s % 2


def from_cover(n, v):
    base, b = divmod(v, 2)
    size, k = 6 * n, 3 * n
    if base < size:
        return base if b == base % 2 else size + half(base, k)
    if base < 7 * n:
        return 3 * size + join_half(base - size, b, n)
    named = base - 7 * n
    i, j = divmod(named, 3)
    return 2 * size + join_half(i + n * j, 1 - b, k)


def model(n, damaged_centre=False):
    size, h = 6 * n, 2 * n
    graph = [set() for _ in range(20 * n)]

    def edge(a, b):
        assert a != b
        graph[a].add(b)
        graph[b].add(a)

    for t in range(size):
        nxt = t + 1 if t + 1 < size else 0
        edge(t, nxt)
        edge(size + t, size + nxt)
        edge(t, 2 * size + t)
        edge(size + t, 2 * size + t)
        edge(2 * size + t, 3 * size + t % (n if damaged_centre else h))
    return graph


def coordinate_deck(n, v):
    size, k = 6 * n, 3 * n
    if v < size:
        return size + half(v, k)
    if v < 2 * size:
        return half(v - size, k)
    if v < 3 * size:
        return 2 * size + half(v - 2 * size, k)
    return 3 * size + half(v - 3 * size, n)


def adjacency_matches(graph, cover, mapping):
    return (set(mapping) == set(range(len(cover))) and
            all({mapping[w] for w in graph[v]} == cover[mapping[v]]
                for v in range(len(graph))))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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
    for n in range(1, args.max_n + 1, 2):
        graph = model(n)
        source = module.source_graph(n)
        cover = module.cdc(source)
        mapping = tuple(to_cover(n, v) for v in range(20 * n))
        assert adjacency_matches(graph, cover, mapping)
        assert all(from_cover(n, to_cover(n, v)) == v for v in range(20 * n))
        assert all(to_cover(n, from_cover(n, v)) == v for v in range(20 * n))
        assert all(to_cover(n, coordinate_deck(n, v)) == (mapping[v] ^ 1)
                   for v in range(20 * n))
        for i in range(n):
            for j in range(3):
                a = i + n * j
                assert divmod(a, n) == (j, i)
                leaf = 7 * n + 3 * i + j
                assert source[leaf] == {6 * n + i, a, a + 3 * n}
        rows.append({'n': n, 'vertices': len(graph),
                     'edges': sum(map(len, graph)) // 2,
                     'mapping_sha256': hashlib.sha256(json.dumps(mapping).encode()).hexdigest(),
                     'all_adjacency_inverse_and_deck_checks': True})
    for n in (2, 4):
        assert len({to_cover(n, v) for v in range(20 * n)}) < 20 * n
    n = 3
    mapping = tuple(to_cover(n, v) for v in range(20 * n))
    assert not adjacency_matches(model(n, damaged_centre=True),
                                 module.cdc(module.source_graph(n)), mapping)
    damaged = module.source_graph(n)
    damaged[0].remove(1)
    damaged[1].remove(0)
    assert not adjacency_matches(model(n), module.cdc(damaged), mapping)
    report = {'utc': datetime.now(timezone.utc).isoformat(),
              'python': platform.python_version(), 'seconds': round(time.perf_counter() - start, 6),
              'source_sha256': digest(__file__), 'original_definition_sha256': digest(original),
              'lean_sources': {name: digest(root / name)
                               for name in ['OddCoordinates.lean', 'OddCoverIso.lean']},
              'cases': rows, 'damage_controls_detected': 4, 'success': True,
              'scope': 'Finite semantic cross-check only; the all-odd conclusion comes from the compiled Lean maps and adjacency iff.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS:', len(rows), 'odd parameters; 4 damage controls;', report['seconds'], 'seconds')


if __name__ == '__main__':
    main()
