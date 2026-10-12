#!/usr/bin/env python3
"""Small exact regressions for the unique simple-theta maximizer.

The direct count is obtained from graph labels on a constructed spanning tree.
It does not evaluate T, import a discovery program, or assume a compression
inequality. Binomial boundary counts enter only after the direct enumeration.
The universal proof is reviewed separately in MAXIMIZERS_REVIEW.md.
"""

from collections import Counter, deque
from fractions import Fraction
from itertools import product
from math import comb
import json


def graph_from_lengths(lengths):
    if len(lengths) != 3 or any(x < 1 for x in lengths):
        raise ValueError("three positive lengths are required")
    if lengths.count(1) > 1:
        raise ValueError("repeated length-one paths duplicate a simple edge")
    edges = []
    next_vertex = 2
    for length in lengths:
        path = [0] + list(range(next_vertex, next_vertex + length - 1)) + [1]
        edges.extend(tuple(sorted(pair)) for pair in zip(path, path[1:]))
        next_vertex += length - 1
    assert len(set(edges)) == len(edges) == sum(lengths)
    assert next_vertex == sum(lengths) - 1
    adjacency = [[] for _ in range(next_vertex)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    return edges, adjacency


def direct_facets(lengths):
    edges, adjacency = graph_from_lengths(lengths)
    n = len(adjacency)
    parent = [None] * n
    parent[0] = -1
    order = []
    queue = deque([0])
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in adjacency[u]:
            if parent[v] is None:
                parent[v] = u
                queue.append(v)
    assert len(order) == n
    by_endpoint = Counter()
    non_lipschitz = 0
    inactive_disconnected = 0
    # Every normalized Lipschitz integer labeling has exactly one word of
    # increments on this fixed tree, so this finite traversal is exhaustive.
    for word in product((-1, 0, 1), repeat=n - 1):
        labels = [0] * n
        for v, delta in zip(order[1:], word):
            labels[v] = labels[parent[v]] + delta
        if any(abs(labels[u] - labels[v]) > 1 for u, v in edges):
            non_lipschitz += 1
            continue
        seen = {0}
        stack = [0]
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in seen and abs(labels[u] - labels[v]) == 1:
                    seen.add(v)
                    stack.append(v)
        if len(seen) == n:
            by_endpoint[labels[1]] += 1
        else:
            inactive_disconnected += 1
    assert sum(by_endpoint.values()) > 0
    assert inactive_disconnected > 0
    assert all(by_endpoint[t] == by_endpoint[-t] for t in by_endpoint)
    assert sum(by_endpoint.values()) + non_lipschitz + inactive_disconnected == 3 ** (n - 1)
    return {
        "lengths": list(lengths),
        "vertices": n,
        "edges": len(edges),
        "facet_count": sum(by_endpoint.values()),
        "facets_by_second_endpoint": dict(sorted(by_endpoint.items())),
        "rejected_non_lipschitz": non_lipschitz,
        "rejected_disconnected_active_edges": inactive_disconnected,
    }


def legal_sorted_triples(n):
    for a in range(1, n + 2):
        for b in range(a, n + 2):
            c = n + 1 - a - b
            if c >= b and [a, b, c].count(1) <= 1:
                yield (a, b, c)


def predicted_triple(n):
    if n % 2 == 0:
        k = n // 2
        lengths = (k, k, 1) if k % 2 == 0 else (k + 1, k - 1, 1)
    else:
        k = (n + 1) // 2
        lengths = (k - 1, k - 1, 2) if k % 2 == 0 else (k, k - 2, 2)
    return tuple(sorted(lengths))


def closed_value(n):
    k = n // 2 if n % 2 == 0 else (n + 1) // 2
    if k % 2 == 0:
        central = comb(k, k // 2)
        return (Fraction(k * k + 2, 2) if n % 2 == 0
                else Fraction(k * k - 2 * k + 6, 4)) * central ** 2
    central = comb(k - 1, (k - 1) // 2)
    return (Fraction(2 * k * (k * k + 1), k + 1) if n % 2 == 0
            else Fraction(k * (k * k - 2 * k + 5), k + 1)) * central ** 2


def main():
    per_order = []
    all_rows = []
    for n in range(4, 9):
        rows = [direct_facets(t) for t in legal_sorted_triples(n)]
        best = max(row["facet_count"] for row in rows)
        winners = [tuple(row["lengths"]) for row in rows if row["facet_count"] == best]
        assert winners == [predicted_triple(n)]
        exact = closed_value(n)
        assert exact.denominator == 1 and best == exact
        per_order.append({"vertices": n, "legal_unordered_triples": len(rows),
                          "unique_maximizer": list(winners[0]), "facet_count": best})
        all_rows.extend(rows)
    try:
        graph_from_lengths((1, 1, 3))
    except ValueError:
        duplicate_control = "rejected"
    else:
        raise AssertionError("illegal simple-domain control accepted")
    counts = {tuple(row["lengths"]): row["facet_count"] for row in all_rows}
    # Each inequality is witnessed by a direct graph count at both ends.
    comparisons = {
        "even_compression_x_equals_2": ((2, 2, 3), (1, 2, 4)),
        "odd_compression_y_equals_1": ((1, 3, 4), (2, 3, 3)),
        "even_boundary_balancing": ((1, 2, 6), (1, 4, 4)),
        "odd_boundary_balancing": ((1, 2, 5), (2, 3, 3)),
        "all_even_exclusion": ((2, 2, 2), (1, 2, 3)),
        "all_odd_exclusion": ((1, 3, 3), (1, 2, 4)),
    }
    controls = []
    for name, (left, right) in comparisons.items():
        assert counts[left] < counts[right]
        controls.append({"name": name, "from": list(left), "to": list(right),
                         "from_count": counts[left], "to_count": counts[right]})
    print(json.dumps({"method": "graph construction and spanning-tree integer-label enumeration",
                      "finite_vertex_window": [4, 8], "per_order": per_order,
                      "strict_comparison_controls": controls,
                      "duplicate_length_one_control": duplicate_control,
                      "graphs": all_rows}, indent=2))


if __name__ == "__main__":
    main()
