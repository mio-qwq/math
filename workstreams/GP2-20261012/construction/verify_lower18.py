#!/usr/bin/env python3
"""Independent audit of the ternary strict code a<=c, b>d.

Python standard library only.  The graph is reconstructed from the original
shift-and-append adjacency; no optimizer, inherited certificate, or overlap
formula supplies the distances used to check general position.

Run from the repository root:
  python workstreams/GP2-20261012/construction/verify_lower18.py

The deterministic certificate contains original adjacency, exact selected
vertices, and every selected-pair distance in the four finite audits.  The
all-parameter theorem is proved in LOWER18_INDEPENDENT_REVIEW.md.
"""

from collections import Counter, deque
from copy import deepcopy
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform


HERE = Path(__file__).resolve().parent
Word = tuple[int, ...]
Poly = dict[tuple[int, ...], int]


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def selected_pattern(w: Word) -> bool:
    return w[0] <= w[2] and w[1] > w[3]


def dictionary(alphabet_size: int) -> set[Word]:
    return {w for w in product(range(alphabet_size), repeat=4)
            if selected_pattern(w)}


def strict_audit(code: set[Word], alphabet_size: int) -> dict:
    require(all(len(w) == 4 and all(0 <= x < alphabet_size for x in w)
                for w in code), "dictionary/alphabet binding mismatch")
    histogram = Counter()
    first_violation = None
    for w in product(range(alphabet_size), repeat=8):
        hits = [i for i in range(5) if w[i:i+4] in code]
        histogram[len(hits)] += 1
        if len(hits) > 2 and first_violation is None:
            first_violation = {"word": list(w), "selected_starts": hits}
    return {
        "alphabet_size": alphabet_size,
        "words_checked": alphabet_size**8,
        "occurrence_histogram": dict(sorted(histogram.items())),
        "maximum_selected_occurrences": max(histogram),
        "first_violation": first_violation,
    }


def block_map(sizes: tuple[int, int, int]) -> tuple[int, ...]:
    require(len(sizes) == 3 and all(n >= 0 for n in sizes),
            "invalid block sizes")
    return tuple(i for i, n in enumerate(sizes) for _ in range(n))


def graph_from_adjacency(m: int) -> tuple[list[Word], list[list[int]]]:
    require(m >= 3, "original Kautz alphabet must have at least three letters")
    vertices = [w for w in product(range(m), repeat=4)
                if all(w[i] != w[i+1] for i in range(3))]
    index = {w: i for i, w in enumerate(vertices)}
    adjacency = [[index[w[1:] + (letter,)] for letter in range(m)
                  if letter != w[-1]] for w in vertices]
    require(len(vertices) == m * (m-1)**3, "wrong ambient vertex count")
    return vertices, adjacency


def bfs_all(adjacency: list[list[int]]) -> list[list[int]]:
    rows = []
    for start in range(len(adjacency)):
        row = [-1] * len(adjacency)
        row[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                if row[v] == -1:
                    row[v] = row[u] + 1
                    queue.append(v)
        require(-1 not in row, "unexpected unreachable vertex")
        rows.append(row)
    return rows


def overlap_distance(u: Word, v: Word) -> int:
    if u == v:
        return 0
    for overlap in (3, 2, 1):
        if u[-overlap:] == v[:overlap]:
            return 4-overlap
    return 4


def gp_audit(distance_rows: list[str]) -> dict:
    distances = [[int(c) for c in row] for row in distance_rows]
    n = len(distances)
    require(all(len(row) == n for row in distances), "nonsquare distances")
    checked = 0
    for u in range(n):
        for middle in range(n):
            if middle == u:
                continue
            for v in range(n):
                if v == u or v == middle:
                    continue
                checked += 1
                require(distances[u][v] !=
                        distances[u][middle] + distances[middle][v],
                        f"geodesic triple {u},{middle},{v}")
    require(checked == n*(n-1)*(n-2), "ordered triple count mismatch")
    return {"distinct_ordered_triples_checked": checked,
            "geodesic_triples_found": 0}


def exact_size(sizes: tuple[int, int, int]) -> int:
    x, y, z = sizes
    m = x+y+z
    t = x*y+x*z+y*z
    return t*((m-1)**2-t) + 2*x*y*z


def make_case(sizes: tuple[int, int, int]) -> dict:
    m = sum(sizes)
    vertices, adjacency = graph_from_adjacency(m)
    pi = block_map(sizes)
    chosen = [i for i, w in enumerate(vertices)
              if selected_pattern(tuple(pi[a] for a in w))]
    distances = bfs_all(adjacency)
    for i, u in enumerate(vertices):
        for j, v in enumerate(vertices):
            require(distances[i][j] == overlap_distance(u, v),
                    "BFS/overlap distance disagreement")
    selected_distances = ["".join(str(distances[i][j]) for j in chosen)
                          for i in chosen]
    require(len(chosen) == exact_size(sizes), "exact count formula mismatch")
    gp = gp_audit(selected_distances)
    return {
        "m": m,
        "ordered_block_sizes": list(sizes),
        "ambient_vertices_lexicographic": [list(w) for w in vertices],
        "original_shift_append_adjacency": adjacency,
        "selected_vertex_indices": chosen,
        "selected_vertices": [list(vertices[i]) for i in chosen],
        "selected_pair_distances_as_digit_rows": selected_distances,
        "claimed_selected_count": len(chosen),
        "ambient_ordered_pairs_BFS_checked": len(vertices)**2,
        "maximum_BFS_distance": max(map(max, distances)),
        "gp_audit": gp,
    }


def replay_case(case: dict) -> None:
    sizes = tuple(case["ordered_block_sizes"])
    require(sum(sizes) == case["m"], "alphabet size/block sum mismatch")
    vertices, adjacency = graph_from_adjacency(case["m"])
    require(case["ambient_vertices_lexicographic"] == [list(w) for w in vertices],
            "ambient vertex list mismatch")
    require(case["original_shift_append_adjacency"] == adjacency,
            "original adjacency mismatch")
    pi = block_map(sizes)
    chosen = [i for i, w in enumerate(vertices)
              if selected_pattern(tuple(pi[a] for a in w))]
    require(case["selected_vertex_indices"] == chosen,
            "target set does not equal the defined full lift")
    require(case["selected_vertices"] == [list(vertices[i]) for i in chosen],
            "explicit target vertex mismatch")
    require(case["claimed_selected_count"] == len(chosen) == exact_size(sizes),
            "claimed count mismatch")
    distances = bfs_all(adjacency)
    selected_distances = ["".join(str(distances[i][j]) for j in chosen)
                          for i in chosen]
    require(case["selected_pair_distances_as_digit_rows"] == selected_distances,
            "BFS distance certificate mismatch")
    require(case["ambient_ordered_pairs_BFS_checked"] == len(vertices)**2,
            "ambient ordered-pair count mismatch")
    require(case["maximum_BFS_distance"] == max(map(max, distances)),
            "maximum distance mismatch")
    require(case["gp_audit"] == gp_audit(selected_distances),
            "GP audit count mismatch")


def pconst(n: int, variables: int = 3) -> Poly:
    return {(0,)*variables: n} if n else {}


def pvar(i: int, variables: int = 3) -> Poly:
    powers = [0]*variables
    powers[i] = 1
    return {tuple(powers): 1}


def padd(*polynomials: Poly) -> Poly:
    out = Counter()
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] += coefficient
    return {k: v for k, v in out.items() if v}


def pscale(polynomial: Poly, factor: int) -> Poly:
    return {k: factor*v for k, v in polynomial.items() if factor*v}


def pmul(a: Poly, b: Poly) -> Poly:
    out = Counter()
    for ka, va in a.items():
        for kb, vb in b.items():
            require(len(ka) == len(kb), "polynomial variable mismatch")
            out[tuple(x+y for x, y in zip(ka, kb))] += va*vb
    return {k: v for k, v in out.items() if v}


def ppow(a: Poly, power: int, variables: int = 3) -> Poly:
    out = pconst(1, variables)
    for _ in range(power):
        out = pmul(out, a)
    return out


def psubstitute(a: Poly, values: tuple[Poly, ...], variables: int) -> Poly:
    out = {}
    for powers, coefficient in a.items():
        term = pconst(coefficient, variables)
        for exponent, value in zip(powers, values):
            term = pmul(term, ppow(value, exponent, variables))
        out = padd(out, term)
    return out


def polynomial_audit(code: set[Word]) -> dict:
    x, y, z = (pvar(i) for i in range(3))
    symbols = (x, y, z)
    generated = {}
    for word in code:
        term = symbols[word[0]]
        for i in range(1, 4):
            factor = padd(symbols[word[i]], pconst(-int(word[i] == word[i-1])))
            term = pmul(term, factor)
        generated = padd(generated, term)
    m = padd(x, y, z)
    t = padd(pmul(x, y), pmul(x, z), pmul(y, z))
    compact = padd(pmul(t, padd(ppow(padd(m, pconst(-1)), 2), pscale(t, -1))),
                   pscale(pmul(pmul(x, y), z), 2))
    require(generated == compact, "18-pattern/all-block polynomial mismatch")
    q = pvar(0, 1)
    q1 = padd(q, pconst(1, 1))
    residues = []
    for r, values in enumerate(((q, q, q), (q, q, q1), (q, q1, q1))):
        polynomial = psubstitute(generated, values, 1)
        residues.append({"r": r, "q_coefficients_low_to_high":
                         [polynomial.get((i,), 0) for i in range(5)]})
    expected = [[0, 0, 3, -16, 18], [0, 0, -2, 8, 18],
                [0, 4, 18, 32, 18]]
    require([row["q_coefficients_low_to_high"] for row in residues] == expected,
            "balanced residue polynomial mismatch")
    shifted = psubstitute(generated,
                          (padd(x, pconst(-1)), y, padd(z, pconst(1))), 3)
    difference = padd(shifted, pscale(generated, -1))
    d = padd(x, pscale(z, -1), pconst(-1))
    factor = padd(ppow(x, 2), ppow(y, 2), ppow(z, 2),
                  pscale(x, -3), pscale(z, -1), pconst(2))
    require(difference == pmul(d, factor), "pair-balancing identity mismatch")
    return {
        "all_block_sizes_identity": "N=t*((m-1)^2-t)+2*x*y*z",
        "definitions": "m=x+y+z; t=x*y+x*z+y*z",
        "coefficient_ring": "Z[x,y,z]",
        "expanded_coefficients": {",".join(map(str, k)): v
                                  for k, v in sorted(generated.items())},
        "balanced_residue_polynomials": residues,
        "pair_balancing_difference":
            "(x-z-1)*(x^2+y^2+z^2-3*x-z+2)",
    }


def rejected_case(name: str, case: dict) -> dict:
    try:
        replay_case(case)
    except ValueError as exc:
        return {"name": name, "detected": True, "reason": str(exc)}
    raise ValueError(f"negative control was incorrectly accepted: {name}")


def negative_controls(code: set[Word], first_case: dict) -> list[dict]:
    results = []
    mutated = strict_audit(code | {(0, 0, 0, 0)}, 3)
    require(mutated["first_violation"] is not None, "added word was not rejected")
    results.append({"name": "added_constant_template_word", "detected": True,
                    "witness": mutated["first_violation"]})
    weak = {w for w in product(range(3), repeat=4)
            if w[0] <= w[2] and w[1] >= w[3]}
    mutated = strict_audit(weak, 3)
    require(mutated["first_violation"] is not None, "weak inequality accepted")
    results.append({"name": "strict_inequality_changed_to_weak", "detected": True,
                    "witness": mutated["first_violation"]})
    mutated = strict_audit(dictionary(4), 4)
    require(mutated["first_violation"] is not None, "four-block extension accepted")
    results.append({"name": "three_block_rule_used_on_four_blocks", "detected": True,
                    "witness": mutated["first_violation"]})
    bad = deepcopy(first_case)
    bad["m"] += 1
    results.append(rejected_case("wrong_alphabet_binding", bad))
    bad = deepcopy(first_case)
    row = list(bad["selected_pair_distances_as_digit_rows"][0])
    row[1] = str((int(row[1])+1) % 5)
    bad["selected_pair_distances_as_digit_rows"][0] = "".join(row)
    results.append(rejected_case("damaged_selected_distance", bad))
    bad = deepcopy(first_case)
    bad["selected_vertex_indices"].pop()
    results.append(rejected_case("damaged_target_set", bad))
    bad = deepcopy(first_case)
    bad["original_shift_append_adjacency"][0].pop()
    results.append(rejected_case("removed_original_arc", bad))
    bad = deepcopy(first_case)
    bad["claimed_selected_count"] += 1
    results.append(rejected_case("incorrect_claimed_count", bad))
    return results


def main() -> None:
    code = dictionary(3)
    require(len(code) == 18, "unexpected dictionary size")
    strict = strict_audit(code, 3)
    require(strict["first_violation"] is None, "ternary dictionary is not strict")
    require(strict["maximum_selected_occurrences"] == 2, "wrong strict maximum")
    histogram = Counter(sum(w[i] == w[i+1] for i in range(3)) for w in code)
    polynomials = polynomial_audit(code)
    cases = [make_case(sizes) for sizes in
             ((1, 1, 1), (1, 1, 2), (1, 2, 2), (2, 2, 2))]
    certificate = {
        "schema": "GP2-20261012/independent-lower18/v1",
        "template_alphabet": [0, 1, 2],
        "predicate": "word[0] <= word[2] and word[1] > word[3]",
        "template_words_lexicographic": [list(w) for w in sorted(code)],
        "strict_window_audit": strict,
        "equal_adjacent_block_pair_histogram": dict(sorted(histogram.items())),
        "exact_symbolic_polynomial_audit": polynomials,
        "distance_encoding": "Row and column order: selected_vertex_indices; digits are exact directed BFS distances.",
        "finite_original_graph_cases": cases,
        "negative_controls": negative_controls(code, cases[0]),
    }
    target = HERE / "lower18_certificate.json"
    target.write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":"))
                      + "\n", encoding="utf-8")
    reloaded = json.loads(target.read_text(encoding="utf-8"))
    require(reloaded["template_words_lexicographic"] == [list(w) for w in sorted(code)],
            "serialized dictionary mismatch")
    for case in reloaded["finite_original_graph_cases"]:
        replay_case(case)
    summary = {
        "result": "PASS",
        "python": platform.python_version(),
        "template_size": len(code),
        "strict_window_audit": strict,
        "exact_symbolic_polynomial_audit": polynomials,
        "finite_cases": [{"m": c["m"],
                          "ordered_block_sizes": c["ordered_block_sizes"],
                          "ambient_vertices": len(c["ambient_vertices_lexicographic"]),
                          "selected_vertices": c["claimed_selected_count"],
                          "all_BFS_ordered_pairs": c["ambient_ordered_pairs_BFS_checked"],
                          **c["gp_audit"]} for c in cases],
        "negative_controls": certificate["negative_controls"],
        "certificate_file": target.name,
        "certificate_sha256": sha256(target.read_bytes()).hexdigest(),
        "claim_boundary": "Finite original-adjacency/BFS audit and exact polynomial identities; the universal strict-code and GP theorem is a separate written proof, not a full Lean theorem.",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
