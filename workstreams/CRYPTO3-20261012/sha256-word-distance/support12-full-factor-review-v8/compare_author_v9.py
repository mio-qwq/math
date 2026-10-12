#!/usr/bin/env python3
"""Independent comparison of corrected author v9 to the blind v8 review."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-full-factor-v9"
V8_AUTHOR = HERE.parent / "support12-full-factor-v8"

AUTHOR_HASHES = {
    "manifest.json": "a0438580b430fdd031cecd0ea07c87363c5c942f5f8fc3848864ba1a51ae6b98",
    "PROOF.md": "efba27236a949965e8689462703b4ed675a0484c0c5a84302b621c59d9bd0395",
    "CERTIFICATE.json": "352b1c650d04811b3f29830ecf515e774bbf9c2573c164ac7c6d82f53c9821e2",
    "check.py": "84516b87f1319e4a4af660b070e627f7c98b46d2a561c4a4e7d2ef150b37ad1e",
}
BLIND_HASHES = {
    "check_independent.py": "a8b21e86b6884314ba8185ab225701a302c27eee97cbd75940217d1e15cde96f",
    "INDEPENDENT_PROOF.md": "b826b4e1dd158c7a041c6c6ebe49a01d7742bd2232bd81bab47082d73a58513e",
    "PRE_AUTHOR_FREEZE.md": "289a1767531dd0b08e3e9f2e29a98b5de50961b3dda90910252b125fddb2c5ec",
    "INDEPENDENT_RUN.json": "ce216ce12166c22b88f2857e99dff944547e0e34046daeeffe2ca7ee7eb2e12f",
    "PRE_AUTHOR_FREEZE.json": "0ce4247c7a571321060f61c3bda95c63c08f547739bfe0809aedf9af6e7ad475",
}
V8_MANIFEST_SHA256 = "02a3729a66b7e474eb2abfeb33920160e2d60386f324ab5d4ef1b5c1e2bc0814"


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(form):
    return {name: coefficient for name, coefficient in sorted(form.items()) if coefficient}


def add_scaled(target, source, multiplier):
    result = dict(target)
    for name, coefficient in source.items():
        result[name] = result.get(name, 0) + multiplier * coefficient
        if result[name] == 0:
            del result[name]
    return result


def gf2_rank(columns):
    basis = {}
    for column in columns:
        value = column
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF


def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def canonical_up_to_sign(form):
    items = tuple(sorted((name, coefficient) for name, coefficient in form.items() if coefficient))
    require(items, "zero form cannot be a nonzero support condition")
    if items[0][1] < 0:
        items = tuple((name, -coefficient) for name, coefficient in items)
    return items


def load_blind_module():
    path = HERE / "check_independent.py"
    require(digest(path) == BLIND_HASHES["check_independent.py"], "blind checker changed")
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("frozen_blind_factor_v8", path)
    module = importlib.util.module_from_spec(spec)
    require(spec.loader is not None, "blind loader")
    spec.loader.exec_module(module)
    return module


def main():
    for name, expected in BLIND_HASHES.items():
        require(digest(HERE / name) == expected, "pre-author blind file changed: " + name)
    for name, expected in AUTHOR_HASHES.items():
        require(digest(AUTHOR / name) == expected, "author v9 announced file changed: " + name)
    manifest = json.loads((AUTHOR / "manifest.json").read_text())
    for name, expected in manifest["files"].items():
        require(digest(AUTHOR / name) == expected, "author v9 manifest mismatch: " + name)
    require(digest(V8_AUTHOR / "manifest.json") == V8_MANIFEST_SHA256,
            "rejected v8 failure object changed")

    blind = load_blind_module()
    blind_report = blind.verify_spec()
    require(blind_report["status"] == "PASS", "blind proof replay")
    cert = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    require(cert["support_identifier"] == 12 and cert["support_identifier_is_zero_based"],
            "author target indexing")
    require(cert["active_indices"] == blind.SUPPORT, "author v9 target differs from blind target")
    require(cert["nonzero_row_count"] == 25 and cert["zero_row_count"] == 23,
            "author row counts")

    blind_rows_all, blind_tagged = blind.original_rows(set(blind.SUPPORT))
    author_rows = cert["original_rows"]
    for offset, row in enumerate(author_rows):
        t = 16 + offset
        expected = {blind.VARIABLES[j]: coefficient
                    for j, coefficient in enumerate(blind_rows_all[offset]) if coefficient}
        require(row == {"t": t, "coefficients": expected}, "author row mismatch at t=" + str(t))

    # Express every author free coordinate in the blind frozen parameters.
    author_free_to_blind = {name: blind.FORMS[name] for name in cert["free_variables"]}
    reduced_by_pivot = {row["pivot"]: row["coefficients"] for row in cert["reduced_rows"]}
    author_forms_in_blind = {}
    for variable in cert["variables"]:
        if variable in author_free_to_blind:
            form = author_free_to_blind[variable]
        else:
            equation = reduced_by_pivot[variable]
            require(equation.get(variable) == 1, "nonunit author pivot: " + variable)
            form = {}
            for free_variable, coefficient in equation.items():
                if free_variable != variable:
                    require(free_variable in author_free_to_blind,
                            "author reduced row is not in free coordinates")
                    form = add_scaled(form, author_free_to_blind[free_variable], -coefficient)
        author_forms_in_blind[variable] = normalized(form)
        require(author_forms_in_blind[variable] == normalized(blind.FORMS[variable]),
                "author normal form differs from blind form: " + variable)

    require(len(author_forms_in_blind) == 39, "normal-form coordinate coverage")
    require(set(cert["free_variables"]) == {
        "d10", "d11", "d13", "d15", "F11", "F13", "G10",
        "G11", "G13", "F15", "G26", "F29", "F42", "F57",
    }, "author free-coordinate set")

    private = ["G10", "G11", "G13", "F57"]
    require(all(set(blind.FORMS[name]) == {blind.FREE_TO_PARAMETER[name]} for name in private),
            "blind private forms")
    projected = {"a", "b", "c", "e", "p", "q", "r", "s", "u", "v"}
    used = set()
    for node in blind.FULL_FACTOR_NODES.values():
        for form in node[1:]:
            used.update(form)
    require(used == projected, "ten-scalar projected graph")
    require(len(blind.FULL_FACTOR_NODES) == 13, "factor count")
    require(sum(node[0] == "DFG" for node in blind.FULL_FACTOR_NODES.values()) == 9,
            "full joint-factor count")
    require(sum(node[0] in ("DF", "DG") for node in blind.FULL_FACTOR_NODES.values()) == 4,
            "projected-factor count")

    # V9's seven distinct d-nonzero forms map exactly to the blind seven.
    author_d_conditions = [
        {"d10": 1}, {"d11": 1}, {"d13": 1}, {"d15": 1},
        {"F11": 1, "d10": 1}, {"F13": 1, "G26": 1}, {"F42": 1},
    ]
    translated = set()
    for condition in author_d_conditions:
        form = {}
        for coordinate, coefficient in condition.items():
            form = add_scaled(form, author_free_to_blind[coordinate], coefficient)
        translated.add(canonical_up_to_sign(form))
    blind_conditions = [
        {"a": 1}, {"b": 1}, {"c": 1}, {"e": 1}, {"u": 1},
        {"q": 1, "r": 1}, {"v": 1},
    ]
    require(translated == {canonical_up_to_sign(x) for x in blind_conditions},
            "v9 nonzero conditions do not match blind conditions")

    require(gf2_rank([sigma0(1 << i) for i in range(32)]) == 32,
            "independent sigma0 bijectivity")
    require(gf2_rank([sigma1(1 << i) for i in range(32)]) == 32,
            "independent sigma1 bijectivity")

    completed = subprocess.run(
        [sys.executable, "-B", str(AUTHOR / "check.py"), "--negative"],
        cwd=HERE.parents[3], text=True, capture_output=True, timeout=30, check=False,
    )
    require(completed.returncode == 0, "author v9 checker failed")
    self_check = json.loads(completed.stdout)
    require(self_check["status"] == "PASS", "author v9 checker status")
    require(len(self_check["negative_controls"]) == 6 and
            all(item["rejected"] for item in self_check["negative_controls"]),
            "author v9 negative controls")
    summary = self_check["summary"]
    require(summary["integer_rank"] == 25 and summary["free_rank"] == 14,
            "author v9 rank summary")
    require(len(summary["private_parameters"]) == 4 and len(summary["shared_parameters"]) == 10,
            "author v9 factor split summary")
    require(summary["connected_pair_factors"] == 13, "author v9 connected factors")
    require(summary["v8_failure_manifest_preserved"] is True, "v8 failure binding")

    result = {
        "schema": "CRYPTO3-support12-full-factor-v9-independent-comparison",
        "status": "ACCEPT",
        "target_binding": {
            "support_identifier": 12,
            "zero_based": True,
            "active_indices": blind.SUPPORT,
            "source_sha256": blind.SUPPORT_SHA256,
            "rejected_v8_manifest_preserved": V8_MANIFEST_SHA256,
        },
        "row_comparison": {"all_original_rows_equal": 48, "nonzero": 25, "zero": 23},
        "linear_module": {
            "unit_rank": 25,
            "free_rank": 14,
            "all_coordinate_forms_equal_under_change_of_basis": 39,
            "author_unit_operations_replayed_and_reversed": summary["unit_operations"],
        },
        "factor_theorem": {
            "actual_pair_factors": 13,
            "full_joint_DFG": 9,
            "exact_projected_DF_or_DG": 4,
            "private_coordinates": private,
            "shared_scalars": sorted(projected),
            "shared_count": 10,
            "connected": True,
            "distinct_active_d_nonzero_forms": 7,
        },
        "sigma_bijectivity": {"sigma0_gf2_rank": 32, "sigma1_gf2_rank": 32},
        "negative_controls_rejected": 6,
        "scope": {
            "complete_written_proof": "exact independent-active-pair factorization",
            "independent_AI_acceptance": True,
            "factor_system_feasibility_decided": False,
            "base_message_completion": False,
            "distance13_witness": False,
            "distance14_lower_bound": False,
            "Lean": False,
        },
        "author_hashes": AUTHOR_HASHES,
        "blind_hashes": BLIND_HASHES,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
