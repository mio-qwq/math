#!/usr/bin/env python3
"""Short replay for the CRYPTO3 stage-10 checkpoint."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
V9_SHA256 = "094eceeba2e3c5b68fb4310b10fe0dfc0b487744a8d58a481331670f90992c80"
PACKAGES = (
    ROOT / "sha256-word-distance" / "support12-v16-q33-63-v10",
    ROOT / "sha256-word-distance" / "support12-v16-q33-63-review-v10",
    ROOT / "sha256-word-distance" / "support12-v16-core-q33-63-v10",
    ROOT / "sha256-word-distance" / "support12-v16-core-q33-63-review-v10",
    ROOT / "sha256-word-distance" / "support12-base-factor-normal-v10",
)


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
    if sha(ROOT / "continuation-v9" / "SHA256.json") != V9_SHA256:
        raise AssertionError("stage-9 manifest changed")
    manifests = [verify_manifest(path) for path in PACKAGES]
    classification_review = json.loads((PACKAGES[1] / "ACCEPTANCE.json").read_text())
    if classification_review["decision"] != "ACCEPT":
        raise AssertionError("independent classification acceptance missing")
    review = json.loads((PACKAGES[3] / "AUDIT.json").read_text())
    if review["status"] != "ACCEPT" or len(review["accepted_q"]) != 16:
        raise AssertionError("independent core acceptance missing")
    runs = []
    if not args.manifest_only:
        runs.append(run([sys.executable, "-B", str(PACKAGES[3] /
                        "independent_review.py")]))
        runs.append(run([sys.executable, "-B", str(PACKAGES[4] /
                        "verify_candidate.py")]))
    print(json.dumps({"status": "PASS", "manifests": manifests,
                      "independent_accepted_q": len(review["accepted_q"]),
                      "classification_review": "ACCEPT",
                      "runs": runs}, sort_keys=True))


if __name__ == "__main__":
    main()
