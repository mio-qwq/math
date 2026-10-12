#!/usr/bin/env python3
"""Read-only replay of the blind proof, v8 rejection and v9 acceptance."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((HERE / "SHA256.json").read_text())
    for name, expected in manifest["files"].items():
        if name == "replay_readonly.py":
            continue
        assert sha(HERE / name) == expected, name
    commands = [
        ("blind", HERE / "check_independent.py", ["--negative"], "PASS"),
        ("v8", HERE / "compare_author_v8.py", [], "REJECT"),
        ("v9", HERE / "compare_author_v9.py", [], "ACCEPT"),
    ]
    results = []
    for label, script, arguments, expected_status in commands:
        completed = subprocess.run(
            [sys.executable, "-B", str(script), *arguments], cwd=ROOT,
            text=True, capture_output=True, timeout=60, check=False,
        )
        assert completed.returncode == 0, (label, completed.stderr)
        payload = json.loads(completed.stdout)
        assert payload["status"] == expected_status, label
        results.append({"gate": label, "status": payload["status"]})
    print(json.dumps({
        "schema": "CRYPTO3-support12-full-factor-review-v8-v9-readonly-replay",
        "status": "PASS",
        "gates": results,
        "scope": "v8 rejected for wrong support object; corrected v9 accepted only at independent-active-pair factorization layer",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
