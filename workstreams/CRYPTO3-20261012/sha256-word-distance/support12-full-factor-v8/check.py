#!/usr/bin/env python3
"""Definition-level checker for the exact support-12 factorisation."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 1 << 32
MASK = N - 1
ACTIVE = [10, 11, 15, 18, 20, 26, 27, 28, 29, 34, 42, 43, 57]
KINDS = ("d", "F", "G")
VARIABLES = [f"{kind}{i}" for i in ACTIVE for kind in KINDS]
FREE = [
    "d10", "d11", "d15", "F11", "G10", "G11", "F15",
    "G18", "G26", "F27", "G27", "F29", "F42", "F57",
]
PIVOTS = [v for v in VARIABLES if v not in FREE]


def lin(**kw):
    return {k: v for k, v in kw.items() if v}


# Each entry is the right side of (d_i,F_i,G_i), in the 14 free symbols.
FACTOR_RHS = {
    10: (lin(d10=1), lin(d11=-1), lin(G10=1)),
    11: (lin(d11=1), lin(F11=1), lin(G11=1)),
    15: (lin(d15=1), lin(F15=1), lin(d10=-1)),
    18: (lin(d11=1), lin(F11=-1, d10=-1), lin(G18=1)),
    20: (lin(G18=1), lin(G26=-1), lin(d15=-1)),
    26: (lin(F11=1, d10=1), lin(G18=-1, d11=-2), lin(G26=1)),
    27: (lin(G18=1, d11=1), lin(F27=1), lin(G27=1)),
    28: (lin(G26=1), lin(G18=-2, d11=-3), lin(F15=-1)),
    29: (lin(G27=1), lin(F29=1), lin(d15=-1)),
    34: (lin(G18=1, d11=2), lin(F27=-1, F11=-1, d10=-1),
         lin(G27=-1, G18=-1)),
    42: (lin(F27=1, F11=1, d10=1), lin(F42=1),
         lin(F29=-1, G26=-1)),
    43: (lin(G18=-1, d11=-2), lin(F27=-1, F11=-1, d10=-1),
         lin(G27=-1)),
    57: (lin(F42=1), lin(F57=1), lin(G18=1, d11=2)),
}


def add_term(row, name, value):
    row[name] = row.get(name, 0) + value
    if row[name] == 0:
        del row[name]


def original_rows(active=ACTIVE, offsets=(2, 7, 15, 16)):
    support = set(active)
    rows = []
    for t in range(16, 64):
        coeff = {}
        if t in support:
            add_term(coeff, f"d{t}", 1)
        for kind, i in (("G", t - offsets[0]), ("d", t - offsets[1]),
                        ("F", t - offsets[2]), ("d", t - offsets[3])):
            if i in support:
                add_term(coeff, f"{kind}{i}", -1)
        rows.append({"t": t, "coefficients": coeff})
    return rows


def dense(coeff):
    return [coeff.get(v, 0) for v in VARIABLES]


def sparse(row):
    return {v: row[i] for i, v in enumerate(VARIABLES) if row[i]}


def apply_operation(matrix, op):
    kind = op["op"]
    if kind == "swap":
        a, b = op["a"], op["b"]
        matrix[a], matrix[b] = matrix[b], matrix[a]
    elif kind == "negate":
        r = op["row"]
        matrix[r] = [-x for x in matrix[r]]
    elif kind == "add":
        t, s, m = op["target"], op["source"], op["multiplier"]
        matrix[t] = [x + m * y for x, y in zip(matrix[t], matrix[s])]
    else:
        raise AssertionError(f"unknown row operation {kind!r}")


def inverse_operation(op):
    if op["op"] in ("swap", "negate"):
        return op
    answer = dict(op)
    answer["multiplier"] = -answer["multiplier"]
    return answer


def expected_reduced():
    result = []
    for pivot in PIVOTS:
        i = int(pivot[1:])
        kind = pivot[0]
        rhs = FACTOR_RHS[i][KINDS.index(kind)]
        coeff = {pivot: 1}
        for name, value in rhs.items():
            add_term(coeff, name, -value)
        result.append({"pivot": pivot, "coefficients": coeff})
    return result


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def gf2_rank(columns):
    basis = {}
    for value in columns:
        x = value
        while x:
            top = x.bit_length() - 1
            if top in basis:
                x ^= basis[top]
            else:
                basis[top] = x
                break
    return len(basis)


def check_payload(data):
    assert data["schema"] == "CRYPTO3-support12-full-factor-v8"
    assert data["modulus"] == N
    assert data["support_index"] == 12
    assert data["active_indices"] == ACTIVE
    assert data["variables"] == VARIABLES
    assert data["free_variables"] == FREE
    assert data["pivot_variables"] == PIVOTS

    source = (HERE / data["support_source"]["path"]).resolve()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == data["support_source"]["sha256"]
    source_data = json.loads(source.read_text())
    assert source_data["supports"][11] == ACTIVE

    rows = original_rows()
    assert data["original_rows"] == rows
    nonzero = [row for row in rows if row["coefficients"]]
    zero = [row["t"] for row in rows if not row["coefficients"]]
    assert len(nonzero) == data["nonzero_row_count"] == 25
    assert len(zero) == data["zero_row_count"] == 23
    assert zero == [16, 19, 21, 23, 24, 32, 37, 38, 39, 40, 46, 47,
                    48, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63]

    matrix0 = [dense(row["coefficients"]) for row in nonzero]
    matrix = copy.deepcopy(matrix0)
    for op in data["integer_unit_row_operations"]:
        apply_operation(matrix, op)
    reduced = expected_reduced()
    assert data["reduced_rows"] == reduced
    assert [sparse(row) for row in matrix] == [x["coefficients"] for x in reduced]
    # Reverse every supplied unit operation: this checks exact module equality,
    # not merely equality of ranks over a convenient field.
    reverse = copy.deepcopy(matrix)
    for op in reversed(data["integer_unit_row_operations"]):
        apply_operation(reverse, inverse_operation(op))
    assert reverse == matrix0

    expected_factor_records = {}
    for i in ACTIVE:
        expected_factor_records[str(i)] = {}
        for kind, rhs in zip(KINDS, FACTOR_RHS[i]):
            name = f"{kind}{i}"
            if name in FREE:
                expected_factor_records[str(i)][kind] = {name: 1}
            else:
                expected_factor_records[str(i)][kind] = next(
                    row["coefficients"] for row in reduced if row["pivot"] == name
                )
    assert data["factor_records"] == expected_factor_records

    appearances = {v: [] for v in FREE}
    for i, triples in FACTOR_RHS.items():
        used = set().union(*[set(expr) for expr in triples])
        for name in used:
            appearances[name].append(i)
    private = {v: where for v, where in appearances.items() if len(where) == 1}
    shared = {v: where for v, where in appearances.items() if len(where) > 1}
    assert private == {"G10": [10], "G11": [11], "F57": [57]}
    assert len(shared) == 11
    # Every pair factor is connected through the shared-variable incidence graph.
    reached = {10}
    changed = True
    while changed:
        changed = False
        for where in shared.values():
            if reached.intersection(where) and not set(where).issubset(reached):
                reached.update(where)
                changed = True
    assert reached == set(ACTIVE)

    # The SHA-256 small sigmas used by every factor are binary-linear bijections.
    assert gf2_rank([sigma0(1 << i) for i in range(32)]) == 32
    assert gf2_rank([sigma1(1 << i) for i in range(32)]) == 32
    return {
        "rows": 48,
        "nonzero_rows": 25,
        "zero_rows": 23,
        "integer_rank": 25,
        "free_rank": 14,
        "private_parameters": private,
        "shared_parameters": shared,
        "connected_pair_factors": 13,
        "sigma0_binary_rank": 32,
        "sigma1_binary_rank": 32,
    }


def negative_controls(pristine):
    tests = []

    bad = copy.deepcopy(pristine)
    bad["active_indices"][-1] = 58
    tests.append(("damaged support", bad))

    bad = copy.deepcopy(pristine)
    bad["original_rows"][17]["coefficients"]["d18"] = 2
    tests.append(("damaged original coefficient", bad))

    bad = copy.deepcopy(pristine)
    bad["integer_unit_row_operations"] = bad["integer_unit_row_operations"][:-1]
    tests.append(("deleted unit operation", bad))

    bad = copy.deepcopy(pristine)
    bad["reduced_rows"][11]["coefficients"]["d11"] = 2
    tests.append(("damaged factor coefficient", bad))

    bad = copy.deepcopy(pristine)
    bad["factor_records"]["18"]["G"] = bad["factor_records"]["18"]["F"]
    tests.append(("split same-pair F/G record", bad))

    bad = copy.deepcopy(pristine)
    bad["support_source"]["sha256"] = "0" * 64
    tests.append(("damaged source binding", bad))

    results = []
    for name, bad in tests:
        rejected = False
        try:
            check_payload(bad)
        except (AssertionError, KeyError, IndexError):
            rejected = True
        assert rejected, name
        results.append({"case": name, "rejected": True})
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    data = json.loads((HERE / "CERTIFICATE.json").read_text())
    summary = check_payload(data)
    result = {"status": "PASS", "summary": summary}
    if args.negative:
        result["negative_controls"] = negative_controls(data)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
