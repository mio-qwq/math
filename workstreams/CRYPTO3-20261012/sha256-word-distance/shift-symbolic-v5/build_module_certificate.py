#!/usr/bin/env python3
"""Finite exact unit elimination for two possible inverse boundaries."""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED_SUPPORT_HASH = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
MOD = 1 << 32


def source_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def original_rows(support):
    variables = [(name, i) for name in ("d", "F", "G") for i in support]
    lookup = {variable: j for j, variable in enumerate(variables)}
    rows = []
    for t in range(16, 64):
        row = [0] * len(variables)
        for name, index, coefficient in [("d", t, 1), ("G", t-2, -1),
                                          ("d", t-7, -1), ("F", t-15, -1),
                                          ("d", t-16, -1)]:
            if index in support:
                row[lookup[name, index]] += coefficient
        rows.append(row)
    return variables, rows


def eliminate(rows):
    matrix = [row[:] for row in rows]
    transform = [[int(i == j) for j in range(len(rows))] for i in range(len(rows))]
    operations, pivots = [], []
    rank = 0
    for column in range(len(rows[0])):
        unit = next((r for r in range(rank, len(matrix)) if matrix[r][column] in (1, -1)), None)
        if unit is None:
            continue
        if unit != rank:
            matrix[rank], matrix[unit] = matrix[unit], matrix[rank]
            transform[rank], transform[unit] = transform[unit], transform[rank]
            operations.append(["swap", rank, unit])
        if matrix[rank][column] == -1:
            matrix[rank] = [-x for x in matrix[rank]]
            transform[rank] = [-x for x in transform[rank]]
            operations.append(["negate", rank])
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = -matrix[row][column]
            matrix[row] = [a + factor*b for a,b in zip(matrix[row], matrix[rank])]
            transform[row] = [a + factor*b for a,b in zip(transform[row], transform[rank])]
            operations.append(["add", row, rank, factor])
        pivots.append(column)
        rank += 1
        if rank == len(matrix):
            break
    assert all(not any(row) for row in matrix[rank:])
    return matrix, transform, operations, pivots


def one_certificate(sid, support):
    variables, rows = original_rows(support)
    matrix, transform, operations, pivots = eliminate(rows)
    lookup = {variable: i for i,variable in enumerate(variables)}
    target = [0] * len(variables)
    target[lookup["d",15]] = 1
    target[lookup[("d",8) if sid == 9 else ("G",13)]] = -1
    residual = target[:]
    combination = [0] * len(rows)
    for row,pivot in enumerate(pivots):
        factor = residual[pivot]
        residual = [a-factor*b for a,b in zip(residual,matrix[row])]
        combination = [a+factor*b for a,b in zip(combination,transform[row])]
    free = [i for i in range(len(variables)) if i not in pivots]
    # This is one exact witness, not sampling evidence for a universal claim.
    witness = [0] * len(variables)
    for exponent,column in enumerate(free):
        witness[column] = 3 ** exponent
    for row,pivot in enumerate(pivots):
        witness[pivot] = -sum(matrix[row][j]*witness[j] for j in free)
    assert all(x % MOD != 0 for x in witness)
    assert all(sum(a*b for a,b in zip(row,witness)) == 0 for row in rows)
    boundary_integer = sum(a*b for a,b in zip(target,witness))
    assert boundary_integer % MOD != 0
    return {
        "support_index": sid,
        "support": support,
        "variables": [list(variable) for variable in variables],
        "original_rows": rows,
        "original_recurrence_indices": list(range(16,64)),
        "unit_row_operations": operations,
        "transformed_rows": matrix,
        "integer_row_transform": transform,
        "pivot_columns": pivots,
        "integer_rank": len(pivots),
        "free_columns": free,
        "boundary_target": target,
        "target_minus_residual_original_row_combination": combination,
        "reduced_boundary_residual": residual,
        "boundary_residual_terms": [[*variables[j], c] for j,c in enumerate(residual) if c],
        "witness_integer_values": witness,
        "witness_mod32_values": [x % MOD for x in witness],
        "witness_boundary_integer": boundary_integer,
        "witness_boundary_mod32": boundary_integer % MOD,
        "witness_all_active_d_F_G_nonzero": True,
        "countermodel_scope": "all 48 additive difference rows and necessary active d/F/G nonzero; actual f/g word-pair realizability NOT asserted",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    path = ROOT / "supports-v2.json"
    assert source_hash(path) == EXPECTED_SUPPORT_HASH
    supports = json.loads(path.read_text())["supports"]
    data = {
        "schema": "crypto3-backward-boundary-linear-module-v5",
        "source_support_sha256": source_hash(path),
        "generator_sha256": source_hash(Path(__file__).resolve()),
        "modulus": MOD,
        "objects": [one_certificate(sid,supports[sid]) for sid in (9,12)],
        "claim": "Neither boundary target belongs to the row module generated by all 48 original additive difference recurrences over integers or Z/(2^32).",
        "unclaimed": "No counterexample to true-schedule inverse reductions; real sigma derivative coupling is retained as an unresolved lifting condition.",
    }
    rendered = json.dumps(data,indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered,end="")


if __name__ == "__main__":
    main()
