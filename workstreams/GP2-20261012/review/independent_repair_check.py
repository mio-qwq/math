#!/usr/bin/env python3
"""Independent finite semantic checks for the elementary strict-code repair.

Imports only the independently written review checker, never discovery code.
The universal fiber-extension argument is audited in the companion Markdown.
"""

from collections import Counter
from itertools import permutations, product
from pathlib import Path
import hashlib
import json

from independent_window_check import (
    bfs, build_certificate, gp_violation, kautz_graph, verify_certificate,
)


SOURCE_SHA256 = "56ed0af016042abcbca256b52f6fb7539edb908fe81d6ba585a21102f9c4c4f5"


def threshold_checks(thresholds):
    rows = []
    for a in range(1, 4):
        for b in range(1, 4):
            if a + b > 4:
                continue
            first, second = sorted((a, b), reverse=True)
            first_bad = 4 * first + first * (first - 1) // 2
            second_bad = (4 + first) * second + second * (second - 1) // 2
            if first_bad > thresholds[first] or second_bad > thresholds[second]:
                raise ValueError("threshold cannot guarantee distinct extension")
            rows.append({"a": a, "b": b, "first_length": first,
                         "second_length": second, "first_bad": first_bad,
                         "second_bad": second_bad})
    return rows


def repair(selected, m, thresholds):
    if any(len(w) != 4 or any(type(a) is not int or a < 0 or a >= m for a in w)
           or any(w[j] == w[j + 1] for j in range(3)) for w in selected):
        raise ValueError("selected word violates original graph parameter binding")
    left = {a: Counter(w[a:] for w in selected) for a in range(1, 4)}
    right = {a: Counter(w[:4 - a] for w in selected) for a in range(1, 4)}
    return {w for w in selected if len(set(w)) == 4
            and all(left[a][w[a:]] > thresholds[a] * m ** (a - 1)
                    and right[a][w[:4 - a]] > thresholds[a] * m ** (a - 1)
                    for a in range(1, 4))}


def is_strict(selected, m):
    for word in product(range(m), repeat=8):
        if sum(word[i:i + 4] in selected for i in range(5)) > 2:
            return False
    return True


def main():
    directory = Path(__file__).resolve().parent
    source = directory.parent / "construction" / "STRICT_WINDOW_REPAIR.md"
    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    if source_sha256 != SOURCE_SHA256:
        raise ValueError("frozen proof source hash differs")
    thresholds = {1: 7, 2: 13, 3: 15}
    rows = threshold_checks(thresholds)
    graph_words, ids, arcs = kautz_graph(8)
    distance_rows = {}
    def dist(u, v):
        if ids[u] not in distance_rows:
            distance_rows[ids[u]] = bfs(arcs, ids[u])
        return distance_rows[ids[u]][ids[v]]
    geodesics = []
    for row in rows:
        a, b = row["a"], row["b"]
        segment = tuple(range(a + b + 4))
        u, v, w = segment[:4], segment[a:a + 4], segment[a + b:a + b + 4]
        actual = [dist(u, v), dist(v, w), dist(u, w)]
        assert actual == [a, b, a + b]
        assert u[a:] == v[:4 - a]
        assert w[:4 - b] == v[b:]
        geodesics.append({"a": a, "b": b, "windows": [u, v, w],
                          "original_graph_distances": actual})

    odd = {w for w in permutations(range(4))
           if sum(w[i] > w[j] for i in range(4) for j in range(i + 1, 4)) % 2}
    assert len(odd) == 12
    verify_certificate(build_certificate(4, odd))
    bad_word = (0, 1, 3, 2, 0, 1, 3, 2)
    selected_positions = [i for i in range(5) if bad_word[i:i + 4] in odd]
    assert selected_positions == [0, 2, 4]
    assert bad_word[:4] == bad_word[4:]
    repaired = repair(odd, 4, thresholds)
    assert not repaired and is_strict(repaired, 4)
    assert len(odd - repaired) <= 73 * 4 ** 3

    blown_word = (0, 2, 6, 4, 1, 3, 7, 5)
    blown_windows = [blown_word[i:i + 4] for i in (0, 2, 4)]
    assert all(tuple(a // 2 for a in w) in odd for w in blown_windows)
    assert len(set(blown_windows)) == 3
    blowup_distances = [[dist(u, v) for v in blown_windows] for u in blown_windows]
    assert blowup_distances[0][1] == 2 and blowup_distances[1][2] == 2
    assert blowup_distances[0][2] == 4
    assert gp_violation(list(range(3)), blowup_distances) is not None

    negatives = {}
    for length in (1, 2, 3):
        wrong = dict(thresholds)
        wrong[length] -= 1
        try:
            threshold_checks(wrong)
        except ValueError as error:
            negatives["threshold_" + str(length)] = str(error)
        else:
            raise AssertionError("damaged threshold accepted")
    try:
        repair(odd, 3, thresholds)
    except ValueError as error:
        negatives["alphabet_binding"] = str(error)
    else:
        raise AssertionError("damaged alphabet binding accepted")
    corrupted = [r[:] for r in blowup_distances]
    corrupted[0][2] -= 1
    assert corrupted != [[dist(u, v) for v in blown_windows] for u in blown_windows]
    negatives["distance_binding"] = "changed distance differs from original-adjacency BFS"

    print(json.dumps({"status": "PASS", "frozen_source_sha256": source_sha256,
                      "threshold_rows": rows,
                      "injective_geodesic_gap_cases": geodesics,
                      "odd_permutation_gp_size": len(odd),
                      "strict_failure_positions": selected_positions,
                      "blowup_bad_windows": blown_windows,
                      "blowup_distances": blowup_distances,
                      "repaired_small_fixture_size": len(repaired),
                      "negative_controls": negatives,
                      "scope": "Finite semantics only; all-parameter theorem is reviewed in writing."},
                     indent=2))


if __name__ == "__main__":
    main()
