#!/usr/bin/env python3
"""Post-disclosure review of two fixed-word written proofs.

The raw original-word counts and arbitrary-bit DP predate this written-proof
review. Only discovery mathematics was read; discovery implementations were not.
No new original-word enumeration is performed by this script.
"""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys

from general_independent_verify import correlation


HERE = Path(__file__).resolve().parent


def chi(ell, x):
    return 1 if x % (1 << (ell + 1)) < (1 << ell) else -1


def triangle(ell, x):
    period = 1 << (ell + 1)
    z = x % period
    return min(z, period - z)


def area(ell, t):
    assert t >= 0
    h = 1 << ell
    k, z = divmod(t, 2 * h)
    if z <= h:
        tail = z * (z + 1) // 2
    else:
        tail = h * h - (2 * h - z) * (2 * h - z - 1) // 2
    return k * h * h + tail


def signed_primitives(ell, t):
    h = 1 << ell
    k, z = divmod(t, 2 * h)  # Euclidean quotient, including negative t.
    f0 = min(z, 2 * h - z)
    g1 = z * (z - 1) // 2 if z <= h else h * (h - 1) - z * (z - 1) // 2
    f1 = -k * h * h + k * (2 * h) * f0 + g1
    return f0, f1


def direct_t(ell, p, a):
    return sum(chi(ell, x - a) * triangle(p, x) for x in range(a))


def abel_t(ell, p, a):
    if a == 0:
        return 0
    return -sum(triangle(ell, z) * chi(p, a - 1 - z) for z in range(1, a))


def area_t(ell, p, a):
    h, big_p = 1 << ell, 1 << p
    t = (a - 1) % (2 * big_p)
    return -area(ell, t) if t <= big_p else area(ell, t - big_p) - h * big_p // 2


def signed_t(ell, p, a):
    base0, base1 = signed_primitives(ell, -a)

    def q0(e):
        return signed_primitives(ell, e - a)[0] - base0

    def q1(e):
        return signed_primitives(ell, e - a)[1] - base1 + a * q0(e)

    big_p = 1 << p
    t = a % (2 * big_p)
    if t <= big_p:
        return q1(t)
    return 2 * q1(big_p) - q1(t) + 2 * big_p * (q0(t) - q0(big_p))


def closed_correlation(r, q, a, t_function=area_t):
    size = 1 << (r + q)
    a %= size
    numerator = size * (1 - 2 * a) + 2 * a * (a - 1)
    numerator += 4 * sum((1 << ell) * t_function(ell, ell + q, a) for ell in range(r))
    return Fraction(numerator, (1 << r) * size * size)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    files = [Path(__file__).resolve(), HERE / "general_independent_verify.py",
             HERE / "general_fixed_word_counts.jsonl", HERE / "general_standard32_exact.json",
             HERE.parent / "proofs" / "fixed_first_word.md",
             HERE.parent / "proofs" / "fixed_word_sign.md"]
    report = {"started_utc": datetime.now(timezone.utc).isoformat(),
              "command": [sys.executable, str(Path(__file__).resolve())],
              "environment": {"python": sys.version, "platform": platform.platform()},
              "source_and_input_sha256": {str(p): sha(p) for p in files},
              "independence": "Post-disclosure written-proof review; discovery code never read."
                              " Original-word and DP data generated before these proofs were read.",
              "new_original_word_enumerations": 0, "random_seed": None}
    try:
        primitive_pairs = 0
        for ell in range(6):
            period = 1 << (ell + 1)
            for t in range(-3 * period - 1, 3 * period + 2):
                a0, a1 = signed_primitives(ell, t)
                b0, b1 = signed_primitives(ell, t + 1)
                assert b0 - a0 == chi(ell, t), ("F0", ell, t)
                assert b1 - a1 == t * chi(ell, t), ("F1", ell, t)
                primitive_pairs += 1

        auxiliary_cases = 0
        auxiliary_a0 = 0
        for p in range(1, 7):
            for ell in range(p):
                h, big_p = 1 << ell, 1 << p
                for a in range(4 * big_p + 2):
                    original = direct_t(ell, p, a)
                    assert original == abel_t(ell, p, a), ("Abel", ell, p, a)
                    assert original == area_t(ell, p, a), ("area T", ell, p, a)
                    assert original == signed_t(ell, p, a), ("signed T", ell, p, a)
                    assert -h * big_p // 2 <= original <= 0, ("bound", ell, p, a)
                    t = (a - 1) % (2 * big_p)
                    assert area(ell, t) == sum(triangle(ell, z) for z in range(1, t + 1))
                    auxiliary_cases += 1
                    auxiliary_a0 += int(a == 0)

        original_rows = [json.loads(line) for line in (HERE / "general_fixed_word_counts.jsonl")
                         .read_text().splitlines()]
        word_checks = []
        class_counts = {"A=0 positive": 0, "A=1 equals -C0": 0, "A>=2 below -C0": 0}
        for row in original_rows:
            n, r, q, full_a = row["n"], row["r"], row["q"], row["a"]
            if not (r >= 1 and q >= 1 and r + q < n):
                continue
            i, size = r + q, 1 << (r + q)
            a = full_a % size
            observed = Fraction(row["signed_sums"][i], row["samples"])
            direct_prefix = closed_correlation(r, q, a, direct_t)
            triangle_prefix = closed_correlation(r, q, a)
            signed_prefix = closed_correlation(r, q, a, signed_t)
            assert observed == direct_prefix == triangle_prefix == signed_prefix
            c0 = Fraction(1, 1 << (2 * r + q))
            if a == 0:
                assert observed == c0
                class_counts["A=0 positive"] += 1
            elif a == 1:
                assert observed == -c0
                class_counts["A=1 equals -C0"] += 1
            else:
                assert observed < -c0
                class_counts["A>=2 below -C0"] += 1
            word_checks.append({"n": n, "r": r, "q": q, "a": full_a, "A_low": a,
                                "correlation": str(observed), "pass": True})

        standard = json.loads((HERE / "general_standard32_exact.json").read_text())
        standard_checks = []
        for literal, spectrum in standard["fixed_a"].items():
            a = int(literal, 16)
            independently_computed = Fraction(spectrum[28]["numerator"], spectrum[28]["denominator"])
            formula = closed_correlation(16, 12, a)
            alternative = closed_correlation(16, 12, a, signed_t)
            assert independently_computed == formula == alternative
            standard_checks.append({"a": literal, "correlation": str(formula), "pass": True,
                                    "reference": "Previously generated independent arbitrary-bit DP output"})
        zero = correlation(32, 16, 12, 28, fixed_a=0)
        assert zero == closed_correlation(16, 12, 0) == Fraction(1, 1 << 44)
        standard_checks.append({"a": "0x00000000", "correlation": str(zero), "pass": True,
                                "reference": "Independent arbitrary-bit DP recomputed at A=0"})
        report.update({"status": "pass", "exit_code": 0,
                       "signed_primitive_parameter_pairs": primitive_pairs,
                       "signed_primitive_identities_checked": 2 * primitive_pairs,
                       "signed_primitive_domain": "ell=0..5; t=-3*2^(ell+1)-1 .. 3*2^(ell+1)+1",
                       "auxiliary_parameter_cases": auxiliary_cases,
                       "auxiliary_A0_cases": auxiliary_a0,
                       "auxiliary_domain": "p=1..6; ell=0..p-1; A=0..4*2^p+1",
                       "auxiliary_checks": "Direct T equals Abel convolution, triangular-area formula,"
                                           " signed-primitive formula; T bound; area versus direct triangle sum",
                       "original_word_sign_comparisons": len(word_checks),
                       "sign_class_counts": class_counts,
                       "word_comparisons": word_checks,
                       "standard_endpoint_comparisons": standard_checks})
    except Exception as exc:
        report.update({"status": "failed", "exit_code": 1, "error": repr(exc)})
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (HERE / "fixed_proof_review_run.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in
                      ("status", "signed_primitive_parameter_pairs", "signed_primitive_identities_checked",
                       "auxiliary_parameter_cases", "auxiliary_A0_cases", "original_word_sign_comparisons",
                       "sign_class_counts", "standard_endpoint_comparisons")}, indent=2))


if __name__ == "__main__":
    main()
