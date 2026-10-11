#!/usr/bin/env python3
"""Research implementation for exact three-add ChaCha correlations.

This is discovery/self-check code, not independent verification.
No random samples are used.  The direct experiment enumerates all four inputs.
The closed formulas are derived in ../proofs/*.md.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import resource
import shlex
import sys
import time


def rol(x: int, r: int, n: int) -> int:
    r %= n
    return ((x << r) | (x >> ((n - r) % n))) & ((1 << n) - 1)


def actual_and_linear(a: int, b: int, c: int, d: int,
                      n: int, r: int, q: int) -> tuple[int, int]:
    """Direct original-input implementation; no carry transform is used."""
    modulus_mask = (1 << n) - 1
    s = (a + b) & modulus_mask
    t = rol(d ^ s, r, n)
    u = (c + t) & modulus_mask
    v = rol(b ^ u, q, n)
    w = (s + v) & modulus_mask
    linear = a ^ b ^ rol(b ^ c, q, n) ^ rol(a ^ b ^ d, r + q, n)
    return w, linear


def uniform_special(r: int, q: int) -> Fraction:
    assert r >= 1 and q >= 1
    return (-Fraction(1, 3 * (1 << r))
            - Fraction(1, 7 * (1 << q))
            + Fraction(4, 3 * (1 << (3 * r + 2 * q)))
            + Fraction(1, 7 * (1 << (3 * r + q))))


def square_prefix_0(t: int, ell: int) -> int:
    """F0(t+1)-F0(t)=(-1)^bit_ell(t), including negative t."""
    h = 1 << ell
    residue = t % (2 * h)
    return residue if residue <= h else 2 * h - residue


def square_prefix_1(t: int, ell: int) -> int:
    """F1(t+1)-F1(t)=t*(-1)^bit_ell(t), including negative t."""
    h = 1 << ell
    period = 2 * h
    quotient, residue = divmod(t, period)
    tail = (residue * (residue - 1) // 2 if residue <= h
            else h * (h - 1) - residue * (residue - 1) // 2)
    return (-quotient * h * h
            + quotient * period * square_prefix_0(residue, ell) + tail)


def triangle_shifted_prefix(a: int, ell: int, p: int) -> int:
    """Sum_{x=0}^{a-1} (-1)^bit_ell(x-a) H_p(x), exactly.

    Since p > ell, complete periods have zero contribution.
    Runs in a constant number of arithmetic operations on O(n)-bit integers.
    """
    assert p > ell
    half_period = 1 << p
    period = 2 * half_period
    t = a % period

    def q0(end: int) -> int:
        return square_prefix_0(end - a, ell) - square_prefix_0(-a, ell)

    def q1(end: int) -> int:
        return (square_prefix_1(end - a, ell) - square_prefix_1(-a, ell)
                + a * q0(end))

    if t <= half_period:
        return q1(t)
    return (2 * q1(half_period) - q1(t)
            + period * (q0(t) - q0(half_period)))


def fixed_a_special(a: int, r: int, q: int) -> Fraction:
    """Exact correlation for fixed first word, at bit r+q < n."""
    assert r >= 1 and q >= 1
    i = r + q
    N = 1 << i
    A = a % N
    numerator = N * (1 - 2 * A) + 2 * A * (A - 1)
    numerator += 4 * sum((1 << ell) * triangle_shifted_prefix(A, ell, ell + q)
                         for ell in range(r))
    return Fraction(numerator, (1 << r) * N * N)


def positive_range(n: int, r: int, q: int, i: int) -> Fraction:
    assert r >= q >= 1 and r + q < n and 0 <= i < r + q
    distance = n - r - q
    k = (i - q) % n
    return Fraction(1, 1 << (distance + i + k))


def direct_all(n: int, r: int, q: int) -> dict:
    """Enumerate 2^(4n) inputs and retain all output-bit/fixed-a sums."""
    limit = 1 << n
    all_counts = [0] * n
    fixed_counts = []
    fixed_denominator = 1 << (3 * n)
    special_bit = r + q
    for a in range(limit):
        counts = [0] * n
        for b in range(limit):
            for c in range(limit):
                for d in range(limit):
                    actual, linear = actual_and_linear(a, b, c, d, n, r, q)
                    error = actual ^ linear
                    for i in range(n):
                        counts[i] += 1 - 2 * ((error >> i) & 1)
        fixed_counts.append(counts[special_bit])
        assert Fraction(counts[special_bit], fixed_denominator) == fixed_a_special(a, r, q)
        for i in range(n):
            all_counts[i] += counts[i]
    denominator = 1 << (4 * n)
    assert Fraction(all_counts[special_bit], denominator) == uniform_special(r, q)
    assert sum((fixed_a_special(a, r, q) for a in range(limit)), Fraction()) / limit == uniform_special(r, q)
    assert fixed_a_special(0, r, q) == Fraction(1, 1 << (3 * r + 2 * q)) * (1 << (r + q))
    positive_checks = []
    if r >= q:
        for i in range(r + q):
            expected = positive_range(n, r, q, i)
            assert Fraction(all_counts[i], denominator) == expected
            positive_checks.append(i)
    naive = Fraction(1, 1 << (3 * r + 2 * q))
    assert uniform_special(r, q) < 0 < naive
    return {
        "n": n, "r": r, "q": q, "special_bit": special_bit,
        "input_tuples": denominator,
        "uniform_signed_numerators_all_bits": all_counts,
        "uniform_denominator": denominator,
        "uniform_correlations_all_bits": [str(Fraction(c, denominator)) for c in all_counts],
        "fixed_a_special_signed_numerators": fixed_counts,
        "fixed_a_denominator": fixed_denominator,
        "formula_uniform_special": str(uniform_special(r, q)),
        "naive_independent_carries_prediction": str(naive),
        "positive_range_checked_bits": positive_checks,
        "status": "passed_research_self_check",
    }


def check_prefix_arithmetic() -> dict:
    cases = 0
    for ell in range(6):
        for t in range(-70, 71):
            sign = 1 - 2 * ((t >> ell) & 1)
            assert square_prefix_0(t + 1, ell) - square_prefix_0(t, ell) == sign
            assert square_prefix_1(t + 1, ell) - square_prefix_1(t, ell) == t * sign
            cases += 1
        for p in range(ell + 1, 7):
            for a in range(140):
                direct = sum((1 - 2 * (((x - a) >> ell) & 1))
                             * square_prefix_0(x, p) for x in range(a))
                assert direct == triangle_shifted_prefix(a, ell, p)
                cases += 1
    return {"cases": cases, "status": "passed_research_self_check"}


def fraction_record(value: Fraction) -> dict:
    return {"numerator": value.numerator, "denominator": value.denominator,
            "fraction": str(value), "decimal_approximation": float(value),
            "negative_log2_absolute": -math.log2(abs(float(value))) if value else None}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=5)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 3 <= args.max_n <= 5:
        parser.error("This bounded reproducibility run supports max-n from 3 through 5.")
    start = time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    prefix = check_prefix_arithmetic()
    experiments = []
    estimated_tuples = sum((1 << (4 * n)) * ((n - 1) * (n - 2) // 2)
                           for n in range(3, args.max_n + 1))
    print(f"Planned exact input tuples: {estimated_tuples}; no random sampling.", flush=True)
    for n in range(3, args.max_n + 1):
        for r in range(1, n):
            for q in range(1, n - r):
                record = direct_all(n, r, q)
                experiments.append(record)
                print(f"PASS n={n} r={r} q={q} special={record['formula_uniform_special']}", flush=True)
    constants = [0x61707865, 0x3320646E, 0x79622D32, 0x6B206574]
    standard = {
        "n": 32, "r": 16, "q": 12, "special_bit": 28,
        "uniform_inputs": fraction_record(uniform_special(16, 12)),
        "fixed_first_word": {f"0x{a:08x}": fraction_record(fixed_a_special(a, 16, 12))
                             for a in [0] + constants},
        "method": "theorem and integer prefix formula; no 32-bit exhaustive experiment",
        "model_limit": "three-add local function; b,c,d uniform; no feed-forward or cipher attack",
    }
    report = {
        "status": "passed_research_self_check",
        "independent_verification": False,
        "started_at_utc": started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - start,
        "command": shlex.join([sys.executable] + sys.argv),
        "exit_code_on_success": 0,
        "randomness": "none; complete deterministic enumeration",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "machine": platform.machine(),
                        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        "planned_and_executed_input_tuples": estimated_tuples,
        "prefix_self_checks": prefix,
        "experiments": experiments,
        "standard_parameters": standard,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(standard, indent=2), flush=True)
    print(f"Saved {args.output}; exit code 0.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
