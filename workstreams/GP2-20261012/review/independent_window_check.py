#!/usr/bin/env python3
"""Independent adjacency/BFS and exact moment audit for the Ka(m,4) bound.

Standard library only.  Normal execution does not write files.
Use --write-certificates to emit the two finite witnesses and the seven-window
distance certificate in this script's directory.
"""

from collections import Counter, deque
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations, product
from math import prod, sqrt
from pathlib import Path
import argparse
import json


class VerificationError(Exception):
    pass


def kautz_graph(m):
    if type(m) is not int or m < 3:
        raise VerificationError("alphabet parameter must be an integer >= 3")
    words = [w for w in product(range(m), repeat=4)
             if all(w[i] != w[i + 1] for i in range(3))]
    index = {w: i for i, w in enumerate(words)}
    edges = [[index[w[1:] + (a,)] for a in range(m) if a != w[-1]]
             for w in words]
    return words, index, edges


def bfs(edges, source):
    distance = [-1] * len(edges)
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in edges[u]:
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                queue.append(v)
    if min(distance) < 0:
        raise VerificationError("unexpected unreachable vertex")
    return distance


def gp_violation(chosen_indices, distances):
    for u, w, v in permutations(chosen_indices, 3):
        if distances[u][w] + distances[w][v] == distances[u][v]:
            return (u, w, v)
    return None


def build_certificate(m, chosen):
    words, index, edges = kautz_graph(m)
    return {"schema": "kautz4-original-adjacency-v1", "m": m, "k": 4,
            "alphabet": list(range(m)), "vertices": [list(w) for w in words],
            "adjacency": edges,
            "distances": [bfs(edges, u) for u in range(len(words))],
            "chosen": [list(w) for w in sorted(chosen)],
            "cardinality": len(chosen)}


def verify_certificate(certificate):
    if certificate.get("schema") != "kautz4-original-adjacency-v1":
        raise VerificationError("schema mismatch")
    if certificate.get("k") != 4:
        raise VerificationError("word-length parameter mismatch")
    m = certificate["m"]
    words, index, edges = kautz_graph(m)
    if certificate.get("alphabet") != list(range(m)):
        raise VerificationError("alphabet binding mismatch")
    if certificate.get("vertices") != [list(w) for w in words]:
        raise VerificationError("vertex-list parameter binding mismatch")
    if certificate.get("adjacency") != edges:
        raise VerificationError("original adjacency mismatch")
    distances = [bfs(edges, u) for u in range(len(words))]
    if certificate.get("distances") != distances:
        raise VerificationError("BFS distance matrix mismatch")
    chosen = [tuple(w) for w in certificate["chosen"]]
    if len(set(chosen)) != len(chosen) or any(w not in index for w in chosen):
        raise VerificationError("invalid or repeated chosen vertex")
    if certificate.get("cardinality") != len(chosen):
        raise VerificationError("claimed cardinality mismatch")
    violation = gp_violation([index[w] for w in chosen], distances)
    if violation is not None:
        raise VerificationError("chosen set contains a geodesic triple: "
                                + str([words[i] for i in violation]))
    return words, index, edges, distances


def overlap_distance(u, v):
    if u == v:
        return 0
    return 4 - max([0] + [r for r in range(1, 4) if u[-r:] == v[:r]])


def seven_window_check():
    words, index, edges = kautz_graph(7)
    cycle = tuple(range(7))
    windows = [tuple(cycle[(i + j) % 7] for j in range(4)) for i in range(7)]
    ids = [index[w] for w in windows]
    rows = [bfs(edges, u) for u in ids]
    witnesses = []
    for triple in combinations(range(7), 3):
        gaps = [(triple[(j + 1) % 3] - triple[j]) % 7 for j in range(3)]
        after_largest = (gaps.index(max(gaps)) + 1) % 3
        start = triple[after_largest]
        finish = triple[(after_largest + 2) % 3]
        length = (finish - start) % 7
        path_positions = [(start + j) % 7 for j in range(length + 1)]
        assert 2 <= length <= 4
        assert set(triple).issubset(path_positions)
        assert all(ids[path_positions[j + 1]] in edges[ids[path_positions[j]]]
                   for j in range(length))
        assert rows[start][ids[finish]] == length
        witnesses.append({"triple": list(triple), "path": path_positions,
                          "length": length})
    assert len(witnesses) == 35
    return {"m": 7, "k": 4, "cycle": list(cycle),
            "windows": [list(w) for w in windows],
            "window_distances": [[rows[i][ids[j]] for j in range(7)]
                                 for i in range(7)],
            "geodesic_triple_witnesses": witnesses}


def cyclic_histogram(m, selected, length):
    hist = Counter()
    for word in product(range(m), repeat=length):
        doubled = word + word[:3]
        count = sum(doubled[i:i + 4] in selected for i in range(length))
        hist[count] += 1
    return hist


def exact_moments(m, selected):
    p = Fraction(len(selected), m ** 4)
    q = []
    for shift in range(1, 4):
        count = sum(word[:4] in selected and word[shift:shift + 4] in selected
                    for word in product(range(m), repeat=4 + shift))
        q.append(Fraction(count, m ** (4 + shift)))
    data = {"m": m, "cardinality": len(selected), "p": str(p),
            "q_1_2_3": [str(x) for x in q]}
    for length in (7, 9):
        hist = cyclic_histogram(m, selected, length)
        mean = Fraction(sum(n * count for n, count in hist.items()), m ** length)
        pairs = Fraction(sum(n * (n - 1) // 2 * count for n, count in hist.items()),
                         m ** length)
        assert mean == length * p
        target = length * sum(q) + (9 * p * p if length == 9 else 0)
        assert pairs == target
        if length == 9:
            assert pairs >= 2 * mean - 3
        data[str(length)] = {"histogram": dict(sorted(hist.items())),
                             "mean": str(mean), "pair_moment": str(pairs)}
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificates", action="store_true")
    options = parser.parse_args()
    # A finite witness reported in the source paper, independently verified here.
    selected3 = {tuple(int(x) - 1 for x in w) for w in
                 ("1312", "1313", "2121", "2132", "2312", "2313", "2321")}
    # A separate explicit family: first letter 0, last three letters in {1,2,3}.
    selected4 = {(0, a, b, c) for a, b, c in product((1, 2, 3), repeat=3)
                 if a != b and b != c}
    certificates = [build_certificate(3, selected3), build_certificate(4, selected4)]
    checked_pairs = 0
    for certificate in certificates:
        words, index, edges, distances = verify_certificate(certificate)
        for i, u in enumerate(words):
            for j, v in enumerate(words):
                assert distances[i][j] == overlap_distance(u, v)
                checked_pairs += 1

    negative_results = {}
    original = certificates[0]
    words, index, edges, distances = verify_certificate(original)
    corrupt = deepcopy(original)
    for w in words:
        if list(w) not in original["chosen"]:
            proposal = original["chosen"] + [list(w)]
            if gp_violation([index[tuple(v)] for v in proposal], distances):
                corrupt["chosen"] = proposal
                corrupt["cardinality"] += 1
                break
    bad_distance = deepcopy(original)
    bad_distance["distances"][0][1] += 1
    bad_parameter = deepcopy(original)
    bad_parameter["m"] = 4
    bad_graph = deepcopy(original)
    bad_graph["adjacency"][0].pop()
    for name, data in [("corrupt_gp_set", corrupt), ("wrong_distance", bad_distance),
                       ("wrong_parameter_binding", bad_parameter),
                       ("wrong_adjacency", bad_graph)]:
        try:
            verify_certificate(data)
        except VerificationError as error:
            negative_results[name] = str(error)
        else:
            raise AssertionError("negative test was wrongly accepted: " + name)

    seven = seven_window_check()
    # This is a finite verification of the polynomial inequality used at nine.
    assert all(n * (n - 1) // 2 >= 2 * n - 3 for n in range(10))
    moments = [exact_moments(3, selected3), exact_moments(4, selected4)]
    delta221 = 1 - Fraction(prod(221 - j for j in range(7)), 221 ** 7)
    assert delta221 <= Fraction(11, 120)
    if options.write_certificates:
        directory = Path(__file__).resolve().parent
        for certificate in certificates:
            filename = directory / ("gp_m%d_certificate.json" % certificate["m"])
            filename.write_text(json.dumps(certificate, indent=2) + "\n")
        (directory / "seven_window_geodesic_certificate.json").write_text(
            json.dumps(seven, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "bfs_overlap_pairs": checked_pairs,
                      "seven_distinct_triples_checked": len(seven["geodesic_triple_witnesses"]),
                      "negative_tests": negative_results,
                      "exact_cyclic_moments": moments,
                      "delta_221": str(delta221),
                      "asymptotic_root_approx": (9 - sqrt(33)) / 12}, indent=2))


if __name__ == "__main__":
    main()
