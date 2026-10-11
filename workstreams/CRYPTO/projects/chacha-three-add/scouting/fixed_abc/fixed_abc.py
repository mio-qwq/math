#!/usr/bin/env python3
"""L0 fixed-abc input-distribution scout, with only d uniform.

No third-party library, no new large enumeration, no imported project code.
The bounded checks fix 17 parameter tuples and enumerate at most 16 d values.
"""

from __future__ import annotations

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


def rol(x, amount, n):
    amount %= n
    return ((x << amount) | (x >> ((n - amount) % n))) & ((1 << n) - 1)


def original(a, b, c, d, n, r, q):
    mask = (1 << n) - 1
    s = (a + b) & mask
    t = rol(d ^ s, r, n)
    u = (c + t) & mask
    y = rol(b ^ u, q, n)
    w = (s + y) & mask
    linear = a ^ b ^ rol(b ^ c, q, n) ^ rol(a ^ b ^ d, r + q, n)
    return w, linear, s, u, y


def fixed_sign(a, b, s, n, r, q, i):
    first_carry = a ^ b ^ s
    k = (i - r - q) % n
    return 1 - 2 * (((first_carry >> i) ^ (first_carry >> k)) & 1)


def fixed_abc_correlation(a, b, c, n, r, q, i):
    assert n >= 1 and 0 <= r < n and 0 <= q < n and 0 <= i < n
    assert all(0 <= word < (1 << n) for word in (a, b, c))
    s = (a + b) & ((1 << n) - 1)
    j = (i - q) % n
    sigma = fixed_sign(a, b, s, n, r, q, i)
    if i >= q:
        prefix_bits, steps = q, j
        source_start, sum_start = 0, q
        denominator = 1 << q
        initial_carry = s & (denominator - 1)
        counts = [denominator - initial_carry, initial_carry, 0, 0]
        regime = "i_ge_q"
    else:
        prefix_bits, steps = n - q, i
        source_start, sum_start = n - q, 0
        denominator = 1 << prefix_bits
        initial_borrow = c & (denominator - 1)
        counts = [denominator - initial_borrow, 0, initial_borrow, 0]
        regime = "i_lt_q"
    max_integer_bits = max(denominator.bit_length(), *(value.bit_length() for value in counts))
    for t in range(steps):
        p, out_p = source_start + t, sum_start + t
        c_bit, b_bit, s_bit = (c >> p) & 1, (b >> p) & 1, (s >> out_p) & 1
        updated = [0] * 4
        for state, count in enumerate(counts):
            beta, gamma = state >> 1, state & 1
            for u in range(2):
                beta_next = int(c_bit + beta > u)
                gamma_next = (s_bit + (u ^ b_bit) + gamma) // 2
                updated[2 * beta_next + gamma_next] += count
        counts = updated
        denominator *= 2
        assert sum(counts) == denominator
        max_integer_bits = max(max_integer_bits, denominator.bit_length(),
                               *(value.bit_length() for value in counts))
    assert denominator == 1 << (i if i >= q else j)
    numerator = sigma * (counts[0] - counts[1] - counts[2] + counts[3])
    value = Fraction(numerator, denominator)
    assert -1 <= value <= 1
    assert max_integer_bits <= n
    return value, {"regime": regime, "prefix_bits": prefix_bits,
                   "shared_bit_steps": steps, "initial_phase": sigma,
                   "terminal_counts": counts, "unreduced_denominator": denominator,
                   "max_integer_bits": max_integer_bits}


CASES = [
    (1, 0, 0, 0, 0, 0), (1, 0, 0, 1, 1, 1),
    (2, 0, 0, 1, 2, 1), (2, 1, 1, 3, 1, 2),
    (3, 1, 2, 5, 2, 3), (3, 2, 1, 6, 3, 5),
    (3, 0, 1, 0, 0, 0), (3, 1, 0, 7, 1, 4),
    (4, 0, 0, 3, 5, 11), (4, 1, 1, 10, 7, 8),
    (4, 1, 3, 9, 6, 13), (4, 3, 1, 15, 1, 7),
    (4, 2, 2, 1, 7, 15), (4, 3, 3, 12, 3, 9),
    (4, 2, 0, 0, 0, 4), (4, 0, 3, 7, 9, 0),
    (4, 1, 0, 0, 0, 7),
]


def main():
    output = Path(__file__).with_name("results.json")
    start = time.monotonic()
    started = datetime.now(timezone.utc).isoformat()
    planned_d = sum(1 << case[0] for case in CASES)
    planned_coefficients = sum(case[0] for case in CASES)
    assert len(CASES) == 17 and planned_d == 188 and planned_coefficients == 54
    print(f"Planned 17 fixed tuples, {planned_d} exact d inputs, {planned_coefficients} bit correlations; n<=4.", flush=True)
    records = []
    identity_checks = 0
    product_failures = []
    missing_phase_failures = []
    for n, r, q, a, b, c in CASES:
        signed = [0] * n
        for d in range(1 << n):
            w, linear, s, u, y = original(a, b, c, d, n, r, q)
            for i in range(n):
                original_sign = 1 - 2 * (((w ^ linear) >> i) & 1)
                j = (i - q) % n
                sigma = fixed_sign(a, b, s, n, r, q, i)
                borrow = (u & ((1 << j) - 1)) < (c & ((1 << j) - 1))
                carry = (s & ((1 << i) - 1)) + (y & ((1 << i) - 1)) >= (1 << i)
                assert original_sign == sigma * (1 - 2 * (borrow ^ carry))
                identity_checks += 1
                signed[i] += original_sign
        for i in range(n):
            exact = Fraction(signed[i], 1 << n)
            predicted, diagnostics = fixed_abc_correlation(a, b, c, n, r, q, i)
            assert predicted == exact
            s = (a + b) & ((1 << n) - 1)
            j = (i - q) % n
            sigma = fixed_sign(a, b, s, n, r, q, i)
            carry_marginal = 1 - Fraction(2 * (s & ((1 << i) - 1)), 1 << i)
            borrow_marginal = 1 - Fraction(2 * (c & ((1 << j) - 1)), 1 << j)
            incorrect_product = sigma * carry_marginal * borrow_marginal
            parameters = {"n": n, "r": r, "q": q, "a": a, "b": b, "c": c, "i": i}
            if incorrect_product != exact:
                product_failures.append(parameters | {"actual": str(exact), "false_product": str(incorrect_product)})
            if sigma * exact != exact:
                missing_phase_failures.append(parameters | {"actual": str(exact), "without_phase": str(sigma * exact)})
            if c == 0:
                assert exact == sigma * carry_marginal
            if s == 0:
                assert exact == sigma * borrow_marginal
            records.append(parameters | {"exact_correlation": str(exact),
                                         "signed_sum_over_d": signed[i],
                                         "d_count": 1 << n, "diagnostics": diagnostics})
    assert identity_checks == 692
    assert any(row["n"] == 4 and row["r"] == 0 and row["q"] == 3
               and row["a"] == 7 and row["b"] == 9 and row["c"] == 0 and row["i"] == 0
               and row["actual"] == "-1" and row["without_phase"] == "1"
               for row in missing_phase_failures)
    assert any(row["n"] == 2 and row["r"] == 0 and row["q"] == 0
               and row["a"] == 1 and row["b"] == 2 and row["c"] == 1 and row["i"] == 1
               and row["actual"] == "-1" and row["false_product"] == "0"
               for row in product_failures)
    print("PASS 692 pointwise carry identities and all 54 exact bit correlations; both planned negative controls fail as expected.", flush=True)
    examples = [
        ("rfc_a_zero_bc", 0x61707865, 0, 0),
        ("rfc_a_pattern_bc", 0x61707865, 0x01234567, 0x89ABCDEF),
        ("rfc_a_second_pattern_bc", 0x61707865, 0xDEADBEEF, 0x10203040),
        ("zero_s_zero_c", 0, 0, 0),
        ("zero_s_half_c", 0, 0, 0x00008000),
        ("zero_s_max_c", 0, 0, 0x0000FFFF),
    ]
    standard = []
    for label, a, b, c in examples:
        value, diagnostics = fixed_abc_correlation(a, b, c, 32, 16, 12, 28)
        if a == b == 0:
            assert value == 1 - Fraction(c & 0xFFFF, 1 << 15)
        if b == c == 0:
            assert value == 1 - Fraction(a & ((1 << 28) - 1), 1 << 27)
        standard.append({"label": label, "a_hex": f"{a:08x}", "b_hex": f"{b:08x}",
                         "c_hex": f"{c:08x}", "n": 32, "r": 16, "q": 12, "i": 28,
                         "exact_correlation": str(value), "decimal": float(value),
                         "diagnostics": diagnostics})
    report = {
        "status": "passed_research_self_check",
        "classification": "L0 input-distribution clarification using ordinary four-state constant-operation kernels",
        "independent_verification": False,
        "randomness": "none; fixed literal cases and complete enumeration of d only for n<=4",
        "started_at_utc": started,
        "finished_at_utc": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": time.monotonic() - start,
        "command": shlex.join([sys.executable] + sys.argv),
        "exit_code_on_success": 0,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {"python": sys.version, "platform": platform.platform(),
                        "machine": platform.machine(),
                        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},
        "fixed_parameter_cases": len(CASES),
        "enumerated_d_inputs": planned_d,
        "pointwise_identity_checks": identity_checks,
        "exact_correlation_checks": planned_coefficients,
        "incorrect_product_counterexamples": product_failures,
        "omitted_phase_counterexamples": missing_phase_failures,
        "records": records,
        "standard32_analytical_examples": standard,
        "standard_scope": "Six exact small-state evaluations; no enumeration or statistical estimate at n=32.",
    }
    output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(standard, indent=2), flush=True)
    print(f"Saved {output}; exit code 0.", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
