#!/usr/bin/env python3
"""Bounded threshold-sum check for the overlap-bit closed form.

Uses direct borrow/carry threshold sums, not the root agent's dynamic program.
This is a discovering-agent self-check, with no random sampling and no new
four-input enumeration.  Also probes outside the proposed theorem domain.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import resource
import shlex
import sys
import time


def power2(exponent: int) -> Fraction:
    return Fraction(1 << exponent) if exponent >= 0 else Fraction(1, 1 << -exponent)


def coefficients(r: int, q: int) -> tuple[Fraction, Fraction, Fraction]:
    a = -power2(-r) / 3 + 4 * power2(-3 * r - 2 * q) / 3
    b = -power2(-q) / 7 - power2(-3 * r - q) / 7
    d = 2 * power2(-3 * r - q) / 7
    return a, b, d


def overlap_formula(r: int, q: int, k: int) -> Fraction:
    a, b, d = coefficients(r, q)
    return a * power2(-2 * k) + b * power2(-k) + d * power2(-4 * k)


def last_carry_sums(i: int) -> tuple[list[int], list[list[int]]]:
    """For every S, directly sum signs over Y, with every one-bit mask."""
    N = 1 << i
    base = [0] * N
    masked = [[0] * N for _ in range(i)]
    for s in range(N):
        for y in range(N):
            sign = 1 - 2 * (s + y >= N)
            base[s] += sign
            for p in range(i):
                masked[p][s] += sign * (1 - 2 * ((y >> p) & 1))
    return base, masked


def first_borrow_sums(i: int, k: int) -> tuple[list[int], list[list[int]]]:
    """For every S, directly sum signs over B, with every one-bit mask."""
    N, lowmask = 1 << i, (1 << k) - 1
    base = [0] * N
    masked = [[0] * N for _ in range(i)]
    for s in range(N):
        for b in range(N):
            high_borrow = b > s
            low_borrow = (b & lowmask) > (s & lowmask)
            sign = 1 - 2 * (high_borrow ^ low_borrow)
            base[s] += sign
            for ell in range(i):
                masked[ell][s] += sign * (1 - 2 * ((b >> ell) & 1))
    return base, masked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-i", type=int, default=8)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 2 <= args.max_i <= 8:
        parser.error("Bounded threshold run requires 2 <= max-i <= 8.")
    planned_pairs = sum(i * (1 << (2 * i)) for i in range(2, args.max_i + 1))
    print(f"Planned borrow/carry threshold pair evaluations: {planned_pairs}.", flush=True)
    start = time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    records = []
    outside = []
    moment_checks = 0
    theorem_cases = 0
    for i in range(2, args.max_i + 1):
        N = 1 << i
        g0, gp = last_carry_sums(i)
        for k in range(i - 1):
            f0, fe = first_borrow_sums(i, k)
            actual_m0 = Fraction(sum(x * y for x, y in zip(f0, g0)), N ** 3)
            K, H = 1 << k, 1 << (i - k)
            predicted_m0 = Fraction(4 - H * H, 3 * K * H * H)
            assert actual_m0 == predicted_m0
            for q in range(1, i - k):
                r = i - k - q
                j = r + k
                moment_rows = []
                actual_correlation = actual_m0
                for ell in range(j):
                    p = ell + q
                    actual_m = Fraction(sum(x * y for x, y in zip(fe[ell], gp[p])), N ** 3)
                    predicted_m = power2(ell + p - k) / (N * N)
                    if ell < k:
                        predicted_m *= 2
                    if k <= q:
                        assert actual_m == predicted_m
                        moment_checks += 1
                    actual_correlation -= (1 << ell) * actual_m
                    moment_rows.append({"ell": ell, "p": p, "actual": str(actual_m),
                                        "candidate_formula": str(predicted_m)})
                actual_correlation /= 1 << j
                predicted_correlation = overlap_formula(r, q, k)
                if k <= q:
                    assert actual_correlation == predicted_correlation
                    theorem_cases += 1
                elif actual_correlation != predicted_correlation:
                    outside.append({"i": i, "r": r, "q": q, "k": k,
                                    "actual": str(actual_correlation),
                                    "extrapolated_candidate": str(predicted_correlation)})
                records.append({"i": i, "r": r, "q": q, "k": k,
                                "inside_theorem_domain": k <= q,
                                "M0": str(actual_m0),
                                "moments": moment_rows,
                                "actual_correlation": str(actual_correlation),
                                "candidate_correlation": str(predicted_correlation)})
        print(f"PASS in-domain threshold moments at i={i}", flush=True)
    # Reuse only this discovering agent's already frozen original-input counts.
    direct_path = Path(__file__).with_name("results") / "exact_signed_max5.json"
    prior = json.loads(direct_path.read_text())
    direct_checks = []
    for case in prior["experiments"]:
        n, r, q = case["n"], case["r"], case["q"]
        for i in range(r + q, n):
            k = i - r - q
            if k <= q:
                actual = Fraction(case["uniform_correlations_all_bits"][i])
                assert actual == overlap_formula(r, q, k)
                direct_checks.append({"n": n, "r": r, "q": q, "i": i,
                                      "exact_correlation": str(actual)})
    reported = [Fraction(-47180567524833621, 1 << 70),
                Fraction(-88356335546507093, 1 << 72),
                Fraction(-170707871589853653, 1 << 74),
                Fraction(-335410943676546677, 1 << 76)]
    standard = []
    for k in range(4):
        value = overlap_formula(16, 12, k)
        assert value == reported[k]
        standard.append({"n": 32, "r": 16, "q": 12, "k": k, "i": 28 + k,
                         "exact_correlation": str(value), "decimal": float(value)})
    for r in range(1, 8):
        for q in range(3, 8):
            for k in range(q - 2):
                assert (overlap_formula(r, q, k + 3)
                        == Fraction(13, 16) * overlap_formula(r, q, k + 2)
                        - Fraction(11, 64) * overlap_formula(r, q, k + 1)
                        + Fraction(1, 128) * overlap_formula(r, q, k))
    report = {
        "status": "passed_research_self_check",
        "independent_verification": False,
        "randomness": "none",
        "started_at_utc": started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - start,
        "command": shlex.join([sys.executable] + sys.argv),
        "exit_code_on_success": 0,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "prior_original_input_result_sha256": hashlib.sha256(direct_path.read_bytes()).hexdigest(),
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "machine": platform.machine(),
                        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        "planned_and_executed_threshold_pairs": planned_pairs,
        "inside_theorem_parameter_cases": theorem_cases,
        "inside_theorem_masked_moment_checks": moment_checks,
        "reused_original_input_checks": direct_checks,
        "outside_domain_counterexamples": outside,
        "standard_parameters": standard,
        "records": records,
        "scope": "Exact threshold moments and analytical formula; not a cipher attack or novelty certificate.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Outside-domain mismatches: {len(outside)}; first: {outside[:1]}", flush=True)
    print(json.dumps(standard, indent=2), flush=True)
    print(f"Saved {args.output}; exit code 0.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
