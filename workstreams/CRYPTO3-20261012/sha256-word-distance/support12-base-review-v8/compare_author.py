#!/usr/bin/env python3
"""Exact post-freeze comparison with the support12-base-lift-v8 author package."""

import argparse
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / "support12-base-lift-v8"
EXPECTED_AUTHOR_MANIFEST = "374732f8fee671cd7290d7596ab7f0cb85bb83502b3c94a124d7a78280802dc6"
EXPECTED_PRE_FREEZE = ""
MASK = (1 << 32) - 1
FULL = (1 << 64) - 1


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def check_manifest():
    manifest_path = AUTHOR / "SHA256.json"
    require(digest(manifest_path) == EXPECTED_AUTHOR_MANIFEST,
            "author manifest hash mismatch")
    manifest = json.loads(manifest_path.read_text())
    checked = {}
    for name, expected in manifest["files"].items():
        actual = digest(AUTHOR / name)
        require(actual == expected, "author file hash mismatch: " + name)
        checked[name] = actual
    require(set(manifest["excluded"]) == {"SHA256.json"}, "manifest exclusion mismatch")
    return checked


def validate_order(support, anchors, order, residuals, rows, occurrence_type):
    known = set(support) | set(anchors)
    used = set()
    targets = set()
    kinds = Counter()
    for t, target in order:
        require(t in rows and t not in used, "author row invalid or repeated")
        unknown = [value for value in rows[t] if value not in known]
        require(unknown == [target], "author target is not unique unknown")
        require(target not in targets, "author target repeated")
        kinds[occurrence_type(t, target)] += 1
        known.add(target)
        targets.add(target)
        used.add(t)
    require(known == set(range(64)), "author order does not complete 64 coordinates")
    require(len(order) == len(used) == len(targets) == 46,
            "author row/target distinctness count")
    require(sorted(set(rows) - used) == list(residuals) == [33, 57],
            "author residual complement mismatch")
    return {"rows": len(used), "targets": len(targets),
            "residual_rows": sorted(set(rows) - used),
            "step_type_counts": dict(sorted(kinds.items()))}


def bitset_close(anchors, support_mask, row_masks):
    known = support_mask
    for value in anchors:
        known |= 1 << value
    while True:
        before = known
        for row_mask in row_masks:
            unknown = row_mask & ~known & FULL
            if unknown and not unknown & (unknown - 1):
                known |= unknown
        if known == FULL or known == before:
            return known


def independent_first_size5(support, author_anchors, rows):
    inactive = [value for value in range(64) if value not in support]
    support_mask = sum(1 << value for value in support)
    row_masks = [sum(1 << value for value in rows[t]) for t in sorted(rows)]
    trials = 0
    first = None
    for anchors in itertools.combinations(inactive, 5):
        trials += 1
        if bitset_close(anchors, support_mask, row_masks) == FULL:
            first = anchors
            break
    require(first == tuple(author_anchors), "author anchors are not first lexicographic success")
    require(trials == 1_498_469, "first-success trial count mismatch")
    return {"trials_to_first_success": trials, "first_anchors": list(first)}


def generic_reconstruct(coordinates, order, rows, inverse0, inverse1, sigma0, sigma1):
    words = dict(coordinates)
    for t, target in order:
        require(target not in words, "generic target already assigned")
        require(set(rows[t]) - {target} <= set(words), "generic row another unknown")
        if target == t:
            value = sigma1(words[t - 2]) + words[t - 7] + sigma0(words[t - 15]) + words[t - 16]
        elif target == t - 2:
            value = inverse1((words[t] - words[t - 7] - sigma0(words[t - 15]) - words[t - 16]) & MASK)
        elif target == t - 7:
            value = words[t] - sigma1(words[t - 2]) - sigma0(words[t - 15]) - words[t - 16]
        elif target == t - 15:
            value = inverse0((words[t] - sigma1(words[t - 2]) - words[t - 7] - words[t - 16]) & MASK)
        elif target == t - 16:
            value = words[t] - sigma1(words[t - 2]) - words[t - 7] - sigma0(words[t - 15])
        else:
            raise ValueError("generic target absent")
        words[target] = value & MASK
    return [words[index] for index in range(64)]


def compare_implementation(independent, author, rows):
    for bit in range(32):
        basis = 1 << bit
        require(author.sigma0(basis) == independent.sigma0(basis), "sigma0 basis mismatch")
        require(author.sigma1(basis) == independent.sigma1(basis), "sigma1 basis mismatch")
        require(author.sigma0(author.INV0(basis)) == basis, "author sigma0 right inverse")
        require(author.INV0(author.sigma0(basis)) == basis, "author sigma0 left inverse")
        require(author.sigma1(author.INV1(basis)) == basis, "author sigma1 right inverse")
        require(author.INV1(author.sigma1(basis)) == basis, "author sigma1 left inverse")
    inverse0_columns, inverse0 = independent.inverse_columns(independent.sigma0)
    inverse1_columns, inverse1 = independent.inverse_columns(independent.sigma1)
    require([author.INV0(1 << bit) for bit in range(32)] == inverse0_columns,
            "sigma0 inverse columns differ")
    require([author.INV1(1 << bit) for bit in range(32)] == inverse1_columns,
            "sigma1 inverse columns differ")

    blocks = [
        list(range(16)),
        [MASK - value for value in range(16)],
        [((0xD2511F53 * (value + 3)) ^ 0xCD9E8D57) & MASK for value in range(16)],
        [(1 << 31) ^ (1 << value) for value in range(16)],
    ]
    roundtrips = []
    for number, block in enumerate(blocks):
        expected = independent.expand(block)
        active = {index: expected[index] for index in author.SUPPORT}
        parameters = {index: expected[index] for index in author.PARAMETERS}
        candidate, residuals = author.complete(active, parameters)
        coordinates = dict(active)
        coordinates.update(parameters)
        own = generic_reconstruct(coordinates, author.ORDER, rows, inverse0, inverse1,
                                  independent.sigma0, independent.sigma1)
        require(candidate == own == expected, "author/independent roundtrip mismatch")
        require(residuals == {33: 0, 57: 0}, "author roundtrip residual")
        roundtrips.append({"fixture": number,
                           "schedule_sha256": independent.words_hash(expected)})
    return {"basis_function_comparisons": 64,
            "inverse_compositions_checked": 128,
            "inverse_columns_exact_match": True,
            "cross_implementation_roundtrips": roundtrips}


def rerun_author_verifier():
    completed = subprocess.run([sys.executable, "-B", "verify_completion.py"],
                               cwd=AUTHOR, text=True, capture_output=True, check=False)
    require(completed.returncode == 0, "author verifier rerun failed")
    require(completed.stderr == "", "author verifier emitted stderr")
    rerun = json.loads(completed.stdout)
    frozen = json.loads((AUTHOR / "VERIFICATION.json").read_text())
    require(rerun == frozen, "author verifier rerun differs from frozen output")
    require(frozen["negative_controls"]["damaged_active_10"]["nonzero_residuals"] == [33, 57],
            "author active-damage control did not hit both residuals")
    require(frozen["negative_controls"]["corrupted_constructed_31"]["rejected_used_rows"],
            "author constructed-coordinate control was not rejected")
    return {"exact_frozen_output_match": True,
            "roundtrips": len(frozen["roundtrips"]),
            "negative_controls": sorted(frozen["negative_controls"])}


def compare_frozen_structural(author, independent, rows):
    frozen = json.loads((AUTHOR / "STRUCTURAL.json").read_text())
    scans = frozen["scans"]
    require([scan["anchor_count"] for scan in scans] == [3, 4, 5], "scan sizes")
    require(scans[0]["trials"] == 20_825 and scans[0]["success"] is None,
            "size-three scan record")
    require(scans[1]["trials"] == 249_900 and scans[1]["success"] is None,
            "size-four scan record")
    success = scans[2]["success"]
    require(success["anchors"] == list(author.PARAMETERS), "frozen success anchors")
    require([tuple(item) for item in success["order"]] == list(author.ORDER),
            "frozen success order differs from implementation")
    require(success["unused_equations"] == list(author.RESIDUAL_INDICES),
            "frozen residuals differ from implementation")
    pre_run = json.loads((HERE / "PRE-AUTHOR-RUN.json").read_text())
    require(pre_run["minimality"]["sets_by_size"]["3"] == 20_825,
            "independent size-three count")
    require(pre_run["minimality"]["sets_by_size"]["4"] == 249_900,
            "independent size-four count")
    require(pre_run["minimality"]["sets_checked_below_five"] == 272_052,
            "independent lower-size exhaustive count")
    return independent_first_size5(set(author.SUPPORT), author.PARAMETERS, rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checked = check_manifest()
    independent = load_module("support12_base_independent", HERE / "check_independent.py")
    author = load_module("support12_base_author", AUTHOR / "base_completion.py")
    rows = independent.recurrence_rows()
    require(tuple(independent.EXPECTED_SUPPORT) == tuple(author.SUPPORT), "support mismatch")
    require(list(author.PARAMETERS) != independent.EXPECTED_ANCHORS,
            "charts were not independently distinct")
    author_structure = validate_order(author.SUPPORT, author.PARAMETERS, author.ORDER,
                                      author.RESIDUAL_INDICES, rows,
                                      independent.occurrence_type)
    frozen_search = compare_frozen_structural(author, independent, rows)
    implementation = compare_implementation(independent, author, rows)
    verifier = rerun_author_verifier()

    report = {
        "schema": "CRYPTO3-support12-base-lift-v8-independent-comparison",
        "status": "ACCEPT",
        "author_manifest_sha256": digest(AUTHOR / "SHA256.json"),
        "author_files_checked": checked,
        "pre_author_freeze_sha256": digest(HERE / "PRE-AUTHOR-FREEZE.json"),
        "chart_comparison": {
            "independent_anchors": independent.EXPECTED_ANCHORS,
            "author_anchors": list(author.PARAMETERS),
            "anchors_are_distinct": True,
            "shared_residual_rows": list(author.RESIDUAL_INDICES),
            "author_structure": author_structure,
            "author_first_lexicographic_size5": frozen_search,
            "independent_lower_size_sets_checked": 272_052
        },
        "implementation_comparison": implementation,
        "author_verifier_rerun": verifier,
        "theorem_scope": "exact base interpolation bijection for arbitrary prescribed first words on support 12",
        "not_accepted": ["residual solvability", "active-pair realization", "full message pair",
                         "distance-13 attainability", "distance at least 14", "Lean formalization"],
        "author_files_modified": False
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
