#!/usr/bin/env python3
"""BFS-based independent certificate for all seven-letter equality types.

No discovery program or discovery output is imported/read.  This program
generates all restricted-growth strings of length seven from scratch.
"""

from collections import Counter, deque
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json


class RejectedCertificate(Exception):
    pass


def require(condition, reason):
    if not condition:
        raise RejectedCertificate(reason)


class OriginalKautz:
    def __init__(self, alphabet_size):
        require(type(alphabet_size) is int and alphabet_size >= 2,
                "invalid graph alphabet size")
        self.words = [w for w in product(range(alphabet_size), repeat=4)
                      if all(w[i] != w[i + 1] for i in range(3))]
        self.ids = {w: i for i, w in enumerate(self.words)}
        self.arcs = [[self.ids[w[1:] + (a,)] for a in range(alphabet_size)
                     if w[-1] != a] for w in self.words]
        self.rows = {}

    def distance(self, u, v):
        uid = self.ids[u]
        if uid not in self.rows:
            dist = [-1] * len(self.words)
            dist[uid] = 0
            queue = deque([uid])
            while queue:
                i = queue.popleft()
                for j in self.arcs[i]:
                    if dist[j] < 0:
                        dist[j] = dist[i] + 1
                        queue.append(j)
            require(min(dist) >= 0, "unexpected disconnected Kautz graph")
            self.rows[uid] = dist
        return self.rows[uid][self.ids[v]]


def equality_patterns(length=7):
    def visit(prefix, next_label):
        if len(prefix) == length:
            yield tuple(prefix)
            return
        for label in range(next_label + 1):
            yield from visit(prefix + [label], max(next_label, label + 1))
    yield from visit([0], 1)


def local_data(pattern, graphs):
    alphabet_size = max(pattern) + 1
    windows = [tuple(pattern[(i + j) % 7] for j in range(4)) for i in range(7)]
    multiplicities = Counter(w for w in windows
                             if all(w[j] != w[j + 1] for j in range(3)))
    words = sorted(multiplicities)
    weights = [multiplicities[w] for w in words]
    if words:
        graph = graphs.setdefault(alphabet_size, None)
        if graph is None:
            graph = graphs[alphabet_size] = OriginalKautz(alphabet_size)
        distance = [[graph.distance(u, v) for v in words] for u in words]
    else:
        distance = []
    return alphabet_size, words, weights, distance


def triple_witness(mask, distance):
    selected = [i for i in range(len(distance)) if mask & (1 << i)]
    for u, w, v in permutations(selected, 3):
        if distance[u][w] + distance[w][v] == distance[u][v]:
            return [u, w, v]
    return None


def weight(mask, weights):
    return sum(a for i, a in enumerate(weights) if mask & (1 << i))


def make_record(pattern, graphs):
    k, words, weights, distance = local_data(pattern, graphs)
    subsets = range(1 << len(words))
    feasible = [mask for mask in subsets if triple_witness(mask, distance) is None]
    maximum = max(weight(mask, weights) for mask in feasible)
    witness = next(mask for mask in feasible if weight(mask, weights) == maximum)
    rejections = [{"mask": mask, "triple": triple_witness(mask, distance)}
                  for mask in subsets if weight(mask, weights) > maximum]
    return {"pattern": list(pattern), "alphabet_size": k,
            "legal_words": [list(w) for w in words], "multiplicities": weights,
            "bfs_distances": distance, "capacity": maximum,
            "attaining_mask": witness, "higher_weight_rejections": rejections}


def check_record(record, graphs):
    pattern = tuple(record["pattern"])
    require(len(pattern) == 7, "incorrect pattern length")
    # Parameter binding uses the actual canonical equality pattern.
    require(pattern[0] == 0 and all(type(v) is int and v >= 0 for v in pattern),
            "invalid equality labels")
    for i in range(1, 7):
        require(pattern[i] <= 1 + max(pattern[:i]), "noncanonical equality pattern")
    k, words, weights, distance = local_data(pattern, graphs)
    require(record["alphabet_size"] == k, "alphabet-size binding mismatch")
    require(record["legal_words"] == [list(w) for w in words],
            "original-adjacency vertex mismatch")
    require(record["multiplicities"] == weights, "window multiplicity mismatch")
    require(record["bfs_distances"] == distance, "original-adjacency BFS mismatch")
    capacity = record["capacity"]
    require(type(capacity) is int and 0 <= capacity <= 7, "invalid capacity")
    witness = record["attaining_mask"]
    require(type(witness) is int and 0 <= witness < (1 << len(words)),
            "invalid attaining subset")
    require(weight(witness, weights) == capacity, "capacity witness weight mismatch")
    require(triple_witness(witness, distance) is None, "capacity witness is not GP")

    rejections = record["higher_weight_rejections"]
    required_masks = {mask for mask in range(1 << len(words))
                      if weight(mask, weights) > capacity}
    masks = [r["mask"] for r in rejections]
    require(len(masks) == len(set(masks)) and set(masks) == required_masks,
            "higher-weight rejection coverage mismatch")
    for rejection in rejections:
        mask = rejection["mask"]
        triple = rejection["triple"]
        require(isinstance(triple, list) and len(triple) == 3
                and len(set(triple)) == 3, "invalid rejection triple")
        require(all(type(i) is int and 0 <= i < len(words)
                    and mask & (1 << i) for i in triple),
                "rejection triple not in rejected set")
        u, w, v = triple
        require(distance[u][w] + distance[w][v] == distance[u][v],
                "rejection triple is not on a shortest path")
    return k, max(0, capacity * (capacity - 2))


def check_package(package):
    require(package["schema"] == "kautz4-seven-cycle-equality-types-v1",
            "schema mismatch")
    expected_patterns = set(equality_patterns())
    records = package["records"]
    patterns = [tuple(record["pattern"]) for record in records]
    require(len(patterns) == len(set(patterns)) and set(patterns) == expected_patterns,
            "equality-type coverage mismatch")
    graphs = {}
    coefficients = Counter()
    for record in records:
        k, excess = check_record(record, graphs)
        coefficients[k] += excess
    stated = {int(k): value for k, value in package["excess_coefficients"].items()}
    require(dict(coefficients) == stated, "excess coefficient sum mismatch")
    return coefficients, sum(len(graph.rows) for graph in graphs.values())


def falling(m, k):
    answer = 1
    for j in range(k):
        answer *= m - j
    return answer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-certificate", action="store_true")
    parser.add_argument("--verify-certificate", type=Path)
    options = parser.parse_args()
    if options.verify_certificate is not None:
        package = json.loads(options.verify_certificate.read_text())
        coefficients, bfs_rows = check_package(package)
        print(json.dumps({"status": "PASS", "verified_stored_certificate": True,
                          "equality_types": len(package["records"]),
                          "independent_original_graph_bfs_rows": bfs_rows,
                          "excess_coefficients": dict(sorted(coefficients.items()))}, indent=2))
        return
    graphs = {}
    records = [make_record(pattern, graphs) for pattern in equality_patterns()]
    require(len(records) == 877, "Bell number mismatch")
    coefficients = Counter()
    distribution = Counter()
    for record in records:
        k = record["alphabet_size"]
        capacity = record["capacity"]
        coefficients[k] += max(0, capacity * (capacity - 2))
        distribution[k, capacity] += 1
    package = {"schema": "kautz4-seven-cycle-equality-types-v1",
               "excess_coefficients": dict(sorted(coefficients.items())),
               "records": records}
    verified, bfs_rows = check_package(package)
    require(dict(verified) == {1: 0, 2: 56, 3: 84, 4: 105, 5: 21, 6: 0, 7: 0},
            "unexpected independently derived coefficient vector")
    require(all(r["capacity"] <= 2 for r in records if r["alphabet_size"] >= 6),
            "six-distinct-letter lemma failed")

    negative = {}
    copies = {}
    bad = deepcopy(package)
    target = next(r for r in bad["records"] if r["capacity"] >= 3)
    target["capacity"] -= 1
    copies["understated_capacity"] = bad
    bad = deepcopy(package)
    target = next(r for r in bad["records"] if len(r["legal_words"]) >= 2)
    target["bfs_distances"][0][1] += 1
    copies["wrong_distance"] = bad
    bad = deepcopy(package)
    bad["records"][0]["alphabet_size"] += 1
    copies["wrong_parameter_binding"] = bad
    bad = deepcopy(package)
    bad["excess_coefficients"][5] -= 1
    copies["understated_final_coefficient"] = bad
    bad = deepcopy(package)
    target = next(r for r in bad["records"] if r["higher_weight_rejections"])
    target["higher_weight_rejections"].pop()
    copies["missing_rejection"] = bad
    for name, bad in copies.items():
        try:
            check_package(bad)
        except RejectedCertificate as error:
            negative[name] = str(error)
        else:
            raise AssertionError("tampered certificate accepted: " + name)

    # These polynomial identities are checked exactly at enough points to
    # distinguish the displayed degree-seven-or-less polynomials; the text
    # also gives the direct symbolic expansions.
    for m in range(2, 10):
        P = 8 * falling(m, 2) + 12 * falling(m, 3) + 15 * falling(m, 4) + 3 * falling(m, 5)
        require(7 * P == sum(c * falling(m, k) for k, c in coefficients.items()),
                "P polynomial coefficient conversion mismatch")
        require(P == 3*m**5 - 15*m**4 + 27*m**3 - 13*m**2 - 2*m,
                "P polynomial expansion mismatch")
        require(Fraction(3 * P, m ** 7) < 1, "root-branch threshold check failed")
    if options.write_certificate:
        output = Path(__file__).resolve().parent / "independent_collision_certificate.json"
        output.write_text(json.dumps(package, separators=(",", ":")) + "\n")
    print(json.dumps({"status": "PASS", "equality_types": len(records),
                      "independent_original_graph_bfs_rows": bfs_rows,
                      "capacity_distribution": [
                          {"blocks": k, "capacity": cap, "count": count}
                          for (k, cap), count in sorted(distribution.items())],
                      "excess_coefficients": dict(sorted(coefficients.items())),
                      "P_falling_coefficients": {"2": 8, "3": 12, "4": 15, "5": 3},
                      "negative_tests": negative}, indent=2))


if __name__ == "__main__":
    main()
