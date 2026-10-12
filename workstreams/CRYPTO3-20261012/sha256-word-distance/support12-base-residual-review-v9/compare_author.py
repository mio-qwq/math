#!/usr/bin/env python3
"""Read-only exact comparison of support12-base-residual-v9."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / "support12-base-residual-v9"
EXPECTED_AUTHOR_MANIFEST_SHA256 = (
    "cbdfa2fd8d76c4e7bc511f10c30d15b43763144dfd1eac6fff758e1d5ee6546f"
)
PRE_AUTHOR_HASHES = {
    "PRE-AUTHOR-DERIVATION.md":
        "1d77df8a63d389f822d6080e734de99ec741738b24ab8170dcb53719eeb3f97c",
    "PRE-AUTHOR-RUN.json":
        "974d1bc37036ddd205d171873162291920c24d29eda9f450bf4f9a8748e3e6f9",
    "check_independent.py":
        "21880a099f32f2eef7f2295c2039e3f52321a7b3ce5bd5e7a3b1410a898195af",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    for name, expected in PRE_AUTHOR_HASHES.items():
        assert sha(HERE / name) == expected

    manifest_path = AUTHOR / "SHA256.json"
    assert sha(manifest_path) == EXPECTED_AUTHOR_MANIFEST_SHA256
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    author_files = {path.name for path in AUTHOR.iterdir() if path.is_file()}
    assert author_files == set(manifest["files"]) | {"SHA256.json"}
    for name, entry in manifest["files"].items():
        payload = (AUTHOR / name).read_bytes()
        assert len(payload) == entry["bytes"]
        assert hashlib.sha256(payload).hexdigest() == entry["sha256"]

    provenance = json.loads((AUTHOR / "PROVENANCE.json").read_text())
    for relative, expected in provenance["accepted_inputs"].items():
        source = (AUTHOR / relative).resolve()
        assert source.is_file() and sha(source) == expected
    assert provenance["active_support"] == [
        10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57
    ]
    assert provenance["base_parameters"] == [9, 12, 14, 19, 22]
    assert provenance["endpoint_symbols_at_57"] == {"b": "G57", "z": "d57"}

    author_run = subprocess.check_output(
        [sys.executable, "-B", str(AUTHOR / "verify_residual_merge.py")]
    )
    assert author_run == (AUTHOR / "CHECK.json").read_bytes()
    independent_run = subprocess.check_output(
        [sys.executable, "-B", str(HERE / "check_independent.py")]
    )
    assert independent_run == (HERE / "PRE-AUTHOR-RUN.json").read_bytes()

    author_check = json.loads(author_run)
    independent = json.loads(independent_run)
    assert author_check["dependency_sources_affected_by_u57"] == [57, 59, 61, 63]
    assert independent["old_chart"]["coordinates_depending_on_u57"] == [57, 59, 61, 63]
    assert independent["old_chart"]["R33_depends_on_u57"] is False
    assert independent["old_chart"]["R57_rhs_depends_on_u57"] is False
    assert independent["rewritten_chart"]["residual_rows"] == [33]
    assert independent["composition"]["exact_composed_condition"] == (
        "g(B+z)-g(B)=b mod 2^32"
    )
    assert author_check["negative_control"]["projection_is_insufficient"] is True
    assert independent["composition"][
        "pg_is_only_a_necessary_projection_after_base_composition"
    ] is True

    proof = (AUTHOR / "PROOF.md").read_text(encoding="utf-8")
    for required in (
        "R57 = u57 - H",
        "g(H+z)-g(H) = b",
        "does **not** remove the word-57 constraint",
        "neither solves `R33=0` nor proves that (5) can be met",
    ):
        assert required in proof

    print(json.dumps({
        "schema": "CRYPTO3-support12-base-residual-review-v9-comparison",
        "status": "ACCEPT",
        "author_manifest_sha256": EXPECTED_AUTHOR_MANIFEST_SHA256,
        "author_manifest_members": len(manifest["files"]),
        "accepted_input_hashes": provenance["accepted_inputs"],
        "coordinates_affected_by_u57": [57, 59, 61, 63],
        "old_residuals": [33, 57],
        "rewritten_residuals": [33],
        "forced_base": "H=g(C55)+C50+f(C42)+C41",
        "exact_position57_condition": "g(H+z)-g(H)=b mod 2^32",
        "projected_PG_alone_sufficient": False,
        "author_checker_matches_frozen_receipt": True,
        "independent_checker_matches_pre_author_freeze": True,
        "scope": "coordinate reduction only; no solvability and no message pair",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
