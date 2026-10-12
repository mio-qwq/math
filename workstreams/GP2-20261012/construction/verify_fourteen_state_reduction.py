#!/usr/bin/env python3
"""Exact checks for the fourteen-profile theorem; no solver or dependencies."""

from itertools import product
import json


PROFILES = [(a, b) for a in range(1, 5) for b in range(a + 1, 7)]


def h(profile, t):
    a, b = profile
    assert 1 <= a <= 4 and a < b <= 6
    return int(a <= t) + int(b <= t)


def allowed(u, v):
    a, b = u
    c, d = v
    return c <= a + 1 and (b >= 5 or d <= b + 1)


def marked(u, v):
    a, b = u
    c, d = v
    return c == 1 and b >= 5 and d <= a + 1


def max_target_walks(edges):
    previous = {p: 0 for p in PROFILES}
    columns = [previous]
    for _ in range(5):
        current = {p: -100 for p in PROFILES}
        for u, v, weight in edges:
            current[v] = max(current[v], previous[u] + weight)
        assert all(value >= 0 for value in current.values())
        columns.append(current)
        previous = current
    return columns


def full_graph_counts(code, r):
    """The five-step recurrence on the original full triple shift graph."""
    states = list(product(range(r), repeat=3))
    columns = [{s: 0 for s in states}]
    for _ in range(5):
        current = {s: -100 for s in states}
        for source in states:
            for letter in range(r):
                word = source + (letter,)
                target = word[1:]
                current[target] = max(
                    current[target], columns[-1][source] + int(word in code))
        columns.append(current)
    return columns


def literal_strict(code, r):
    return all(sum(word[t:t + 4] in code for t in range(5)) <= 2
               for word in product(range(r), repeat=8))


def canonical_assignment(code, r):
    columns = full_graph_counts(code, r)
    assert max(columns[5].values()) <= 2, "input is not a strict code"
    if not code:
        return {s: (4, 6) for s in columns[0]}, columns
    gamma = {}
    for s in columns[0]:
        a = next(t for t in range(1, 5) if columns[t][s] >= 1)
        b = next((t for t in range(1, 6) if columns[t][s] >= 2), 6)
        gamma[s] = (a, b)
        assert (a, b) in PROFILES
        assert [columns[t][s] for t in range(6)] == [h((a, b), t) for t in range(6)]
    return gamma, columns


def completion(code, r):
    gamma, columns = canonical_assignment(code, r)
    completed = set()
    for word in product(range(r), repeat=4):
        u, v = gamma[word[:3]], gamma[word[1:]]
        assert allowed(u, v)
        if marked(u, v):
            completed.add(word)
    assert code <= completed
    assert literal_strict(completed, r)
    if code:
        assert full_graph_counts(completed, r) == columns
        gamma2, _ = canonical_assignment(completed, r)
        assert gamma2 == gamma
    return completed, gamma


def expect_failure(label, action):
    try:
        action()
    except AssertionError:
        return label
    raise AssertionError("negative control accepted: " + label)


def assert_target_bound(edges):
    columns = max_target_walks(edges)
    assert max(columns[5].values()) <= 2


def main():
    assert len(PROFILES) == 14
    edges = []
    for u, v in product(PROFILES, repeat=2):
        direct_allowed = all(h(v, t) >= h(u, t - 1) for t in range(1, 6))
        direct_marked = all(h(v, t) >= h(u, t - 1) + 1 for t in range(1, 6))
        assert allowed(u, v) == direct_allowed
        assert marked(u, v) == direct_marked
        assert not marked(u, v) or allowed(u, v)
        if allowed(u, v):
            edges.append((u, v, int(marked(u, v))))
    assert len(edges) == 138
    assert sum(weight for _, _, weight in edges) == 20
    columns = max_target_walks(edges)
    for t, column in enumerate(columns):
        assert all(value <= h(p, t) for p, value in column.items())
    assert max(columns[5].values()) == 2

    cases = [
        (1, set()),
        (2, {(0, 0, 0, 1)}),
        (2, {(0, 0, 0, 1), (0, 0, 1, 1)}),
        (2, {(0, 0, 1, 0), (0, 1, 1, 0), (0, 1, 1, 1)}),
        (3, {(0, 0, 0, 1)}),
        (4, {(0, 1, 3, 2)}),
    ]
    example_results = []
    for r, code in cases:
        assert literal_strict(code, r)
        completed, gamma = completion(code, r)
        example_results.append({
            "alphabet_size": r,
            "input_code": [list(w) for w in sorted(code)],
            "completed_code": [list(w) for w in sorted(completed)],
            "used_profiles": [list(p) for p in sorted(set(gamma.values()))],
            "triple_states": r ** 3,
            "literal_eight_letter_checks": r ** 8,
            "profiles_preserved_when_nonempty": True,
        })

    controls = [
        expect_failure("invalid_equal_hit_times", lambda: h((4, 4), 5)),
        expect_failure("spurious_marked_loop", lambda: assert_target_bound(
            edges + [((1, 2), (1, 2), 1)])),
        expect_failure("nonstrict_constant_code", lambda: canonical_assignment(
            {(0, 0, 0, 0)}, 2)),
    ]
    report = {
        "status": "PASS",
        "profiles": [list(p) for p in PROFILES],
        "allowed_arcs": len(edges),
        "marked_arcs": sum(weight for _, _, weight in edges),
        "target_edges": [[PROFILES.index(u), PROFILES.index(v), weight]
                         for u, v, weight in edges],
        "target_F0_through_F5": [[column[p] for column in columns] for p in PROFILES],
        "examples": example_results,
        "negative_controls": controls,
        "scope": "finite semantics; no optimization and no full Lean claim",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
