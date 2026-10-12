#!/usr/bin/env python3
"""Replay accepted stage-8 results and preserve rejected/stopped boundaries."""
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
    [PREFIX + "support12-full-factor-review-v8/replay_readonly.py"],
    [PREFIX + "support12-base-review-v8/replay_readonly.py"],
    [PREFIX + "support12-image-v8/check.py", "--negative"],
    [PREFIX + "support12-image-review-v8/check_independent.py", "--negative"],
]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest():
    path = ROOT / "continuation-v8/SHA256.json"
    packet = json.loads(path.read_text())
    seen = set()
    for entry in packet["files"]:
        relative = entry["path"]
        assert relative not in seen, "duplicate stage8 path"
        seen.add(relative)
        target = (ROOT / relative).resolve()
        assert target.is_relative_to(ROOT) and target != path
        raw = target.read_bytes()
        assert len(raw) == entry["bytes"], "stage8 length: " + relative
        assert hashlib.sha256(raw).hexdigest() == entry["sha256"], "stage8 hash: " + relative
    return {"files_checked": len(seen), "sha256": digest(path)}


def prior_integrity():
    path = ROOT / "continuation-v7/replay.py"
    spec = importlib.util.spec_from_file_location("crypto3_stage7", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {"stages4_to_6": module.prior_integrity(), "stage7": module.check_manifest()}


def check_stopped_probe(root):
    directory = root / (PREFIX + "support12-full-probe-v8")
    manifest_path = directory / "SHA256.json"
    manifest = json.loads(manifest_path.read_text())
    for entry in manifest["files"]:
        relative = entry["path"]
        target = directory / relative
        assert len(target.read_bytes()) == entry["bytes"], "probe length: " + relative
        assert digest(target) == entry["sha256"], "probe hash: " + relative
    result = json.loads((directory / "run-01/RESULT.json").read_text())
    receipt = json.loads((directory / "RECEIPT.json").read_text())
    assert result["result"] == "unknown" and result["reason_unknown"] == "timeout"
    assert result["solver_checks"] == 1 and result["timeout_ms"] == 30000
    assert result["base_schedule_constraints"] is False and "model" not in result
    assert receipt["status"] == "STOPPED_UNKNOWN"
    assert receipt["sat_model_obtained"] is False
    assert receipt["unsat_certificate_obtained"] is False
    assert receipt["model_verifier_executed"] is False
    assert receipt["stopping_rule"].startswith("UNKNOWN ends this mechanism")
    assert digest(directory / "run-01/MODEL.smt2") == result["smt2_sha256"]
    return {
        "status": "STOPPED_UNKNOWN",
        "reason": "timeout",
        "solver_checks": 1,
        "solver_rerun": False,
        "manifest_sha256": digest(manifest_path),
    }


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

    integrity = {"scope": "first execution before freeze"} if args.freeze_run else check_manifest()
    result = {
        "schema": "crypto3-stage8-isolated-replay-v1",
        "python": sys.version,
        "base_commit": "22c0853b24e3f7cbcb43738a8b4fc2170fa60ce6",
        "prior_frozen_integrity": prior_integrity(),
        "stage8_integrity": integrity,
        "stopped_probe": check_stopped_probe(ROOT),
        "runs": [],
    }
    with tempfile.TemporaryDirectory(prefix="crypto3-stage8-") as temp:
        target = Path(temp) / "CRYPTO3-20261012"
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "check-subsets"))
        for command in COMMANDS:
            source = target / command[0]
            start = time.monotonic()
            run = subprocess.run(
                [sys.executable, "-B"] + command,
                cwd=target,
                text=True,
                capture_output=True,
            )
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
            assert source.read_bytes() == (ROOT / command[0]).read_bytes(), "source changed during replay"
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
        "factor_review": "v8 REJECT; v9 ACCEPT",
        "stopped_probe_rerun": False,
        "older_large_enumerations_rerun": False,
        "seconds": sum(r["seconds"] for r in result["runs"]),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
