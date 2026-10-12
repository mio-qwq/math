#!/usr/bin/env python3
"""Independent algebraic factorization of all 48 support-12 rows.

This checker deliberately imports no author code and does not solve any
SHA-256 base-message completion problem.  It proves the exact linear
elimination behind the independent-active-pair factor theorem.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MOD = 1 << 32
MASK = MOD - 1
SUPPORT = [10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57]
SUPPORT_SHA256 = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"

VARIABLES = [f"{kind}{i}" for i in SUPPORT for kind in ("d", "F", "G")]
FREE_TO_PARAMETER = {
    "G10": "z10", "G11": "z11", "G13": "z13", "G15": "a",
    "G26": "p", "G28": "s", "F29": "q", "G29": "u",
    "G42": "r", "F43": "c", "G43": "e", "d57": "v",
    "F57": "z57", "G57": "b",
}

# Every variable as an integer linear form in the fourteen free parameters.
# Four z-parameters disappear after boundary projection; the remaining ten
# are the scalar factor-theorem parameters.
FORMS = {
    "d10": {"a": -1}, "F10": {"b": -1}, "G10": {"z10": 1},
    "d11": {"b": 1}, "F11": {"a": 1, "c": -1}, "G11": {"z11": 1},
    "d13": {"e": -1}, "F13": {"p": -1, "q": -1, "r": -1}, "G13": {"z13": 1},
    "d15": {"u": -1}, "F15": {"s": -1}, "G15": {"a": 1},
    "d18": {"b": 1}, "F18": {"c": 1}, "G18": {"e": 1, "b": -1},
    "d20": {"b": -1}, "F20": {"q": 1, "r": 1}, "G20": {"u": 1},
    "d26": {"c": -1}, "F26": {"b": -1}, "G26": {"p": 1},
    "d28": {"q": -1, "r": -1}, "F28": {"b": -1}, "G28": {"s": 1},
    "d29": {"e": -1}, "F29": {"q": 1}, "G29": {"u": 1},
    "d34": {"b": 1}, "F34": {"c": 1}, "G34": {"e": 1, "b": 1},
    "d42": {"c": -1}, "F42": {"v": 1}, "G42": {"r": 1},
    "d43": {"b": -1}, "F43": {"c": 1}, "G43": {"e": 1},
    "d57": {"v": 1}, "F57": {"z57": 1}, "G57": {"b": 1},
}

FULL_FACTOR_NODES = {
    10: ("DF", FORMS["d10"], FORMS["F10"]),
    11: ("DF", FORMS["d11"], FORMS["F11"]),
    13: ("DF", FORMS["d13"], FORMS["F13"]),
    15: ("DFG", FORMS["d15"], FORMS["F15"], FORMS["G15"]),
    18: ("DFG", FORMS["d18"], FORMS["F18"], FORMS["G18"]),
    20: ("DFG", FORMS["d20"], FORMS["F20"], FORMS["G20"]),
    26: ("DFG", FORMS["d26"], FORMS["F26"], FORMS["G26"]),
    28: ("DFG", FORMS["d28"], FORMS["F28"], FORMS["G28"]),
    29: ("DFG", FORMS["d29"], FORMS["F29"], FORMS["G29"]),
    34: ("DFG", FORMS["d34"], FORMS["F34"], FORMS["G34"]),
    42: ("DFG", FORMS["d42"], FORMS["F42"], FORMS["G42"]),
    43: ("DFG", FORMS["d43"], FORMS["F43"], FORMS["G43"]),
    57: ("DG", FORMS["d57"], FORMS["G57"]),
}


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix_multiply(left, right):
    return [[sum(left[i][k] * right[k][j] for k in range(len(right)))
             for j in range(len(right[0]))] for i in range(len(left))]


def original_rows(support):
    index = {name: j for j, name in enumerate(VARIABLES)}
    all_rows = []
    nonzero = []
    for t in range(16, 64):
        row = [0] * len(VARIABLES)
        for kind, j, coefficient in (
            ("d", t, 1), ("G", t - 2, -1), ("d", t - 7, -1),
            ("F", t - 15, -1), ("d", t - 16, -1),
        ):
            if j in support:
                row[index[f"{kind}{j}"]] += coefficient
        all_rows.append(row)
        if any(row):
            nonzero.append((t, row))
    return all_rows, nonzero


def unit_rref(matrix):
    """RREF using only swaps, sign changes and integral row additions."""
    rows = [row[:] for row in matrix]
    m, n = len(rows), len(rows[0])
    transform = [[int(i == j) for j in range(m)] for i in range(m)]
    pivots = []
    operations = []
    pivot_row = 0
    for column in range(n):
        candidate = next((i for i in range(pivot_row, m)
                          if abs(rows[i][column]) == 1), None)
        if candidate is None:
            continue
        if candidate != pivot_row:
            rows[pivot_row], rows[candidate] = rows[candidate], rows[pivot_row]
            transform[pivot_row], transform[candidate] = transform[candidate], transform[pivot_row]
            operations.append(["swap", pivot_row, candidate])
        if rows[pivot_row][column] == -1:
            rows[pivot_row] = [-x for x in rows[pivot_row]]
            transform[pivot_row] = [-x for x in transform[pivot_row]]
            operations.append(["negate", pivot_row])
        require(rows[pivot_row][column] == 1, "nonunit pivot")
        for i in range(m):
            if i == pivot_row or rows[i][column] == 0:
                continue
            coefficient = -rows[i][column]
            rows[i] = [x + coefficient * y for x, y in zip(rows[i], rows[pivot_row])]
            transform[i] = [x + coefficient * y for x, y in zip(transform[i], transform[pivot_row])]
            operations.append(["add", i, pivot_row, coefficient])
        pivots.append(column)
        pivot_row += 1
        if pivot_row == m:
            break
    return rows, transform, pivots, operations


def parameter_matrix(parameter_names):
    return [[FORMS[name].get(parameter, 0) for parameter in parameter_names]
            for name in VARIABLES]


def normalized_form(form):
    return {key: value for key, value in sorted(form.items()) if value}


def form_from_rref(row, free_columns, free_parameters):
    return normalized_form({free_parameters[j]: -row[column]
                            for j, column in enumerate(free_columns)
                            if row[column]})


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def sigma_by_bits(x, which):
    a, b, s = (7, 18, 3) if which == 0 else (17, 19, 10)
    result = 0
    for j in range(32):
        bit = ((x >> ((j + a) % 32)) & 1) ^ ((x >> ((j + b) % 32)) & 1)
        if j + s < 32:
            bit ^= (x >> (j + s)) & 1
        result |= bit << j
    return result


def evaluate_form(form, values):
    return sum(coefficient * values[name] for name, coefficient in form.items()) % MOD


def verify_spec(forms=FORMS, support=SUPPORT):
    require(sorted(support) == support and len(set(support)) == 13, "support coverage")
    support_path = ROOT / "supports-v2.json"
    require(digest(support_path) == SUPPORT_SHA256, "support source changed")
    stored = json.loads(support_path.read_text())["supports"][12]
    require(stored == support, "support index 12 mismatch")

    all_rows, tagged = original_rows(set(support))
    require(len(all_rows) == 48, "not all original rows reconstructed")
    require(len(tagged) == 25, "nonzero-row count")
    zero_times = [t for t, row in zip(range(16, 64), all_rows) if not any(row)]
    require(len(zero_times) == 23, "zero-row count")

    matrix = [row for _, row in tagged]
    reduced, transform, pivots, operations = unit_rref(matrix)
    require(matrix_multiply(transform, matrix) == reduced, "unimodular transform mismatch")
    require(len(pivots) == 25, "row rank")
    require(all(reduced[i][p] == 1 for i, p in enumerate(pivots)), "pivot normalization")
    require(all(reduced[i][p] == 0 for i in range(len(reduced)) for p in pivots if p != pivots[i]),
            "pivot columns not reduced")

    free_columns = [j for j in range(len(VARIABLES)) if j not in pivots]
    free_variables = [VARIABLES[j] for j in free_columns]
    require(set(free_variables) == set(FREE_TO_PARAMETER), "unexpected free coordinates")
    free_parameters = [FREE_TO_PARAMETER[name] for name in free_variables]
    require(len(set(free_parameters)) == 14, "parameter collision")

    for row_number, pivot_column in enumerate(pivots):
        derived = form_from_rref(reduced[row_number], free_columns, free_parameters)
        require(derived == normalized_form(forms[VARIABLES[pivot_column]]),
                "wrong pivot formula for " + VARIABLES[pivot_column])
    for variable in free_variables:
        require(normalized_form(forms[variable]) == {FREE_TO_PARAMETER[variable]: 1},
                "wrong free formula for " + variable)

    basis = parameter_matrix(free_parameters)
    require(matrix_multiply(matrix, basis) == [[0] * 14 for _ in matrix], "A*B != 0")
    projection = [[basis[column][j] for j in range(14)] for column in free_columns]
    require(projection == [[int(i == j) for j in range(14)] for i in range(14)],
            "free-coordinate projection not identity")

    # The factor graph is the fourteen-coordinate parameterization after the
    # four boundary-only coordinates are existentially projected away.
    require(set(FULL_FACTOR_NODES) == set(support), "factor-node coverage")
    require([FULL_FACTOR_NODES[i][0] for i in support].count("DFG") == 9, "full-node count")
    require([FULL_FACTOR_NODES[i][0] for i in support].count("DF") == 3, "DF-node count")
    require([FULL_FACTOR_NODES[i][0] for i in support].count("DG") == 1, "DG-node count")
    used = set()
    for node in FULL_FACTOR_NODES.values():
        for form in node[1:]:
            used.update(form)
    require(used == {"a", "b", "c", "e", "p", "q", "r", "s", "u", "v"},
            "projected graph parameters")
    active_conditions = ["a", "b", "c", "e", "u", "q+r", "v"]

    test_words = [0, 1, MASK, 0x12345678, 0x89ABCDEF, 0x80000000, 0x00010001]
    require(all(sigma0(x) == sigma_by_bits(x, 0) for x in test_words), "sigma0 definition mismatch")
    require(all(sigma1(x) == sigma_by_bits(x, 1) for x in test_words), "sigma1 definition mismatch")

    # Deterministic modular evaluation samples exercise signs and wraparound.
    for seed in (0, 1, 0x12345678, MASK):
        values = {name: (seed * 0x9E3779B1 + (j + 1) * 0x6A09E667) & MASK
                  for j, name in enumerate(free_parameters)}
        vector = [evaluate_form(forms[name], values) for name in VARIABLES]
        require(all(sum(coefficient * value for coefficient, value in zip(row, vector)) % MOD == 0
                    for row in matrix), "modular parameter sample violates a row")

    return {
        "schema": "CRYPTO3-support12-full-factor-independent-v8",
        "status": "PASS",
        "support": support,
        "source_support_sha256": SUPPORT_SHA256,
        "original_rows": 48,
        "nonzero_rows": [t for t, _ in tagged],
        "zero_rows": zero_times,
        "variables": len(VARIABLES),
        "rank_by_unit_pivots": len(pivots),
        "free_coordinates": free_variables,
        "free_parameters": free_parameters,
        "unit_row_operations": len(operations),
        "max_abs_transform_entry": max(abs(x) for row in transform for x in row),
        "factor_graph": {str(i): {"predicate": node[0], "forms": node[1:]}
                         for i, node in FULL_FACTOR_NODES.items()},
        "projected_scalar_parameters": ["a", "b", "c", "e", "p", "q", "r", "s", "u", "v"],
        "active_nonzero_conditions": active_conditions,
        "logical_scope": "necessary and sufficient for thirteen independent actual-word pairs; no cross-index base-message completion",
        "sigma_definition_samples": len(test_words),
        "modular_parameter_samples": 4,
    }


def negative_controls():
    results = []
    controls = []

    damaged = copy.deepcopy(FORMS)
    damaged["G34"]["b"] = -1
    controls.append(("flip_G34_b_sign", damaged, SUPPORT))

    damaged = copy.deepcopy(FORMS)
    damaged["F13"].pop("r")
    controls.append(("omit_F13_r_term", damaged, SUPPORT))

    damaged_support = SUPPORT[:-1]
    controls.append(("omit_active_57", FORMS, damaged_support))

    for name, forms, support in controls:
        try:
            verify_spec(forms=forms, support=support)
        except (ValueError, KeyError) as error:
            results.append({"name": name, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("negative control accepted: " + name)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = verify_spec()
    if args.negative:
        report["negative_controls"] = negative_controls()
    report["checker_sha256"] = digest(Path(__file__).resolve())
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
