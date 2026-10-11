#!/usr/bin/env python3
"""Ordinary post-disclosure code review of the supplied streaming implementation.

This imports the reviewed implementation explicitly. It is not blind validation
and does not rerun the developer's 1650-case harness. The 18 cases are precisely
the ones already checked in the preceding independent mathematical phase.
"""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
OLD = HERE.parent
PROJECT = OLD.parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def as_lists(matrix):
    return [list(row) for row in matrix]


def main():
    source = PROJECT / "experiments/streaming_prefix.py"
    expected_sha = "225348096f0e4bddbd13a117840ea45ea5976c32b6a4ec65e2d0ee4476d905b7"
    assert sha(source) == expected_sha
    target = load_module("reviewed_streaming_prefix", source)
    reference = load_module("prior_matrix_specification", HERE / "matrix_spec_checks.py")
    prior = json.loads((HERE / "matrix_spec_run.json").read_text())
    manifest_path = OLD / "INDEPENDENT_VERIFICATION_MANIFEST.json"
    manifest_hash = sha(manifest_path)
    frozen = json.loads(manifest_path.read_text())
    inputs = [source, PROJECT / "proofs/streaming_prefix_baseline.md",
              PROJECT / "experiments/STREAMING_PREFIX_RUN.md",
              PROJECT / "experiments/results/streaming_prefix_run.json",
              HERE / "matrix_spec_checks.py", HERE / "matrix_spec_run.json"]
    report = {"started_utc": datetime.now(timezone.utc).isoformat(),
              "command": [sys.executable, str(Path(__file__).resolve())],
              "review_mode": "Ordinary source review and targeted execution after explicit implementation disclosure",
              "source_sha256": sha(Path(__file__).resolve()),
              "reviewed_and_reference_sha256": {str(p): sha(p) for p in inputs},
              "new_original_word_enumerations": 0,
              "full_1650_case_harness_rerun": False,
              "random_seed": None}
    try:
        table_checks = []
        phase_cases = [(0, 1, 1), (0, 0, 0), (0, 1, 0), (0, 0, 1)]
        for mode, fixed in [("uniform", None), ("0", 0), ("1", 1)]:
            p = reference.KERNELS[fixed]["none"]
            pinv = reference.inverse(p)
            assert as_lists(target.BASES[mode]["matrix"]) == p
            assert as_lists(target.BASES[mode]["inverse"]) == pinv
            for code, (position, i, k) in enumerate(phase_cases):
                d = reference.phase(position, i, k)
                transition, transition_inverse, insertions = target.TABLES[mode][code]
                assert as_lists(transition) == reference.multiply(p, d)
                assert as_lists(transition_inverse) == reference.multiply(d, pinv)
                for mask in ("B", "Y", "BY"):
                    expected = reference.multiply(reference.multiply(reference.multiply(d, pinv),
                                                                      reference.KERNELS[fixed][mask]), d)
                    assert as_lists(insertions[mask]) == expected
                    table_checks.append({"mode": mode, "phase_code": code, "mask": mask, "pass": True})
        cases = []
        for row in prior["comparisons"]:
            n, r, q, i, a = row["n"], row["r"], row["q"], row["i"], row["fixed_a"]
            stats = target.ArithmeticStats()
            actual = target.streaming_correlation(n, r, q, i, fixed_a=a, stats=stats)
            assert actual == Fraction(row["correlation"])
            length, distance = (i-q, q) if i >= q else (i, n-q)
            expected_matrices = 0 if length == 0 else (4*length if distance == 0 else 2*distance + 8*length)
            expected_rows = n + (length if distance and length else 0)
            assert stats.matrix_products == expected_matrices
            assert stats.row_products == expected_rows
            assert stats.matrix_products <= 8*n and stats.row_products <= 2*n
            cases.append({"n": n, "r": r, "q": q, "i": i, "fixed_a": a,
                          "correlation": str(actual), "matrix_products": stats.matrix_products,
                          "row_products": stats.row_products, "pass": True})
        for item in frozen["files"]:
            assert sha(OLD / item["file"]) == item["sha256"]
        assert sha(manifest_path) == manifest_hash
        assert sha(source) == expected_sha
        report.update({"status": "pass", "exit_code": 0,
                       "constant_phase_mask_table_comparisons": len(table_checks),
                       "original_selected_cases_reused": len(cases),
                       "table_checks": table_checks, "cases": cases,
                       "exact_dynamic_operation_count_formulas_passed": True,
                       "reviewed_source_and_old_22_files_unchanged": True})
    except Exception as exc:
        report.update({"status": "failed", "exit_code": 1, "error": repr(exc)})
        raise
    finally:
        report["finished_utc"] = datetime.now(timezone.utc).isoformat()
        (HERE / "ordinary_code_review_run.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in
                      ("status", "constant_phase_mask_table_comparisons", "original_selected_cases_reused",
                       "exact_dynamic_operation_count_formulas_passed", "full_1650_case_harness_rerun",
                       "reviewed_source_and_old_22_files_unchanged")}, indent=2))


if __name__ == "__main__":
    main()
