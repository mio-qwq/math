#!/usr/bin/env python3
"""Build the exact support-12 independent-active-pair factor certificate."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path

ACTIVE = [10, 11, 15, 18, 20, 26, 27, 28, 29, 34, 42, 43, 57]
KINDS = ("d", "F", "G")
VARIABLES = [f"{kind}{i}" for i in ACTIVE for kind in KINDS]
FREE = [
    "d10", "d11", "d15", "F11", "G10", "G11", "F15",
    "G18", "G26", "F27", "G27", "F29", "F42", "F57",
]
PIVOTS = [v for v in VARIABLES if v not in FREE]


def original_rows():
    rows = []
    support = set(ACTIVE)
    for t in range(16, 64):
        coeff = {}

        def add(name, value):
            coeff[name] = coeff.get(name, 0) + value

        if t in support:
            add(f"d{t}", 1)
        for kind, i in (("G", t - 2), ("d", t - 7),
                        ("F", t - 15), ("d", t - 16)):
            if i in support:
                add(f"{kind}{i}", -1)
        coeff = {k: v for k, v in coeff.items() if v}
        rows.append({"t": t, "coefficients": coeff})
    return rows


def dense(coeff):
    return [coeff.get(v, 0) for v in VARIABLES]


def eliminate(nonzero_rows):
    matrix = [dense(row["coefficients"]) for row in nonzero_rows]
    labels = [row["t"] for row in nonzero_rows]
    operations = []
    cursor = 0
    for pivot_name in PIVOTS:
        col = VARIABLES.index(pivot_name)
        candidate = next(
            (i for i in range(cursor, len(matrix)) if abs(matrix[i][col]) == 1),
            None,
        )
        if candidate is None:
            raise RuntimeError(f"no unit pivot for {pivot_name}")
        if candidate != cursor:
            matrix[cursor], matrix[candidate] = matrix[candidate], matrix[cursor]
            labels[cursor], labels[candidate] = labels[candidate], labels[cursor]
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
        cursor += 1
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
    factors = {}
    for i in ACTIVE:
        factors[str(i)] = {
            kind: next(
                row["coefficients"] for row in reduced
                if row["pivot"] == f"{kind}{i}"
            ) if f"{kind}{i}" in PIVOTS else {f"{kind}{i}": 1}
            for kind in KINDS
        }
    source = Path(__file__).parents[1] / "supports-v2.json"
    payload = {
        "schema": "CRYPTO3-support12-full-factor-v8",
        "modulus": 2**32,
        "support_index": 12,
        "support_source": {
            "path": "../supports-v2.json",
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        },
        "active_indices": ACTIVE,
        "variables": VARIABLES,
        "free_variables": FREE,
        "pivot_variables": PIVOTS,
        "original_rows": rows,
        "nonzero_row_count": len(nonzero),
        "zero_row_count": len(rows) - len(nonzero),
        "integer_unit_row_operations": operations,
        "reduced_rows": reduced,
        "factor_records": factors,
        "scope": "independent active pairs; no base schedule completion",
    }
    out = Path(__file__).with_name("CERTIFICATE.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS", "rows": len(rows), "nonzero": len(nonzero),
        "rank": len(PIVOTS), "free_rank": len(FREE),
        "operations": len(operations), "output": str(out),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
