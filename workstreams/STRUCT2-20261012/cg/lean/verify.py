#!/usr/bin/env python3
"""Compile the finite original-graph Lean proof and preserve the actual audit."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


THEOREMS = [
    "fast_source_exact", "cdc_adjacency_is_original",
    "original_edge_count", "original_loopless", "original_symmetric",
    "cdc_loopless", "cdc_symmetric", "next_complete", "next_distinct",
    "cdc_cubic", "indexed_iff_actual", "indexed_six_cycle_classification",
    "actual_six_cycle_iff_not_centre", "deck_strong",
    "companion_guide_strong", "reflection_guide_strong",
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lean", type=Path, required=True)
    parser.add_argument("--adapter", type=Path)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()
    directory = Path(__file__).resolve().parent
    source = directory / "Cg3.lean"
    compiler = args.lean.resolve()
    environment = os.environ.copy()
    if args.adapter:
        adapter = args.adapter.resolve()
        environment["STRUCT2_LEAN_BIN"] = str(compiler)
        environment["LD_PRELOAD"] = str(adapter)
    version = subprocess.run(
        [str(compiler), "--version"], env=environment,
        text=True, capture_output=True, check=True,
    ).stdout.strip()
    assert "version 4.34.1," in version, version
    assert "5045d0056413266e57c625dcd7c365b10e377c52" in version, version
    source_text = source.read_text()
    code_without_comments = re.sub(r"/-.*?-/", "", source_text, flags=re.S)
    code_without_comments = re.sub(r"--[^\n]*", "", code_without_comments)
    assert not re.search(r"\b(sorry|admit|native_decide|axiom)\b", code_without_comments)
    command = [
        str(compiler), "-j1", "--profile", "-o", "Cg3.olean", "Cg3.lean",
    ]
    start = time.perf_counter()
    completed = subprocess.run(
        command, cwd=directory, env=environment,
        text=True, capture_output=True, timeout=args.timeout,
    )
    elapsed = time.perf_counter() - start
    transcript = (
        "VERSION\n" + version + "\n\nCOMMAND\n" + " ".join(command)
        + "\n\nSTDOUT\n" + completed.stdout
        + "\nSTDERR\n" + completed.stderr
        + "\nEXIT CODE\n" + str(completed.returncode) + "\n"
    )
    (directory / "compile.log").write_text(transcript)
    audits = {}
    for name in THEOREMS:
        full_name = "Struct2.Cg3." + name
        lines = [line for line in completed.stdout.splitlines() if line.startswith("'" + full_name + "'")]
        assert len(lines) == 1, (full_name, lines)
        line = lines[0]
        if "does not depend on any axioms" in line:
            axioms = []
        else:
            match = re.search(r"depends on axioms: \[(.*)\]", line)
            assert match, line
            axioms = [item.strip() for item in match.group(1).split(",") if item.strip()]
        audits[full_name] = axioms
    axiom_union = sorted({axiom for values in audits.values() for axiom in values})
    acceptable_axioms = {"propext", "Quot.sound", "Classical.choice"}
    report = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "lean_version": version,
        "compiler_sha256": digest(compiler),
        "source_sha256": digest(source),
        "verification_script_sha256": digest(__file__),
        "adapter_used": bool(args.adapter),
        "adapter_binary_sha256": digest(args.adapter) if args.adapter else None,
        "adapter_source_sha256": digest(directory / "runtime_path.c") if args.adapter else None,
        "command": command,
        "exit_code": completed.returncode,
        "seconds": round(elapsed, 6),
        "axioms": audits,
        "axiom_union": axiom_union,
        "native_decide_used": False,
        "custom_axioms_used": False,
        "mathlib_used": False,
        "scope": "n=3: original adjacency, cubic CDC, actual six-cycle centre classification, three explicit strong guides; no all-n group classification.",
        "success": completed.returncode == 0 and set(axiom_union) <= acceptable_axioms,
        "compile_log_sha256": digest(directory / "compile.log"),
        "olean_sha256": digest(directory / "Cg3.olean") if (directory / "Cg3.olean").exists() else None,
    }
    (directory / "verification.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(transcript)
    print("VERIFICATION", json.dumps({
        "success": report["success"], "seconds": report["seconds"],
        "axiom_union": axiom_union, "source_sha256": report["source_sha256"],
    }))
    assert report["success"]


if __name__ == "__main__":
    main()
