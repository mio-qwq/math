#!/usr/bin/env python3
"""Fresh replay of the ROBReady module and its exact local imports."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", required=True, type=Path)
    parser.add_argument("--proc-self-compat", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    lean = args.lean.resolve()
    output = (args.output or here.parent / "subagents/lean/evidence/rob-ready").resolve()
    output.mkdir(parents=True, exist_ok=True)
    receipt = {
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "runner_sha256": digest(Path(__file__)),
        "mathlib": None,
        "proc_self_compat": args.proc_self_compat,
        "compilations": [],
    }
    with tempfile.TemporaryDirectory(prefix="ilp1-ready-") as tempname:
        temp = Path(tempname)
        env = dict(os.environ, LEAN_PATH=str(temp))
        if args.proc_self_compat:
            compat = temp / "proc_self_compat.so"
            subprocess.run(["cc", "-shared", "-fPIC", "-O2",
                            str(here / "proc_self_compat.c"), "-ldl", "-o", str(compat)],
                           check=True, capture_output=True, text=True)
            env["LD_PRELOAD"] = str(compat)
            receipt["compat_source_sha256"] = digest(here / "proc_self_compat.c")
        version = subprocess.run([str(lean), "--version"], env=env, capture_output=True,
                                 text=True, check=True).stdout.strip()
        if "version 4.34.1," not in version:
            raise RuntimeError(f"Unexpected compiler: {version}")
        receipt["lean_version"] = version
        for name in ("ROBModel", "ROBOperational", "ROBWorkBounds", "ROBReady"):
            source = here / f"{name}.lean"
            started = time.monotonic()
            run = subprocess.run([str(lean), "-o", str(temp / f"{name}.olean"), source.name],
                                 cwd=here, env=env, capture_output=True, text=True, timeout=120)
            log = run.stdout + run.stderr
            (output / f"{name}.log").write_text(log)
            audits = {
                decl: [a.strip() for a in raw.split(",") if a.strip()]
                for decl, raw in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", log)
            }
            audits.update({decl: [] for decl in
                           re.findall(r"'([^']+)' does not depend on any axioms", log)})
            unexpected = sorted({a for values in audits.values() for a in values}
                                - {"propext", "Classical.choice", "Quot.sound"})
            receipt["compilations"].append({
                "source": source.name, "source_sha256": digest(source),
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "exit_code": run.returncode, "axiom_audits": audits,
                "unexpected_axioms": unexpected,
            })
            if run.returncode or unexpected or not audits:
                (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
                raise RuntimeError(f"Failed {source.name}:\n{log}")
            print(f"PASS {source.name}: {len(audits)} audited declarations")
    receipt["completed_utc"] = datetime.now(timezone.utc).isoformat()
    receipt["status"] = "PASS"
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
