#!/usr/bin/env python3
"""Verify a CRYPTO snapshot against the worktree or an explicit Git revision.

This checks evidence integrity only. It does not rerun mathematical experiments
or turn their finite checks into a proof or an originality certification.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--ref", help="Read recorded files at this explicit Git revision")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    manifest = json.loads(args.snapshot.read_text())
    revision = None
    if args.ref:
        revision = subprocess.check_output(
            ["git", "rev-parse", "--verify", args.ref + "^{commit}"],
            cwd=root, text=True,
        ).strip()
    failures = []
    seen = set()
    for entry in manifest["files"]:
        name = entry["path"]
        path = PurePosixPath(name)
        if (not name.startswith("workstreams/CRYPTO/") or path.is_absolute()
                or ".." in path.parts or name in seen):
            failures.append({"path": name, "error": "unsafe or duplicate manifest path"})
            continue
        seen.add(name)
        try:
            data = (subprocess.check_output(["git", "show", revision + ":" + name], cwd=root)
                    if revision else (root / name).read_bytes())
            actual = hashlib.sha256(data).hexdigest()
            if actual != entry["sha256"] or len(data) != entry["bytes"]:
                failures.append({"path": name, "error": "hash or byte length mismatch",
                                 "actual_sha256": actual, "actual_bytes": len(data)})
        except (OSError, subprocess.CalledProcessError) as error:
            failures.append({"path": name, "error": str(error)})
    print(json.dumps({
        "status": "passed" if not failures else "failed",
        "snapshot": str(args.snapshot.resolve()),
        "revision": revision or "worktree",
        "files_checked": len(seen),
        "failures": failures,
        "scope": "byte and SHA-256 integrity; not a new mathematical or novelty review",
    }, indent=2))
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
