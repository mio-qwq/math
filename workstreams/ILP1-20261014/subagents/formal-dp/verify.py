#!/usr/bin/env python3
"""Compile the Bellman/finite-search additions and audit all printed axioms."""
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


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", default=shutil.which("lean"))
    parser.add_argument("--proc-self-compat", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.lean:
        parser.error("--lean must identify the Lean 4.34.1 binary")
    lean = str(Path(args.lean).resolve())
    here = Path(__file__).resolve().parent
    core = here.parents[1] / "formal"
    output = (args.output or here / "evidence").resolve()
    output.mkdir(parents=True, exist_ok=True)
    sources = [core / "ROBModel.lean", core / "ROBOperational.lean",
               here / "ROBBellman.lean", here / "FiniteSearch.lean", here / "BellmanExact.lean"]
    receipt = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "baseline_commit": "d7e2e6eeae34479f9ecd123fcf4471c1c57575d7",
        "runner_sha256": digest(Path(__file__)),
        "mathlib": None,
        "imports": "Lean bundled Std, ROBModel, ROBOperational, ROBBellman",
        "proc_self_compat": args.proc_self_compat,
        "scope": "arbitrary-size operational potential proof; generic list-path exact search; Bellman attainment",
        "excluded": ["Python solver verification", "concrete ROB successor-list completeness"],
        "compilations": [],
    }
    with tempfile.TemporaryDirectory(prefix="ilp1-bellman-") as tmpname:
        tmp = Path(tmpname)
        env = dict(os.environ, LEAN_PATH=str(tmp))
        if args.proc_self_compat:
            source = core / "proc_self_compat.c"
            compat = tmp / "proc_self_compat.so"
            subprocess.run(["cc", "-shared", "-fPIC", "-O2", str(source), "-ldl", "-o", str(compat)],
                           check=True, capture_output=True, text=True)
            env["LD_PRELOAD"] = str(compat)
            receipt["compat_source_sha256"] = digest(source)
        version = subprocess.run([lean, "--version"], env=env,
                                 capture_output=True, text=True, check=True).stdout.strip()
        receipt["lean_version"] = version
        if "version 4.34.1," not in version:
            raise RuntimeError(f"Unpinned compiler: {version}")
        for source in sources:
            started = time.monotonic()
            run = subprocess.run([lean, "-o", str(tmp / f"{source.stem}.olean"), source.name],
                                 cwd=source.parent, env=env, capture_output=True, text=True, timeout=120)
            log = run.stdout + run.stderr
            (output / f"{source.stem}.log").write_text(log)
            audits = {name: [a.strip() for a in axlist.split(",") if a.strip()]
                      for name, axlist in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", log)}
            for name in re.findall(r"'([^']+)' does not depend on any axioms", log):
                audits[name] = []
            unexpected = sorted({a for values in audits.values() for a in values} -
                                {"propext", "Classical.choice", "Quot.sound"})
            receipt["compilations"].append({
                "source": str(source.relative_to(here.parents[1])),
                "sha256": digest(source), "exit_code": run.returncode,
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "axiom_audits": audits, "unexpected_axioms": unexpected,
            })
            if run.returncode or unexpected or not audits:
                (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
                raise RuntimeError(f"Compilation/axiom audit failed: {source.name}\n{log}")
            print(f"PASS {source.name}: {len(audits)} audited declarations")
    receipt["completed_utc"] = datetime.now(timezone.utc).isoformat()
    receipt["status"] = "PASS"
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
