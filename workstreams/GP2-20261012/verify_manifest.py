#!/usr/bin/env python3
"""Verify the frozen stage's exact file bytes; no files are modified."""
from pathlib import Path
import hashlib
import json


def main():
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / "MANIFEST.json").read_text())
    records = manifest["files"]
    for name, record in records.items():
        path = root / name
        if path.resolve().parent != root and root not in path.resolve().parents:
            raise ValueError(f"Path escapes the package: {name}")
        data = path.read_bytes()
        if len(data) != record["bytes"]:
            raise ValueError(f"Wrong byte count: {name}")
        if hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise ValueError(f"Wrong SHA256: {name}")
    print(f"PASS: {len(records)} frozen files match MANIFEST.json")
    print("The manifest is authenticated by the separately verified signed Git commit.")
    print("Files added in subsequent research stages are outside this frozen list.")


if __name__ == "__main__":
    main()
