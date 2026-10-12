#!/usr/bin/env python3
"""Invoke the frozen ten-state check functions explicitly, with negative controls.

The inherited verify_ten.py defines checks but has no executable entry point.
Running that file directly therefore exits zero without checking anything.
This wrapper leaves the authenticated frozen file unchanged.
"""
from __future__ import annotations
import copy
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "stage2"))
import verify_ten


def main():
    path = ROOT / "stage2" / "certificate.json"
    data = json.loads(path.read_text())
    report = {
        "scope": "Definition-level ten-state semantic replay; universal theorem uses its written proof",
        "frozen_certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "target": verify_ten.check(data["ten_target"]),
        "examples": verify_ten.finite_examples(data["jiggs"]),
        "negative_controls": [],
        "inherited_direct_command": "verify_ten.py has no __main__ entry point and does not execute checks",
    }
    for name in ("profiles", "pair_types", "letter_types", "allowed", "marked"):
        damaged = copy.deepcopy(data["ten_target"])
        if name in ("allowed", "marked"):
            damaged[name][0][0] ^= 1
        else:
            damaged[name][0][0] += 1
        try:
            verify_ten.check(damaged)
        except ValueError as error:
            report["negative_controls"].append({"field": name, "rejected": True, "reason": str(error)})
        else:
            raise RuntimeError(f"Damaged {name} certificate accepted")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
