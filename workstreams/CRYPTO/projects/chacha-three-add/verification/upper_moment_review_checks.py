#!/usr/bin/env python3
"""Post-disclosure check of intermediate overlap-region moment formulas.

Uses the independently written four-state evaluator. Discovery implementations
are not read or imported. The earlier blind upper-range result is left intact.
"""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

from general_independent_verify import integer_moment


HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    paths = [Path(__file__).resolve(), HERE / "general_independent_verify.py",
             HERE / "upper_range_independent_run.json",
             HERE.parent / "proofs" / "overlap_bit_closed_form.md"]
    report = {"started_utc": datetime.now(timezone.utc).isoformat(),
              "command": [sys.executable, str(Path(__file__).resolve())],
              "source_and_input_sha256": {str(p): sha(p) for p in paths},
              "independence": "Post-disclosure manuscript review; previously independent DP, no discovery implementation read.",
              "domain": "r,q=1..5;0<=k<=q;i=r+q+k;n=i+1",
              "random_seed": None}
    try:
        unmasked = []
        masked = []
        low_count, high_count = 0, 0
        boundary_count, zero_count, beyond_r_count = 0, 0, 0
        for r in range(1, 6):
            for q in range(1, 6):
                for k in range(q + 1):
                    i = r + q + k
                    n = i + 1
                    h_size, k_size, n_size = 1 << (r + q), 1 << k, 1 << i
                    observed = Fraction(integer_moment(n, i, k), 8**n)
                    expected = (Fraction(-1, 3) + Fraction(4, 3 * h_size**2)) / k_size
                    assert observed == expected, ("M0", r, q, k, observed, expected)
                    unmasked.append({"r": r, "q": q, "k": k,
                                     "moment": str(observed), "pass": True})
                    boundary_count += int(k == q)
                    zero_count += int(k == 0)
                    beyond_r_count += int(k >= r)
                    for ell in range(r + k):
                        p = ell + q
                        observed = Fraction(integer_moment(n, i, k, h=ell, l=p), 8**n)
                        factor = 2 if ell < k else 1
                        expected = Fraction(factor * 2**(ell + p - k), n_size**2)
                        assert observed == expected, ("masked", r, q, k, ell, p, observed, expected)
                        low_count += int(ell < k)
                        high_count += int(ell >= k)
                        masked.append({"r": r, "q": q, "k": k, "ell": ell, "p": p,
                                       "branch": "low" if ell < k else "high",
                                       "moment": str(observed), "pass": True})

        # In the required domain failure, exactly the p<k low mask is outside
        # the block-affine identity. Check that moment separately and exactly.
        actual_failure_moment = Fraction(integer_moment(5, 4, 2, h=0, l=1), 8**5)
        wrongly_extended_moment = Fraction(1, 256)
        assert actual_failure_moment == 0
        assert actual_failure_moment != wrongly_extended_moment
        report.update({"status": "pass", "exit_code": 0,
                       "unmasked_moment_comparisons": len(unmasked),
                       "masked_moment_comparisons": len(masked),
                       "low_mask_comparisons": low_count, "high_mask_comparisons": high_count,
                       "parameter_cases_at_k_equals_q": boundary_count,
                       "parameter_cases_at_k_equals_zero": zero_count,
                       "parameter_cases_with_k_at_least_r": beyond_r_count,
                       "unmasked": unmasked, "masked": masked,
                       "invalid_block_negative_control": {
                           "n": 5, "r": 1, "q": 1, "k": 2, "i": 4,
                           "ell": 0, "p": 1, "violated_condition": "p>=k",
                           "actual_moment": str(actual_failure_moment),
                           "incorrectly_extended_moment": str(wrongly_extended_moment),
                           "contribution_to_correlation_difference": "1/2048"}})
    except Exception as exc:
        report.update({"status": "failed", "exit_code": 1, "error": repr(exc)})
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (HERE / "upper_moment_review_run.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in
                      ("status", "unmasked_moment_comparisons", "masked_moment_comparisons",
                       "low_mask_comparisons", "high_mask_comparisons",
                       "parameter_cases_at_k_equals_q", "parameter_cases_at_k_equals_zero",
                       "parameter_cases_with_k_at_least_r", "invalid_block_negative_control")}, indent=2))


if __name__ == "__main__":
    main()
