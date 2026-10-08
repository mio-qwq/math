"""Exact certificates for two reflexive local pair-cost families.

Standard library only. Rebuilds every actual conflict/coverage edge and actual
uncovered set. Optional edge packing certifies cover sharpness. Does not prove
the unrestricted local-cost conjecture; parameter-wide proofs are in the note.
All require checks remain active under python -O.
"""

from __future__ import annotations

import copy
import json
import sys
from fractions import Fraction as Q


def require(ok, message):
    if not ok:
        raise ValueError(message)


def rational(value):
    require(type(value) is str, "costs and parameters must be rational strings")
    result = Q(value)
    require(result >= 0, "negative cost or parameter")
    return result


def matrix(raw, n, m):
    require(isinstance(raw, list) and len(raw) == n, "incorrect matrix rows")
    require(all(isinstance(row, list) and len(row) == m for row in raw), "incorrect matrix columns")
    return {(i, j): rational(v) for i, row in enumerate(raw) for j, v in enumerate(row)}


def relation(raw, n):
    require(isinstance(raw, list), "relation must be a list")
    result = set()
    for pair in raw:
        require(isinstance(pair, list) and len(pair) == 2 and all(type(v) is int for v in pair),
                "invalid relation pair")
        a, b = pair
        require(0 <= a < n and 0 <= b < n, "relation outside domain")
        require((a, b) not in result, "duplicate relation pair")
        result.add((a, b))
    require(all((i, i) in result for i in range(n)), "relation not reflexive")
    return result


def node(tag, pair):
    return tag, pair[0], pair[1]


def graph(n, m, E, F, x, y, h, z):
    grid = {(i, j) for i in range(n) for j in range(m)}
    conflicts = {(r, c) for r in grid for c in grid if (r[0], c[0]) in E and (c[1], r[1]) in F}
    H = {(r[0], c[1]) for r, c in conflicts}
    Z = {(c[0], r[1]) for r, c in conflicts}
    require(H == grid and Z == grid, "diagonal corner identity failed")
    edges = {(node("R", r), node("C", c)) for r, c in conflicts}
    edges |= {(node("R", r), node("ZR", t)) for r in grid for t in Z
              if r[1] == t[1] and (r[0], t[0]) in E}
    edges |= {(node("ZL", t), node("C", c)) for t in Z for c in grid
              if t[0] == c[0] and (c[1], t[1]) in F}
    for (p, j), (i, s) in conflicts:
        require(x[p, j] * y[i, s] <= h[p, s] * z[i, j], "actual local constraint failed")
    weights = {node("R", t): x[t] for t in grid}
    weights.update({node("C", t): y[t] for t in grid})
    weights.update({node(tag, t): z[t] for t in grid for tag in ("ZL", "ZR")})
    return grid, conflicts, edges, weights


def verify_cover(cover, grid, E, F, edges, weights, h, z):
    require(cover <= set(weights), "invalid cover vertex")
    require(cover <= {v for edge in edges for v in edge}, "isolated vertex selected")
    require(all(a in cover or b in cover for a, b in edges), "uncovered actual graph edge")
    kept_r = {r for r in grid if node("R", r) not in cover}
    kept_c = {c for c in grid if node("C", c) not in cover}
    require(all((r[0], c[0]) not in E or (c[1], r[1]) not in F for r in kept_r for c in kept_c),
            "survivors conflict")
    U = {t for t in grid if not any(r[1] == t[1] and (r[0], t[0]) in E for r in kept_r)
         and not any(c[0] == t[0] and (c[1], t[1]) in F for c in kept_c)}
    cover_cost = sum((weights[v] for v in cover), Q(0))
    deleted = sum((weights[node("R", r)] for r in grid - kept_r), Q(0))
    deleted += sum((weights[node("C", c)] for c in grid - kept_c), Q(0))
    require(cover_cost <= sum(h.values(), Q(0)) + sum(z.values(), Q(0)), "cover bound failed")
    require(deleted <= sum(h.values(), Q(0)) + sum((z[t] for t in U), Q(0)), "pruning bound failed")
    return cover_cost, deleted, U


def exchange_witness(a, b):
    """Each entry is (probability, R pair, C pair), indexed by its H corner."""
    mu = {t: [(Q(1), t, t)] for t in ((0, 0), (0, 1), (1, 0), (1, 1))}
    if b >= a and b > 0:
        theta = (b - a) / b
        mu[0, 0] = [(1 - theta, (0, 0), (0, 0)), (theta, (0, 1), (0, 0))]
        mu[0, 1] = [(1 - theta, (0, 1), (0, 1)), (theta, (0, 1), (1, 1))]
    elif a >= b and a > 0:
        theta = (a - b) / a
        mu[0, 0] = [(1 - theta, (0, 0), (0, 0)), (theta, (0, 0), (1, 0))]
        mu[1, 0] = [(1 - theta, (1, 0), (1, 0)), (theta, (1, 1), (1, 0))]
    return mu


def check(case):
    family = case["family"]
    require(family in ("proportional", "exchange"), "unknown family")
    dims = case["sizes"]
    require(isinstance(dims, list) and len(dims) == 2 and
            all(type(v) is int and v >= 0 for v in dims), "invalid dimensions")
    n, m = dims
    E, F = relation(case["E"], n), relation(case["F"], m)
    h, z = matrix(case["h"], n, m), matrix(case["z"], n, m)
    if family == "proportional":
        w, kappa = matrix(case["w"], n, m), rational(case["kappa"])
        x, y = w, {t: kappa * value for t, value in w.items()}
    else:
        require((n, m) == (2, 2), "exchange family must be 2 by 2")
        path = {(0, 0), (0, 1), (1, 1)}
        require(E == path and F == path, "exchange family requires the two specified paths")
        a, b = rational(case["a"]), rational(case["b"])
        x = {(0, 0): a, (0, 1): b, (1, 0): b, (1, 1): a}
        y = {(0, 0): b, (0, 1): a, (1, 0): a, (1, 1): b}
    grid, conflicts, edges, weights = graph(n, m, E, F, x, y, h, z)
    covers = [({node(tag, t) for tag in tags for t in grid}, label)
              for tags, label in ((('R', 'ZL'), 'delete_R'), (('C', 'ZR'), 'delete_C'),
                                  (('R', 'C'), 'delete_both'))]
    result = {"family": family, "actual_conflicts": len(conflicts),
              "H_mass": str(sum(h.values(), Q(0))), "Z_mass": str(sum(z.values(), Q(0)))}
    if family == "proportional":
        H0 = sum(h.values(), Q(0))
        X0, Y0 = sum(x.values(), Q(0)), sum(y.values(), Q(0))
        require(X0 * Y0 <= H0 * sum(z.values(), Q(0)), "total multiplicative bound failed")
        selected = covers[0] if X0 <= H0 else covers[1] if Y0 <= H0 else covers[2]
        expected_U = set() if selected[1] != 'delete_both' else grid
        amount, deletion, U = verify_cover(selected[0], grid, E, F, edges, weights, h, z)
        require(U == expected_U, "incorrect three-cover actual U")
        result.update(selected_cover=selected[1], cover_cost=str(amount), deletion_cost=str(deletion),
                      uncovered=[list(t) for t in sorted(U)])
        if case.get("sharp", False):
            require(type(case["sharp"]) is bool, "sharp flag must be boolean")
            require(all(h[t] == min(Q(1), kappa) * w[t] and z[t] == max(Q(1), kappa) * w[t]
                        for t in grid), "incorrect sharp family costs")
            packing = {}
            for t in grid:
                packing[node("R", t), node("ZR", t)] = x[t]
                packing[node("ZL", t), node("C", t)] = y[t]
            load = {v: Q(0) for v in weights}
            for (u, v), value in packing.items():
                require((u, v) in edges and value >= 0, "packing uses nonedge")
                load[u] += value; load[v] += value
            require(all(load[v] <= weights[v] for v in weights), "packing exceeds vertex cost")
            lower = sum(packing.values(), Q(0))
            require(lower == amount == H0 + sum(z.values(), Q(0)), "sharp cover equality failed")
            # The deletion lower bound is symbolic: each diagonal pair pays
            # min(x,y), plus max(x,y) when its corner is actually uncovered.
            require(all(min(x[t], y[t]) == h[t] and max(x[t], y[t]) == z[t] for t in grid),
                    "diagonal deletion lower certificate failed")
            require(deletion == H0 + sum((z[t] for t in U), Q(0)), "sharp pruning equality failed")
            result.update(packing_value=str(lower), diagonal_pruning_lower_bound="H+actual_U")
    else:
        require(len(conflicts) == 9, "incorrect two-path original edges")
        expected_conflicts = {((0, 0), (0, 0)), ((0, 0), (1, 0)),
                              ((0, 1), (0, 0)), ((0, 1), (0, 1)),
                              ((0, 1), (1, 0)), ((0, 1), (1, 1)),
                              ((1, 0), (1, 0)), ((1, 1), (1, 0)), ((1, 1), (1, 1))}
        require(conflicts == expected_conflicts, "actual nine-edge identity failed")
        mu = exchange_witness(a, b)
        v = {t: Q(0) for t in grid}
        B = {t: Q(0) for t in grid}
        for corner, terms in mu.items():
            require(sum((prob for prob, r, c in terms), Q(0)) == 1, "witness probabilities not normalized")
            for prob, r, c in terms:
                require(prob >= 0 and (r, c) in conflicts and (r[0], c[1]) == corner,
                        "invalid witness support")
                angle = c[0], r[1]
                v[angle] += prob * x[r] * y[c]
                B[angle] += prob * h[corner]
        require(sum(B.values(), Q(0)) == sum(h.values(), Q(0)), "H distribution mass mismatch")
        require(all(v[t] <= B[t] * z[t] for t in grid), "weighted local bound failed")
        expected_v = ({(0, 0): a*a, (0, 1): a*a+b*b-a*b, (1, 0): a*b, (1, 1): b*b}
                      if b >= a else {(0, 0): b*b, (0, 1): a*b, (1, 0): b*b+a*a-a*b, (1, 1): a*a})
        require(v == expected_v, "symbolic witness identity failed")
        require((a*a+b*b-a*b) >= a*b, "two-root symbolic inequality failed")
        amount, deletion, U = verify_cover(covers[2][0], grid, E, F, edges, weights, h, z)
        require(U == grid and amount == deletion == 4*(a+b), "all-original cover identity failed")
        result.update(selected_cover='delete_both', cover_cost=str(amount), deletion_cost=str(deletion),
                      uncovered=[list(t) for t in sorted(U)], witness_v=[str(v[t]) for t in sorted(v)])
        if "sqrt_lower" in case:
            ell = matrix(case["sqrt_lower"], n, m)
            require(all(ell[t]**2 <= v[t] for t in grid), "invalid rational square-root lower bound")
            margin = 2*sum(ell.values(), Q(0))-amount
            require(margin >= 0, "rational witness does not pay original cost")
            result["all_angle_costs_certified_margin"] = str(margin)
    if "expected" in case:
        require(isinstance(case["expected"], dict), "expected fields must be an object")
        require(all(result.get(key) == value for key, value in case["expected"].items()),
                "expected result mismatch")
    return result


def read_suite(path):
    with open(path, encoding="utf-8") as stream:
        suite = json.load(stream)
    require(suite.get("format") == "reflexive-cost-families-v1" and isinstance(suite["cases"], list),
            "invalid suite format")
    return suite


def self_test(path):
    suite = read_suite(path)
    results = [check(case) for case in suite["cases"]]
    sharp = next(case for case in suite["cases"] if case.get("sharp") and case["kappa"] == "3")
    mixed = next(case for case in suite["cases"] if case.get("sqrt_lower") and case["a"] == "1")
    bad = []
    def mutation(original, mutate):
        item = copy.deepcopy(original);mutate(item);bad.append(item)
    mutation(sharp, lambda c: c["E"].remove([0, 0]))
    mutation(sharp, lambda c: c["h"][0].__setitem__(0, "0"))
    mutation(sharp, lambda c: c["w"][0].__setitem__(0, "-1"))
    mutation(sharp, lambda c: c["E"].append(c["E"][0]))
    mutation(sharp, lambda c: c.update(kappa=3))
    mutation(mixed, lambda c: c["sqrt_lower"][0].__setitem__(1, "4"))
    mutation(mixed, lambda c: c["F"].append([1, 0]))
    for case in bad:
        try:
            check(case)
        except ValueError:
            pass
        else:
            raise ValueError("damaged family certificate accepted")
    return {"status": "PASS", "cases_checked": len(results), "mutations_rejected": len(bad)}


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        from pathlib import Path
        path = Path(__file__).resolve().parents[1] / "examples" / "reflexive-cost-families.json"
        print(json.dumps(self_test(path), sort_keys=True));return
    require(len(sys.argv) == 2, "usage: check_reflexive_cost_families.py SUITE | --self-test")
    suite = read_suite(sys.argv[1])
    print(json.dumps({"status": "ACCEPT", "cases": [
        {"name": case["name"], **check(case)} for case in suite["cases"]]}, sort_keys=True))


if __name__ == "__main__":
    main()
