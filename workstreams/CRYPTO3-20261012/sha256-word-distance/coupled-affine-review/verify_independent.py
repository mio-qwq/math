#!/usr/bin/env python3
"""Check the frozen independent reconstruction and deliberate failures.

This validator uses the reviewer's frozen matrix reconstruction, never
the discoverer's implementation. It also checks the general table
against direct modular arithmetic on every width-three instance.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

import reconstruct as independent

HERE = Path(__file__).resolve().parent


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def original_sigma(x, a, b, s):
    return sum((((x >> ((i + a) % 32)) & 1) ^ ((x >> ((i + b) % 32)) & 1)
                ^ (((x >> (i + s)) & 1) if i + s < 32 else 0)) << i
               for i in range(32))


def table_holds(a, b, x, y, width):
    parity = a ^ b
    if parity & 1:
        return False
    odd = [i for i in range(1, width) if parity >> i & 1]
    for choice in range(1 << len(odd)):
        signs = {i: (choice >> j) & 1 for j, i in enumerate(odd)}
        valid = True
        for i in range(width - 1):
            ai, bi = (a >> i) & 1, (b >> i) & 1
            enext = (parity >> (i + 1)) & 1
            if ai == bi == 0:
                valid &= enext == 0
                continue
            if ai == bi == 1:
                left, right = (x >> i) & 1, (y >> i) & 1
            else:
                left = signs[i]
                right = ((x if ai else y) >> i) & 1
            if enext:
                valid &= left == right and signs[i + 1] == left
            else:
                valid &= left != right
        if valid:
            return True
    return False


def check_numeric_table():
    count = 0
    width = 3
    modulus = 1 << width
    for a, b, x, y in itertools.product(range(modulus), repeat=4):
        direct = ((x ^ a) - x + (y ^ b) - y) % modulus == 0
        require(table_holds(a, b, x, y, width) == direct, "global affine-table mismatch")
        count += 1
    H = 1 << 31
    fixtures = [
        {"a": H, "b": H, "x": 0, "y": 0, "integer_sum": 1 << 32, "final_carry": 1},
        {"a": H, "b": H, "x": H, "y": H, "integer_sum": -(1 << 32), "final_carry": -1},
    ]
    for item in fixtures:
        a, b, x, y = (item[k] for k in ("a", "b", "x", "y"))
        total = (x ^ a) - x + (y ^ b) - y
        require(total == item["integer_sum"] and total % (1 << 32) == 0, "wrap fixture arithmetic")
        require(table_holds(a, b, x, y, 32), "wrongly fixed final carry")
    return count, fixtures


def check_dependency(rows, indices):
    require(type(indices) is list and len(indices) == len(set(indices)), "invalid row selection")
    coefficient = rhs = 0
    for j in indices:
        require(type(j) is int and 0 <= j < len(rows), "row selection range")
        coefficient ^= rows[j]["coefficient"]
        rhs ^= rows[j]["rhs"]
    require(coefficient == 0 and rhs == 1, "row selection does not prove 0=1")


def check_certificate(certificate):
    require(certificate["K"] == 0xfbca7000, "wrong K")
    require(certificate["fK"] == original_sigma(certificate["K"], 7, 18, 3), "wrong fK")
    require(certificate["gK"] == original_sigma(certificate["K"], 17, 19, 10), "wrong gK")
    masks = independent.all_candidate_masks()
    require(len(masks) == certificate["candidate_count"] == 132, "candidate count")
    require(certificate["necessary_mask_universe"] == 1 << 19, "mask-universe size")
    require([case["A"] for case in certificate["cases"]] == masks, "incomplete necessary mask cover")
    sizes = []
    for case in certificate["cases"]:
        names, rows = independent.build_system(case["A"])
        require(case["variable_count"] == len(names), "variable count mismatch")
        require(case["row_count"] == len(rows), "row count mismatch")
        require(case["matrix_sha256"] == independent.matrix_hash(rows), "wrong reconstructed matrix")
        require(case["status"] == "contradiction", "case not excluded")
        check_dependency(rows, case["xor_contradiction_rows"])
        sizes.append(len(case["xor_contradiction_rows"]))
    require(certificate["not_excluded"] == [], "nonempty uncovered list")
    return {"candidate_masks": len(masks), "contradictions": len(masks),
            "maximum_original_rows_in_one_conflict": max(sizes),
            "minimum_original_rows_in_one_conflict": min(sizes)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    checkpoint = json.loads((HERE / "PRE-AUTHOR-CHECKPOINT.json").read_text())
    for name, expected in checkpoint["files"].items():
        require(hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected,
                "pre-author checkpoint changed: " + name)
    require(checkpoint["author_short_proof_files_read"] is False, "incorrect reconstruction sequence")
    for word in [0, 0xffffffff, independent.K, *[1 << j for j in range(32)]]:
        require(independent.f(word) == original_sigma(word, 7, 18, 3), "sigma0 original bits")
        require(independent.g(word) == original_sigma(word, 17, 19, 10), "sigma1 original bits")
    encoded_columns = 0
    for rotations, shift in (((7, 18), 3), ((17, 19), 10)):
        for offset in (0, 32):
            matrix = independent.sigma_rows(rotations, shift, offset)
            for j in range(32):
                column = sum(((r >> (offset + j)) & 1) << i for i, r in enumerate(matrix))
                require(column == original_sigma(1 << j, *rotations, shift), "sigma row-source mismatch")
                encoded_columns += 1
    certificate = json.loads((HERE / "INDEPENDENT-CERTIFICATE.json").read_text())
    report = check_certificate(certificate)
    table_cases, fixtures = check_numeric_table()
    report.update(local_truth_table_cases=independent.truth_table(),
                  width_three_all_input_table_cases=table_cases,
                  final_carry_fixtures=fixtures, original_sigma_matrix_columns=encoded_columns,
                  negative_controls=[])
    if args.negative:
        def rejected(name, action):
            try:
                action()
            except (ValueError, KeyError, IndexError):
                report["negative_controls"].append({"name": name, "rejected": True})
            else:
                raise ValueError("negative control was accepted: " + name)

        bad = copy.deepcopy(certificate)
        bad["cases"].pop()
        rejected("omitted_necessary_A", lambda: check_certificate(bad))
        bad = copy.deepcopy(certificate)
        bad["K"] ^= 1
        rejected("changed_fixed_K", lambda: check_certificate(bad))
        bad = copy.deepcopy(certificate)
        bad["cases"][0]["xor_contradiction_rows"].pop()
        rejected("removed_conflict_row", lambda: check_certificate(bad))
        bad = copy.deepcopy(certificate)
        bad["cases"][0]["xor_contradiction_rows"].append(bad["cases"][0]["xor_contradiction_rows"][0])
        rejected("duplicated_conflict_row", lambda: check_certificate(bad))
        bad = copy.deepcopy(certificate)
        bad["cases"][0]["matrix_sha256"] = "0" * 64
        rejected("tampered_matrix_hash", lambda: check_certificate(bad))
        case = certificate["cases"][0]
        _, damaged = independent.build_system(case["A"])
        damaged[case["xor_contradiction_rows"][0]]["rhs"] ^= 1
        rejected("flipped_affine_rhs", lambda: check_dependency(damaged, case["xor_contradiction_rows"]))
        rejected("wrong_sigma1_rotation", lambda: require(
            original_sigma(independent.K, 18, 19, 10) == certificate["gK"], "wrong g constant"))
        rejected("incorrect_zero_final_carry", lambda: require(
            fixtures[0]["integer_sum"] == 0, "valid modular sum has nonzero final carry"))
    report.update(status="pass", author_short_proof_used=False,
                  sat_smt_or_RUP_used=False,
                  scope="fixed-K local four-word exclusion only; no actual-distance claim")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
