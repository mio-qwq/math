#!/usr/bin/env python3
"""Replay stage-9 short gates without repeating the long q-class enumeration."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent.parent
PREFIX = "sha256-word-distance/"
COMMANDS = [
    [PREFIX + "support12-base-residual-v9/verify_residual_merge.py"],
    [PREFIX + "support12-d0005-v9/check.py"],
    [PREFIX + "support12-d000f-v9/check.py"],
    [PREFIX + "support12-factor-signature-v9/check.py", "--negative"],
    [PREFIX + "support12-v16-core-batch-v9/check.py"],
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest():
    path = ROOT / "continuation-v9/SHA256.json"
    packet = json.loads(path.read_text())
    seen = set()
    for entry in packet["files"]:
        relative = entry["path"]
        assert relative not in seen, "duplicate stage9 path"
        seen.add(relative)
        target = (ROOT / relative).resolve()
        assert target.is_relative_to(ROOT) and target != path
        raw = target.read_bytes()
        assert len(raw) == entry["bytes"], "stage9 length: " + relative
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"], "stage9 hash: " + relative
    return {"files_checked": len(seen), "sha256": digest(path)}


def prior_integrity():
    path = ROOT / "continuation-v8/replay.py"
    spec = importlib.util.spec_from_file_location("crypto3_stage8", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.check_manifest()


def check_acceptance(root):
    path = root / "continuation-v9/ACCEPTANCE.json"
    packet = json.loads(path.read_text())
    assert packet["status"] == "ACCEPT"
    checked = []
    for entry in packet["artifacts"]:
        target = root / entry["path"]
        assert target.is_file(), entry["path"]
        assert digest(target) == entry["sha256"], entry["path"]
        checked.append(entry["path"])
    assert len(checked) == len(set(checked))
    return {"status": "ACCEPT", "artifacts_checked": len(checked)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--freeze-run", action="store_true")
    parser.add_argument("--manifest-only", action="store_true")
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    if args.record:
        assert not args.record.resolve().is_relative_to(ROOT), "record outside frozen workstream"
    if args.manifest_only:
        print(json.dumps({"status": "PASS", **check_manifest()}, sort_keys=True))
        return

    result = {
        "schema": "crypto3-stage9-isolated-replay-v1",
        "python": sys.version,
        "base_commit": "e2a81b71bcc83ab72f325934c449d27ef198efb3",
        "prior_stage8_integrity": prior_integrity(),
        "stage9_integrity": ({"scope": "first execution before freeze"}
                             if args.freeze_run else check_manifest()),
        "acceptance": check_acceptance(ROOT),
        "long_q_classification_rerun": False,
        "runs": [],
    }
    with tempfile.TemporaryDirectory(prefix="crypto3-stage9-") as temp:
        target = Path(temp) / "CRYPTO3-20261012"
        shutil.copytree(ROOT, target,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "check-subsets"))
        for command in COMMANDS:
            source = target / command[0]
            start = time.monotonic()
            run = subprocess.run([sys.executable, "-B"] + command,
                                 cwd=target, text=True, capture_output=True)
            entry = {
                "argv": ["python", "-B"] + command,
                "exit_code": run.returncode,
                "seconds": time.monotonic() - start,
                "stdout": run.stdout,
                "stderr": run.stderr,
                "checker_sha256": digest(source),
                "stdout_sha256": hashlib.sha256(run.stdout.encode()).hexdigest(),
            }
            result["runs"].append(entry)
            assert source.read_bytes() == (ROOT / command[0]).read_bytes(), "source changed"
            if run.returncode:
                if args.record:
                    args.record.write_text(json.dumps(result, indent=2) + "\n")
                raise RuntimeError("failed " + command[0] + "\n" + run.stdout + run.stderr)
    result["status"] = "PASS"
    if args.record:
        args.record.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "status": "PASS",
        "commands_passed": len(COMMANDS),
        "accepted_artifacts": result["acceptance"]["artifacts_checked"],
        "long_q_classification_rerun": False,
        "seconds": sum(run["seconds"] for run in result["runs"]),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
