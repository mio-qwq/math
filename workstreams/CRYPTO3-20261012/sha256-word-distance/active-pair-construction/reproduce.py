#!/usr/bin/env python3
"""Replay this bounded investigation without changing stored evidence."""
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
            ("analyze.py", [], "ANALYSIS.json"),
            ("fixed_mask_probe.py", [], "FIXED-MASK-RUN.json"),
            ("verify.py", ["--negative"], "VERIFICATION.json")):
        command = [sys.executable, "-B", script, *arguments]
        start = time.monotonic()
        completed = subprocess.run(command, cwd=HERE, capture_output=True, text=True)
        elapsed = time.monotonic() - start
        record = {"command": command, "exit_code": completed.returncode,
                  "seconds": round(elapsed, 6), "stderr": completed.stderr,
                  "script_sha256": hashlib.sha256((HERE / script).read_bytes()).hexdigest(),
                  "expected_output_sha256": hashlib.sha256((HERE / expected).read_bytes()).hexdigest()}
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
    print(json.dumps({"status": "pass", "python": sys.version,
                      "uses_external_dependencies": False, "runs": runs}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
