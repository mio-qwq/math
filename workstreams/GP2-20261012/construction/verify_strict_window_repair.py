#!/usr/bin/env python3
"""Finite semantic checks for STRICT_WINDOW_REPAIR.md; Python stdlib only.

The universal O(m^3) theorem is proved in the accompanying note. This script
checks the original graph semantics, threshold arithmetic, simultaneous fiber
deletion, and a finite obstruction to naive blow-up. It performs no optimization
and does not import any discovery program or previous Kautz verifier.
"""

from collections import Counter, deque
from itertools import combinations, permutations, product
import json


THRESHOLDS = {1: 7, 2: 13, 3: 15}


def valid_word(word, m):
    return (len(word) == 4 and all(0 <= x < m for x in word)
            and all(word[i] != word[i + 1] for i in range(3)))


def graph(m):
    """Build exactly the specified shift-and-append adjacency."""
    assert m >= 2
    words = [w for w in product(range(m), repeat=4) if valid_word(w, m)]
    index = {w: i for i, w in enumerate(words)}
    adjacency = []
    for w in words:
        adjacency.append([index[w[1:] + (letter,)]
                          for letter in range(m) if letter != w[-1]])
    assert len(words) == m * (m - 1) ** 3
    assert sum(map(len, adjacency)) == m * (m - 1) ** 4
    return words, index, adjacency


def bfs(adjacency, source):
    distance = [-1] * len(adjacency)
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                queue.append(v)
    assert all(d >= 0 for d in distance)
    return distance


def overlap_distance(u, v):
    if u == v:
        return 0
    for overlap in (3, 2, 1):
        if u[-overlap:] == v[:overlap]:
            return 4 - overlap
    return 4


def gp_witness(selected, index, adjacency):
    """Return an original-BFS geodesic triple, or None."""
    ids = sorted(index[w] for w in selected)
    distances = {i: bfs(adjacency, i) for i in ids}
    for a, b, c in permutations(ids, 3):
        if distances[a][b] + distances[b][c] == distances[a][c]:
            return a, b, c
    return None


def strict_witness(code, alphabet_size):
    for word in product(range(alphabet_size), repeat=8):
        hits = [t for t in range(5) if word[t:t + 4] in code]
        if len(hits) > 2:
            return word, hits
    return None


def repair(selected, m, thresholds=THRESHOLDS):
    """The one-pass simultaneous rule; all counts refer to the input set."""
    assert all(valid_word(w, m) for w in selected)
    left = {l: Counter(w[l:] for w in selected) for l in (1, 2, 3)}
    right = {l: Counter(w[:4 - l] for w in selected) for l in (1, 2, 3)}
    return {
        w for w in selected
        if len(set(w)) == 4
        and all(left[l][w[l:]] > thresholds[l] * m ** (l - 1)
                and right[l][w[:4 - l]] > thresholds[l] * m ** (l - 1)
                for l in (1, 2, 3))
    }


def threshold_check(thresholds):
    rows = []
    for a in range(1, 4):
        for b in range(1, 4):
            if a + b > 4:
                continue
            large, small = max(a, b), min(a, b)
            first_bad = 4 * large + large * (large - 1) // 2
            second_bad = (4 + large) * small + small * (small - 1) // 2
            assert first_bad <= thresholds[large]
            assert second_bad <= thresholds[small]
            rows.append([a, b, first_bad, second_bad])
    assert len(rows) == 6
    return rows


def expect_rejected(label, check):
    try:
        check()
    except AssertionError:
        return label
    raise AssertionError("negative control was accepted: " + label)


def assert_equal(actual, expected):
    assert actual == expected, (actual, expected)


def main():
    report = {"scope": "finite semantic checks; universal theorem is written"}
    report["threshold_rows"] = threshold_check(THRESHOLDS)
    assert 3 + 2 * sum(THRESHOLDS.values()) == 73
    controls = []
    for l in (1, 2, 3):
        damaged = dict(THRESHOLDS)
        damaged[l] -= 1
        controls.append(expect_rejected(
            "threshold_T%d_minus_one" % l,
            lambda damaged=damaged: threshold_check(damaged)))

    words4, index4, adjacency4 = graph(4)
    distance_pairs = 0
    for i, u in enumerate(words4):
        actual = bfs(adjacency4, i)
        for j, v in enumerate(words4):
            assert actual[j] == overlap_distance(u, v)
            distance_pairs += 1
    report["all_pair_original_BFS_checks_m4"] = distance_pairs

    def inversion_count(w):
        return sum(w[i] > w[j] for i in range(4) for j in range(i + 1, 4))

    odd = {w for w in permutations(range(4)) if inversion_count(w) % 2 == 1}
    assert len(odd) == 12
    assert gp_witness(odd, index4, adjacency4) is None
    repeated_word = (0, 1, 3, 2, 0, 1, 3, 2)
    repeated_hits = [t for t in range(5) if repeated_word[t:t + 4] in odd]
    assert repeated_hits == [0, 2, 4]
    assert repeated_word[:4] == repeated_word[4:]
    repaired_odd = repair(odd, 4)
    assert not repaired_odd
    assert strict_witness(repaired_odd, 4) is None
    report["finite_GP_not_strict"] = {
        "alphabet": 4, "set": [list(w) for w in sorted(odd)],
        "bad_window_word": list(repeated_word), "hits": repeated_hits,
        "repair_size": len(repaired_odd),
        "small_parameter_note": "thresholds intentionally give empty repair",
    }

    words8, index8, adjacency8 = graph(8)
    lifted_word = (0, 2, 6, 4, 1, 3, 7, 5)
    assert len(set(lifted_word)) == 8
    triple = [lifted_word[t:t + 4] for t in (0, 2, 4)]
    assert all(tuple(letter // 2 for letter in w) in odd for w in triple)
    d0, d1 = (bfs(adjacency8, index8[triple[k]]) for k in (0, 1))
    actual_triple = [d0[index8[triple[1]]], d1[index8[triple[2]]],
                     d0[index8[triple[2]]]]
    assert actual_triple == [2, 2, 4]
    assert gp_witness(set(triple), index8, adjacency8) is not None
    controls.append(expect_rejected(
        "damaged_endpoint_distance_3",
        lambda: assert_equal(actual_triple, [2, 2, 3])))
    controls.append(expect_rejected(
        "wrong_alphabet_binding_7",
        lambda: repair(set(triple), 7)))
    report["naive_blowup_fails"] = {
        "alphabet": 8, "word": list(lifted_word),
        "triple": [list(w) for w in triple],
        "BFS_distances_left_middle_right": actual_triple,
        "graph_vertices": len(words8),
        "graph_arcs": sum(map(len, adjacency8)),
    }

    # New minimal validation template, not the inherited optimized three-block
    # code: 0001 has no proper self-overlap and is a strict code.
    binary_code = {(0, 0, 0, 1)}
    assert strict_witness(binary_code, 2) is None
    assert strict_witness(binary_code | {(0, 0, 0, 0)}, 2) is not None
    block = (0, 0, 1, 1)
    selected4 = {w for w in words4 if tuple(block[x] for x in w) in binary_code}
    assert len(selected4) == 4
    assert gp_witness(selected4, index4, adjacency4) is None
    report["strict_template_lift"] = {
        "template": [[0, 0, 0, 1]], "blocks": [[0, 1], [2, 3]],
        "selected": [list(w) for w in sorted(selected4)],
        "damaged_template_rejected": True,
    }

    # Finite checks of the extension union bound for every possible original
    # gap pair. The exact count below is derived by enumerating all free tuples;
    # the checker compares it to the proof's independent union-bound formula.
    extension_cases = []
    for m in (8, 9):
        for l in (1, 2, 3):
            for fixed_count in range(4, 8 - l + 1):
                fixed = set(range(fixed_count))
                bad = sum(len(set(t)) < l or bool(fixed.intersection(t))
                          for t in product(range(m), repeat=l))
                bound = (fixed_count * l + l * (l - 1) // 2) * m ** (l - 1)
                assert bad <= bound
                extension_cases.append([m, l, fixed_count, bad, bound])
    report["extension_union_bound_cases"] = extension_cases
    report["negative_controls_passed"] = controls
    report["status"] = "PASS"
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
