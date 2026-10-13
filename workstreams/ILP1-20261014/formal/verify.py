#!/usr/bin/env python3
"""Compile the pinned Std-only development and reject nonstandard axioms."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", default=shutil.which("lean"))
    parser.add_argument("--proc-self-compat", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.lean:
        parser.error("supply --lean /absolute/path/to/lean-4.34.1/bin/lean")
    lean = str(Path(args.lean).resolve())
    here = Path(__file__).resolve().parent
    output = (args.output or here.parent / "subagents/lean/evidence").resolve()
    output.mkdir(parents=True, exist_ok=True)
    sources = [here / "ROBModel.lean", here / "ROBOperational.lean"]
    for extra in ("OnlinePair.lean", "ExactEnumeration.lean", "ResourceBounds.lean"):
        if (here / extra).exists():
            sources.append(here / extra)
    receipt = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "mathlib": None,
        "imports": "Lean 4.34.1 bundled Std and preceding local modules only",
        "runner_sha256": sha256(Path(__file__)),
        "proc_self_compat": args.proc_self_compat,
        "compilations": [],
    }
    with tempfile.TemporaryDirectory(prefix="ilp1-lean-") as tmpname:
        tmp = Path(tmpname)
        env = dict(os.environ)
        env["LEAN_PATH"] = str(tmp)
        if args.proc_self_compat:
            compat = tmp / "proc_self_compat.so"
            subprocess.run(
                ["cc", "-shared", "-fPIC", "-O2", str(here / "proc_self_compat.c"),
                 "-ldl", "-o", str(compat)], check=True, capture_output=True, text=True
            )
            env["LD_PRELOAD"] = str(compat)
            receipt["compat_source_sha256"] = sha256(here / "proc_self_compat.c")
        version = subprocess.run([lean, "--version"], env=env,
                                 capture_output=True, text=True, check=True).stdout.strip()
        receipt["lean_version"] = version
        if "version 4.34.1," not in version:
            raise RuntimeError(f"Wrong Lean compiler: {version}")
        for source in sources:
            started = time.monotonic()
            run = subprocess.run(
                [lean, "-o", str(tmp / f"{source.stem}.olean"), source.name],
                cwd=here, env=env, capture_output=True, text=True, timeout=120
            )
            log = run.stdout + run.stderr
            (output / f"{source.stem}.log").write_text(log)
            audits = {}
            for name, axlist in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", log):
                audits[name] = [a.strip() for a in axlist.split(",") if a.strip()]
            for name in re.findall(r"'([^']+)' does not depend on any axioms", log):
                audits[name] = []
            allowed = {"propext", "Classical.choice", "Quot.sound"}
            bad = sorted({a for values in audits.values() for a in values} - allowed)
            item = {
                "source": source.name, "source_sha256": sha256(source),
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "exit_code": run.returncode, "axiom_audits": audits,
                "unexpected_axioms": bad,
            }
            receipt["compilations"].append(item)
            if run.returncode or bad or not audits:
                (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
                raise RuntimeError(f"Verification failed for {source.name}:\n{log}")
            print(f"PASS {source.name}: {len(audits)} audited declarations")
    receipt["completed_utc"] = datetime.now(timezone.utc).isoformat()
    receipt["status"] = "PASS"
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
