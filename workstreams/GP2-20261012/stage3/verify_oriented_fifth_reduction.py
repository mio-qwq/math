#!/usr/bin/env python3
"""Exact identities, exhaustive small cases, and a local-obstruction check."""
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def add(a, b, sign=1):
    return [[a[i][j] + sign * b[i][j] for j in range(len(a))]
            for i in range(len(a))]


def counts(m):
    mt = transpose(m)
    mm = matmul(m, m)
    mmt = matmul(m, mt)
    T = trace(matmul(mmt, mmt))
    L = trace(matmul(mm, mm))
    Y = trace(matmul(mm, matmul(mt, mt)))
    X = trace(matmul(matmul(mm, m), mt))
    r = add(m, mt)
    s = add(m, mt, -1)
    rhs4 = trace(matmul(matmul(matmul(s, s), s), s))
    rhs4 += trace(matmul(matmul(matmul(r, s), r), s))
    return T, L, X, Y, T + L - 2 * X, rhs4


def oriented_matrices(n):
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    for states in product(range(3), repeat=len(pairs)):
        m = [[0] * n for _ in range(n)]
        for state, (i, j) in zip(states, pairs):
            if state == 1:
                m[i][j] = 1
            elif state == 2:
                m[j][i] = 1
        yield m


def verify(data, exhaustive=True):
    witness = data["pointwise_obstruction"]
    rows = witness["matrix_rows"]
    n = witness["order"]
    require(n == 5 and len(rows) == n and all(len(row) == n for row in rows),
            "witness dimensions")
    m = [[int(value) for value in row] for row in rows]
    require(all(m[i][i] == 0 for i in range(n)), "zero diagonal")
    require(all(m[i][j] * m[j][i] == 0 for i in range(n) for j in range(n)),
            "no digons")

    i, k = witness["ordered_pair"]
    mm = matmul(m, m)
    mmt = matmul(m, transpose(m))
    mtm = matmul(transpose(m), m)
    x, y, z, w = mm[i][k], mm[k][i], mmt[i][k], mtm[i][k]
    local = (z - x) * (z - y) + (w - x) * (w - y)
    require([x, y, z, w] == witness["x_y_z_w"], "local flags")
    require(local == witness["pointwise_sum"] == -1, "pointwise obstruction")

    T, L, X, Y, D, rhs4 = counts(m)
    require([T, L, X, Y, D] == witness["global_T_L_X_Y_D"], "global counts")
    require(rhs4 == 4 * D, "R/S trace identity")

    tested = 0
    minima = {}
    if exhaustive:
        for order in range(1, 6):
            minimum = None
            cases = 0
            for matrix in oriented_matrices(order):
                t, ell, xx, yy, dd, rr = counts(matrix)
                require(rr == 4 * dd, "exhaustive trace identity")
                require(dd >= 0, "small candidate counterexample")
                minimum = dd if minimum is None else min(minimum, dd)
                cases += 1
            minima[str(order)] = {"cases": cases, "minimum_D": minimum}
            tested += cases
    return {
        "witness_local_sum": local,
        "witness_global_D": D,
        "trace_identity_rhs": rhs4,
        "exhaustive_cases": tested,
        "exhaustive_by_order": minima,
    }


def main():
    path = Path(__file__).resolve().parent / "oriented_fifth_reduction.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    result = verify(data)
    rejected = []

    damaged = json.loads(json.dumps(data))
    damaged["pointwise_obstruction"]["pointwise_sum"] = 0
    try:
        verify(damaged, exhaustive=False)
    except ValueError as error:
        rejected.append({"damage": "local sum changed", "reason": str(error)})
    else:
        raise RuntimeError("altered local sum accepted")

    damaged = json.loads(json.dumps(data))
    row = list(damaged["pointwise_obstruction"]["matrix_rows"][3])
    row[0] = "1"                         # opposite to the existing 0->3 arc
    damaged["pointwise_obstruction"]["matrix_rows"][3] = "".join(row)
    try:
        verify(damaged, exhaustive=False)
    except ValueError as error:
        rejected.append({"damage": "digon inserted", "reason": str(error)})
    else:
        raise RuntimeError("digon accepted")

    print(json.dumps({
        "status": "PASS",
        "result": result,
        "negative_controls": rejected,
        "scope": "Exact reduction and small evidence; the 1/5 coefficient remains unproved."
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
