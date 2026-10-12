#!/usr/bin/env python3
"""Exact small regressions from Mizzi v3 Definition 6.1.

Python standard library only. No project discovery code or precomputed
automorphism lists are imported. The automorphism search is complete paired
colour refinement with individualization; it does not assume the proposed
dihedral group, ring vertex types, or any group-order formula.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict, deque
import hashlib
import json
from pathlib import Path
import platform
import sys
import time


def edge(graph: list[set[int]], x: int, y: int) -> None:
    assert x != y
    graph[x].add(y)
    graph[y].add(x)


def source_graph(n: int) -> list[set[int]]:
    """Literal Definition 6.1: ring, n centres, three named leaves per centre."""
    graph = [set() for _ in range(10 * n)]
    for t in range(6 * n):
        edge(graph, t, (t + 1) % (6 * n))
    for i in range(n):
        for j in range(3):
            leaf = 7 * n + 3 * i + j
            edge(graph, 6 * n + i, leaf)
            edge(graph, leaf, i + j * n)
            edge(graph, leaf, i + j * n + 3 * n)
    return graph


def cdc(graph: list[set[int]]) -> list[set[int]]:
    result = [set() for _ in range(2 * len(graph))]
    for x, neighbors in enumerate(graph):
        for y in neighbors:
            edge(result, 2 * x, 2 * y + 1)
    return result


def coordinate_model(n: int) -> tuple[list[set[int]], tuple[int, ...]]:
    """Build the independently derived model and its map into the literal CDC."""
    size, h, k = 6 * n, 2 * n, 3 * n
    graph = [set() for _ in range(3 * size + h)]
    mapping = [-1] * len(graph)
    for t in range(size):
        edge(graph, t, (t + 1) % size)
        edge(graph, size + t, size + (t + 1) % size)
        edge(graph, t, 2 * size + t)
        edge(graph, size + t, 2 * size + t)
        edge(graph, 2 * size + t, 3 * size + t % h)
        a = t % k
        leaf = 7 * n + 3 * (a % n) + a // n
        mapping[t] = 2 * t + t % 2
        mapping[size + t] = 2 * ((t + k) % size) + t % 2
        mapping[2 * size + t] = 2 * leaf + 1 - t % 2
    for s in range(h):
        mapping[3 * size + s] = 2 * (6 * n + s % n) + s % 2
    return graph, tuple(mapping)


def is_isomorphism(
    first: list[set[int]], second: list[set[int]], mapping: tuple[int, ...]
) -> bool:
    return (
        len(first) == len(second) == len(mapping)
        and set(mapping) == set(range(len(second)))
        and all(
            {mapping[w] for w in first[v]} == second[mapping[v]]
            for v in range(len(first))
        )
    )


def connected(graph: list[set[int]]) -> bool:
    seen, todo = {0}, deque([0])
    while todo:
        for w in graph[todo.popleft()]:
            if w not in seen:
                seen.add(w)
                todo.append(w)
    return len(seen) == len(graph)


def cycles(graph: list[set[int]], length: int) -> list[tuple[int, ...]]:
    """Enumerate each undirected simple cycle once, using minimum/orientation."""
    result: list[tuple[int, ...]] = []
    for start in range(len(graph)):
        path = [start]

        def visit(vertex: int, used: int) -> None:
            if len(path) == length:
                if start in graph[vertex] and path[1] < path[-1]:
                    result.append(tuple(path))
                return
            for w in sorted(graph[vertex]):
                if w > start and not (used >> w) & 1:
                    path.append(w)
                    visit(w, used | (1 << w))
                    path.pop()

        visit(start, 1 << start)
    return result


def vertex_signatures(graph: list[set[int]]) -> list[tuple[int, int]]:
    incidence = Counter(v for cycle in cycles(graph, 6) for v in cycle)
    return [(len(graph[v]), incidence[v]) for v in range(len(graph))]


def isomorphisms(
    first: list[set[int]],
    second: list[set[int]],
    stop_after: int | None = None,
) -> tuple[list[tuple[int, ...]], dict[str, int | bool]]:
    """Exact paired individualization/refinement, with no proposed-group input.

    Refinement uses only graph-isomorphism invariants. If a colour cell is
    non-singleton, an isomorphism must send its chosen source vertex to
    exactly one target vertex in that cell; all such choices are explored.
    At a discrete leaf the resulting unique permutation is checked on
    complete adjacency lists. This proves enumeration completeness.
    """
    stats: dict[str, int | bool] = {
        "nodes": 0, "discrete_leaves": 0, "pruned": 0,
        "maximum_depth": 0, "complete": True,
    }
    if len(first) != len(second):
        return [], stats
    signatures_a, signatures_b = vertex_signatures(first), vertex_signatures(second)
    vocabulary = {s: i for i, s in enumerate(sorted(set(signatures_a + signatures_b)))}
    initial_a = tuple(vocabulary[s] for s in signatures_a)
    initial_b = tuple(vocabulary[s] for s in signatures_b)
    found: list[tuple[int, ...]] = []

    def refine(a: tuple[int, ...], b: tuple[int, ...]):
        while True:
            if Counter(a) != Counter(b):
                return None
            sig_a = [(a[v], tuple(sorted(a[w] for w in first[v]))) for v in range(len(a))]
            sig_b = [(b[v], tuple(sorted(b[w] for w in second[v]))) for v in range(len(b))]
            vocab = {s: i for i, s in enumerate(sorted(set(sig_a + sig_b)))}
            next_a = tuple(vocab[s] for s in sig_a)
            next_b = tuple(vocab[s] for s in sig_b)
            if Counter(next_a) != Counter(next_b):
                return None
            if len(vocab) == len(set(a)):
                return next_a, next_b
            a, b = next_a, next_b

    def search(a: tuple[int, ...], b: tuple[int, ...], depth: int) -> None:
        stats["nodes"] += 1
        stats["maximum_depth"] = max(stats["maximum_depth"], depth)
        state = refine(a, b)
        if state is None:
            stats["pruned"] += 1
            return
        a, b = state
        cells_a: dict[int, list[int]] = defaultdict(list)
        cells_b: dict[int, list[int]] = defaultdict(list)
        for v, color in enumerate(a):
            cells_a[color].append(v)
        for v, color in enumerate(b):
            cells_b[color].append(v)
        nonsingletons = [(len(vertices), color) for color, vertices in cells_a.items() if len(vertices) > 1]
        if not nonsingletons:
            stats["discrete_leaves"] += 1
            mapping = tuple(cells_b[color][0] for color in a)
            if is_isomorphism(first, second, mapping):
                found.append(mapping)
            return
        _, color = min(nonsingletons)
        source = cells_a[color][0]
        fresh = max(a + b) + 1
        next_a = list(a)
        next_a[source] = fresh
        for target in cells_b[color]:
            if stop_after is not None and len(found) >= stop_after:
                stats["complete"] = False
                return
            next_b = list(b)
            next_b[target] = fresh
            search(tuple(next_a), tuple(next_b), depth + 1)

    search(initial_a, initial_b, 0)
    assert len(set(found)) == len(found)
    return found, stats


def inverse(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for x, y in enumerate(permutation):
        result[y] = x
    return tuple(result)


def conjugate(p: tuple[int, ...], g: tuple[int, ...]) -> tuple[int, ...]:
    inv = inverse(p)
    return tuple(p[g[inv[v]]] for v in range(len(p)))


def folding(cover: list[set[int]], involution: tuple[int, ...]) -> list[set[int]]:
    total = len(cover)
    assert is_isomorphism(cover, cover, involution)
    assert all(involution[involution[v]] == v for v in range(total))
    assert all((involution[v] ^ v) & 1 for v in range(total))
    assert all(involution[v] not in cover[v] for v in range(total)), "loop-producing guide"
    base = [
        {j for j in range(total // 2) if involution[2 * j] in cover[2 * i]}
        for i in range(total // 2)
    ]
    assert all(i not in base[i] and all(i in base[j] for j in base[i]) for i in range(len(base)))
    mapping = tuple(v if v % 2 == 0 else involution[v] + 1 for v in range(total))
    assert is_isomorphism(cover, cdc(base), mapping)
    return base


def graph_hash(graph: list[set[int]]) -> str:
    data = json.dumps([sorted(neighbors) for neighbors in graph], separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


def check_parameter(n: int) -> dict:
    start = time.perf_counter()
    base = source_graph(n)
    cover = cdc(base)
    model, coordinate_map = coordinate_model(n)
    assert is_isomorphism(model, cover, coordinate_map)
    assert connected(base) and connected(cover)
    assert all(len(neighbors) == 3 for neighbors in base + cover)
    assert len({frozenset(neighbors) for neighbors in cover}) == len(cover)
    hexagons = cycles(cover, 6)
    incidence = Counter(v for cycle in hexagons for v in cycle)
    centre_counts = [incidence[2 * (6 * n + i) + e] for i in range(n) for e in (0, 1)]
    automorphisms, auto_stats = isomorphisms(cover, cover)
    assert auto_stats["complete"]
    switching = [
        p for p in automorphisms
        if all(p[p[v]] == v and (p[v] ^ v) & 1 for v in range(len(cover)))
    ]
    strong = [p for p in switching if all(p[v] not in cover[v] for v in range(len(cover)))]
    remaining = set(strong)
    classes = []
    while remaining:
        representative = min(remaining)
        orbit = {conjugate(p, representative) for p in automorphisms}
        assert orbit <= remaining
        classes.append((representative, orbit))
        remaining -= orbit
    records, folds = [], []
    for representative, orbit in classes:
        quotient = folding(cover, representative)
        assert connected(quotient)
        folds.append(quotient)
        quotient_automorphisms, quotient_stats = isomorphisms(quotient, quotient)
        assert quotient_stats["complete"]
        centralizer = [
            p for p in automorphisms
            if all(p[representative[v]] == representative[p[v]] for v in range(len(cover)))
        ]
        assert len(centralizer) == 2 * len(quotient_automorphisms)
        assert len(orbit) * len(centralizer) == len(automorphisms)
        records.append({
            "class_size": len(orbit),
            "representative": list(representative),
            "centralizer_order": len(centralizer),
            "base_automorphism_order": len(quotient_automorphisms),
            "base_triangles": len(cycles(quotient, 3)),
            "base_adjacency_sha256": graph_hash(quotient),
            "equals_original_labelled_base": quotient == base,
            "base_automorphism_search": quotient_stats,
        })
    comparisons = []
    for i in range(len(folds)):
        for j in range(i + 1, len(folds)):
            found, stats = isomorphisms(folds[i], folds[j], stop_after=1)
            assert not found and stats["complete"]
            comparisons.append({"classes": [i, j], "isomorphic": False, "search": stats})
    assert sum(record["equals_original_labelled_base"] for record in records) == 1
    if n >= 3:
        assert len(automorphisms) == 24 * n
        assert len(strong) == 3 * n + 2
        assert sorted(len(orbit) for _, orbit in classes) == [1, 1, 3 * n]
        assert set(centre_counts) == {0}
        assert len(hexagons) == 6 * n
        assert sorted(record["base_automorphism_order"] for record in records) == [4, 12 * n, 12 * n]
    else:
        assert n == 1
        assert len(automorphisms) == 240 and len(strong) == 11
        assert sorted(len(orbit) for _, orbit in classes) == [1, 10]
        assert all(count > 0 for count in centre_counts)
    controls = {}
    if n == 3:
        damaged = [set(neighbors) for neighbors in base]
        damaged[0].remove(1)
        damaged[1].remove(0)
        controls["removed_original_ring_edge_rejected"] = not is_isomorphism(model, cdc(damaged), coordinate_map)
        damaged_map = list(coordinate_map)
        damaged_map[0], damaged_map[1] = damaged_map[1], damaged_map[0]
        controls["swapped_coordinate_images_rejected"] = not is_isomorphism(model, cover, tuple(damaged_map))
        forbidden = next(p for p in switching if p not in set(strong))
        try:
            folding(cover, forbidden)
        except AssertionError as exc:
            controls["adjacent_image_involution_rejected"] = str(exc) == "loop-producing guide"
        else:
            controls["adjacent_image_involution_rejected"] = False
        assert all(controls.values()) and len(controls) == 3
    return {
        "n": n, "base_vertices": len(base), "cover_vertices": len(cover),
        "cover_edges": sum(map(len, cover)) // 2,
        "cover_adjacency_sha256": graph_hash(cover),
        "coordinate_map_checked_all_adjacency_lists": True,
        "six_cycles": len(hexagons),
        "centre_six_cycle_incidence": centre_counts,
        "automorphism_count": len(automorphisms),
        "automorphism_search": auto_stats,
        "switching_involutions": len(switching),
        "strong_switching_involutions": len(strong),
        "conjugacy_classes": records,
        "pairwise_base_isomorphism_checks": comparisons,
        "negative_controls": controls,
        "seconds": round(time.perf_counter() - start, 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parameters", nargs="*", type=int, default=[1, 3, 5, 7])
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("check_results.json"))
    args = parser.parse_args()
    assert all(n >= 1 and n % 2 == 1 for n in args.parameters)
    results = {
        "source": "Mizzi arXiv:2603.27559v3 Definition 6.1",
        "python": sys.version,
        "platform": platform.platform(),
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "Finite exact regressions; the all-parameter theorem is a separate written proof.",
        "parameters": [],
    }
    for n in args.parameters:
        record = check_parameter(n)
        results["parameters"].append(record)
        args.output.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
        print(
            f"n={n}: Aut={record['automorphism_count']} "
            f"strong={record['strong_switching_involutions']} "
            f"classes={[item['class_size'] for item in record['conjugacy_classes']]} "
            f"base_Aut={[item['base_automorphism_order'] for item in record['conjugacy_classes']]} "
            f"C6={record['six_cycles']} seconds={record['seconds']}",
            flush=True,
        )


if __name__ == "__main__":
    main()
