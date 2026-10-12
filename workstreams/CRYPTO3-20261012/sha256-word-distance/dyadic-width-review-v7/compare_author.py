#!/usr/bin/env python3
"""Read-only exact-source/certificate comparison after the pre-author freeze."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "dyadic-width-v7"
AUTHOR_MANIFEST_HASH = "a6eebd06e58db8b6ec1c98b4fa20e4c6cffdbd56e97cd36b14b8a6851dd27d35"
PREAUTHOR_HASH = "dc7308c53472ad73eb4bdc0dd00d8a7e5f6a8f4bb68400d8600472c7209075fb"


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    checkpoint_path = HERE / "PRE-AUTHOR-CHECKPOINT.json"
    need(digest(checkpoint_path) == PREAUTHOR_HASH, "pre-author checkpoint identity")
    checkpoint = json.loads(checkpoint_path.read_text())
    need(checkpoint["author_content_read"] is False, "pre-author scope")
    for name, expected_hash in checkpoint["frozen_files_sha256"].items():
        need(digest(HERE / name) == expected_hash, "pre-author frozen file changed")
    manifest_path = AUTHOR / "SHA256.json"
    need(digest(manifest_path) == AUTHOR_MANIFEST_HASH, "pinned author manifest identity")
    manifest = json.loads(manifest_path.read_text())
    expected_names = {"PROOF.md", "check.py", "CERTIFICATE.json", "README.md", "RUN.json"}
    need(len(manifest["files"]) == 5
         and {row["path"] for row in manifest["files"]} == expected_names,
         "complete author manifest coverage")
    for row in manifest["files"]:
        file = AUTHOR / row["path"]
        need(file.stat().st_size == row["bytes"] and digest(file) == row["sha256"],
             "author file exact bytes")
    independent = json.loads((HERE / "VERIFICATION.json").read_text())
    matrix = independent["all_g_output_rows"]
    cases = []
    for budget in independent["case_budgets"]:
        k = budget["k"]
        if k == 9:
            continue
        cases.append({"k": k, "modulus": budget["modulus"],
                      "common": budget["modulus"] // 2,
                      "unchanged_rows": [[j, matrix[j]] for j in range(22, k+13)],
                      "flipping_row": [k+13, matrix[k+13]],
                      "maximum_odd_q": budget["q_max"], "lifts": budget["h_count"],
                      "positive_count": budget["signed_lift_count"] // 2,
                      "signed_count": budget["signed_lift_count"]})
    expected = {"schema": "crypto3-shared-term-width-v7", "cases": cases,
                "integer_q_bound": (1 << 22)-1, "shared_term_bound": 4*((1 << 22)-1),
                "reversal_lift": "(-h) mod lifts"}
    packet = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    need(packet == expected, "author certificate versus independent reconstruction")
    run = json.loads((AUTHOR / "RUN.json").read_text())
    need(run["exit_code"] == 0 and run["checker_sha256"] == digest(AUTHOR / "check.py"),
         "author run recorded checker identity")
    print(json.dumps({"schema": "CRYPTO3-dyadic-width-exact-author-comparison-v7",
                      "passed": True, "author_manifest_sha256": AUTHOR_MANIFEST_HASH,
                      "pre_author_checkpoint_sha256": PREAUTHOR_HASH,
                      "author_files": manifest["files"],
                      "certificate_matches_independent_reconstruction": True,
                      "valuation_layers_compared": len(cases),
                      "author_checker_imported_or_executed": False,
                      "author_run_scope": "Identity and recorded exit checked; author run not independently rerun.",
                      "comparison_script_sha256": digest(Path(__file__))}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
