#!/usr/bin/env python3
"""Read-only replay of this exact independent review and author checker."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main():
    runs = []
    for script, arguments, expected in (
            ("reconstruct.py", [], "INDEPENDENT-CERTIFICATE.json"),
            ("verify_independent.py", ["--negative"], "INDEPENDENT-VERIFICATION.json"),
            ("compare_author.py", ["--negative"], "COMPARISON.json"),
            ("../coupled-short-proof/check.py", ["--negative"], "AUTHOR-CHECKER-RERUN.json")):
        command = [sys.executable, "-B", script, *arguments]
        start = time.monotonic()
        completed = subprocess.run(command, cwd=HERE, capture_output=True, text=True)
        elapsed = time.monotonic() - start
        record = {"command": command, "exit_code": completed.returncode,
                  "seconds": round(elapsed, 6), "stderr": completed.stderr,
                  "source_sha256": hashlib.sha256((HERE / script).read_bytes()).hexdigest(),
                  "stored_output_sha256": hashlib.sha256((HERE / expected).read_bytes()).hexdigest()}
        if completed.returncode:
            record["stdout"] = completed.stdout
            runs.append(record)
            print(json.dumps({"status": "failed", "runs": runs}, indent=2))
            raise SystemExit(1)
        record["matches_stored_json"] = json.loads(completed.stdout) == json.loads((HERE / expected).read_text())
        runs.append(record)
        if not record["matches_stored_json"]:
            print(json.dumps({"status": "failed", "runs": runs}, indent=2))
            raise SystemExit(1)
    author_frozen_runs = json.loads((HERE.parent / "coupled-short-proof/RUNS.json").read_text())
    author_output = json.loads(author_frozen_runs["runs"][-1]["stdout"])
    if author_output != json.loads((HERE / "AUTHOR-CHECKER-RERUN.json").read_text()):
        raise ValueError("author checker differs from its own frozen run")
    print(json.dumps({"status": "pass", "python": sys.version, "runs": runs,
                      "author_replay_matches_author_frozen_run": True,
                      "sat_smt_RUP_or_DRUP_used": False}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
