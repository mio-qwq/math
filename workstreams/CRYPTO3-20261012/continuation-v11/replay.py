#!/usr/bin/env python3
"""Short replay for the CRYPTO3 stage-11 checkpoint."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V10_SHA256 = "ed9ce1a9dbe3b8d2cb39745af024a1e84e9444fa72998cf8de31ceb1431308ca"
AUTHOR = ROOT / "sha256-word-distance" / "support12-base-factor-normal-proof-v11"
REVIEW = ROOT / "sha256-word-distance" / "support12-base-factor-normal-review-v11"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(directory):
    manifest = directory / "SHA256.json"
    data = json.loads(manifest.read_text())
    files = data["files"] if "files" in data else data
    for rel, expected in files.items():
        path = directory / rel
        if not path.is_file() or sha(path) != expected:
            raise AssertionError(f"manifest mismatch: {path}")
    return {"package": directory.name, "files": len(files),
            "manifest_sha256": sha(manifest)}


def run(command):
    started = time.monotonic()
    result = subprocess.run(command, cwd=ROOT.parents[1], text=True,
                            capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return {"command": command, "seconds": time.monotonic() - started,
            "stdout_tail": result.stdout.strip()[-1000:]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-only", action="store_true")
    args = parser.parse_args()
    if sha(ROOT / "continuation-v10" / "SHA256.json") != V10_SHA256:
        raise AssertionError("stage-10 manifest changed")
    manifests = [verify_manifest(AUTHOR), verify_manifest(REVIEW)]
    author_run = json.loads((AUTHOR / "RUN.json").read_text())
    audit = json.loads((REVIEW / "AUDIT.json").read_text())
    if author_run["status"] != "PASS":
        raise AssertionError("author symbolic audit missing")
    if audit["status"] != "ACCEPT":
        raise AssertionError("independent acceptance missing")
    runs = []
    if not args.manifest_only:
        runs.append(run([sys.executable, "-B", str(AUTHOR /
                        "check_symbolic.py")]))
        runs.append(run([sys.executable, "-B", str(REVIEW /
                        "check_pre_author.py")]))
        runs.append(run([sys.executable, "-B", str(REVIEW /
                        "compare_author.py")]))
    print(json.dumps({"status": "PASS", "stage10_integrity": "PASS",
                      "manifests": manifests,
                      "independent_review": "ACCEPT", "runs": runs},
                     sort_keys=True))


if __name__ == "__main__":
    main()
