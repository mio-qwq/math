#!/usr/bin/env python3
"""Compare the frozen author v8 object with the true support index 12."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-full-factor-v8"
SOURCE = HERE.parent / "supports-v2.json"

EXPECTED_MANIFEST_SHA256 = "02a3729a66b7e474eb2abfeb33920160e2d60386f324ab5d4ef1b5c1e2bc0814"
EXPECTED_PROOF_SHA256 = "0c2ecb61f3517e1203d8119a7c266010f114e5992daae5df5d4f9e51d723470d"
EXPECTED_CERT_SHA256 = "c6e4b6fee0978ffd942310d83e13564e071881fd3067739fc5caa6e1e84abeac"
EXPECTED_CHECKER_SHA256 = "22579f2a12ac460c8ee49d93cd53457402f3440defc96729ba6d1716ecb3609e"
TRUE_SUPPORT = [10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57]


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(active):
    active = set(active)
    result = {}
    for t in range(16, 64):
        row = {}
        for kind, index, coefficient in (
            ("d", t, 1), ("G", t - 2, -1), ("d", t - 7, -1),
            ("F", t - 15, -1), ("d", t - 16, -1),
        ):
            if index in active:
                name = f"{kind}{index}"
                row[name] = row.get(name, 0) + coefficient
                if row[name] == 0:
                    del row[name]
        result[t] = row
    return result


def main():
    require(digest(AUTHOR / "manifest.json") == EXPECTED_MANIFEST_SHA256,
            "author manifest version changed")
    require(digest(AUTHOR / "PROOF.md") == EXPECTED_PROOF_SHA256, "author proof version changed")
    require(digest(AUTHOR / "CERTIFICATE.json") == EXPECTED_CERT_SHA256,
            "author certificate version changed")
    require(digest(AUTHOR / "check.py") == EXPECTED_CHECKER_SHA256,
            "author checker version changed")

    manifest = json.loads((AUTHOR / "manifest.json").read_text())
    for name, expected in manifest["files"].items():
        require(digest(AUTHOR / name) == expected, "author manifest file mismatch: " + name)

    source = json.loads(SOURCE.read_text())
    require(source["supports"][12] == TRUE_SUPPORT, "true source index 12 changed")
    cert = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    author_support = cert["active_indices"]
    require(cert["support_index"] == 12, "unexpected author label")
    require(author_support == source["supports"][11], "author no longer equals wrong index 11")
    require(author_support != TRUE_SUPPORT, "fatal target mismatch unexpectedly absent")

    correct_rows = rows(TRUE_SUPPORT)
    author_rows = rows(author_support)
    changed = [t for t in range(16, 64) if correct_rows[t] != author_rows[t]]
    require(changed == [20, 27, 28, 29, 34, 42, 43], "unexpected changed-row set")
    require(sum(bool(x) for x in correct_rows.values()) == 25, "correct nonzero count")
    require(sum(bool(x) for x in author_rows.values()) == 25, "author nonzero count")
    require([t for t, row in correct_rows.items() if not row] ==
            [t for t, row in author_rows.items() if not row],
            "zero-row times should be a nondiscriminating coincidence")

    require(set(cert["factor_records"]) == {str(i) for i in author_support},
            "author factor coverage not its own support")
    require("13" not in cert["factor_records"] and "27" in cert["factor_records"],
            "factor target mismatch not exposed")

    completed = subprocess.run(
        [sys.executable, "-B", str(AUTHOR / "check.py"), "--negative"],
        cwd=HERE.parents[4], text=True, capture_output=True, timeout=30, check=False,
    )
    require(completed.returncode == 0, "author self-check did not replay")
    self_check = json.loads(completed.stdout)
    require(self_check["status"] == "PASS", "author self-check status")
    require(len(self_check["negative_controls"]) == 6 and
            all(item["rejected"] for item in self_check["negative_controls"]),
            "author negative controls")

    result = {
        "schema": "CRYPTO3-support12-full-factor-v8-independent-comparison",
        "status": "REJECT",
        "reason": "fatal support-object mismatch: author labels index 12 but factors source supports[11]",
        "true_support_index_12": TRUE_SUPPORT,
        "author_active_indices": author_support,
        "author_actual_source_index": 11,
        "set_difference": {
            "missing_from_author": sorted(set(TRUE_SUPPORT) - set(author_support)),
            "spurious_in_author": sorted(set(author_support) - set(TRUE_SUPPORT)),
        },
        "changed_original_rows": {
            str(t): {"true": correct_rows[t], "author": author_rows[t]} for t in changed
        },
        "nondiscriminating_coincidences": {
            "nonzero_rows_both": 25,
            "zero_rows_both": 23,
            "zero_row_times_equal": True,
            "author_rank": self_check["summary"]["integer_rank"],
            "author_free_rank": self_check["summary"]["free_rank"],
        },
        "factor_mismatch": {
            "missing_true_factor": 13,
            "spurious_author_factor": 27,
            "correct_private_boundary_parameters": ["G10", "G11", "G13", "F57"],
            "correct_private_count": 4,
            "correct_shared_count_after_boundary_projection": 10,
            "author_private_parameters": self_check["summary"]["private_parameters"],
            "author_private_count": len(self_check["summary"]["private_parameters"]),
            "author_shared_count": len(self_check["summary"]["shared_parameters"]),
        },
        "author_internal_self_check": {
            "status": "PASS for the wrong index-11 support only",
            "negative_controls_rejected": 6,
            "missing_control": "no binding of claimed support_index 12 to source supports[12]",
        },
        "author_hashes": {
            "manifest.json": EXPECTED_MANIFEST_SHA256,
            "PROOF.md": EXPECTED_PROOF_SHA256,
            "CERTIFICATE.json": EXPECTED_CERT_SHA256,
            "check.py": EXPECTED_CHECKER_SHA256,
        },
        "scope": "reject v8 as evidence about true support12; no judgment against its internal factorization of source index11",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
