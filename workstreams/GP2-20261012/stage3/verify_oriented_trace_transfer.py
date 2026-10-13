#!/usr/bin/env python3
"""Exact structured counterexamples; no optimizer or floating point used.

The 46-vertex witness is checked by matrix products and literal four-index
expansion. The 1057-vertex witness is checked by group convolution and a
separate reconstruction of every outgoing-neighbor set and rooted walks.
"""
from collections import Counter
from fractions import Fraction
import argparse
import hashlib
import json
from math import isqrt
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def transpose(m):
    return [list(row) for row in zip(*m)]


def multiply(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt]
            for row in a]


def matrix_counts(m):
    n = len(m)
    mt = transpose(m)
    mm = multiply(m, m)
    mmt = multiply(m, mt)
    m3 = multiply(mm, m)
    r = [[m[i][j] + m[j][i] for j in range(n)] for i in range(n)]
    r2 = multiply(r, r)
    return {
        "T": sum(x * x for row in mmt for x in row),
        "L": sum(mm[i][j] * mm[j][i] for i in range(n) for j in range(n)),
        "X": sum(m3[i][j] * m[i][j] for i in range(n) for j in range(n)),
        "Y": sum(x * x for row in mm for x in row),
        "R4": sum(x * x for row in r2 for x in row),
    }


def four_index_counts(m):
    n = len(m)
    t = ell = x = y = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    t += m[a][b] * m[c][b] * m[c][d] * m[a][d]
                    ell += m[a][b] * m[b][c] * m[c][d] * m[d][a]
                    x += m[a][b] * m[b][c] * m[c][d] * m[a][d]
                    y += m[a][b] * m[b][c] * m[a][d] * m[d][c]
    return {"T": t, "L": ell, "X": x, "Y": y}


def derived(counts):
    t, ell, x, y, r = (counts[k] for k in ("T", "L", "X", "Y", "R4"))
    require(r == 2 * ell + 8 * x + 4 * y + 2 * t, "sixteen-term identity")
    ratio = Fraction(2 * (t + ell), r)
    return {
        **counts,
        "candidate_slack": t + ell - 2 * x,
        "fifth_slack": 10 * (t + ell) - r,
        "ratio_numerator": ratio.numerator,
        "ratio_denominator": ratio.denominator,
    }


def matrix_digest(m):
    digest = hashlib.sha256()
    for row in m:
        require(all(x in (0, 1) for x in row), "binary matrix digest")
        digest.update(("".join(str(x) for x in row) + "\n").encode("ascii"))
    return digest.hexdigest()


def paley(q):
    require(q > 2 and q % 4 == 3, "Paley modulus class")
    require(all(q % d for d in range(2, isqrt(q) + 1)), "prime modulus")
    residues = {x * x % q for x in range(1, q)}
    require(len(residues) == (q - 1) // 2, "residue count")
    require(not residues.intersection({-x % q for x in residues}), "no digons")
    return [[int((j - i) % q in residues) for j in range(q)] for i in range(q)]


def jordan_witness(spec):
    require(spec == {"prime": 23, "tensor_rows": [[1, 1], [0, 1]]},
            "Jordan construction binding")
    a = paley(spec["prime"])
    q = len(a)
    m = [row + row for row in a] + [[0] * q + row for row in a]
    require(all(m[i][i] == 0 for i in range(2 * q)), "Jordan zero diagonal")
    require(all(not (m[i][j] and m[j][i])
                for i in range(2 * q) for j in range(2 * q)), "Jordan no digons")
    direct = four_index_counts(m)
    products = matrix_counts(m)
    require(direct == {k: products[k] for k in direct}, "four-index mismatch")
    ac = matrix_counts(a)
    require([products[k] for k in ("T", "L", "X", "Y")] ==
            [7 * ac["T"], 2 * ac["L"], 5 * ac["X"], 6 * ac["Y"]],
            "tensor multiplicativity")
    result = derived(products)
    require(result["candidate_slack"] == -759, "candidate not refuted")
    return {"order": 2 * q, "matrix_sha256": matrix_digest(m),
            "four_index_tuples": (2 * q) ** 4, **result}


def group_add(a, b, q):
    return ((a // q + b // q) % 7) * q + (a % q + b % q) % q


def inverse(a, q):
    i, j = divmod(a, q)
    return (-i % 7) * q + (-j % q)


def cayley_support(spec):
    q = spec["prime"]
    paley(q)  # independently checks primality and the residue orientation
    residues = sorted({x * x % q for x in range(1, q)})
    require(spec["major_shifts"] == [0, 4] and spec["minor_shift"] == 1,
            "Cayley shifts binding")
    require(spec["minor_stride"] == 5, "minor stride binding")
    minor = residues[::spec["minor_stride"]]
    require(minor == spec["minor_residues"], "minor residue binding")
    support = ({a * q + b for a in spec["major_shifts"] for b in residues} |
               {spec["minor_shift"] * q + b for b in minor})
    require(0 not in support, "Cayley zero diagonal")
    require(not support.intersection({inverse(x, q) for x in support}),
            "Cayley no digons")
    return q, support


def convolution_counts(q, support):
    n = 7 * q
    two = [0] * n
    for a in support:
        for b in support:
            two[group_add(a, b, q)] += 1
    t = n * sum(x * x for x in two)
    ell = n * sum(two[a] * two[inverse(a, q)] for a in range(n))
    x = n * sum(two[group_add(a, inverse(b, q), q)]
                for a in support for b in support)
    symmetric = support | {inverse(a, q) for a in support}
    symtwo = [0] * n
    for a in symmetric:
        for b in symmetric:
            symtwo[group_add(a, b, q)] += 1
    r4 = n * sum(x * x for x in symtwo)
    return {"T": t, "L": ell, "X": x, "Y": t, "R4": r4}


def adjacency_counts(q, support):
    """Literal neighbor sets and rooted walks, without convolution formulas."""
    n = 7 * q
    out = [{group_add(v, s, q) for s in support} for v in range(n)]
    t = n * sum(len(out[0].intersection(out[v])) ** 2 for v in range(n))
    paths2 = Counter(v for a in out[0] for v in out[a])
    paths3 = Counter()
    for a, multiplicity in paths2.items():
        for v in out[a]:
            paths3[v] += multiplicity
    ell = n * sum(value for v, value in paths3.items() if 0 in out[v])
    x = n * sum(value for v, value in paths3.items() if v in out[0])
    y = n * sum(value ** 2 for value in paths2.values())
    incoming0 = {v for v in range(n) if 0 in out[v]}
    neighbors0 = out[0] | incoming0
    symmetric2 = Counter()
    for a in neighbors0:
        # Derive the incoming set from literal adjacency, not from -support.
        neighbors = out[a] | {v for v in range(n) if a in out[v]}
        symmetric2.update(neighbors)
    r4 = n * sum(value ** 2 for value in symmetric2.values())
    digest = hashlib.sha256()
    for neighbors in out:
        digest.update(("".join("1" if v in neighbors else "0" for v in range(n))
                       + "\n").encode("ascii"))
    return {"T": t, "L": ell, "X": x, "Y": y, "R4": r4}, digest.hexdigest()


def cayley_witness(spec):
    q, support = cayley_support(spec)
    convolution = convolution_counts(q, support)
    adjacency, digest = adjacency_counts(q, support)
    require(convolution == adjacency, "Cayley convolution/adjacency mismatch")
    result = derived(adjacency)
    require(result["fifth_slack"] < 0, "fifth coefficient not refuted")
    return {"order": 7 * q, "degree": len(support), "matrix_sha256": digest,
            "rooted_three_walks": len(support) ** 3, **result}


def base_counterexample(spec):
    weights = spec["circulant_weights"]
    require(weights == [5, 1, 0, 0, 5, 0, 0], "base circulant binding")
    b = [[weights[(j - i) % 7] for j in range(7)] for i in range(7)]
    result = derived(matrix_counts(b))
    require(four_index_counts(b) == {k: result[k] for k in ("T", "L", "X", "Y")},
            "base four-index mismatch")
    require(5 * result["ratio_numerator"] < result["ratio_denominator"],
            "transfer ceiling not below fifth")
    return {"order": 7, **result}


def weighted_local_obstruction():
    m = [[0, 0, 1, 1], [0, 0, 2, 0], [0, 0, 0, 0], [0, 1, 0, 0]]
    mm = multiply(m, m)
    mmt = multiply(m, transpose(m))
    mtm = multiply(transpose(m), m)
    i, k = 2, 3
    flags = [mm[i][k], mm[k][i], mmt[i][k], mtm[i][k]]
    require(flags == [0, 2, 0, 1], "weighted local flags")
    x, y, z, w = flags
    require((z-x)*(z-y)+(w-x)*(w-y) == -1, "weighted local failure")
    kernel = [[int(value > 0) for value in row] for row in m]
    mu = [Fraction(value, 5) for value in (1, 2, 1, 1)]
    # The endpoint square-root factor is exactly 1/5 here, hence no roots.
    factor = Fraction(1, 5)
    fx = factor * sum(mu[j]*kernel[i][j]*kernel[j][k] for j in range(4))
    fy = factor * sum(mu[j]*kernel[k][j]*kernel[j][i] for j in range(4))
    fz = factor * sum(mu[j]*kernel[i][j]*kernel[k][j] for j in range(4))
    fw = factor * sum(mu[j]*kernel[j][i]*kernel[j][k] for j in range(4))
    value = (fz-fx)*(fz-fy)+(fw-fx)*(fw-fy)
    require(value == Fraction(-1, 625), "product-weight local failure")
    return {"order": 4, "integer_flags": flags, "integer_bracket": -1,
            "product_weight_flags": [str(v) for v in (fx, fy, fz, fw)],
            "product_weight_bracket": str(value)}


def verify(data):
    require(data["schema"] == "GP2-oriented-transfer-v1", "schema binding")
    results = {
        "jordan46": jordan_witness(data["jordan46"]["construction"]),
        "cayley1057": cayley_witness(data["cayley1057"]["construction"]),
        "base7": base_counterexample(data["base7"]["construction"]),
        "weighted_local4": weighted_local_obstruction(),
    }
    for name, result in results.items():
        require(result == data[name]["expected"], f"expected result binding: {name}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--derive", action="store_true", help="print computed records only")
    args = parser.parse_args()
    path = Path(__file__).resolve().parent / "oriented_trace_transfer_certificate.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if args.derive:
        print(json.dumps({
            "jordan46": jordan_witness(data["jordan46"]["construction"]),
            "cayley1057": cayley_witness(data["cayley1057"]["construction"]),
            "base7": base_counterexample(data["base7"]["construction"]),
            "weighted_local4": weighted_local_obstruction(),
        }, indent=2, sort_keys=True))
        return
    result = verify(data)
    rejected = []
    for target, field in [("jordan46", "candidate_slack"),
                          ("cayley1057", "fifth_slack"),
                          ("base7", "ratio_denominator")]:
        damaged = json.loads(json.dumps(data))
        damaged[target]["expected"][field] += 1
        try:
            verify(damaged)
        except ValueError as error:
            rejected.append({"damage": f"altered {target}.{field}", "reason": str(error)})
        else:
            raise RuntimeError("tampered count accepted")
    for target in ("jordan46", "cayley1057"):
        damaged = json.loads(json.dumps(data))
        damaged[target]["construction"]["prime"] += 2
        try:
            verify(damaged)
        except ValueError as error:
            rejected.append({"damage": f"altered {target} modulus", "reason": str(error)})
        else:
            raise RuntimeError("tampered modulus accepted")
    damaged = json.loads(json.dumps(data))
    damaged["cayley1057"]["construction"]["minor_residues"][0] = 0
    try:
        verify(damaged)
    except ValueError as error:
        rejected.append({"damage": "altered minor residue", "reason": str(error)})
    else:
        raise RuntimeError("tampered residue accepted")
    print(json.dumps({"status": "PASS", "results": result,
                      "negative_controls": rejected,
                      "scope": "Both candidate and 1/5 coefficient refuted; no Ka4 bound changed."},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
