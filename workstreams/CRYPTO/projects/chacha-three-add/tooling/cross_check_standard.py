#!/usr/bin/env python3
"""Compare separately generated exact 32-bit outputs; do not recompute them."""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    project = Path(__file__).resolve().parent.parent
    root_path = project / "tooling/results/dp_all_bits.json"
    independent_path = project / "verification/general_standard32_exact.json"
    independent_run = project / "verification/general_independent_run.json"
    root = json.loads(root_path.read_text())
    independent = json.loads(independent_path.read_text())
    run = json.loads(independent_run.read_text())
    assert root["status"] == "completed" and run["status"] == "pass"
    assert root["source_sha256"] == sha(project / "tooling/exact_dp.py")
    assert run["standard_values_sha256"] == sha(independent_path)
    assert (independent["n"], independent["r"], independent["q"]) == (32, 16, 12)
    rows = []
    for model in root["standard_table"]:
        a = model["fixed_a"]
        if a == "0x0":
            # The blind standard table did not include a=0. Do not silently
            # label this model independently matched by the present check.
            continue
        expected = independent["uniform_a"] if a is None else independent["fixed_a"][a]
        assert len(model["rows"]) == len(expected) == 32
        for i, (left, right) in enumerate(zip(model["rows"], expected)):
            assert left["output_bit"] == i
            value = Fraction(left["correlation"])
            assert value == Fraction(right["fraction"]), (a, i, left, right)
            rows.append({"fixed_a": a, "i": i, "correlation": str(value), "equal": True})
    assert len(rows) == 160
    result = {
        "status": "pass",
        "utc": datetime.now(timezone.utc).isoformat(),
        "command": [sys.executable, *sys.argv],
        "source_sha256": sha(Path(__file__)),
        "comparison_count": len(rows),
        "method": "Fraction comparison of two separately implemented exact DP outputs",
        "independence_limit": "implementations share a supplied mathematical specification; verification also checks original-word enumeration",
        "unmatched_root_models": ["fixed_a=0 is absent from the independent standard table"],
        "inputs": [{"path": str(p.relative_to(project)), "sha256": sha(p)}
                   for p in (root_path, independent_path, independent_run)],
        "rows": rows,
    }
    output = project / "tooling/results/standard_comparison.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "pass", "comparison_count": len(rows), "output": str(output)}))


if __name__ == "__main__":
    main()
