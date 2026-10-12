#!/usr/bin/env python3
"""Exact small-graph facet checks from Braun--Bruegge, Theorem 5.

The graph-level enumeration has no dependency on a binomial formula or on
any discovery code.  A separate local transcription of Corollary 25 is
used only after the graph counts have been completed, for comparison.
Python 3 standard library only.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import time
from collections import Counter, deque
from pathlib import Path


def validate_graph(order: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    if order < 2 or len(set(edges)) != len(edges):
        raise ValueError("bad order or duplicate edges")
    adj = [[] for _ in range(order)]
    for u, v in edges:
        if not 0 <= u < v < order:
            raise ValueError("edges must be normalized, simple, and in range")
        adj[u].append(v)
        adj[v].append(u)
    seen, pending = {0}, [0]
    for u in pending:
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                pending.append(v)
    if len(seen) != order:
        raise ValueError("graph must be connected")
    return [sorted(row) for row in adj]


def theta(lengths: tuple[int, int, int]) -> tuple[int, list[tuple[int, int]]]:
    if len(lengths) != 3 or any(type(x) is not int or x < 1 for x in lengths):
        raise ValueError("three positive integer lengths required")
    if lengths.count(1) > 1:
        raise ValueError("multiple length-one paths are not a simple theta")
    edges, nxt = [], 2
    for length in lengths:
        path = [0] + list(range(nxt, nxt + length - 1)) + [1]
        nxt += length - 1
        edges.extend(tuple(sorted(e)) for e in zip(path, path[1:]))
    edges.sort()
    assert nxt == sum(lengths) - 1
    assert len(edges) == sum(lengths) == nxt + 1
    validate_graph(nxt, edges)
    return nxt, edges


def rooted_tree(adj: list[list[int]], mode: str) -> list[tuple[int, int]]:
    """Return (parent, child) pairs in an order with parents assigned first."""
    if mode == "dfs":
        seen, tree = {0}, []

        def visit(u: int) -> None:
            for v in reversed(adj[u]):
                if v not in seen:
                    seen.add(v)
                    tree.append((u, v))
                    visit(v)

        visit(0)
        if len(seen) != len(adj):
            raise ValueError("disconnected graph")
        return tree
    if mode != "bfs":
        raise ValueError("tree method must be bfs or dfs")
    pending = deque([0])
    seen = {0}
    tree = []
    while pending:
        u = pending.popleft()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                tree.append((u, v))
                pending.append(v)
    if len(seen) != len(adj):
        raise ValueError("disconnected graph")
    return tree


def valid_facet(labels: tuple[int, ...] | list[int],
                edges: list[tuple[int, int]]) -> tuple[bool, bool]:
    """Return (Lipschitz, facet), applying both clauses of Theorem 5."""
    saturated = [[] for _ in labels]
    for u, v in edges:
        delta = abs(labels[u] - labels[v])
        if delta > 1:
            return False, False
        if delta == 1:
            saturated[u].append(v)
            saturated[v].append(u)
    seen, pending = {0}, [0]
    for u in pending:
        for v in saturated[u]:
            if v not in seen:
                seen.add(v)
                pending.append(v)
    return True, len(seen) == len(labels)


def enumerate_facets(order: int, edges: list[tuple[int, int]], mode="bfs") -> dict:
    adj = validate_graph(order, edges)
    tree = rooted_tree(adj, mode)
    facets, lipschitz = [], 0
    for increments in itertools.product((-1, 0, 1), repeat=order - 1):
        labels = [0] * order
        for (parent, child), delta in zip(tree, increments):
            labels[child] = labels[parent] + delta
        lip, facet = valid_facet(labels, edges)
        lipschitz += lip
        if facet:
            facets.append(tuple(labels))
    facets.sort()
    encoded = json.dumps(facets, separators=(",", ":")).encode()
    return {
        "order": order,
        "edges": edges,
        "spanning_tree": tree,
        "tree_method": mode,
        "tree_increment_assignments": 3 ** (order - 1),
        "lipschitz_assignments": lipschitz,
        "facets": len(facets),
        "endpoint_difference_histogram": dict(sorted(Counter(f[1] for f in facets).items())),
        "normalized_facet_labels_sha256": hashlib.sha256(encoded).hexdigest(),
    }


def row_coefficient(length: int, displacement: int) -> int:
    if length < 0 or (length + displacement) % 2:
        return 0
    up = (length + displacement) // 2
    return math.comb(length, up) if 0 <= up <= length else 0


def path_sum_F(lengths: tuple[int, int, int]) -> int:
    """Independent sum over the common endpoint displacement."""
    low = min(lengths)
    return sum(math.prod(row_coefficient(x, d) for x in lengths)
               for d in range(-low, low + 1))


def cycle_formula(length: int) -> int:
    if length < 2:
        raise ValueError("only cycles of length at least two are used here")
    if length % 2:
        return length * math.comb(length - 1, (length - 1) // 2)
    return math.comb(length, length // 2)


def corollary25(lengths: tuple[int, int, int]) -> tuple[int, str]:
    """Transcribe only the cases that correspond to simple three-path graphs."""
    theta(lengths)  # Reject the multigraph case (e, 1, 1).
    evens = sorted(x for x in lengths if x % 2 == 0)
    odds = sorted(x for x in lengths if x % 2 == 1)
    if not evens or not odds:
        return path_sum_F(lengths), "25(i)"
    if len(evens) == 2:
        a, b = evens
        c = odds[0]
        second = a * b * path_sum_F((a - 1, b - 1, c))
        if c == 1:
            return second + cycle_formula(a) * cycle_formula(b), "25(iii)"
        return c * path_sum_F((a, b, c - 1)) + second, "25(ii), two even"
    a, b = odds
    c = evens[0]
    first = c * path_sum_F((a, b, c - 1))
    if a == 1:
        return first + b * cycle_formula(b - 1) * cycle_formula(c), "25(iv)"
    return first + a * b * path_sum_F((a - 1, b - 1, c)), "25(ii), two odd"


def M_value(order: int) -> int:
    """Definition 12's numeric expression, as expanded in Theorem 18.

    At order 3 the expression is formal; no simple three-vertex, four-edge
    graph exists.  No such graph is constructed or asserted by this code.
    """
    if order < 3:
        raise ValueError("M expression starts at 3")
    if order % 2 == 0:
        return 2 * M_value(order - 1)
    k = (order + 1) // 2
    if k % 2:
        return k * k * math.comb(k - 1, (k - 1) // 2) ** 2
    return (k + 1) * (k - 1) * math.comb(k, k // 2) * math.comb(k - 2, (k - 2) // 2)


def damage_controls() -> dict:
    rejected = []
    for lengths in ((1, 1, 1), (1, 1, 2), (0, 2, 3), (-1, 3, 4)):
        try:
            theta(lengths)
        except ValueError:
            rejected.append(lengths)
        else:
            raise AssertionError("invalid simple-theta parameters accepted")
    n, edges = theta((1, 2, 2))
    assert valid_facet([0] * n, edges) == (True, False)
    bad_labels = [0] * n
    bad_labels[1] = 2
    assert valid_facet(bad_labels, edges) == (False, False)
    known = []
    for order, e, expected in (
        (4, [(0, 1), (1, 2), (2, 3)], 8),
        (3, [(0, 1), (0, 2), (1, 2)], 6),
        (4, [(0, 1), (0, 3), (1, 2), (2, 3)], 6),
        (5, [(0, 1), (0, 4), (1, 2), (2, 3), (3, 4)], 30),
    ):
        count = enumerate_facets(order, e)["facets"]
        assert count == expected
        known.append({"order": order, "edges": e, "facets": count})
    return {"invalid_parameters_rejected": rejected,
            "constant_labeling_rejected_by_connectivity": True,
            "edge_jump_two_rejected_by_Lipschitz": True,
            "tree_and_cycle_controls": known}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("actual_facet_checks.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    cases = ((1, 2, 2), (1, 2, 3), (1, 2, 4), (1, 3, 4),
             (1, 4, 4), (1, 4, 5), (1, 4, 6),
             (2, 2, 3), (2, 2, 5), (2, 3, 3), (2, 3, 4),
             (2, 3, 5), (2, 4, 5), (3, 3, 4), (3, 4, 4),
             (1, 3, 3), (2, 2, 2), (2, 2, 4), (3, 3, 3))
    report = {"method": "integer vertex labels via spanning-tree increments; Theorem 5",
              "source": "https://cs.uwaterloo.ca/journals/JIS/VOL26/Braun/braun6.pdf",
              "source_pdf_sha256": "52e4b28b4e4106af07768940e60bb06fdd76f638b288e0139ec7bc5c05dd397a",
              "python": platform.python_version(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "damage_controls": damage_controls(), "cases": []}
    for lengths in cases:
        order, edges = theta(lengths)
        result = enumerate_facets(order, edges)
        formula, formula_case = corollary25(lengths)
        assert result["facets"] == formula, (lengths, result["facets"], formula)
        assert result["facets"] <= M_value(order), lengths
        if lengths in ((1, 2, 2), (2, 3, 4), (3, 3, 4)):
            alternate = enumerate_facets(order, edges, "dfs")
            assert {tuple(sorted(e)) for e in alternate["spanning_tree"]} != {tuple(sorted(e)) for e in result["spanning_tree"]}
            assert alternate["normalized_facet_labels_sha256"] == result["normalized_facet_labels_sha256"]
            result["second_spanning_tree"] = alternate["spanning_tree"]
            result["second_spanning_tree_same_label_set"] = True
        result.update({"path_lengths": lengths, "corollary25_count": formula,
                       "corollary25_case": formula_case, "M": M_value(order)})
        report["cases"].append(result)
        print(f"{lengths}: n={order}, graph={result['facets']}, Cor25={formula}, M={M_value(order)}")
    report["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"PASS: {len(cases)} graph cases; {report['elapsed_seconds']} seconds")


if __name__ == "__main__":
    main()
