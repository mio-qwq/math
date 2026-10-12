#!/usr/bin/env python3
"""Build the corrected support-index-12 joint-factor certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ACTIVE = [10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57]
KINDS = ("d", "F", "G")
VARIABLES = [f"{kind}{i}" for i in ACTIVE for kind in KINDS]
FREE = [
    "d10", "d11", "d13", "d15", "F11", "F13", "G10",
    "G11", "G13", "F15", "G26", "F29", "F42", "F57",
]
PIVOTS = [v for v in VARIABLES if v not in FREE]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def original_rows():
    support = set(ACTIVE)
    rows = []
    for t in range(16, 64):
        coeff = {}

        def add(name, value):
            coeff[name] = coeff.get(name, 0) + value
            if coeff[name] == 0:
                del coeff[name]

        if t in support:
            add(f"d{t}", 1)
        for kind, i in (("G", t - 2), ("d", t - 7),
                        ("F", t - 15), ("d", t - 16)):
            if i in support:
                add(f"{kind}{i}", -1)
        rows.append({"t": t, "coefficients": coeff})
    return rows


def eliminate(nonzero):
    matrix = [[row["coefficients"].get(v, 0) for v in VARIABLES]
              for row in nonzero]
    operations = []
    for cursor, pivot in enumerate(PIVOTS):
        col = VARIABLES.index(pivot)
        candidate = next(
            (i for i in range(cursor, len(matrix)) if abs(matrix[i][col]) == 1),
            None,
        )
        if candidate is None:
            raise RuntimeError(f"no unit pivot for {pivot}")
        if candidate != cursor:
            matrix[cursor], matrix[candidate] = matrix[candidate], matrix[cursor]
            operations.append({"op": "swap", "a": cursor, "b": candidate})
        if matrix[cursor][col] == -1:
            matrix[cursor] = [-x for x in matrix[cursor]]
            operations.append({"op": "negate", "row": cursor})
        for i in range(len(matrix)):
            if i == cursor or matrix[i][col] == 0:
                continue
            multiplier = -matrix[i][col]
            matrix[i] = [
                x + multiplier * y for x, y in zip(matrix[i], matrix[cursor])
            ]
            operations.append({
                "op": "add", "target": i, "source": cursor,
                "multiplier": multiplier,
            })
    reduced = []
    for pivot, row in zip(PIVOTS, matrix):
        reduced.append({
            "pivot": pivot,
            "coefficients": {
                v: row[i] for i, v in enumerate(VARIABLES) if row[i]
            },
        })
    return operations, reduced


def main():
    rows = original_rows()
    nonzero = [row for row in rows if row["coefficients"]]
    operations, reduced = eliminate(nonzero)
    root = HERE.parent
    support_source = root / "supports-v2.json"
    boundary = root / "actual-boundary-v6" / "PROOF.md"
    base_structural = root / "support12-base-lift-v8" / "STRUCTURAL.json"
    payload = {
        "schema": "CRYPTO3-support12-full-factor-v9",
        "modulus": 2**32,
        "support_identifier": 12,
        "support_identifier_is_zero_based": True,
        "active_indices": ACTIVE,
        "target_bindings": {
            "supports_v2": {
                "path": "../supports-v2.json", "array_index": 12,
                "sha256": sha(support_source),
            },
            "accepted_actual_boundary_proof": {
                "path": "../actual-boundary-v6/PROOF.md",
                "sha256": sha(boundary),
            },
            "base_lift_structural": {
                "path": "../support12-base-lift-v8/STRUCTURAL.json",
                "sha256": sha(base_structural),
            },
        },
        "variables": VARIABLES,
        "free_variables": FREE,
        "pivot_variables": PIVOTS,
        "original_rows": rows,
        "nonzero_row_count": len(nonzero),
        "zero_row_count": len(rows) - len(nonzero),
        "integer_unit_row_operations": operations,
        "reduced_rows": reduced,
        "scope": "correct support index 12; independent active pairs only",
    }
    out = HERE / "CERTIFICATE.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS", "support_identifier": 12,
        "rows": 48, "nonzero": len(nonzero), "rank": len(PIVOTS),
        "free_rank": len(FREE), "operations": len(operations),
        "output": str(out),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
