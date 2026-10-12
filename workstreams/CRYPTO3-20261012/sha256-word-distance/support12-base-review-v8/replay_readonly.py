#!/usr/bin/env python3
"""Read-only replay for the support-12 base interpolation review."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-base-lift-v8"
EXPECTED_AUTHOR_MANIFEST = "374732f8fee671cd7290d7596ab7f0cb85bb83502b3c94a124d7a78280802dc6"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_listing(manifest_path):
    manifest = json.loads(manifest_path.read_text())
    for name, expected in manifest["files"].items():
        actual = digest(manifest_path.parent / name)
        require(actual == expected, "manifest mismatch: " + str(manifest_path.parent / name))
    return len(manifest["files"])


def run_json(script):
    completed = subprocess.run([sys.executable, "-B", str(script)],
                               cwd=HERE.parents[3], text=True,
                               capture_output=True, check=False)
    require(completed.returncode == 0, script.name + " failed: " + completed.stderr)
    require(completed.stderr == "", script.name + " emitted stderr")
    return json.loads(completed.stdout)


def main():
    freeze = json.loads((HERE / "PRE-AUTHOR-FREEZE.json").read_text())
    for name, expected in freeze["files_sha256"].items():
        require(digest(HERE / name) == expected, "pre-author freeze mismatch: " + name)
    require(digest(AUTHOR / "SHA256.json") == EXPECTED_AUTHOR_MANIFEST,
            "author manifest changed")
    author_files = verify_listing(AUTHOR / "SHA256.json")
    review_files = verify_listing(HERE / "SHA256.json")
    independent = run_json(HERE / "check_independent.py")
    comparison = run_json(HERE / "compare_author.py")
    require(independent["status"] == "PASS" and independent["phase"] == "PRE-AUTHOR",
            "independent replay status")
    require(comparison["status"] == "ACCEPT", "comparison replay status")
    print(json.dumps({
        "schema": "CRYPTO3-support12-base-review-v8-readonly-replay",
        "status": "PASS",
        "pre_author_files_checked": len(freeze["files_sha256"]),
        "author_files_checked": author_files,
        "review_files_checked": review_files,
        "independent_anchor_sets_below_five": independent["minimality"]["sets_checked_below_five"],
        "author_first_size5_trial": comparison["chart_comparison"]["author_first_lexicographic_size5"]["trials_to_first_success"],
        "accepted_scope": comparison["theorem_scope"]
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
