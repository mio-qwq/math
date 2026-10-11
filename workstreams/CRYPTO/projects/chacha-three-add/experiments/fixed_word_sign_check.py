#!/usr/bin/env python3
"""Bounded exact cross-check of the fixed-word sign corollary.

Discovery/self-check only; imports the discovering implementation.
No random sampling and no larger original-input brute force.
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

from exact_signed import fixed_a_special, square_prefix_0, triangle_shifted_prefix


def triangle_area(t: int, ell: int) -> int:
    assert t >= 0
    h = 1 << ell
    k, z = divmod(t, 2 * h)
    tail = (z * (z + 1) // 2 if z <= h
            else h * h - (2 * h - z) * (2 * h - z - 1) // 2)
    return k * h * h + tail


def nonpositive_triangle_product(a: int, ell: int, p: int) -> int:
    assert a >= 0 and p > ell
    h, P = 1 << ell, 1 << p
    t = (a - 1) % (2 * P)
    if t <= P:
        return -triangle_area(t, ell)
    return triangle_area(t - P, ell) - h * P // 2


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-i", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not 2 <= args.max_i <= 12:
        parser.error("Bounded run requires 2 <= max-i <= 12.")
    planned_cases = sum((i - 1) * (1 << i) for i in range(2, args.max_i + 1))
    print(f"Planned fixed-word formula cases: {planned_cases}; no input brute force or sampling.", flush=True)
    started = datetime.now(timezone.utc).isoformat()
    start = time.monotonic()
    area_cases = 0
    for ell in range(7):
        for t in range(140):
            assert triangle_area(t, ell) == sum(square_prefix_0(z, ell) for z in range(1, t + 1))
            area_cases += 1
    term_cases = 0
    records = []
    for i in range(2, args.max_i + 1):
        N = 1 << i
        for r in range(1, i):
            q = i - r
            positive_count = 0
            negative_count = 0
            minimum = Fraction(1)
            minimum_a = []
            c0 = Fraction(1, 1 << (2 * r + q))
            for a in range(N):
                terms = []
                for ell in range(r):
                    p = ell + q
                    term = nonpositive_triangle_product(a, ell, p)
                    assert term == triangle_shifted_prefix(a, ell, p)
                    assert -(1 << (ell + p - 1)) <= term <= 0
                    terms.append(term)
                    term_cases += 1
                numerator = N * (1 - 2 * a) + 2 * a * (a - 1)
                numerator += 4 * sum((1 << ell) * term for ell, term in enumerate(terms))
                value = Fraction(numerator, (1 << r) * N * N)
                assert value == fixed_a_special(a, r, q)
                if a == 0:
                    assert value == c0
                elif a == 1:
                    assert value == -c0
                else:
                    assert value < -c0
                positive_count += value > 0
                negative_count += value < 0
                if value < minimum:
                    minimum, minimum_a = value, [a]
                elif value == minimum:
                    minimum_a.append(a)
            assert positive_count == 1 and negative_count == N - 1
            records.append({"i": i, "r": r, "q": q, "a_cases": N,
                            "positive_count": positive_count, "negative_count": negative_count,
                            "minimum_on_this_finite_domain": str(minimum),
                            "minimum_a": minimum_a})
        print(f"PASS all r+q={i}, all A in [0,{N})", flush=True)
    report = {
        "status": "passed_research_self_check",
        "independent_verification": False,
        "randomness": "none; deterministic bounded formula-domain scan",
        "started_at_utc": started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - start,
        "command": shlex.join([sys.executable] + sys.argv),
        "exit_code_on_success": 0,
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "machine": platform.machine(),
                        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        "source_sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                          for name in ("fixed_word_sign_check.py", "exact_signed.py")},
        "planned_and_executed_formula_cases": planned_cases,
        "triangle_area_direct_cases": area_cases,
        "triangle_product_comparison_cases": term_cases,
        "records": records,
        "scope": "Analytical formula self-check; no finite scan is treated as a general proof or an attack.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Saved {args.output}; exit code 0.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
