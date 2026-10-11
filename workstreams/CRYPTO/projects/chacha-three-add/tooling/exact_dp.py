#!/usr/bin/env python3
"""Exact signed correlations for the specified three-addition word program.

This implementation uses the four-state reduction in GENERAL_REDUCTION.md.
It does not approximate dependent carries as independent.  Python 3.10+;
standard library only.  A finite-state method is not a novelty certificate.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys
import time


CONSTANTS = (0x61707865, 0x3320646E, 0x79622D32, 0x6B206574)


def validate(n: int, r: int, q: int, i: int, fixed_a: int | None) -> None:
    if n < 1 or not (0 <= r < n and 0 <= q < n and 0 <= i < n):
        raise ValueError("require n>=1 and r,q,i in [0,n)")
    if fixed_a is not None and not 0 <= fixed_a < (1 << n):
        raise ValueError("fixed_a must be an n-bit unsigned integer")


def moment_count(
    n: int,
    i: int,
    k: int,
    insertion: tuple[int, int] | None = None,
    fixed_a: int | None = None,
) -> int:
    """Unnormalized signed sum over all S,B,Y (or S,Y when a is fixed).

    State index = 2*borrow + carry.  Boundary phases use the state BEFORE
    processing bit p.  All final states are accepted (arithmetic is modular).
    The same boundary can occur twice; its borrow phases cancel by XOR.
    """
    counts = [1, 0, 0, 0]
    h, ell = insertion if insertion is not None else (-1, -1)
    for p in range(n):
        next_counts = [0, 0, 0, 0]
        a_bit = ((fixed_a >> p) & 1) if fixed_a is not None else None
        for state, count in enumerate(counts):
            if not count:
                continue
            borrow, carry = divmod(state, 2)
            boundary = (borrow if p == i else 0) ^ (borrow if p == k else 0)
            boundary ^= carry if p == i else 0
            for s in (0, 1):
                if fixed_a is None:
                    choices = ((b, int(s < b + borrow)) for b in (0, 1))
                else:
                    b = (s - a_bit - borrow) & 1
                    choices = ((b, int(s < a_bit + borrow)),)
                for b, next_borrow in choices:
                    for y in (0, 1):
                        next_carry = (s + y + carry) >> 1
                        phase = boundary ^ (b if p == h else 0)
                        phase ^= y if p == ell else 0
                        next_counts[2 * next_borrow + next_carry] += (
                            -count if phase else count
                        )
        counts = next_counts
    return sum(counts)


def correlation_details(
    n: int, r: int, q: int, i: int, fixed_a: int | None = None
) -> dict:
    validate(n, r, q, i, fixed_a)
    j = (i - q) % n
    k = (i - r - q) % n
    unmasked = moment_count(n, i, k, fixed_a=fixed_a)
    numerator = unmasked
    terms = []
    for ell in range(i):
        h = (ell - q) % n
        if h < j:
            count = moment_count(n, i, k, (h, ell), fixed_a)
            numerator -= count << h
            terms.append({"b_bit": h, "y_bit": ell, "signed_count": str(count)})
    moment_denominator = 1 << ((3 if fixed_a is None else 2) * n)
    value = Fraction(numerator, moment_denominator << j)
    return {
        "n": n,
        "r": r,
        "q": q,
        "output_bit": i,
        "middle_carry_bit": j,
        "rotated_first_carry_bit": k,
        "fixed_a": None if fixed_a is None else hex(fixed_a),
        "correlation": str(value),
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "correlation_float": float(value),
        "unmasked_moment_count": str(unmasked),
        "moment_denominator": str(moment_denominator),
        "masked_moments": terms,
        "automata_evaluated": 1 + len(terms),
    }


def correlation(
    n: int, r: int, q: int, i: int, fixed_a: int | None = None
) -> Fraction:
    return Fraction(correlation_details(n, r, q, i, fixed_a)["correlation"])


def special_formula(r: int, q: int) -> Fraction:
    """Independent closed expression; only valid at i=r+q<n, r,q>=1."""
    return (
        -Fraction(1, 3 << r)
        - Fraction(1, 7 << q)
        + Fraction(4, 3 << (3 * r + 2 * q))
        + Fraction(1, 7 << (3 * r + q))
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_checks(project: Path) -> dict:
    # These exact original-word counts were produced independently, before
    # this DP implementation.  They include zero rotations and wraparound.
    counts_path = project / "verification/independent_word_counts.jsonl"
    discovery_path = project / "experiments/results/exact_signed_max5.json"
    count_checks = 0
    parameter_checks = 0
    for line in counts_path.read_text().splitlines():
        row = json.loads(line)
        if row["kind"] != "exhaustive":
            continue
        n, r, q = (row[key] for key in ("n", "r", "q"))
        for i, count in enumerate(row["signed_sums"]):
            expected = Fraction(count, row["samples"])
            got = correlation(n, r, q, i)
            assert got == expected, (n, r, q, i, got, expected)
            count_checks += 1
        parameter_checks += 1

    # The discovering agent's conditional original-word counts use yet
    # another implementation.  All first words, not just a=0, are checked.
    discovery = json.loads(discovery_path.read_text())
    fixed_checks = 0
    for row in discovery["experiments"]:
        for a, count in enumerate(row["fixed_a_special_signed_numerators"]):
            expected = Fraction(count, row["fixed_a_denominator"])
            got = correlation(row["n"], row["r"], row["q"], row["special_bit"], a)
            assert got == expected, (row["n"], row["r"], row["q"], a, got, expected)
            fixed_checks += 1

    # Boundary n=1, r=q=i=0: modulo-2 addition is XOR identically.
    assert correlation(1, 0, 0, 0) == 1
    assert correlation(1, 0, 0, 0, 0) == 1
    assert correlation(1, 0, 0, 0, 1) == 1
    for args in [(0, 0, 0, 0, None), (3, 3, 0, 0, None),
                 (3, 0, -1, 0, None), (3, 0, 0, 3, None),
                 (3, 0, 0, 0, 8), (3, 0, 0, 0, -1)]:
        try:
            correlation(*args)
        except ValueError:
            pass
        else:
            raise AssertionError(("invalid arguments accepted", args))

    # General-width closed-form checks are algebraic cross-checks, not
    # exhaustive original-input evidence at those widths.
    closed_checks = 0
    for n, r, q in [(7, 2, 3), (9, 5, 2), (16, 7, 5),
                    (32, 16, 12), (64, 31, 17)]:
        assert correlation(n, r, q, r + q) == special_formula(r, q)
        assert correlation(n, r, q, r + q, 0) == Fraction(1, 1 << (2*r + q))
        closed_checks += 2
        if r >= q:
            for i in range(r+q):
                exponent = n-r-q+i+((i-q) % n)
                assert correlation(n, r, q, i) == Fraction(1, 1 << exponent)
                closed_checks += 1

    # Deliberate independent-carry substitution has the wrong sign.
    true_value = correlation(32, 16, 12, 28)
    false_value = Fraction(1, 1 << 72)
    assert true_value < 0 < false_value
    return {
        "status": "passed",
        "independent_original_word_parameter_sets": parameter_checks,
        "independent_original_word_bit_comparisons": count_checks,
        "discovery_fixed_a_original_word_comparisons": fixed_checks,
        "additional_closed_expression_comparisons": closed_checks,
        "one_bit_boundary_checks": 3,
        "invalid_parameter_checks": 6,
        "negative_control": {"actual": str(true_value), "false_independence": str(false_value)},
        "inputs": [
            {"path": str(path.relative_to(project)), "sha256": sha256(path)}
            for path in (counts_path, discovery_path)
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--standard-table", action="store_true")
    parser.add_argument("--n", type=int, default=32)
    parser.add_argument("--r", type=int, default=16)
    parser.add_argument("--q", type=int, default=12)
    parser.add_argument("--bit", type=int, default=28)
    parser.add_argument("--fixed-a", type=lambda s: int(s, 0))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    start = datetime.now(timezone.utc)
    clock = time.perf_counter()
    project = Path(__file__).resolve().parent.parent
    result = {
        "status": "completed",
        "started_at_utc": start.isoformat(),
        "argv": [sys.executable, *sys.argv],
        "python": sys.version,
        "platform": platform.platform(),
        "source_sha256": sha256(Path(__file__)),
        "randomness": "none; exact integer dynamic programming",
        "model": "three additions only; four uniform inputs or fixed a and uniform b,c,d",
    }
    if args.check:
        result["checks"] = run_checks(project)
    if args.standard_table:
        result["standard_table"] = [
            {
                "fixed_a": None if a is None else hex(a),
                "rows": [correlation_details(32, 16, 12, i, a) for i in range(32)],
            }
            for a in (None, 0, *CONSTANTS)
        ]
    if not args.standard_table:
        result["result"] = correlation_details(args.n, args.r, args.q, args.bit, args.fixed_a)
    result["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    result["elapsed_seconds"] = time.perf_counter() - clock
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps({"status": result["status"], "output": str(args.output),
                          "elapsed_seconds": result["elapsed_seconds"],
                          "checks": result.get("checks")}))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
