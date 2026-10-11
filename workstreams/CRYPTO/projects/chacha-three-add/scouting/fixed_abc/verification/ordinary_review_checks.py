#!/usr/bin/env python3
"""Post-disclosure ordinary review; does not rerun the discovery harness.

Compare discovery evaluator with the frozen independent original-word values,
then use the already frozen independent evaluator on exactly the six disclosed
standard-width examples. No original-input enumeration is performed here.
"""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SCOUT = HERE.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    report = {"started_utc": datetime.now(timezone.utc).isoformat(),
              "command": [sys.executable, str(Path(__file__).resolve())],
              "environment": {"python": sys.version, "platform": platform.platform()},
              "review_type": "Ordinary post-disclosure proof/code/results review, following a frozen independent stage",
              "discovery_harness_rerun": False,
              "original_word_inputs_enumerated_in_this_run": 0,
              "randomness": "none"}
    try:
        frozen_path = HERE / "INDEPENDENT_STAGE_MANIFEST.json"
        assert sha(frozen_path) == "05dda496968ff4d50a182b745cb68126a1e510b3746a5bb619b7ca48f2a7af8e"
        frozen = json.loads(frozen_path.read_text())
        for entry in frozen["files"]:
            assert sha(HERE / entry["file"]) == entry["sha256"]
        discovery_source = SCOUT / "fixed_abc.py"
        assert sha(discovery_source) == "fa914112701aa6c6608c2b21f0a84fbc4e4615d9dac09c86b52ca41b7420a33e"
        reference = load_module("frozen_independent_fixed_abc", HERE / "independent_fixed_abc.py")
        discovery = load_module("reviewed_discovery_fixed_abc", discovery_source)
        raw_receipt = json.loads((HERE / "independent_run.json").read_text())
        discovery_receipt = json.loads((SCOUT / "results.json").read_text())
        assert discovery_receipt["source_sha256"] == sha(discovery_source)

        original_value_checks = []
        for row in raw_receipt["comparisons"]:
            n,r,q,i,a,b,c = (row[key] for key in ("n","r","q","i","a","b","c"))
            value,detail = discovery.fixed_abc_correlation(a,b,c,n,r,q,i)
            assert value == Fraction(row["correlation"])
            assert detail["terminal_counts"] == row["state_details"]["terminal_integer_counts"]
            assert detail["unreduced_denominator"] == row["state_details"]["denominator_before_reduction"]
            assert detail["initial_phase"] == 1-2*row["state_details"]["constant_phase"]
            original_value_checks.append({key:row[key] for key in ("n","r","q","i","a","b","c","correlation")})

        standard_checks = []
        rows = discovery_receipt["standard32_analytical_examples"]
        assert len(rows) == 6
        for row in rows:
            a,b,c = (int(row[key],16) for key in ("a_hex","b_hex","c_hex"))
            n,r,q,i = (row[key] for key in ("n","r","q","i"))
            value,detail = reference.four_state_correlation(n,r,q,i,a,b,c)
            reviewed_value,reviewed_detail = discovery.fixed_abc_correlation(a,b,c,n,r,q,i)
            assert value == reviewed_value == Fraction(row["exact_correlation"])
            assert detail["terminal_integer_counts"] == reviewed_detail["terminal_counts"] == row["diagnostics"]["terminal_counts"]
            assert detail["denominator_before_reduction"] == row["diagnostics"]["unreduced_denominator"]
            if a == b == 0:
                assert value == 1-Fraction(2*(c % (1 << ((i-q)%n))),1 << ((i-q)%n))
            if b == c == 0:
                assert value == 1-Fraction(2*(a % (1 << i)),1 << i)
            standard_checks.append({key:row[key] for key in ("label","a_hex","b_hex","c_hex","n","r","q","i","exact_correlation")})

        # Internal receipt consistency only. This does not independently repeat
        # the discovering agent's 188-input original-word run.
        assert len(discovery.CASES) == discovery_receipt["fixed_parameter_cases"] == 17
        assert sum(1 << case[0] for case in discovery.CASES) == discovery_receipt["enumerated_d_inputs"] == 188
        assert sum(case[0] for case in discovery.CASES) == len(discovery_receipt["records"]) == 54
        assert sum(case[0]*(1 << case[0]) for case in discovery.CASES) == discovery_receipt["pointwise_identity_checks"] == 692
        for row in discovery_receipt["records"]:
            assert row["d_count"] == 1 << row["n"]
            assert Fraction(row["signed_sum_over_d"],row["d_count"]) == Fraction(row["exact_correlation"])
            assert sum(row["diagnostics"]["terminal_counts"]) == row["diagnostics"]["unreduced_denominator"]

        # Ordinary analytical check of the newly disclosed false-independence
        # control. These two symbolic bit alternatives are not a word harness.
        complementary = []
        for u0 in (0,1):
            borrow = 1-u0  # c=1, U-c incoming borrow at bit one
            carry = u0     # S=3, b=2: Y_0=U_0, S_0=1
            assert borrow ^ carry == 1
            complementary.append({"U_0":u0,"borrow_1":borrow,"carry_1":carry})
        signed_borrow = sum(1-2*row["borrow_1"] for row in complementary)/2
        signed_carry = sum(1-2*row["carry_1"] for row in complementary)/2
        assert signed_borrow == signed_carry == 0

        files = [SCOUT/name for name in ("SCOUT.md","fixed_abc.py","results.json","RUN.md")]
        report.update({"status":"pass","exit_code":0,"source_sha256":sha(Path(__file__).resolve()),
                       "independent_stage_manifest_sha256":sha(frozen_path),
                       "frozen_independent_files_unchanged":len(frozen["files"]),
                       "reviewed_files_sha256":{str(p.relative_to(SCOUT)):sha(p) for p in files},
                       "discovery_against_independent_raw_bit_values":len(original_value_checks),
                       "raw_value_checks":original_value_checks,
                       "standard_analytical_checks":standard_checks,
                       "newly_disclosed_symbolic_negative_control":{"n":2,"r":0,"q":0,"a":1,"b":2,"c":1,"i":1,"bit_cases":complementary,"actual":"-1","false_marginal_product":"0"},
                       "discovery_receipt_arithmetic_consistent":True,
                       "classification":"L0 model calibration; no novelty or attack claim"})
    except Exception as exc:
        report.update({"status":"failed","exit_code":1,"error":repr(exc)})
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (HERE / "ordinary_review_run.json").write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({"status":report["status"],
                      "discovery_vs_frozen_original_bit_values":len(original_value_checks),
                      "independent_standard_analytical_values":len(standard_checks),
                      "original_word_inputs_enumerated_in_this_run":0,
                      "discovery_harness_rerun":False},indent=2))


if __name__ == "__main__":
    main()
