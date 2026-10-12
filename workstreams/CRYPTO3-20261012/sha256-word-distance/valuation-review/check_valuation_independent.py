#!/usr/bin/env python3
"""Independent small certificate for the four-support v2(D)<=20 claim.

Uses only the Python standard library and per-output-bit FIPS equations.
No author proof, code, structural certificate, or SAT solver is imported.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import platform
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASK = (1 << 32) - 1
SUPPORT_SHA256 = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
COORDINATES = [(6, 19, 35, 44), (7, 21, 37, 46),
               (12, 18, 34, 43), (13, 20, 36, 45)]
OFFSETS = [0, 2, 9, 11, 15, 16, 18, 24, 27, 31, 32]
COMBINATIONS = {
    "d_y_minus_d_x": {16: 1},
    "d_r_plus_d_x": {32: -1, 16: -1},
    "F_y_minus_F_x": {15: 1, 31: -1, 24: -1},
    "G_y_minus_G_x_minus_2d_x": {18: -1, 2: 1, 11: -1, 9: 2, 0: -2},
    "G_y_minus_G_r_minus_d_x": {18: -1, 27: 1, 9: 1, 0: -1},
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sigma(word: int, rotations: tuple[int, int], shift: int) -> int:
    require(type(word) is int and 0 <= word <= MASK, "unsigned input word")
    result = 0
    for out in range(32):
        value = 0
        for distance in rotations:
            value ^= (word >> ((out + distance) % 32)) & 1
        if out + shift < 32:
            value ^= (word >> (out + shift)) & 1
        result |= value << out
    return result


def f(word: int) -> int:
    return sigma(word, (7, 18), 3)


def g(word: int) -> int:
    return sigma(word, (17, 19), 10)


def hx(word: int) -> str:
    return f"{word:08x}"


def row_list(row: dict[tuple[str, int], int]) -> list[dict]:
    return [{"kind": key[0], "index": key[1], "coefficient": coefficient}
            for key, coefficient in sorted(row.items()) if coefficient]


def recurrence(support: set[int], t: int) -> dict[tuple[str, int], int]:
    require(16 <= t < 64, "recurrence boundary")
    original = [("d", t, 1), ("G", t-2, -1), ("d", t-7, -1),
                ("F", t-15, -1), ("d", t-16, -1)]
    return {(kind, index): coefficient for kind, index, coefficient in original
            if index in support}


def bridge_records(source: bytes) -> list[dict]:
    require(hashlib.sha256(source).hexdigest() == SUPPORT_SHA256, "frozen support bytes")
    supports = json.loads(source)["supports"]
    result = []
    for index, x, y, r in COORDINATES:
        support = set(supports[index])
        require({x, y, r} <= support, "nonzero distinguished input differences")
        rows = {offset: recurrence(support, x+offset) for offset in OFFSETS}
        expected_rows = {
            0: {("d", x): 1, ("d", x-7): -1},
            2: {("d", x+2): 1, ("G", x): -1, ("d", x-5): -1},
            9: {("d", x+2): -1, ("d", x-7): -1},
            11: {("d", x+11): 1, ("d", x-5): -1},
            15: {("d", x+8): -1, ("F", x): -1},
            16: {("d", y): 1, ("d", x): -1},
            18: {("G", y): -1, ("d", x+11): -1, ("d", x+2): -1},
            24: {("d", x+24): 1, ("d", x+8): -1},
            27: {("G", r): -1, ("d", x+11): -1},
            31: {("d", x+24): -1, ("F", y): -1},
            32: {("d", r): -1, ("d", y): -1},
        }
        require(rows == expected_rows, "all original restricted recurrence rows")
        targets = {
            "d_y_minus_d_x": {("d", y): 1, ("d", x): -1},
            "d_r_plus_d_x": {("d", r): 1, ("d", x): 1},
            "F_y_minus_F_x": {("F", y): 1, ("F", x): -1},
            "G_y_minus_G_x_minus_2d_x": {("G", y): 1, ("G", x): -1, ("d", x): -2},
            "G_y_minus_G_r_minus_d_x": {("G", y): 1, ("G", r): -1, ("d", x): -1},
        }
        identities = []
        for name, factors in COMBINATIONS.items():
            total = Counter()
            for offset, factor in factors.items():
                for term, coefficient in rows[offset].items():
                    total[term] += factor * coefficient
            combined = {term: coefficient for term, coefficient in total.items() if coefficient}
            require(combined == targets[name], "integer row-combination identity")
            identities.append({"name": name, "factors": [
                {"t": x+offset, "factor": factor} for offset, factor in sorted(factors.items())],
                "result": row_list(combined)})
        result.append({"support_index": index, "support": supports[index],
                       "x": x, "y": y, "r": r,
                       "source_recurrences": [{"t": x+offset, "terms": row_list(rows[offset])}
                                              for offset in OFFSETS],
                       "integer_combinations": identities})
    return result


def first_singleton_obstruction(p: int, q: int) -> int | None:
    for i in range(32):
        single = ((p >> i) & 1) != ((q >> i) & 1)
        previous_off = i == 0 or ((p | q) >> (i-1)) & 1 == 0
        if single and previous_off:
            return i
    return None


def carry_zero_failure(p: int, q: int) -> int | None:
    possible = {0}
    for i in range(32):
        left = (-1, 1) if (p >> i) & 1 else (0,)
        right = (-1, 1) if (q >> i) & 1 else (0,)
        next_possible = set()
        for carry in possible:
            for a in left:
                for b in right:
                    value = carry + a + b
                    if value % 2 == 0:
                        next_possible.add(value // 2)
        possible = next_possible
        require(possible <= {-1, 0, 1}, "signed carry range")
        if not possible:
            return i
    return None


def rebuild(source: bytes) -> dict:
    require(g(0x80000000) == 0x00205000, "sigma1 conformance")
    require(f(0x80000000) == 0x11002000, "sigma0 conformance")
    high_columns = [{"input_bit": j, "g_image": hx(g(1 << j))}
                    for j in range(21, 32)]
    require(all(g(1 << j) < (1 << 22) for j in range(21, 32)), "high21 output below22")
    require(all(g(1 << j) < (1 << 21) for j in range(21, 31)), "non-top interval output below21")
    require(3 * (1 << 23) < (1 << 32), "ordinary-integer lift of 2D")
    signed_deltas = [multiple * (1 << 21) for multiple in range(-3, 4)
                     if multiple and abs(multiple * (1 << 21)) < (1 << 23)
                     and abs(2 * multiple * (1 << 21)) < (1 << 23)]
    require(signed_deltas == [-(1 << 21), 1 << 21], "nonzero increment normalization")

    full_interval = 0xffe00000
    n, m = f(full_interval), g(full_interval)
    require(n == 0x1e03fff8 and m == 0x003f980c, "full-interval output masks")
    intervals = []
    for last in range(21, 31):
        input_mask = (1 << (last+1)) - (1 << 21)
        output_f, output_g = f(input_mask), g(input_mask)
        first = first_singleton_obstruction(n, output_f)
        require(first is not None, "mixed interval F obstruction")
        require(carry_zero_failure(n, output_f) == first, "independent carry agreement")
        require(output_g < (1 << 21), "short interval G bound")
        intervals.append({"last": last, "input_mask": hx(input_mask),
                          "f_mask": hx(output_f), "g_mask": hx(output_g),
                          "first_obstruction_bit": first})

    f_mask, g_mask, z_mask = 0x0600ffa8, 0x0020000c, 0x4ea00000
    require(f_mask & ~n == 0 and g_mask & ~m == 0, "parity masks in forced output sets")
    require(z_mask & ~(((1 << 31)-1) ^ ((1 << 21)-1)) == 0, "parity mask in zero input bits")
    require(g_mask & (1 << 21) != 0, "odd forced parity")
    checks = []
    for bit in range(32):
        z = 1 << bit
        fp = (f(z) & f_mask).bit_count() & 1
        gp = (g(z) & g_mask).bit_count() & 1
        zp = (z & z_mask).bit_count() & 1
        require(fp ^ gp ^ zp == 0, "universal binary linear identity")
        checks.append({"input_bit": bit, "f_parity": fp, "g_parity": gp, "z_parity": zp})
    return {
        "schema": "CRYPTO3-independent-irregular-valuation-v1",
        "definition": {"word_bits": 32, "f_rotations": [7, 18], "f_shift": 3,
                       "g_rotations": [17, 19], "g_shift": 10},
        "source_support_sha256": SUPPORT_SHA256,
        "support_bridges": bridge_records(source),
        "high21_g_columns": high_columns,
        "signed_D_candidates_after_both_G_bounds": signed_deltas,
        "positive_D_after_swapping": 1 << 21,
        "mixed_interval_exclusions": intervals,
        "remaining_interval": {"input_mask": hx(full_interval), "f_mask": hx(n), "g_mask": hx(m)},
        "forced_difference_equations": {
            "z_zero_bits": list(range(21, 31)), "f_mask": hx(n), "f_target": "00000000",
            "g_mask": hx(m), "g_target": "00200000"},
        "parity_contradiction": {"f_mask": hx(f_mask), "g_mask": hx(g_mask), "z_mask": hx(z_mask),
                                 "basis_checks": checks, "forced_parities": [0, 1, 0]},
        "valuation_bound": 20,
        "scope": "Necessary valuation bound for four exact supports; no full support exclusion or new global schedule distance bound.",
    }


def verify(data: dict, source: bytes) -> None:
    require(data == rebuild(source), "certificate differs from independent reconstruction")


def negative_controls(data: dict, source: bytes) -> list[dict]:
    cases = []

    def add(name, change):
        bad = copy.deepcopy(data)
        change(bad)
        cases.append((name, bad, source))

    add("wrong_sigma0_rotation", lambda d: d["definition"]["f_rotations"].__setitem__(0, 8))
    add("wrong_sigma1_shift", lambda d: d["definition"].__setitem__("g_shift", 11))
    add("damaged_support_position", lambda d: d["support_bridges"][0]["support"].__setitem__(0, 10))
    add("omit_essential_third_pair_relation", lambda d: d["support_bridges"][0]["integer_combinations"].pop())
    add("wrong_integer_combination", lambda d: d["support_bridges"][0]["integer_combinations"][3]["factors"][0].__setitem__("factor", -1))
    add("invalid_initial_recurrence_boundary", lambda d: d["support_bridges"][0]["source_recurrences"][0].__setitem__("t", 15))
    add("allow_zero_D", lambda d: d["signed_D_candidates_after_both_G_bounds"].append(0))
    add("omit_interval_case", lambda d: d["mixed_interval_exclusions"].pop())
    add("false_carry_bit", lambda d: d["mixed_interval_exclusions"][0].__setitem__("first_obstruction_bit", 24))
    add("tampered_sigma_mask", lambda d: d["remaining_interval"].__setitem__("f_mask", "1e03fff0"))
    add("wrong_parity_coefficient", lambda d: d["parity_contradiction"].__setitem__("f_mask", "0600ffa0"))
    add("false_forced_parity", lambda d: d["parity_contradiction"].__setitem__("forced_parities", [0, 0, 0]))
    add("false_global_claim", lambda d: d.__setitem__("scope", "All four supports excluded."))
    cases.append(("corrupted_source_bytes", data, source + b" "))
    result = []
    for name, bad, bad_source in cases:
        try:
            verify(bad, bad_source)
        except ValueError as error:
            result.append({"control": name, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("negative control accepted: " + name)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=HERE.parent / "supports-v2.json")
    parser.add_argument("--certificate", type=Path, default=HERE / "independent_valuation_certificate.json")
    parser.add_argument("--emit", action="store_true")
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    source = args.source.read_bytes()
    if args.emit:
        args.certificate.write_text(json.dumps(rebuild(source), indent=2) + "\n")
    data = json.loads(args.certificate.read_text())
    verify(data, source)
    controls = negative_controls(data, source) if args.negative else []
    print(json.dumps({"status": "PASS", "python": platform.python_version(),
                      "support_indices": [r["support_index"] for r in data["support_bridges"]],
                      "original_recurrence_rows": 44, "integer_combination_identities": 20,
                      "mixed_interval_exclusions": 10, "universal_identity_basis_checks": 32,
                      "valuation_bound": 20, "negative_controls": controls,
                      "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      "certificate_sha256": hashlib.sha256(args.certificate.read_bytes()).hexdigest(),
                      "scope": data["scope"], "formalization": "not Lean-formalized"}, indent=2))


if __name__ == "__main__":
    main()
