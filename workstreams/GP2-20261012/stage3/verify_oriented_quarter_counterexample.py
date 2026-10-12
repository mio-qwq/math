#!/usr/bin/env python3
"""Exact, standard-library check of the oriented 1/4 trace obstruction."""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def direct_counts(rows):
    """Reconstruct all five counts directly from their four-index sums."""
    n = len(rows)
    T = L = Y = X = R4 = 0
    for a, b, c, d in product(range(n), repeat=4):
        # R is the adjacency matrix of the underlying undirected graph.
        rab = rows[a][b] + rows[b][a]
        rbc = rows[b][c] + rows[c][b]
        rcd = rows[c][d] + rows[d][c]
        rda = rows[d][a] + rows[a][d]
        R4 += rab * rbc * rcd * rda
        L += rows[a][b] * rows[b][c] * rows[c][d] * rows[d][a]
        X += rows[a][b] * rows[b][c] * rows[c][d] * rows[a][d]
        Y += rows[a][b] * rows[b][c] * rows[d][c] * rows[a][d]
        T += rows[a][b] * rows[c][b] * rows[c][d] * rows[a][d]
    return {"T": T, "L": L, "Y": Y, "X": X, "R4": R4}


def verify(data):
    n = data["order"]
    encoded = data["matrix_rows"]
    require(type(n) is int and n == 24, "order binding")
    require(len(encoded) == n, "row count")
    require(all(type(row) is str and len(row) == n for row in encoded), "row width")
    require(all(set(row) <= {"0", "1"} for row in encoded), "binary entries")
    rows = [[int(entry) for entry in row] for row in encoded]
    require(all(rows[i][i] == 0 for i in range(n)), "zero diagonal")
    require(all(rows[i][j] * rows[j][i] == 0
                for i in range(n) for j in range(n)), "no digons")

    counts = direct_counts(rows)
    expected = data["expected"]
    for key in ("T", "L", "Y", "X", "R4"):
        require(counts[key] == expected[key], f"{key} binding")
    T, L, Y, X, R4 = (counts[key] for key in ("T", "L", "Y", "X", "R4"))
    require(R4 == 2 * L + 8 * X + 4 * Y + 2 * T, "sixteen-term trace identity")
    numerator = 2 * (T + L)
    ratio = Fraction(numerator, R4)
    gap = R4 - 8 * (T + L)
    require(numerator == expected["numerator_2_T_plus_L"], "numerator binding")
    require(str(ratio) == expected["reduced_ratio"], "ratio binding")
    require(gap == expected["quarter_gap_R4_minus_8_T_plus_L"], "gap binding")
    require(ratio < Fraction(1, 4), "does not refute quarter coefficient")
    # This is exactly the equivalent proposed inequality that fails.
    require(4 * X + 2 * Y > 3 * (T + L), "equivalent quartic gap")
    return {
        **counts,
        "ratio": str(ratio),
        "quarter_gap": gap,
        "equivalent_gap": 4 * X + 2 * Y - 3 * (T + L),
    }


def main():
    path = Path(__file__).resolve().parent / "oriented_quarter_counterexample.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    result = verify(data)
    rejected = []

    damaged = json.loads(json.dumps(data))
    damaged["expected"]["R4"] += 1
    try:
        verify(damaged)
    except ValueError as error:
        rejected.append({"damage": "R4+1", "reason": str(error)})
    else:
        raise RuntimeError("altered count accepted")

    damaged = json.loads(json.dumps(data))
    row = list(damaged["matrix_rows"][0])
    row[1] = "1"                         # creates the digon 0<->1
    damaged["matrix_rows"][0] = "".join(row)
    try:
        verify(damaged)
    except ValueError as error:
        rejected.append({"damage": "insert digon", "reason": str(error)})
    else:
        raise RuntimeError("digon accepted")

    print(json.dumps({
        "status": "PASS",
        "result": result,
        "negative_controls": rejected,
        "scope": data["scope"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
