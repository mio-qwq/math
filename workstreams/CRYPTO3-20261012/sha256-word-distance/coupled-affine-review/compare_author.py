#!/usr/bin/env python3
"""Compare the frozen author proof with the pre-author reconstruction.

Each selected author row is derived from ONE independently rebuilt
signed-difference subsystem. This avoids using the already inconsistent
full system as a vacuous proof of arbitrary rows. Explicit original-row
XOR combinations are retained for all 384 applications.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

import reconstruct as independent

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "coupled-short-proof"
PINNED = {
    "PROOF.md": "7b3fa0d70c8bb03401e8c1e0223d778650dc806a46fcfac477d2dbd1c753b22b",
    "CERTIFICATE.json": "1428cce8b31378b67db8de32e4480bfedad608b0d62b0bee21742f3f09fa6389",
    "check.py": "71c12525b4938650984a9c87394dcc0fdf5f65e848ec1b606732cd20ff0d0d4d",
    "SHA256.json": "9b0a2bd7fced9e3f8ccaf72ed5fc57a88db00ded403215e9d87d4a9c532bd13b",
    "RUNS.json": "a6ef783ddf1ae1871fa96972bdb65ad6f7fc5fd3019707ff20861649f8c67f4d",
}
LOW32 = (1 << 32) - 1
LOW64 = (1 << 64) - 1
GROUPS = ("q_plus_gq", "p_minus_q", "fp_plus_fq")


def require(ok, message):
    if not ok:
        raise ValueError(message)


def swapped(coefficient):
    # Author: p low, q high. Independent reconstruction: q low, p high.
    return ((coefficient & LOW32) << 32) | ((coefficient >> 32) & LOW32)


def basis_for(indexed_rows):
    basis = {}
    for index, row in indexed_rows:
        coefficient, rhs, used = row["coefficient"], row["rhs"], 1 << index
        while coefficient:
            pivot = coefficient.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = coefficient, rhs, used
                break
            other, parity, provenance = basis[pivot]
            coefficient ^= other
            rhs ^= parity
            used ^= provenance
        else:
            require(rhs == 0, "single modular subsystem unexpectedly inconsistent")
    return basis


def derive(target, basis):
    coefficient, rhs = target
    used = 0
    while coefficient:
        pivot = coefficient.bit_length() - 1
        if pivot not in basis:
            return None
        other, parity, provenance = basis[pivot]
        coefficient ^= other
        rhs ^= parity
        used ^= provenance
    if rhs:
        return None
    return used


def checked_xor(rows, used, target):
    coefficient = rhs = 0
    indices = [i for i in range(len(rows)) if used >> i & 1]
    for i in indices:
        coefficient ^= rows[i]["coefficient"]
        rhs ^= rows[i]["rhs"]
    require((coefficient, rhs) == target, "original-row derivation mismatch")
    return indices


def pin_files():
    for filename, expected in PINNED.items():
        require(hashlib.sha256((AUTHOR / filename).read_bytes()).hexdigest() == expected,
                "author freeze mismatch: " + filename)
    manifest = json.loads((AUTHOR / "SHA256.json").read_text())
    for filename, data in manifest["files"].items():
        raw = (AUTHOR / filename).read_bytes()
        require(len(raw) == data["bytes"] and hashlib.sha256(raw).hexdigest() == data["sha256"],
                "author manifest mismatch: " + filename)
    checkpoint = json.loads((HERE / "PRE-AUTHOR-CHECKPOINT.json").read_text())
    for filename, expected in checkpoint["files"].items():
        require(hashlib.sha256((HERE / filename).read_bytes()).hexdigest() == expected,
                "blind reconstruction changed: " + filename)
    return len(manifest["files"])


def author_namespace():
    # The exact checker has been read and hash-pinned. Loading definitions
    # does not execute its main routine and writes no bytecode or artifacts.
    namespace = {"__name__": "reviewed_frozen_author", "__file__": str(AUTHOR / "check.py")}
    exec(compile((AUTHOR / "check.py").read_text(), str(AUTHOR / "check.py"), "exec"), namespace)
    return namespace


def author_systems(a, ns):
    aff, identity, sigforms, sig = (ns[k] for k in ("affine_carry_rows", "identity_forms", "sigma_forms", "sigma"))
    encoded = [
        aff(independent.K, independent.g(independent.K), identity(32), sigforms(1, 32)),
        aff(a, independent.K, identity(0), identity(32, True)),
        aff(independent.f(a), independent.f(independent.K), sigforms(0, 0), sigforms(0, 32)),
    ]
    result = []
    for rows in encoded:
        result.append([{"coefficient": swapped(row & LOW64), "rhs": (row >> 64) & 1}
                       for row in sorted(rows)])
    return result


def check_partition(cert, independent_masks):
    require(len(cert["families"]) == 10 and len(cert["row_bank"]) == 26, "template sizes")
    classified = []
    for number, family in enumerate(cert["families"]):
        require(family["id"] == number and family["mask_count"] == len(family["masks"]), "family identity")
        classified.extend(int(a, 16) for a in family["masks"])
    require(sorted(classified) == independent_masks and len(set(classified)) == 132,
            "independent 132-mask cover mismatch")
    appendix = (AUTHOR / "PROOF.md").read_text().split("## Appendix A.", 1)[1]
    pieces = re.findall(r"(?ms)^(\d+):\n(.*?)(?=^\d+:|\Z)", appendix)
    require(len(pieces) == 10, "written appendix groups")
    for number, body in pieces:
        labels = re.findall(r"\b[0-9a-f]{8}\b", body)
        require(labels == cert["families"][int(number)]["masks"], "written mask partition differs")


def compare(cert, ns, masks):
    check_partition(cert, masks)
    bank = []
    for number, item in enumerate(cert["row_bank"]):
        coefficient = int(item["coefficient"], 16)
        require(item["id"] == number and 0 <= coefficient <= LOW64 and item["rhs"] in (0, 1),
                "bad author row encoding")
        require(item["p_bits"] == [i for i in range(32) if coefficient >> i & 1], "p coordinate description")
        require(item["q_bits"] == [i for i in range(32) if coefficient >> (32 + i) & 1], "q coordinate description")
        bank.append((swapped(coefficient), item["rhs"]))
    require(len(set(bank)) == 26, "duplicate bank rows")
    applications = []
    subsystem_comparisons = 0
    for family in cert["families"]:
        chosen = family["row_ids"]
        require(len(chosen) == len(set(chosen)) and all(0 <= r < 26 for r in chosen), "template row indices")
        coefficient = rhs = 0
        for row_id in chosen:
            coefficient ^= bank[row_id][0]
            rhs ^= bank[row_id][1]
        require(coefficient == 0 and rhs == 1, "template does not XOR to 0=1")
        for label in family["masks"]:
            a = int(label, 16)
            _, raw = independent.build_system(a)
            projected = []
            for group in GROUPS:
                basis = basis_for([(i, r) for i, r in enumerate(raw) if r["origin"].startswith(group + ":")])
                projected.append({p: row for p, row in basis.items() if p < 64})
            author_groups = author_systems(a, ns)
            for proof_basis, author_rows in zip(projected, author_groups):
                author_basis = basis_for(list(enumerate(author_rows)))
                for row in author_rows:
                    require(derive((row["coefficient"], row["rhs"]), proof_basis) is not None,
                            "author carry projection has an extra restriction")
                for coefficient, rhs, _ in proof_basis.values():
                    require(derive((coefficient, rhs), author_basis) is not None,
                            "author carry projection omitted a restriction")
                subsystem_comparisons += 1
            row_applications = []
            for row_id in chosen:
                target = bank[row_id]
                for group, proof_basis in zip(GROUPS, projected):
                    used = derive(target, proof_basis)
                    if used is not None:
                        indices = checked_xor(raw, used, target)
                        require(all(raw[i]["origin"].startswith(group + ":") for i in indices),
                                "derivation uses multiple modular subsystems")
                        row_applications.append({"author_row_id": row_id,
                                                 "single_modular_subsystem": group,
                                                 "independent_original_rows": indices})
                        break
                else:
                    raise ValueError("author template premise not derived independently")
            applications.append({"A": label, "family": family["id"],
                                 "independent_matrix_sha256": independent.matrix_hash(raw),
                                 "rows": row_applications})
    return {"subsystem_projection_equivalences": subsystem_comparisons,
            "row_applications": applications,
            "row_applications_checked": sum(len(a["rows"]) for a in applications),
            "template_contradictions": len(cert["families"]),
            "distinct_author_rows": len(bank)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    checked_files = pin_files()
    ns = author_namespace()
    cert = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    masks = [c["A"] for c in json.loads((HERE / "INDEPENDENT-CERTIFICATE.json").read_text())["cases"]]
    require(all((a >> 18) & 1 == 0 and (a >> 19) & 1 == 1 for a in masks), "low sigma-bit restriction")
    fixed_zero = sum(1 << i for i in range(12))
    f_rows = independent.sigma_rows((7, 18), 3, 0)
    require(f_rows[0] & ~fixed_zero == 1 << 18 and f_rows[1] & ~fixed_zero == 1 << 19,
            "original output-bit proof of A18,A19")
    count_after_input = 0
    all_17_survivors = []
    for u in range(1 << 17):
        a = 0x81000 | ((u & 31) << 13) | ((u >> 5) << 20)
        if independent.mask_ok(a, independent.K):
            count_after_input += 1
            if independent.mask_ok(independent.f(a), independent.f(independent.K)):
                all_17_survivors.append(a)
    require(count_after_input == 24576 and all_17_survivors == masks, "17-bit universe comparison")
    report = compare(cert, ns, masks)
    require(report["subsystem_projection_equivalences"] == 396 and report["row_applications_checked"] == 384,
            "complete comparison counts")
    report.update(status="pass", exact_author_hashes=PINNED, author_manifest_files_checked=checked_files,
                  necessary_mask_universes={"independent_before_author": 1 << 19,
                                            "author_after_two_proved_fixed_bits": 1 << 17,
                                            "same_final_masks": len(masks)},
                  negative_controls=[])
    if args.negative:
        def rejected(name, change):
            damaged = copy.deepcopy(cert)
            change(damaged)
            try:
                compare(damaged, ns, masks)
            except (ValueError, IndexError):
                report["negative_controls"].append({"name": name, "rejected": True})
            else:
                raise ValueError("comparison accepted damage: " + name)
        rejected("missing_mask_in_cover", lambda c: c["families"][0]["masks"].pop())
        rejected("flipped_template_rhs", lambda c: c["row_bank"][0].__setitem__("rhs", 1 - c["row_bank"][0]["rhs"]))
        rejected("missing_template_premise", lambda c: c["families"][0]["row_ids"].pop())
        rejected("reversed_word_bit_description", lambda c: c["row_bank"][0].__setitem__("p_bits", [0]))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
