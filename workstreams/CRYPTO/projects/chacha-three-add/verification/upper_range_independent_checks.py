#!/usr/bin/env python3
"""Independent finite checks of the proposed upper-output-bit closed form.

This script is based only on the supplied candidate equation. It uses the
verifier's earlier general DP and original-word counts, not discovery code.
Finite agreement is not a substitute for a general proof of the closed form.
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


def candidate(r, q, k):
    a = -Fraction(1, 3 * 2**r) + Fraction(4, 3 * 2**(3*r + 2*q))
    b = -Fraction(1, 7 * 2**q) - Fraction(1, 7 * 2**(3*r + q))
    d = Fraction(2, 7 * 2**(3*r + q))
    return a / 4**k + b / 2**k + d / 16**k


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    paths = [Path(__file__).resolve(), HERE / "general_independent_verify.py",
             HERE / "independent_word_counts.jsonl", HERE / "general_standard32_exact.json"]
    report = {"started_utc": datetime.now(timezone.utc).isoformat(),
              "command": [sys.executable, str(Path(__file__).resolve())],
              "environment": {"python": sys.version, "platform": platform.platform()},
              "source_and_input_sha256": {str(p): sha(p) for p in paths},
              "independence": "Candidate equation supplied; discovery code and upper-range proof not read before this check.",
              "new_original_word_enumerations": 0,
              "random_seed": None,
              "hypotheses": "r,q>=1; 0<=k<=q; i=r+q+k<n; uniform independent input words"}
    try:
        rows = [json.loads(line) for line in (HERE / "independent_word_counts.jsonl")
                .read_text().splitlines()]
        rows = [row for row in rows if row["kind"] == "exhaustive"]
        direct_checks = []
        for row in rows:
            n, r, q = row["n"], row["r"], row["q"]
            if r == 0 or q == 0:
                continue
            for k in range(q + 1):
                i = r + q + k
                if i >= n:
                    continue
                observed = Fraction(row["signed_sums"][i], row["samples"])
                closed = candidate(r, q, k)
                assert observed == closed, ("raw-word counterexample", n, r, q, k, observed, closed)
                direct_checks.append({"n": n, "r": r, "q": q, "k": k,
                                      "correlation": str(observed), "pass": True})

        all_cases = set()
        for r in range(1, 6):
            for q in range(1, 6):
                for k in range(q + 1):
                    i = r + q + k
                    for n in (i + 1, r + 2*q + 1, r + 2*q + 3):
                        all_cases.add((n, r, q, k))
        dp_values = {}
        dp_checks = []
        for n, r, q, k in sorted(all_cases):
            observed = correlation(n, r, q, r + q + k)
            closed = candidate(r, q, k)
            assert observed == closed, ("DP counterexample", n, r, q, k, observed, closed)
            dp_values[n, r, q, k] = observed
            dp_checks.append({"n": n, "r": r, "q": q, "k": k,
                              "correlation": str(observed), "pass": True})

        recurrence_checks = []
        for r in range(1, 6):
            for q in range(3, 6):
                for n in (r + 2*q + 1, r + 2*q + 3):
                    for k in range(q - 2):
                        rhs = (Fraction(13, 16) * dp_values[n, r, q, k + 2]
                               - Fraction(11, 64) * dp_values[n, r, q, k + 1]
                               + Fraction(1, 128) * dp_values[n, r, q, k])
                        assert rhs == dp_values[n, r, q, k + 3]
                        recurrence_checks.append({"n": n, "r": r, "q": q, "k": k, "pass": True})

        standard = json.loads((HERE / "general_standard32_exact.json").read_text())
        standard_checks = []
        for k in range(4):
            value = standard["uniform_a"][28 + k]
            previous = Fraction(value["numerator"], value["denominator"])
            closed = candidate(16, 12, k)
            assert previous == closed
            standard_checks.append({"n": 32, "r": 16, "q": 12, "i": 28 + k, "k": k,
                                    "correlation": str(previous), "pass": True})

        row = next(row for row in rows if (row["n"], row["r"], row["q"]) == (5, 1, 1))
        actual = Fraction(row["signed_sums"][4], row["samples"])
        dp_actual = correlation(5, 1, 1, 4)
        invalid_formula = candidate(1, 1, 2)
        assert actual == dp_actual == Fraction(-7, 256)
        assert invalid_formula == Fraction(-57, 2048)
        assert actual != invalid_formula
        report.update({"status": "pass", "exit_code": 0,
                       "raw_original_word_comparisons": len(direct_checks),
                       "exact_dp_comparisons": len(dp_checks),
                       "dp_domain": "r,q=1..5; k=0..q; n in {r+q+k+1,r+2q+1,r+2q+3}, duplicates removed",
                       "recurrence_comparisons": len(recurrence_checks),
                       "recurrence_domain": "r=1..5;q=3..5;0<=k<=q-3;n in {r+2q+1,r+2q+3}",
                       "direct_checks": direct_checks, "dp_checks": dp_checks,
                       "recurrence_checks": recurrence_checks,
                       "standard_checks": standard_checks,
                       "negative_control": {"n": 5, "r": 1, "q": 1, "k": 2, "i": 4,
                                            "violated_hypothesis": "k<=q",
                                            "raw_original_word_value": str(actual),
                                            "independent_general_dp_value": str(dp_actual),
                                            "incorrectly_extended_formula": str(invalid_formula),
                                            "separated": True},
                       "proof_status_at_run": "Finite and exact-DP checks only; general closed-form proof not yet reviewed"})
    except Exception as exc:
        report.update({"status": "failed", "exit_code": 1, "error": repr(exc)})
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (HERE / "upper_range_independent_run.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in
                      ("status", "raw_original_word_comparisons", "exact_dp_comparisons",
                       "recurrence_comparisons", "standard_checks", "negative_control")}, indent=2))


if __name__ == "__main__":
    main()
