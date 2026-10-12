#!/usr/bin/env python3
"""Definition checker for corrected support-index-12 factorisation."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 1 << 32
MASK = N - 1
ACTIVE = [10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57]
KINDS = ("d", "F", "G")
VARIABLES = [f"{kind}{i}" for i in ACTIVE for kind in KINDS]
FREE = [
    "d10", "d11", "d13", "d15", "F11", "F13", "G10",
    "G11", "G13", "F15", "G26", "F29", "F42", "F57",
]
PIVOTS = [v for v in VARIABLES if v not in FREE]
V8_MANIFEST_SHA256 = "02a3729a66b7e474eb2abfeb33920160e2d60386f324ab5d4ef1b5c1e2bc0814"


def expr(**terms):
    return {k: v for k, v in terms.items() if v}


# Right sides of (d_i,F_i,G_i) in the fourteen free coordinates.
FACTOR_RHS = {
    10: (expr(d10=1), expr(d11=-1), expr(G10=1)),
    11: (expr(d11=1), expr(F11=1), expr(G11=1)),
    13: (expr(d13=1), expr(F13=1), expr(G13=1)),
    15: (expr(d15=1), expr(F15=1), expr(d10=-1)),
    18: (expr(d11=1), expr(F11=-1, d10=-1),
         expr(d11=-1, d13=-1)),
    20: (expr(d11=-1), expr(F13=-1, G26=-1), expr(d15=-1)),
    26: (expr(F11=1, d10=1), expr(d11=-1), expr(G26=1)),
    28: (expr(F13=1, G26=1), expr(d11=-1), expr(F15=-1)),
    29: (expr(d13=1), expr(F29=1), expr(d15=-1)),
    34: (expr(d11=1), expr(F11=-1, d10=-1),
         expr(d11=1, d13=-1)),
    42: (expr(F11=1, d10=1), expr(F42=1),
         expr(F29=-1, F13=-1, G26=-1)),
    43: (expr(d11=-1), expr(F11=-1, d10=-1), expr(d13=-1)),
    57: (expr(F42=1), expr(F57=1), expr(d11=1)),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(row, name, value):
    row[name] = row.get(name, 0) + value
    if row[name] == 0:
        del row[name]


def original_rows(active=ACTIVE, lags=(2, 7, 15, 16)):
    support = set(active)
    rows = []
    for t in range(16, 64):
        coeff = {}
        if t in support:
            add(coeff, f"d{t}", 1)
        for kind, i in (("G", t - lags[0]), ("d", t - lags[1]),
                        ("F", t - lags[2]), ("d", t - lags[3])):
            if i in support:
                add(coeff, f"{kind}{i}", -1)
        rows.append({"t": t, "coefficients": coeff})
    return rows


def dense(coeff):
    return [coeff.get(v, 0) for v in VARIABLES]


def sparse(row):
    return {v: row[i] for i, v in enumerate(VARIABLES) if row[i]}


def expected_reduced():
    rows = []
    for pivot in PIVOTS:
        index = int(pivot[1:])
        rhs = FACTOR_RHS[index][KINDS.index(pivot[0])]
        coeff = {pivot: 1}
        for name, value in rhs.items():
            add(coeff, name, -value)
        rows.append({"pivot": pivot, "coefficients": coeff})
    return rows


def apply_op(matrix, op):
    if op["op"] == "swap":
        a, b = op["a"], op["b"]
        matrix[a], matrix[b] = matrix[b], matrix[a]
    elif op["op"] == "negate":
        r = op["row"]
        matrix[r] = [-x for x in matrix[r]]
    elif op["op"] == "add":
        target, source = op["target"], op["source"]
        multiplier = op["multiplier"]
        matrix[target] = [
            x + multiplier * y
            for x, y in zip(matrix[target], matrix[source])
        ]
    else:
        raise AssertionError(f"unknown operation {op!r}")


def inverse_op(op):
    answer = dict(op)
    if answer["op"] == "add":
        answer["multiplier"] = -answer["multiplier"]
    return answer


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


def check_target_bindings(data):
    assert data["support_identifier"] == 12
    assert data["support_identifier_is_zero_based"] is True
    bindings = data["target_bindings"]

    b = bindings["supports_v2"]
    source = (HERE / b["path"]).resolve()
    assert sha(source) == b["sha256"]
    source_data = json.loads(source.read_text())
    assert b["array_index"] == 12
    assert source_data["supports"][12] == ACTIVE
    assert source_data["supports"][11] != ACTIVE

    b = bindings["accepted_actual_boundary_proof"]
    boundary = (HERE / b["path"]).resolve()
    assert sha(boundary) == b["sha256"]
    compact = "".join(boundary.read_text().split())
    assert "{10,11,13,15,18,20,26,28,29,34,42,43,57}" in compact

    b = bindings["base_lift_structural"]
    structural = (HERE / b["path"]).resolve()
    assert sha(structural) == b["sha256"]
    assert json.loads(structural.read_text())["support"] == ACTIVE

    # The rejected v8 object remains immutable and is bound as a failure record.
    v8_manifest = HERE.parent / "support12-full-factor-v8" / "manifest.json"
    assert sha(v8_manifest) == V8_MANIFEST_SHA256


def check_payload(data):
    assert data["schema"] == "CRYPTO3-support12-full-factor-v9"
    assert data["modulus"] == N
    assert data["active_indices"] == ACTIVE
    check_target_bindings(data)
    assert data["variables"] == VARIABLES
    assert data["free_variables"] == FREE
    assert data["pivot_variables"] == PIVOTS

    rows = original_rows()
    assert data["original_rows"] == rows
    nonzero = [row for row in rows if row["coefficients"]]
    zeros = [row["t"] for row in rows if not row["coefficients"]]
    assert data["nonzero_row_count"] == len(nonzero) == 25
    assert data["zero_row_count"] == len(zeros) == 23
    assert [row["t"] for row in nonzero] == [
        17, 18, 20, 22, 25, 26, 27, 28, 29, 30, 31, 33, 34,
        35, 36, 41, 42, 43, 44, 45, 49, 50, 57, 58, 59,
    ]

    initial = [dense(row["coefficients"]) for row in nonzero]
    matrix = copy.deepcopy(initial)
    for op in data["integer_unit_row_operations"]:
        apply_op(matrix, op)
    reduced = expected_reduced()
    assert data["reduced_rows"] == reduced
    assert [sparse(row) for row in matrix] == [r["coefficients"] for r in reduced]
    restored = copy.deepcopy(matrix)
    for op in reversed(data["integer_unit_row_operations"]):
        apply_op(restored, inverse_op(op))
    assert restored == initial

    appearances = {v: [] for v in FREE}
    for index, triple in FACTOR_RHS.items():
        used = set().union(*(set(component) for component in triple))
        for variable in used:
            appearances[variable].append(index)
    private = {v: x for v, x in appearances.items() if len(x) == 1}
    shared = {v: x for v, x in appearances.items() if len(x) > 1}
    assert private == {"G10": [10], "G11": [11], "G13": [13], "F57": [57]}
    assert len(shared) == 10
    reached = {10}
    changed = True
    while changed:
        changed = False
        for factors in shared.values():
            if reached.intersection(factors) and not set(factors).issubset(reached):
                reached.update(factors)
                changed = True
    assert reached == set(ACTIVE)

    assert gf2_rank([sigma0(1 << i) for i in range(32)]) == 32
    assert gf2_rank([sigma1(1 << i) for i in range(32)]) == 32
    return {
        "support_identifier": 12,
        "active_indices": ACTIVE,
        "rows": 48,
        "nonzero_rows": 25,
        "zero_rows": 23,
        "integer_rank": 25,
        "free_rank": 14,
        "unit_operations": len(data["integer_unit_row_operations"]),
        "private_parameters": private,
        "shared_parameters": shared,
        "connected_pair_factors": len(reached),
        "sigma0_binary_rank": 32,
        "sigma1_binary_rank": 32,
        "v8_failure_manifest_preserved": True,
    }


def negative_controls(pristine):
    cases = []

    bad = copy.deepcopy(pristine)
    bad["target_bindings"]["supports_v2"]["array_index"] = 11
    cases.append(("repeat v8 off-by-one binding", bad))

    bad = copy.deepcopy(pristine)
    bad["active_indices"][2] = 27
    cases.append(("replace active 13 by 27", bad))

    bad = copy.deepcopy(pristine)
    bad["original_rows"][4]["coefficients"].pop("d13")
    cases.append(("delete true row-20 d13 term", bad))

    bad = copy.deepcopy(pristine)
    bad["integer_unit_row_operations"] = bad["integer_unit_row_operations"][:-1]
    cases.append(("delete unit operation", bad))

    bad = copy.deepcopy(pristine)
    bad["reduced_rows"][4]["coefficients"]["d13"] = 0
    cases.append(("damage G18 factor", bad))

    bad = copy.deepcopy(pristine)
    bad["target_bindings"]["base_lift_structural"]["sha256"] = "0" * 64
    cases.append(("damage independent target binding", bad))

    results = []
    for name, bad in cases:
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
    result = {"status": "PASS", "summary": check_payload(data)}
    if args.negative:
        result["negative_controls"] = negative_controls(data)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
