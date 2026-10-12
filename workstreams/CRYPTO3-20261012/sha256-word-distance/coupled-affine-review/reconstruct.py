#!/usr/bin/env python3
"""Independent reconstruction of the fixed-K affine carry proof.

No discoverer code, solver, DRUP file or RUP file is imported or read.
"""
from __future__ import annotations

import hashlib
import itertools
import json

WORD = (1 << 32) - 1
K = 0xfbca7000


def rotate(x, r):
    return ((x >> r) | (x << (32 - r))) & WORD


def f(x):
    return rotate(x, 7) ^ rotate(x, 18) ^ (x >> 3)


def g(x):
    return rotate(x, 17) ^ rotate(x, 19) ^ (x >> 10)


def sigma_rows(rotations, shift, offset):
    return [((1 << ((i + rotations[0]) % 32)) ^
             (1 << ((i + rotations[1]) % 32)) ^
             ((1 << (i + shift)) if i + shift < 32 else 0)) << offset
            for i in range(32)]


def mask_ok(a, b):
    return not ((a ^ b) & ~((a | b) << 1) & WORD)


def truth_table():
    checked = 0
    for a, b in itertools.product(range(2), repeat=2):
        for current in (-1, 0, 1):
            if current % 2 != (a ^ b):
                continue
            s = (1 - current) // 2 if a ^ b else 0
            for u, v, next_parity, next_s in itertools.product(range(2), repeat=4):
                nxt = 1 - 2 * next_s if next_parity else 0
                numeric = 2 * nxt == current + a * (1 - 2 * u) + b * (1 - 2 * v)
                if a == b == 0:
                    affine = next_parity == 0
                else:
                    left, right = (u, v) if a == b == 1 else (s, u if a else v)
                    affine = ((left ^ right) == 1 if next_parity == 0 else
                              left == right and next_s == left)
                assert numeric == affine
                checked += 1
    return checked


def all_candidate_masks():
    candidates = []
    for upper in range(1 << 19):
        a = (upper << 13) | (1 << 12)
        if mask_ok(a, K) and mask_ok(f(a), f(K)):
            candidates.append(a)
    return candidates


def build_system(A):
    q = [1 << i for i in range(32)]
    p = [1 << (32 + i) for i in range(32)]
    fq = sigma_rows((7, 18), 3, 0)
    fp = sigma_rows((7, 18), 3, 32)
    gq = sigma_rows((17, 19), 10, 0)
    equations = [
        ("q_plus_gq", K, g(K), q, gq, 0, 0),
        ("p_minus_q", A, K, p, q, 0, 1),
        ("fp_plus_fq", f(A), f(K), fp, fq, 0, 0),
    ]
    variable_names = ["q" + str(i) for i in range(32)] + ["p" + str(i) for i in range(32)]
    rows = []

    def add(forms, rhs, origin):
        coefficient = 0
        for word, constant in forms:
            coefficient ^= word
            rhs ^= constant
        rows.append({"coefficient": coefficient, "rhs": rhs, "origin": origin})

    for name, mask_a, mask_b, urows, vrows, uconstant, vconstant in equations:
        e = mask_a ^ mask_b
        signs = {}
        for bit in range(1, 32):
            if e >> bit & 1:
                signs[bit] = (1 << len(variable_names), 0)
                variable_names.append(name + ":carry" + str(bit))
        if e & 1:
            add([], 1, name + ":initial_parity")
        for bit in range(31):
            a, b = (mask_a >> bit) & 1, (mask_b >> bit) & 1
            enext = (e >> (bit + 1)) & 1
            if a == b == 0:
                if enext:
                    add([], 1, name + ":bit" + str(bit) + ":00_to_odd")
                continue
            if a == b == 1:
                left, right = (urows[bit], uconstant), (vrows[bit], vconstant)
            else:
                assert bit in signs, "candidate masks have valid initial parity"
                left = signs[bit]
                right = (urows[bit], uconstant) if a else (vrows[bit], vconstant)
            if not enext:
                add([left, right], 1, name + ":bit" + str(bit) + ":next_even")
            else:
                add([left, right], 0, name + ":bit" + str(bit) + ":next_odd_equal")
                add([signs[bit + 1], left], 0, name + ":bit" + str(bit) + ":next_odd_sign")
    return variable_names, rows


def matrix_hash(rows):
    data = [[hex(r["coefficient"]), r["rhs"], r["origin"]] for r in rows]
    return hashlib.sha256(json.dumps(data, separators=(",", ":")).encode()).hexdigest()


def contradiction(rows):
    pivots = {}
    for number, row in enumerate(rows):
        value, rhs, combination = row["coefficient"], row["rhs"], 1 << number
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value, rhs, combination
                break
            other, parity, used = pivots[pivot]
            value ^= other
            rhs ^= parity
            combination ^= used
        else:
            if rhs:
                result = [i for i in range(len(rows)) if combination >> i & 1]
                total = parity = 0
                for i in result:
                    total ^= rows[i]["coefficient"]
                    parity ^= rows[i]["rhs"]
                assert total == 0 and parity == 1
                return result
    return None


def main():
    table_count = truth_table()
    assert mask_ok(K, g(K))
    candidates = all_candidate_masks()
    cases = []
    for a in candidates:
        names, rows = build_system(a)
        conflict = contradiction(rows)
        cases.append({"A": a, "variable_count": len(names), "row_count": len(rows),
                      "matrix_sha256": matrix_hash(rows), "xor_contradiction_rows": conflict,
                      "status": "contradiction" if conflict is not None else "not_excluded"})
    print(json.dumps({
        "schema": "crypto3-independent-fixed-K-affine-carry-reconstruction-v1",
        "K": K, "fK": f(K), "gK": g(K),
        "carry_truth_table_cases": table_count,
        "necessary_mask_universe": 1 << 19,
        "candidate_count": len(candidates),
        "cases": cases,
        "not_excluded": [r["A"] for r in cases if r["status"] != "contradiction"],
        "scope": "fixed K, coupled local four-word condition only",
        "discoverer_files_read": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
