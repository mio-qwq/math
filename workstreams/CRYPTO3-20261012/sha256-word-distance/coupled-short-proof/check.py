#!/usr/bin/env python3
"""Verify the small fixed-K proof using only bit equations and row XORs.

This checker is separately written by the proof author, not an independent
agent review. It imports no discovery program, matrix solver, SAT solver,
CNF, RUP proof, or affine-fibre data. No Gaussian elimination is performed.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORD = (1 << 32) - 1
COEFFICIENTS = (1 << 64) - 1
CONSTANT = 1 << 64
K = 0xfbca7000


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sigma_input_row(kind, output_bit):
    first, second, shift = ((7, 18, 3), (17, 19, 10))[kind]
    result = (1 << ((output_bit+first) % 32)) ^ (1 << ((output_bit+second) % 32))
    if output_bit+shift < 32:
        result ^= 1 << (output_bit+shift)
    return result


SIGMA_ROWS = [[sigma_input_row(kind, bit) for bit in range(32)] for kind in (0, 1)]


def sigma(word, kind):
    require(type(word) is int and 0 <= word <= WORD, "unsigned sigma input")
    return sum(((word & row).bit_count() % 2) << bit for bit, row in enumerate(SIGMA_ROWS[kind]))


def valid_signed_masks(a, b):
    singles = a ^ b
    while singles:
        lowest = singles & -singles
        bit = lowest.bit_length()-1
        if bit == 0 or not ((a | b) >> (bit-1)) & 1:
            return False
        singles ^= lowest
    return True


def exhaustive_masks():
    surviving = []
    first_count = 0
    for choice in range(1 << 17):
        # Free coordinates 13..17 and 20..31, with 12 and 19 fixed to one.
        a = ((choice & 31) << 13) | ((choice >> 5) << 20) | (1 << 12) | (1 << 19)
        if not valid_signed_masks(a, K):
            continue
        first_count += 1
        if valid_signed_masks(sigma(a, 0), sigma(K, 0)):
            surviving.append(a)
    require(first_count == 24576 and len(surviving) == 132, "complete necessary-mask classification")
    require(surviving == sorted(set(surviving)), "unique sorted exhaustive masks")
    return first_count, surviving


def local_truth_table():
    records = []
    for active in (0, 1, 2):
        for sign in ((0, 1) if active == 1 else (0,)):
            for u in ((0, 1) if active else (0,)):
                for v in ((0, 1) if active == 2 else (0,)):
                    incoming = 1-2*sign if active == 1 else 0
                    total = incoming
                    if active:
                        total += 1-2*u
                    if active == 2:
                        total += 1-2*v
                    require(total % 2 == 0, "current mask fixes even bit sum")
                    outgoing = total // 2
                    require(-1 <= outgoing <= 1, "signed carry bound including final bit")
                    for next_parity in (0, 1):
                        accepted = outgoing % 2 == next_parity
                        if active == 0:
                            affine_accepted = not next_parity
                        elif active == 1:
                            affine_accepted = sign ^ u == 1 ^ next_parity
                        else:
                            affine_accepted = u ^ v == 1 ^ next_parity
                        require(accepted == affine_accepted, "complete affine carry transition equivalence")
                        if accepted and next_parity:
                            require(outgoing == 1-2*u, "exact next carry sign substitution")
                        records.append({"active": active, "incoming_sign": sign,
                                        "u": u, "v": v, "next_parity": next_parity,
                                        "outgoing": outgoing, "accepted": accepted})
    require(len(records) == 18, "complete tiny transition table")
    return records


def identity_forms(offset, complement=False):
    return [(1 << (offset+i)) ^ (CONSTANT if complement else 0) for i in range(32)]


def sigma_forms(kind, offset):
    return [row << offset for row in SIGMA_ROWS[kind]]


def affine_carry_rows(a, b, left, right):
    """Equations are encoded as 64 coefficient bits plus an RHS bit at 64."""
    if (a ^ b) & 1:
        return {CONSTANT}  # The specified initial carry is zero.
    equations = set()
    carry_sign_at = {}
    for bit in range(31):
        active = ((a >> bit) & 1) + ((b >> bit) & 1)
        next_parity = ((a ^ b) >> (bit+1)) & 1
        if active == 0:
            if next_parity:
                return {CONSTANT}
            continue
        current = left[bit] if (a >> bit) & 1 else right[bit]
        if active == 2:
            lhs = left[bit] ^ right[bit]
        else:
            require(bit in carry_sign_at, "known nonzero carry sign")
            lhs = carry_sign_at[bit] ^ current
        equation = lhs ^ ((1 ^ next_parity) * CONSTANT)
        if equation:
            equations.add(equation)
        if next_parity:
            carry_sign_at[bit+1] = current
    # Bit31 only requires the already-fixed current parity. The final
    # carry may be -1, 0, or +1 and supplies no further equation.
    return equations


def coupled_rows(a):
    q = identity_forms(32)
    return (affine_carry_rows(K, sigma(K, 1), q, sigma_forms(1, 32))
            | affine_carry_rows(a, K, identity_forms(0), identity_forms(32, True))
            | affine_carry_rows(sigma(a, 0), sigma(K, 0), sigma_forms(0, 0), sigma_forms(0, 32)))


def boundary_checks():
    require(sigma(1 << 31, 0) == 0x11002000, "sigma0 standard high-bit image")
    require(sigma(1 << 31, 1) == 0x00205000, "sigma1 standard high-bit image")
    positive = affine_carry_rows(1, 1, identity_forms(0), identity_forms(32))
    negative = affine_carry_rows(1, 1, identity_forms(0), identity_forms(32, True))
    row = (1 << 0) | (1 << 32)
    require(positive == {row | CONSTANT}, "positive derivative sum parity")
    require(negative == {row}, "negative second derivative sign")
    require(affine_carry_rows(1 << 31, 1 << 31, identity_forms(0), identity_forms(32)) == set(),
            "unrestricted modular final carry")
    require(((1 << 31)+(1 << 31)) % (1 << 32) == 0, "actual nonzero-final-carry example")


def verify(cert, first_count, masks, truth_table):
    require(cert["schema"] == "CRYPTO3-fixed-K-coupled-affine-certificate-v1", "schema")
    require(cert["definition"] == {"word_bits": 32, "f_rotations": [7, 18], "f_shift": 3,
            "g_rotations": [17, 19], "g_shift": 10, "K": "fbca7000", "f_K": "828ee412",
            "g_K": "763e9000"}, "exact fixed-mask FIPS object")
    require(sigma(K, 0) == 0x828ee412 and sigma(K, 1) == 0x763e9000, "direct sigma mask images")
    require(cert["equations"] == ["q+g(q)=q_prime+g(q_prime)", "p_prime+q=p+q_prime",
            "f(p_prime)+f(q_prime)=f(p)+f(q)"], "exact three equations")
    require(cert["mask_reconstruction"] == {"q_prime": "q xor K", "p_prime": "p xor A"}, "word-pair masks")
    require(cert["signed_derivative_coefficients"] == {"h_q": [1, 1], "equal_input_derivatives": [1, -1],
            "opposite_sigma0_derivatives": [1, 1]}, "three derivative polarities")
    require(cert["final_carry"] == "unrestricted modulo 2^32", "modular final carry scope")
    exhaustion = cert["necessary_mask_exhaustivity"]
    require(exhaustion["fixed_one_bits"] == [12, 19]
            and exhaustion["fixed_zero_bits"] == list(range(12)) + [18]
            and exhaustion["free_bits"] == list(range(13, 18)) + list(range(20, 32)), "all 17 free mask bits")
    require(exhaustion["assignments"] == 1 << 17 and exhaustion["after_input_obstruction"] == first_count
            and exhaustion["after_both_obstructions"] == len(masks), "exhaustivity counts")
    raw = "".join(f"{a:08x}\n" for a in masks).encode()
    require(exhaustion["survivor_mask_sha256"] == hashlib.sha256(raw).hexdigest(), "exhaustive mask-set digest")
    require(cert["carry_table_cases"] == truth_table, "complete checked affine carry table")
    bank = []
    for index, item in enumerate(cert["row_bank"]):
        coefficient = int(item["coefficient"], 16)
        require(item["id"] == index and 0 <= coefficient <= COEFFICIENTS
                and item["coefficient"] == f"{coefficient:016x}" and item["rhs"] in (0, 1), "canonical binary row")
        require(item["p_bits"] == [j for j in range(32) if coefficient >> j & 1]
                and item["q_bits"] == [j for j in range(32) if coefficient >> (32+j) & 1], "readable row coordinates")
        bank.append(coefficient | (item["rhs"] << 64))
    require(len(bank) == len(set(bank)), "no duplicate bank rows")
    seen = []
    membership_checks = 0
    for index, family in enumerate(cert["families"]):
        require(family["id"] == index and family["mask_count"] == len(family["masks"]), "canonical proof family")
        chosen = family["row_ids"]
        require(chosen and len(chosen) == len(set(chosen))
                and all(type(i) is int and 0 <= i < len(bank) for i in chosen), "valid XOR row selection")
        total = 0
        for row_id in chosen:
            total ^= bank[row_id]
        require(total == CONSTANT, "direct XOR contradiction 0=1")
        for label in family["masks"]:
            a = int(label, 16)
            require(label == f"{a:08x}" and a in masks, "classified mask membership")
            actual_rows = coupled_rows(a)
            require(all(bank[row_id] in actual_rows for row_id in chosen), "selected equations follow from actual carry systems")
            membership_checks += len(chosen)
            seen.append(a)
    require(sorted(seen) == masks, "all and only the 132 masks covered exactly once")
    require(cert["scope"] == "No solution of the stated three local equations for fixed K; not a complete message-schedule exclusion by itself.", "local theorem scope")
    return {"masks_checked": len(masks), "families": len(cert["families"]), "distinct_rows": len(bank),
            "template_rows_xored": sum(len(f["row_ids"]) for f in cert["families"]),
            "row_membership_checks": membership_checks}


def negative_controls(cert, first_count, masks, truth_table):
    tests = []

    def add(name, change):
        bad = copy.deepcopy(cert)
        change(bad)
        tests.append((name, bad))

    add("wrong_K", lambda c: c["definition"].__setitem__("K", "fbca7001"))
    add("wrong_sigma0_rotation", lambda c: c["definition"]["f_rotations"].__setitem__(0, 8))
    add("wrong_sigma1_shift", lambda c: c["definition"].__setitem__("g_shift", 11))
    add("wrong_input_derivative_sign", lambda c: c["signed_derivative_coefficients"]["equal_input_derivatives"].__setitem__(1, 1))
    add("incorrect_final_carry_zero", lambda c: c.__setitem__("final_carry", "zero"))
    add("omit_free_mask_bit", lambda c: c["necessary_mask_exhaustivity"]["free_bits"].pop())
    add("omit_mask_case", lambda c: c["families"][0]["masks"].pop())
    add("duplicate_mask_case", lambda c: c["families"][0]["masks"].append(c["families"][0]["masks"][0]))
    add("tampered_row_coefficient", lambda c: c["row_bank"][0].__setitem__("coefficient", "0000000000018001"))
    add("tampered_row_rhs", lambda c: c["row_bank"][0].__setitem__("rhs", 1-c["row_bank"][0]["rhs"]))
    add("omit_XOR_premise", lambda c: c["families"][0]["row_ids"].pop())
    add("unclassified_zero_mask", lambda c: c["families"][0]["masks"].__setitem__(0, "00000000"))
    add("damaged_carry_table", lambda c: c["carry_table_cases"][0].__setitem__("accepted", False))
    add("false_full_schedule_scope", lambda c: c.__setitem__("scope", "Entire schedule support excluded."))
    rejected = []
    for name, bad in tests:
        try:
            verify(bad, first_count, masks, truth_table)
        except ValueError as error:
            rejected.append({"control": name, "reason": str(error)})
        else:
            raise ValueError("negative control accepted: " + name)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "CERTIFICATE.json")
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text())
    boundary_checks()
    table = local_truth_table()
    first_count, masks = exhaustive_masks()
    result = verify(cert, first_count, masks, table)
    result.update({"status": "PASS", "python": platform.python_version(), "mask_assignments_examined": 1 << 17,
                   "initial_carry": 0, "final_carry": "unrestricted", "local_transition_cases": len(table),
                   "gaussian_elimination": False, "solver_dependency": False,
                   "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   "certificate_sha256": hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
                   "review_status": "same-author checker; independent-agent review separate",
                   "scope": cert["scope"]})
    if args.negative:
        result["rejected_controls"] = negative_controls(cert, first_count, masks, table)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
