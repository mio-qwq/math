#!/usr/bin/env python3
"""Independent original-graph audit of the transcribed Jiggs 57-word code.

This reads the exact source word list, not an author's verification result.
The reusable BFS engine is this reviewer's earlier verify_lower18.py; its
hash is checked.  No mathematical result about optimum comma-free codes is
used by the verification or by the GP construction.
"""

from collections import Counter
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform

from verify_lower18 import bfs_all, graph_from_adjacency, overlap_distance, require


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "literature_lifts" / "jiggs57_words.txt"
SOURCE_HASH = "26d405621e125016c26edf662bd1d18cb721bb6b09976c421fa5093e531a1f14"
BFS_ENGINE_HASH = "f46274fb83baf013131258cc3e62b62e6f535f5aea81d0fc3e15212ea19d76db"


def load_code() -> set[tuple[int, ...]]:
    require(sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_HASH,
            "transcribed dictionary hash mismatch")
    engine = HERE / "verify_lower18.py"
    require(sha256(engine.read_bytes()).hexdigest() == BFS_ENGINE_HASH,
            "independent original-BFS engine hash mismatch")
    words = SOURCE.read_text(encoding="utf-8").split()
    require(len(words) == len(set(words)) == 57, "wrong dictionary size/duplicates")
    require(all(len(w) == 4 and set(w) <= set("ABCD") for w in words),
            "dictionary alphabet/length mismatch")
    return {tuple("ABCD".index(c) for c in w) for w in words}


def strict_audit(code: set[tuple[int, ...]]) -> dict:
    hist = Counter()
    first = None
    for w in product(range(4), repeat=8):
        hits = [i for i in range(5) if w[i:i+4] in code]
        hist[len(hits)] += 1
        if len(hits) > 2 and first is None:
            first = {"word": list(w), "selected_starts": hits}
    return {"words_checked": 4**8,
            "selected_occurrence_histogram": dict(sorted(hist.items())),
            "maximum_selected_occurrences": max(hist),
            "first_violation": first}


def comma_free_and_adjacency_audit(code: set[tuple[int, ...]]) -> dict:
    pairs = 0
    overlaps = 0
    for u in code:
        for v in code:
            pairs += 1
            require(u[1:] != v[:3], "two selected adjacent windows")
            joined = u+v
            for shift in (1, 2, 3):
                overlaps += 1
                require(joined[shift:shift+4] not in code,
                        "ordinary comma-free violation")
    return {"ordered_codeword_pairs_including_equal": pairs,
            "selected_adjacent_pairs": 0,
            "interior_windows_of_two_codewords_checked": overlaps,
            "comma_free_violations": 0}


def label_map(sizes: tuple[int, ...]) -> tuple[int, ...]:
    require(len(sizes) == 4 and all(n >= 0 for n in sizes), "invalid four blocks")
    return tuple(i for i, n in enumerate(sizes) for _ in range(n))


def lift_size(code: set[tuple[int, ...]], sizes: tuple[int, ...]) -> int:
    total = 0
    for w in code:
        term = sizes[w[0]]
        for i in range(1, 4):
            term *= sizes[w[i]] - int(w[i] == w[i-1])
        total += term
    return total


def scaled_block_polynomial(code: set[tuple[int, ...]],
                            scales: tuple[int, ...]) -> list[int]:
    """Coefficients in Z[q] for block sizes scales[i]*q, from literal words."""
    total = [0]*5
    for word in code:
        term = [0, scales[word[0]]]
        for i in range(1, 4):
            constant = -int(word[i] == word[i-1])
            linear = scales[word[i]]
            new = [0]*(len(term)+1)
            for j, value in enumerate(term):
                new[j] += constant*value
                new[j+1] += linear*value
            term = new
        total = [a+b for a, b in zip(total, term)]
    return total


def gp_bitset_audit(rows: list[str]) -> dict:
    n = len(rows)
    require(all(len(row) == n for row in rows), "nonsquare selected distances")
    outgoing = [[0]*5 for _ in range(n)]
    incoming = [[0]*5 for _ in range(n)]
    for u, row in enumerate(rows):
        for v, char in enumerate(row):
            distance = int(char)
            require(0 <= distance <= 4, "distance outside original diameter")
            require((distance == 0) == (u == v), "zero-distance identity failure")
            outgoing[u][distance] |= 1 << v
            incoming[v][distance] |= 1 << u
    pairs = 0
    splits = 0
    for u, row in enumerate(rows):
        for v, char in enumerate(row):
            if u == v:
                continue
            pairs += 1
            distance = int(char)
            for left in range(1, distance):
                splits += 1
                middles = outgoing[u][left] & incoming[v][distance-left]
                if middles:
                    witness = (middles & -middles).bit_length()-1
                    raise ValueError(f"original geodesic triple {u},{witness},{v}")
    require(pairs == n*(n-1), "endpoint-pair count mismatch")
    return {"ordered_distinct_endpoint_pairs_checked": pairs,
            "positive_distance_splits_checked": splits,
            "distinct_ordered_triples_covered": n*(n-1)*(n-2),
            "geodesic_triples_found": 0}


def make_case(code: set[tuple[int, ...]], sizes: tuple[int, ...]) -> dict:
    m = sum(sizes)
    vertices, adjacency = graph_from_adjacency(m)
    pi = label_map(sizes)
    chosen = [i for i, word in enumerate(vertices)
              if tuple(pi[c] for c in word) in code]
    distances = bfs_all(adjacency)
    for i, u in enumerate(vertices):
        for j, v in enumerate(vertices):
            require(distances[i][j] == overlap_distance(u, v),
                    "independent BFS/overlap disagreement")
    rows = ["".join(str(distances[u][v]) for v in chosen) for u in chosen]
    require(len(chosen) == lift_size(code, sizes), "general lift count mismatch")
    return {"m": m, "ordered_block_sizes": list(sizes),
            "ambient_vertices_lexicographic": [list(w) for w in vertices],
            "original_shift_append_adjacency": adjacency,
            "selected_vertex_indices": chosen,
            "selected_vertices": [list(vertices[i]) for i in chosen],
            "selected_pair_distances_as_digit_rows": rows,
            "claimed_selected_count": len(chosen),
            "all_ambient_ordered_pair_BFS_distances_checked": len(vertices)**2,
            "gp_audit": gp_bitset_audit(rows)}


def replay_case(code: set[tuple[int, ...]], case: dict) -> None:
    sizes = tuple(case["ordered_block_sizes"])
    require(sum(sizes) == case["m"], "alphabet size/block binding mismatch")
    vertices, adjacency = graph_from_adjacency(case["m"])
    require(case["ambient_vertices_lexicographic"] == [list(w) for w in vertices],
            "ambient vertices mismatch")
    require(case["original_shift_append_adjacency"] == adjacency,
            "original adjacency mismatch")
    pi = label_map(sizes)
    chosen = [i for i, word in enumerate(vertices)
              if tuple(pi[c] for c in word) in code]
    require(case["selected_vertex_indices"] == chosen, "exact selected set mismatch")
    require(case["selected_vertices"] == [list(vertices[i]) for i in chosen],
            "explicit selected vertex mismatch")
    require(case["claimed_selected_count"] == len(chosen) == lift_size(code, sizes),
            "claimed count mismatch")
    distances = bfs_all(adjacency)
    rows = ["".join(str(distances[u][v]) for v in chosen) for u in chosen]
    require(case["selected_pair_distances_as_digit_rows"] == rows,
            "BFS selected-distance certificate mismatch")
    require(case["all_ambient_ordered_pair_BFS_distances_checked"] == len(vertices)**2,
            "ambient distance count mismatch")
    require(case["gp_audit"] == gp_bitset_audit(rows), "GP audit totals mismatch")


def reject_case(name: str, code: set[tuple[int, ...]], case: dict) -> dict:
    try:
        replay_case(code, case)
    except ValueError as exc:
        return {"name": name, "detected": True, "reason": str(exc)}
    raise ValueError(f"negative control accepted: {name}")


def negative_controls(code: set[tuple[int, ...]], case: dict) -> list[dict]:
    results = []
    violation = strict_audit(code | {(0, 0, 0, 0)})["first_violation"]
    require(violation is not None, "constant-word mutation passed")
    results.append({"name": "constant_template_word_added", "detected": True,
                    "witness": violation})
    vertices, adjacency = graph_from_adjacency(3)
    distances = bfs_all(adjacency)
    bad_words = [(0, 1, 0, 1), (1, 0, 1, 2), (0, 1, 2, 0)]
    indices = [vertices.index(w) for w in bad_words]
    bad_rows = ["".join(str(distances[u][v]) for v in indices) for u in indices]
    try:
        gp_bitset_audit(bad_rows)
    except ValueError as exc:
        results.append({"name": "actual_original_geodesic_triple", "detected": True,
                        "vertices": [list(w) for w in bad_words],
                        "all_pair_distances": bad_rows, "reason": str(exc)})
    else:
        raise ValueError("bitset GP checker accepted an actual geodesic triple")
    bad = deepcopy(case)
    bad["m"] += 1
    results.append(reject_case("wrong_alphabet_binding", code, bad))
    bad = deepcopy(case)
    row = list(bad["selected_pair_distances_as_digit_rows"][0])
    row[1] = str((int(row[1])+1) % 5)
    bad["selected_pair_distances_as_digit_rows"][0] = "".join(row)
    results.append(reject_case("damaged_directed_distance", code, bad))
    bad = deepcopy(case)
    bad["selected_vertex_indices"].pop()
    results.append(reject_case("damaged_target_set", code, bad))
    bad = deepcopy(case)
    bad["original_shift_append_adjacency"][0].pop()
    results.append(reject_case("removed_original_arc", code, bad))
    bad = deepcopy(case)
    bad["claimed_selected_count"] += 1
    results.append(reject_case("wrong_count", code, bad))
    return results


def main() -> None:
    code = load_code()
    strict = strict_audit(code)
    require(strict["first_violation"] is None, "57-word strict property failed")
    cf = comma_free_and_adjacency_audit(code)
    equalities = Counter(sum(w[i] == w[i+1] for i in range(3)) for w in code)
    require(equalities == {0: 23, 1: 28, 2: 6}, "adjacent equality histogram mismatch")
    # Exact binomial expansion of sum_e h_e q^(4-e)(q-1)^e.
    from math import comb
    coefficients = [0]*5
    for e, number in equalities.items():
        for j in range(e+1):
            coefficients[4-e+j] += number*comb(e, j)*(-1)**(e-j)
    require(coefficients == [0, 0, 6, -40, 57], "equal-block polynomial mismatch")
    require(coefficients == scaled_block_polynomial(code, (1, 1, 1, 1)),
            "equal-block count disagrees with independent per-word expansion")
    rational_scales = (5, 5, 3, 3)
    rational_coefficients = scaled_block_polynomial(code, rational_scales)
    require(rational_coefficients == [0, 0, 94, -2528, 14733],
            "rational-block polynomial mismatch")
    rational_density = Fraction(rational_coefficients[4], sum(rational_scales)**4)
    cases = [make_case(code, sizes) for sizes in
             ((1, 1, 1, 1), (2, 1, 1, 1), (2, 2, 2, 2))]
    certificate = {
        "schema": "GP2-20261012/independent-jiggs57/v1",
        "source_file": "../literature_lifts/jiggs57_words.txt",
        "source_sha256": SOURCE_HASH,
        "independent_original_BFS_engine": "verify_lower18.py",
        "independent_original_BFS_engine_sha256": BFS_ENGINE_HASH,
        "alphabet_mapping": {letter: i for i, letter in enumerate("ABCD")},
        "dictionary_lexicographic": [list(w) for w in sorted(code)],
        "strict_window_audit": strict,
        "comma_free_and_adjacency_audit": cf,
        "equal_adjacent_block_pair_histogram": dict(sorted(equalities.items())),
        "equal_block_q_polynomial_low_to_high": coefficients,
        "rational_block_scales": list(rational_scales),
        "rational_block_q_polynomial_low_to_high": rational_coefficients,
        "rational_weight_density": str(rational_density),
        "finite_original_graph_cases": cases,
        "negative_controls": negative_controls(code, cases[0]),
    }
    target = HERE / "jiggs57_certificate.json"
    target.write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":"))
                      + "\n", encoding="utf-8")
    reloaded = json.loads(target.read_text(encoding="utf-8"))
    require(reloaded["source_sha256"] == SOURCE_HASH, "reloaded source binding mismatch")
    require(reloaded["dictionary_lexicographic"] == [list(w) for w in sorted(code)],
            "reloaded dictionary mismatch")
    for case in reloaded["finite_original_graph_cases"]:
        replay_case(code, case)
    report = {
        "result": "PASS", "python": platform.python_version(),
        "source_sha256": SOURCE_HASH,
        "template_size": len(code),
        "strict_window_audit": strict,
        "comma_free_and_adjacency_audit": cf,
        "equal_adjacent_block_pair_histogram": dict(sorted(equalities.items())),
        "equal_block_q_polynomial_low_to_high": coefficients,
        "rational_block_scales": list(rational_scales),
        "rational_block_q_polynomial_low_to_high": rational_coefficients,
        "rational_weight_density": str(rational_density),
        "uniform_density": str(Fraction(len(code), 4**4)),
        "finite_cases": [{"m": c["m"],
                          "ordered_block_sizes": c["ordered_block_sizes"],
                          "ambient_vertices": len(c["ambient_vertices_lexicographic"]),
                          "selected_vertices": c["claimed_selected_count"],
                          "all_ambient_BFS_ordered_pairs":
                              c["all_ambient_ordered_pair_BFS_distances_checked"],
                          **c["gp_audit"]} for c in cases],
        "negative_controls": certificate["negative_controls"],
        "certificate_file": target.name,
        "certificate_sha256": sha256(target.read_bytes()).hexdigest(),
        "claim_boundary": "Exact finite strict-code verification plus original-adjacency/BFS audits. The arbitrary-block GP theorem is a written lift proof. No optimum-code enumeration or Lean theorem is used.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
