#!/usr/bin/env python3
"""Independent exact-integer and mod-2**32 review; never imports author code.

Without --save this is read only. Optional output is confined to this directory.
"""
import argparse
import copy
import hashlib
import json
import platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
AUTHOR = BASE / "shift-symbolic-v5"
SUPPORTS = BASE / "shift-reduction-v3" / "supports-v2.json"
SUPPORT_HASH = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
AUTHOR_MANIFEST_HASH = "ae65d615bb115c5ccd9ca8ef20fcd9665df7059243a4ad404c4b656622fdf9d1"
N = 1 << 32


def digest(data):
    return hashlib.sha256(data).hexdigest()


def original_matrix(support):
    variables = [(kind, i) for kind in ("d", "F", "G") for i in support]
    columns = {key: j for j, key in enumerate(variables)}
    rows = []
    for t in range(16, 64):
        row = [0] * len(variables)
        for kind, i, coefficient in (("d", t, 1), ("G", t-2, -1),
                                      ("d", t-7, -1), ("F", t-15, -1),
                                      ("d", t-16, -1)):
            if (kind, i) in columns:
                row[columns[kind, i]] += coefficient
        rows.append(row)
    return variables, columns, rows


def expression(columns, terms):
    vector = [0] * len(columns)
    for kind, i, coefficient in terms:
        vector[columns[kind, i]] += coefficient
    return vector


def apply_operation(matrix, operation, inverse=False):
    assert isinstance(operation, list) and operation
    opcode = operation[0]
    assert opcode in ("swap", "negate", "add")
    expected = {"swap": 3, "negate": 2, "add": 4}[opcode]
    assert len(operation) == expected
    assert all(type(x) is int for x in operation[1:])
    indices = operation[1:2] if opcode == "negate" else operation[1:3]
    assert all(0 <= i < 48 for i in indices)
    if opcode == "swap":
        i, j = indices
        assert i != j
        matrix[i], matrix[j] = matrix[j], matrix[i]
    elif opcode == "negate":
        i = indices[0]
        matrix[i] = [-x for x in matrix[i]]
    else:
        i, j = indices
        assert i != j  # Adding to itself need not be an invertible unit operation.
        coefficient = operation[3] * (-1 if inverse else 1)
        matrix[i] = [a + coefficient*b for a, b in zip(matrix[i], matrix[j])]


def product(left, right):
    columns = list(zip(*right))
    return [[sum(a*b for a, b in zip(row, col)) for col in columns] for row in left]


def dot(a, b):
    assert len(a) == len(b)
    return sum(x*y for x, y in zip(a, b))


def inspect(obj, supports):
    sid = obj["support_index"]
    assert sid in (9, 12)
    support = supports[sid]
    assert obj["support"] == support and len(support) == 13
    variables, columns, A = original_matrix(support)
    assert obj["variables"] == [list(v) for v in variables]
    assert obj["original_recurrence_indices"] == list(range(16, 64))
    assert obj["original_rows"] == A
    assert len(A) == 48 and all(len(row) == 39 for row in A)
    I = [[int(i == j) for j in range(48)] for i in range(48)]
    B, U = copy.deepcopy(A), copy.deepcopy(I)
    for op in obj["unit_row_operations"]:
        apply_operation(B, op)
        apply_operation(U, op)
    assert B == obj["transformed_rows"] and U == obj["integer_row_transform"]
    assert product(U, A) == B  # All 48*39 integer coordinates, not sampled.
    reverted_B, reverted_U = copy.deepcopy(B), copy.deepcopy(U)
    for op in reversed(obj["unit_row_operations"]):
        apply_operation(reverted_B, op, inverse=True)
        apply_operation(reverted_U, op, inverse=True)
    assert reverted_B == A and reverted_U == I
    pivots = obj["pivot_columns"]
    free = obj["free_columns"]
    expected_rank = 23 if sid == 9 else 25
    assert obj["integer_rank"] == len(pivots) == expected_rank
    assert pivots == sorted(set(pivots))
    assert free == [j for j in range(39) if j not in pivots]
    for i, pivot in enumerate(pivots):
        assert 0 <= pivot < 39
        assert [row[pivot] for row in B] == [int(j == i) for j in range(48)]
    assert not any(x for row in B[len(pivots):] for x in row)
    if sid == 9:
        target_terms = [("d", 15, 1), ("d", 8, -1)]
        residual_terms = [("F", 9, 1), ("G", 22, 1), ("G", 57, -1)]
        combination = {22: -1, 24: 1, 29: -1, 36: -1, 43: -1, 59: -1}
    else:
        target_terms = [("d", 15, 1), ("G", 13, -1)]
        residual_terms = [("G", 13, -1), ("G", 29, -1)]
        combination = {31: -1}
        assert all(row[columns["G", 13]] == 0 for row in A)
        assert A[29-16] == expression(columns, [("d", 29, 1), ("d", 13, -1)])
    target = expression(columns, target_terms)
    residual = expression(columns, residual_terms)
    assert obj["boundary_target"] == target
    assert obj["reduced_boundary_residual"] == residual
    assert obj["boundary_residual_terms"] == [list(term) for term in residual_terms]
    weights = [combination.get(t, 0) for t in range(16, 64)]
    assert obj["target_minus_residual_original_row_combination"] == weights
    assert product([weights], A)[0] == [a-b for a, b in zip(target, residual)]
    independently_reduced = list(target)
    for i, pivot in enumerate(pivots):
        coefficient = independently_reduced[pivot]
        independently_reduced = [a-coefficient*b for a, b in zip(independently_reduced, B[i])]
    assert independently_reduced == residual
    assert all(residual[j] == 0 for j in pivots)
    assert any(residual[j] in (-1, 1) for j in free)
    integer_model = obj["witness_integer_values"]
    modular_model = obj["witness_mod32_values"]
    assert len(integer_model) == len(modular_model) == 39
    assert all(type(x) is int for x in integer_model + modular_model)
    assert modular_model == [x % N for x in integer_model]
    assert all(x != 0 for x in integer_model)
    assert all(0 < x < N for x in modular_model)
    integer_equations = [dot(row, integer_model) for row in A]
    modular_equations = [dot(row, modular_model) % N for row in A]
    assert integer_equations == [0]*48 and modular_equations == [0]*48
    integer_boundary = dot(target, integer_model)
    modular_boundary = dot(target, modular_model) % N
    assert integer_boundary == obj["witness_boundary_integer"] != 0
    assert modular_boundary == obj["witness_boundary_mod32"] != 0
    assert obj["witness_all_active_d_F_G_nonzero"] is True
    assert dot(residual, integer_model) == integer_boundary
    assert dot(residual, modular_model) % N == modular_boundary
    # Set check for the conditional real-window implication; no actual witness inferred.
    translated_target = 0 if sid == 9 else 6
    assert max(support) < 63
    assert [i+1 for i in support] == supports[translated_target]
    assert any(i+1 < 16 for i in support)
    return {"support_index": sid, "integer_rows": 48, "variables": 39,
            "checked_UA_coordinates": 48*39, "elementary_operations": len(obj["unit_row_operations"]),
            "exact_inverse_operation_replay": True, "unit_row_rank": expected_rank,
            "free_columns": len(free), "boundary_residual": [list(term) for term in residual_terms],
            "integer_model_all_48_rows_zero": True, "mod32_model_all_48_rows_zero": True,
            "all_39_interfaces_nonzero_in_both_models": True,
            "integer_boundary": integer_boundary, "mod32_boundary": modular_boundary,
            "nonmembership_over_integers": True, "nonmembership_over_mod32": True,
            "actual_pair_realization": "unproved and not asserted"}


def negative_controls(objects, supports):
    mutations = [
        ("damaged_source_row", lambda o: o["original_rows"][0].__setitem__(0, 1)),
        ("damaged_U", lambda o: o["integer_row_transform"][0].__setitem__(0, 1)),
        ("nonunit_self_add", lambda o: o["unit_row_operations"].insert(0, ["add", 0, 0, 1])),
        ("wrong_target_combination", lambda o: o["target_minus_residual_original_row_combination"].__setitem__(6, 1)),
        ("wrong_residual", lambda o: o["reduced_boundary_residual"].__setitem__(15, -1)),
        ("zero_active_modular_interface", lambda o: o["witness_mod32_values"].__setitem__(0, 0)),
        ("wrong_boundary_target", lambda o: o["boundary_target"].__setitem__(1, 1)),
        ("bad_integer_lift_same_modular_value", lambda o: o["witness_integer_values"].__setitem__(0, o["witness_integer_values"][0]+N)),
    ]
    rejected = []
    for name, mutation in mutations:
        damaged = copy.deepcopy(objects[0])
        mutation(damaged)
        try:
            inspect(damaged, supports)
        except (AssertionError, KeyError):
            rejected.append(name)
        else:
            raise AssertionError("damaged evidence accepted: " + name)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    support_bytes = SUPPORTS.read_bytes()
    assert digest(support_bytes) == SUPPORT_HASH
    supports = json.loads(support_bytes)["supports"]
    manifest_bytes = (AUTHOR / "SHA256.json").read_bytes()
    assert digest(manifest_bytes) == AUTHOR_MANIFEST_HASH
    manifest = json.loads(manifest_bytes)
    assert len(manifest["files"]) == 6
    author_hashes = {"SHA256.json": AUTHOR_MANIFEST_HASH}
    for name, frozen in manifest["files"].items():
        data = (AUTHOR / name).read_bytes()
        assert len(data) == frozen["bytes"] and digest(data) == frozen["sha256"]
        author_hashes[name] = digest(data)
    cert = json.loads((AUTHOR / "MODULE_CERTIFICATE.json").read_text())
    assert cert["schema"] == "crypto3-backward-boundary-linear-module-v5"
    assert cert["source_support_sha256"] == SUPPORT_HASH
    assert cert["generator_sha256"] == author_hashes["build_module_certificate.py"]
    assert cert["modulus"] == N
    assert [obj["support_index"] for obj in cert["objects"]] == [9, 12]
    results = [inspect(obj, supports) for obj in cert["objects"]]
    output = {"status": "PASS", "review": "independent AI written mathematical review",
              "python": platform.python_version(), "source_support_sha256": SUPPORT_HASH,
              "reviewer_checker_sha256": digest(Path(__file__).read_bytes()),
              "author_source_sha256": author_hashes, "cases": results,
              "negative_controls_rejected": negative_controls(cert["objects"], supports),
              "scope": "All 48 additive rows do not imply either shared backward boundary in the free d/F/G interface module, over Z or Z/(2^32), even with all 39 active interfaces nonzero.",
              "not_claimed": ["actual coupled word-pair counterexample", "reverse time-shift refutation for true schedules", "support exclusion", "global distance14", "Lean", "human review", "originality"]}
    if args.save:
        (HERE / "RUN.json").write_text(json.dumps(output, indent=2, sort_keys=True)+"\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
