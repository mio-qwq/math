#!/usr/bin/env python3
"""Independent exact classifier for the valuation-16 selected twin condition.

This file deliberately imports no code or data from the author package.
It uses only the Python standard library and reconstructs the SHA-256 small
sigma rows from their definitions.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import platform
import sys
import time


MASK32 = (1 << 32) - 1
VARIABLES = 64
COEFFICIENT_MASK = (1 << VARIABLES) - 1
ODD_Q = tuple(range(1, 32, 2))
HERE = Path(__file__).resolve().parent


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def rotate_right(value: int, amount: int) -> int:
    return ((value >> amount) | (value << (32 - amount))) & MASK32


def sigma_direct(value: int, which: int) -> int:
    if which == 0:
        return rotate_right(value, 7) ^ rotate_right(value, 18) ^ (value >> 3)
    return rotate_right(value, 17) ^ rotate_right(value, 19) ^ (value >> 10)


def build_rows(which: int) -> tuple[int, ...]:
    """Build output-bit linear forms by independent basis evaluation."""
    columns = [sigma_direct(1 << bit, which) for bit in range(32)]
    return tuple(
        sum(((columns[input_bit] >> output_bit) & 1) << input_bit
            for input_bit in range(32))
        for output_bit in range(32)
    )


ROWS = (build_rows(0), build_rows(1))


def sigma_rows(value: int, which: int) -> int:
    return sum(((row & value).bit_count() & 1) << bit
               for bit, row in enumerate(ROWS[which]))


for _which in (0, 1):
    for _probe in (0, 1, 2, 3, 0x12345678, 0x80000000, MASK32):
        require(sigma_rows(_probe, _which) == sigma_direct(_probe, _which),
                "row construction disagrees with direct sigma")


@dataclass(frozen=True)
class InputClass:
    xor_mask: int
    equations: tuple[tuple[int, int], ...]
    members: tuple[int, ...]


def input_classes(q: int) -> tuple[InputClass, ...]:
    """Partition the upper half by u xor (u+q), verifying every affine cube."""
    require(q in ODD_Q, "q outside frozen odd interval")
    groups: dict[int, list[int]] = {}
    assignment = []
    for upper in range(1 << 16):
        alpha16 = upper ^ ((upper + q) & 0xFFFF)
        assignment.append(alpha16)
        groups.setdefault(alpha16, []).append(upper)

    classes = []
    seen: set[int] = set()
    for alpha16, members_list in sorted(groups.items()):
        members = tuple(members_list)
        equations = []
        for bit in range(16):
            values = {(upper >> bit) & 1 for upper in members}
            if len(values) == 1:
                equations.append((1 << (bit + 16), next(iter(values))))
        # Exhaustively regenerate the axis-aligned affine cube, instead of
        # relying only on its expected cardinality.
        regenerated = tuple(
            upper for upper in range(1 << 16)
            if all(((upper >> bit) & 1) == rhs
                   for coeff, rhs in equations
                   for bit in ((coeff.bit_length() - 1) - 16,))
        )
        require(regenerated == members, f"non-cube input class q={q} alpha={alpha16:04x}")
        require(not (seen & set(members)), "input classes overlap")
        seen.update(members)
        classes.append(InputClass(alpha16 << 16, tuple(equations), members))

    require(seen == set(range(1 << 16)), "input classes do not cover upper words")
    require(all(assignment[upper] ==
                (upper ^ ((upper + q) & 0xFFFF)) for upper in range(1 << 16)),
            "input assignment recomputation failed")
    return tuple(classes)


def affine_hull_equations(allowed: tuple[int, ...], arity: int) -> tuple[tuple[int, int], ...]:
    """Return all constant parities and exhaustively verify exact recovery."""
    equations = []
    for form in range(1, 1 << arity):
        outputs = {(form & value).bit_count() & 1 for value in allowed}
        if len(outputs) == 1:
            equations.append((form, next(iter(outputs))))
    reconstructed = tuple(
        value for value in range(1 << arity)
        if all(((form & value).bit_count() & 1) == rhs
               for form, rhs in equations)
    )
    require(reconstructed == allowed, "non-affine carry truth table")
    return tuple(equations)


Basis = dict[int, tuple[int, frozenset[int]]]


def insert_equations(basis: Basis,
                     equations: tuple[tuple[int, int], ...],
                     stats: Counter) -> Basis | None:
    """Highest-pivot GF(2) insertion with checked algebraic contradictions."""
    out = dict(basis)
    for coefficient, rhs in equations:
        packed = coefficient | (rhs << VARIABLES)
        receipt = frozenset((packed,))
        while packed & COEFFICIENT_MASK:
            pivot = (packed & COEFFICIENT_MASK).bit_length() - 1
            if pivot not in out:
                out[pivot] = (packed, receipt)
                break
            old_packed, old_receipt = out[pivot]
            packed ^= old_packed
            receipt = receipt.symmetric_difference(old_receipt)
        if packed == (1 << VARIABLES):
            total = 0
            for row in receipt:
                total ^= row
            require(total == (1 << VARIABLES), "invalid contradiction receipt")
            stats["checked_contradictions"] += 1
            return None
        require(packed == 0 or (packed & COEFFICIENT_MASK),
                "malformed reduced equation")
    return out


def transition(which: int, alpha_x: int, alpha_y: int, bit: int,
               incoming_carry: int, target: int) -> tuple[tuple[int, tuple[tuple[int, int], ...]], ...]:
    toggle_x = (sigma_rows(alpha_x, which) >> bit) & 1
    toggle_y = (sigma_rows(alpha_y, which) >> bit) & 1
    forms = []
    if toggle_x:
        forms.append(ROWS[which][bit])
    if toggle_y:
        forms.append(ROWS[which][bit] << 32)

    by_next: dict[int, list[int]] = {}
    for assignment in range(1 << len(forms)):
        cursor = 0
        old_x = 0
        old_y = 0
        if toggle_x:
            old_x = (assignment >> cursor) & 1
            cursor += 1
        if toggle_y:
            old_y = (assignment >> cursor) & 1
        digit = (incoming_carry
                 + ((old_y ^ toggle_y) - old_y)
                 - ((old_x ^ toggle_x) - old_x)
                 - ((target >> bit) & 1))
        if digit % 2 == 0:
            by_next.setdefault(digit // 2, []).append(assignment)

    result = []
    for next_carry, allowed_list in sorted(by_next.items()):
        allowed = tuple(allowed_list)
        little_equations = affine_hull_equations(allowed, len(forms))
        equations = []
        for little_form, rhs in little_equations:
            expanded = 0
            for index, form in enumerate(forms):
                if (little_form >> index) & 1:
                    expanded ^= form
            equations.append((expanded, rhs))
        result.append((next_carry, tuple(equations)))
    return tuple(result)


def impose_bits(start: tuple[Basis, ...], which: int, alpha_x: int, alpha_y: int,
                target: int, bit_count: int, stats: Counter) -> tuple[Basis, ...]:
    states: list[tuple[int, Basis]] = [(0, basis) for basis in start]
    for bit in range(bit_count):
        following = []
        for carry, basis in states:
            for next_carry, equations in transition(
                    which, alpha_x, alpha_y, bit, carry, target):
                stats["carry_edges"] += 1
                inserted = insert_equations(basis, equations, stats)
                if inserted is not None:
                    following.append((next_carry, inserted))
        states = following
    return tuple(basis for _, basis in states)


def representative(basis: Basis) -> int:
    """Set free variables to zero and solve highest-pivot rows bottom-up."""
    word = 0
    for pivot in sorted(basis):
        packed, _ = basis[pivot]
        coefficient = packed & COEFFICIENT_MASK
        rhs = packed >> VARIABLES
        if ((coefficient & word).bit_count() & 1) != rhs:
            word |= 1 << pivot
        require(((coefficient & word).bit_count() & 1) == rhs,
                "representative violates basis row")
    return word


def actual_record(q: int, packed: int, modulus_bits: int) -> dict[str, int]:
    d = q << 16
    x = packed & MASK32
    y = (packed >> 32) & MASK32
    xp = (x + d) & MASK32
    yp = (y + d) & MASK32
    fx = (sigma_direct(xp, 0) - sigma_direct(x, 0)) & MASK32
    fy = (sigma_direct(yp, 0) - sigma_direct(y, 0)) & MASK32
    gx = (sigma_direct(xp, 1) - sigma_direct(x, 1)) & MASK32
    gy = (sigma_direct(yp, 1) - sigma_direct(y, 1)) & MASK32
    modulus = 1 << modulus_bits
    require(fx == fy, "recovered words violate full sigma0 equality")
    require((gy - gx - 2 * d) % modulus == 0,
            "recovered words violate sigma1 gap")
    return {"x": x, "x_plus_D": xp, "y": y, "y_plus_D": yp,
            "F": fx, "G_x": gx, "G_y": gy,
            "gap": (gy - gx) & MASK32}


def classify(q: int, g_bits: int) -> dict:
    d = q << 16
    classes = input_classes(q)
    stats: Counter = Counter()
    f_leaves = 0
    g_leaves = 0
    records = []
    for class_x in classes:
        for class_y in classes:
            y_equations = tuple((coefficient << 32, rhs)
                                for coefficient, rhs in class_y.equations)
            initial = insert_equations(
                {}, class_x.equations + y_equations, stats)
            require(initial is not None, "independent input cubes conflict")
            after_f = impose_bits((initial,), 0, class_x.xor_mask,
                                  class_y.xor_mask, 0, 32, stats)
            f_leaves += len(after_f)
            after_g = impose_bits(after_f, 1, class_x.xor_mask,
                                  class_y.xor_mask, 2 * d, g_bits, stats)
            g_leaves += len(after_g)
            for basis in after_g:
                record = actual_record(q, representative(basis), g_bits)
                record["xor_x"] = class_x.xor_mask
                record["xor_y"] = class_y.xor_mask
                records.append(record)
    require(len(records) == g_leaves, "survivor reconstruction count mismatch")
    histogram = Counter(len(item.members) for item in classes)
    return {
        "q": q,
        "D": d,
        "input_class_count": len(classes),
        "input_class_size_histogram": {str(k): v for k, v in sorted(histogram.items())},
        "mask_pair_count": len(classes) ** 2,
        "sigma0_leaves": f_leaves,
        "sigma1_bits": g_bits,
        "twin_leaves": g_leaves,
        "representatives": records,
        "stats": dict(stats),
    }


def validate_full_record(q: int, record: dict[str, int]) -> None:
    d = q << 16
    x = record["x"]
    xp = record["x_plus_D"]
    y = record["y"]
    yp = record["y_plus_D"]
    require((xp - x) & MASK32 == d and (yp - y) & MASK32 == d,
            "recorded input difference is wrong")
    fx = (sigma_direct(xp, 0) - sigma_direct(x, 0)) & MASK32
    fy = (sigma_direct(yp, 0) - sigma_direct(y, 0)) & MASK32
    gx = (sigma_direct(xp, 1) - sigma_direct(x, 1)) & MASK32
    gy = (sigma_direct(yp, 1) - sigma_direct(y, 1)) & MASK32
    require(fx == fy == record["F"], "recorded sigma0 values are wrong")
    require(gx == record["G_x"] and gy == record["G_y"],
            "recorded sigma1 values are wrong")
    require((gy - gx) & MASK32 == record["gap"] == ((2 * d) & MASK32),
            "recorded full sigma1 gap is wrong")


def reversal_control(q: int, record: dict[str, int]) -> None:
    d = q << 16
    negative_d = (-d) & MASK32
    x, xp = record["x_plus_D"], record["x"]
    y, yp = record["y_plus_D"], record["y"]
    require((xp - x) & MASK32 == negative_d and
            (yp - y) & MASK32 == negative_d,
            "reversed pair has wrong negative difference")
    fx = (sigma_direct(xp, 0) - sigma_direct(x, 0)) & MASK32
    fy = (sigma_direct(yp, 0) - sigma_direct(y, 0)) & MASK32
    gx = (sigma_direct(xp, 1) - sigma_direct(x, 1)) & MASK32
    gy = (sigma_direct(yp, 1) - sigma_direct(y, 1)) & MASK32
    require(fx == fy == ((-record["F"]) & MASK32),
            "reversal does not negate common sigma0 derivative")
    require((gy - gx) & MASK32 == ((2 * negative_d) & MASK32),
            "reversal does not produce negative-orientation gap")


def negative_controls(full_results: list[dict]) -> dict:
    rejected = 0
    attempted = 0
    for result in full_results:
        q = result["q"]
        for record in result["representatives"]:
            validate_full_record(q, record)
            reversal_control(q, record)
            for field in ("x_plus_D", "y_plus_D", "F", "G_x", "G_y", "gap"):
                attempted += 1
                damaged = dict(record)
                damaged[field] ^= 1
                try:
                    validate_full_record(q, damaged)
                except RuntimeError:
                    rejected += 1
    require(rejected == attempted, "damaged witness was not rejected")
    return {"damaged_witnesses_attempted": attempted,
            "damaged_witnesses_rejected": rejected,
            "all_full_witnesses_reversed_and_checked": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "PRE_AUTHOR_RUN.json")
    args = parser.parse_args()
    start = time.monotonic()
    full = []
    low31 = []
    for q in ODD_Q:
        full_result = classify(q, 32)
        full.append(full_result)
        # A separate low-31 run is a sharp-boundary guard for exclusions.
        low_result = classify(q, 31)
        low31.append({
            "q": q,
            "sigma0_leaves": low_result["sigma0_leaves"],
            "low31_twin_leaves": low_result["twin_leaves"],
            "representatives": low_result["representatives"],
        })
        if full_result["twin_leaves"] == 0 and low_result["twin_leaves"]:
            require(all(record["gap"] != ((2 * (q << 16)) & MASK32)
                        for record in low_result["representatives"]),
                    "low-31 survivor accidentally satisfies full theorem")

    controls = negative_controls(full)
    payload = {
        "schema": "CRYPTO3-support12-v16-independent-pre-author-v9",
        "status": "PASS",
        "question": "selected twin core for D=q*2^16, odd q in 1..31",
        "full32": full,
        "low31_control": low31,
        "controls": controls,
        "negative_orientation": "checked by actual reversal for every full survivor; excluded positive q transfers bijectively",
        "scope": "local selected twin only; not the third pair, reciprocal edge, support, message pair, or distance-14 proof",
        "python": sys.version,
        "platform": platform.platform(),
        "elapsed_seconds": time.monotonic() - start,
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "elapsed_seconds": payload["elapsed_seconds"],
        "classification": [
            [row["q"], row["input_class_count"], row["sigma0_leaves"], row["twin_leaves"]]
            for row in full
        ],
        "low31": [[row["q"], row["low31_twin_leaves"]] for row in low31],
        "controls": controls,
        "output": str(args.output),
    }, indent=2))


if __name__ == "__main__":
    main()
