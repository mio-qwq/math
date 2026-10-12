#!/usr/bin/env python3
"""Check the listed immutable release bytes using only the standard library."""
import hashlib
import json
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    data = json.loads((root / "SHA256.json").read_text())
    assert data["schema"] == "crypto3-release-sha256-v1"
    assert data["manifest_self_hash"] is False
    names = set()
    for item in data["files"]:
        name = item["path"]
        assert name not in names, "duplicate manifest path"
        names.add(name)
        path = (root / name).resolve()
        assert path.is_relative_to(root), "path outside release"
        assert path != root / "SHA256.json", "manifest cannot hash itself"
        raw = path.read_bytes()
        assert len(raw) == item["bytes"], "wrong size: " + name
        assert hashlib.sha256(raw).hexdigest() == item["sha256"], "wrong hash: " + name
    print(json.dumps({"status": "PASS", "files_checked": len(names),
                      "manifest_sha256": hashlib.sha256((root / "SHA256.json").read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
