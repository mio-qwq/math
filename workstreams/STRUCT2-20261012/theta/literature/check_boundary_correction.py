#!/usr/bin/env python3
"""Exact definition-based diagnostics for the displayed Proposition 30 identities.

No external dependencies. This enumerates graph labelings, not the F summation.
It is a finite regression; the universal proof is in PROPOSITION30_CORRECTION.md.
"""

from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb
import json


def theta_edges(lengths):
    if len(lengths) != 3 or any(x < 1 for x in lengths):
        raise ValueError("three positive path lengths required")
    if lengths.count(1) > 1:
        raise ValueError("duplicate length-one paths do not give a simple theta")
    edges = []
    paths = []
    next_vertex = 2
    for length in lengths:
        path = [0] + list(range(next_vertex, next_vertex + length - 1)) + [1]
        next_vertex += length - 1
        edges.extend(zip(path, path[1:]))
        paths.append(path)
    if len({tuple(sorted(e)) for e in edges}) != len(edges):
        raise AssertionError("constructed graph has duplicate edges")
    assert len(edges) == sum(lengths)
    assert next_vertex == sum(lengths) - 1
    return next_vertex, edges, paths


def connected_active_graph(order, edges, labels):
    adjacency = [[] for _ in range(order)]
    for u, v in edges:
        delta = abs(labels[u] - labels[v])
        assert delta <= 1
        if delta == 1:
            adjacency[u].append(v)
            adjacency[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        for v in adjacency[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == order


def direct_boundary_count(a, b):
    order, edges, paths = theta_edges([a, b, 1])
    # Every allowed path labeling is determined by its sequence of increments.
    choices = []
    for length in [a, b]:
        by_sum = {-1: [], 0: [], 1: []}
        for increments in product((-1, 0, 1), repeat=length):
            total = sum(increments)
            if total in by_sum:
                by_sum[total].append(increments)
        choices.append(by_sum)
    counts = Counter()
    rejected = Counter()
    for t in (-1, 0, 1):
        for left, right in product(choices[0][t], choices[1][t]):
            labels = [None] * order
            labels[0], labels[1] = 0, t
            for path, increments in zip(paths[:2], (left, right)):
                current = 0
                for vertex, increment in zip(path[1:], increments):
                    current += increment
                    if labels[vertex] is not None:
                        assert labels[vertex] == current
                    labels[vertex] = current
            assert all(value is not None for value in labels)
            if connected_active_graph(order, edges, labels):
                counts[t] += 1
            else:
                rejected[t] += 1
    return {
        "lengths": [a, b, 1],
        "vertices": order,
        "edges": len(edges),
        "facets": sum(counts.values()),
        "facets_by_other_endpoint": dict(sorted(counts.items())),
        "disconnected_active_graphs_rejected": sum(rejected.values()),
    }


def arithmetic_m(n):
    # Arithmetic expression from Theorem 18; n=4 is handled numerically.
    if n < 4:
        raise ValueError("the simple bicyclic problem starts at n=4")
    k = n // 2 if n % 2 == 0 else (n + 1) // 2
    if k % 2 == 0:
        value = (k + 1) * (k - 1) * comb(k, k // 2) * comb(k - 2, (k - 2) // 2)
    else:
        value = k * k * comb(k - 1, (k - 1) // 2) ** 2
    return value * (2 if n % 2 == 0 else 1)


def main():
    results = []
    for k in (2, 4, 5, 6):
        a, b = (k, k) if k % 2 == 0 else (k + 1, k - 1)
        row = direct_boundary_count(a, b)
        closed = Fraction(a * b + 2, 2) * comb(a, a // 2) * comb(b, b // 2)
        assert closed.denominator == 1
        assert row["facets"] == closed
        assert row["disconnected_active_graphs_rejected"] > 0
        m = arithmetic_m(2 * k)
        actual = Fraction(row["facets"], m)
        correct = Fraction(k * k + (2 if k % 2 == 0 else 1), k * (k + 1))
        printed = Fraction(k * k + (1 if k % 2 == 0 else 2), k * (k + 1))
        assert actual == correct
        assert actual != printed
        assert actual <= 1
        row.update(k=k, arithmetic_M=m, actual_ratio=str(actual),
                   corrected_ratio=str(correct), printed_ratio=str(printed))
        results.append(row)
    try:
        theta_edges([2, 1, 1])
    except ValueError:
        duplicate_path_control = "rejected as outside simple theta domain"
    else:
        raise AssertionError("simple-graph domain control failed")
    print(json.dumps({"method": "normalized integer labels and active-edge connectivity",
                      "results": results,
                      "duplicate_path_control": duplicate_path_control}, indent=2))


if __name__ == "__main__":
    main()
