#!/usr/bin/env python3
"""Small F2 consequence check for the 132 necessary input masks."""

import hashlib
import json
import time
from collections import Counter
from pathlib import Path

from mask_probe import K, f

HERE = Path(__file__).resolve().parent


def solve(a):
    b, ell = f(a), f(K)
    equations = []
    for i in range(31):
        if (a & K) >> i & 1:
            rhs = ((a ^ K) >> (i+1)) & 1
            equations.append((1 << i, rhs, {"kind": "z", "bit": i, "rhs": rhs}))
        if (b & ell) >> i & 1:
            coeff = sum(((f(1 << j) >> i) & 1) << j for j in range(32))
            rhs = 1 ^ (((b ^ ell) >> (i+1)) & 1)
            equations.append((coeff, rhs, {"kind": "f(z)", "bit": i, "rhs": rhs}))
    pivot = {}
    for i, (coefficient, rhs, _) in enumerate(equations):
        proof = 1 << i
        while coefficient:
            j = coefficient.bit_length()-1
            if j not in pivot:
                pivot[j] = (coefficient, rhs, proof)
                break
            other, bit, other_proof = pivot[j]
            coefficient ^= other
            rhs ^= bit
            proof ^= other_proof
        if not coefficient and rhs:
            chosen = [j for j in range(len(equations)) if proof >> j & 1]
            check_row = check_rhs = 0
            for j in chosen:
                check_row ^= equations[j][0]
                check_rhs ^= equations[j][1]
            assert check_row == 0 and check_rhs == 1
            return {"mask": f"{a:08x}", "status": "inconsistent",
                    "contradiction": [equations[j][2] for j in chosen]}
    return {"mask": f"{a:08x}", "status": "consistent", "rank": len(pivot),
            "equations": len(equations)}


def main():
    start = time.monotonic()
    path = HERE / "MASK_PROBE.json"
    first = json.loads(path.read_text())
    masks = [int(v, 16) for v in first["survivors_if_at_most_256"]]
    assert len(masks) == 132
    cases = [solve(a) for a in masks]
    remaining = [row["mask"] for row in cases if row["status"] == "consistent"]
    signatures = Counter()
    for case in cases:
        if case["status"] == "inconsistent":
            signature = tuple((eq["kind"], eq["bit"]) for eq in case["contradiction"])
            signatures[signature] += 1
    result = {"schema": "CRYPTO3-coupled-short-adjacent-probe-v1",
              "mechanism": "linear consequences of adjacent carry parity for the two derivative equations",
              "source_probe_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
              "masks_checked": len(masks), "rejected": len(masks)-len(remaining),
              "remaining_masks": remaining,
              "contradiction_signatures": [{"rows": list(key), "count": value}
                                           for key, value in signatures.most_common()],
              "cases": cases, "seconds": time.monotonic()-start,
              "scope": "Necessary mask/linear relaxation only; no h-fibre premise or full coupled nonexistence claim."}
    (HERE / "ADJACENT_PROBE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "cases"}, indent=2))


if __name__ == "__main__":
    main()
