#!/usr/bin/env python3
"""Independent, standard-library check of the support-12 base chart."""

import argparse
import copy
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MOD = 1 << 32
MASK = MOD - 1
SUPPORT_HASH = "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf"
EXPECTED_SUPPORT = [10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57]
EXPECTED_ANCHORS = [21, 22, 23, 24, 32]
EXPECTED_RESIDUALS = [33, 57]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rotr(x, amount):
    return ((x >> amount) | (x << (32 - amount))) & MASK


def sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def inverse_columns(function):
    """Derive the inverse matrix from the function's 32 basis images."""
    rows = []
    for output_bit in range(32):
        coefficients = sum(
            1 << input_bit
            for input_bit in range(32)
            if (function(1 << input_bit) >> output_bit) & 1
        )
        rows.append(coefficients | (1 << (32 + output_bit)))
    for column in range(32):
        pivots = [row for row in range(column, 32) if (rows[row] >> column) & 1]
        require(pivots, "sigma matrix is singular at column %d" % column)
        pivot = pivots[0]
        rows[column], rows[pivot] = rows[pivot], rows[column]
        for row in range(32):
            if row != column and ((rows[row] >> column) & 1):
                rows[row] ^= rows[column]
    require([row & MASK for row in rows] == [1 << i for i in range(32)],
            "left matrix did not reduce to identity")
    inverse_rows = [row >> 32 for row in rows]

    def inverse(value):
        return sum(
            (((inverse_rows[bit] & value).bit_count() & 1) << bit)
            for bit in range(32)
        )

    columns = [inverse(1 << bit) for bit in range(32)]
    for bit in range(32):
        require(function(columns[bit]) == 1 << bit,
                "right inverse basis composition failed")
        require(inverse(function(1 << bit)) == 1 << bit,
                "left inverse basis composition failed")
    return columns, inverse


def recurrence_rows():
    return {t: (t, t - 2, t - 7, t - 15, t - 16) for t in range(16, 64)}


def occurrence_type(t, target):
    positions = {
        t: "identity_output",
        t - 2: "sigma1_inverse",
        t - 7: "identity_lag7",
        t - 15: "sigma0_inverse",
        t - 16: "identity_lag16",
    }
    require(target in positions, "target absent from recurrence row")
    return positions[target]


def validate_structure(certificate):
    require(certificate["source_support_index"] == 12, "wrong support index")
    require(certificate["source_support_sha256"] == SUPPORT_HASH,
            "wrong frozen support hash")
    support = certificate["fixed_active_indices"]
    anchors = certificate["free_anchor_indices"]
    require(support == EXPECTED_SUPPORT, "wrong support coordinates")
    require(anchors == EXPECTED_ANCHORS, "wrong anchor coordinates")
    require(not (set(support) & set(anchors)), "active-anchor overlap")
    require(len(set(anchors)) == len(anchors), "duplicate anchor")
    rows = recurrence_rows()
    known = set(support) | set(anchors)
    used = set()
    types = Counter()
    for item in certificate["solve_steps"]:
        require(isinstance(item, list) and len(item) == 2, "malformed solve step")
        t, target = item
        require(t in rows and t not in used, "invalid or reused row")
        unknown = [coordinate for coordinate in rows[t] if coordinate not in known]
        require(unknown == [target], "target is not the unique unknown")
        types[occurrence_type(t, target)] += 1
        known.add(target)
        used.add(t)
    require(known == set(range(64)), "coordinate elimination is incomplete")
    residuals = sorted(set(rows) - used)
    require(residuals == certificate["residual_rows"] == EXPECTED_RESIDUALS,
            "wrong residual row partition")
    require(dict(sorted(types.items())) == dict(sorted(certificate["step_type_counts"].items())),
            "step-type counts mismatch")
    require(len(used) == 46, "wrong number of used recurrence rows")
    require(len(anchors) - len(residuals) == 3, "anchor-residual dimension count")
    return {"used_rows": sorted(used), "residual_rows": residuals,
            "step_type_counts": dict(sorted(types.items()))}


def closure(anchor_set, support, rows):
    known = set(support) | set(anchor_set)
    while True:
        before = len(known)
        for coordinates in rows.values():
            unknown = [coordinate for coordinate in coordinates if coordinate not in known]
            if len(unknown) == 1:
                known.add(unknown[0])
        if len(known) == 64 or len(known) == before:
            return known


def exhaustive_minimality():
    support = set(EXPECTED_SUPPORT)
    inactive = sorted(set(range(64)) - support)
    rows = recurrence_rows()
    counts = {}
    total = 0
    for size in range(5):
        checked = 0
        for anchors in itertools.combinations(inactive, size):
            checked += 1
            require(len(closure(anchors, support, rows)) < 64,
                    "found a completing anchor set below size five: %r" % (anchors,))
        counts[str(size)] = checked
        total += checked
    require(total == 272052, "wrong exhaustive anchor count")
    require(len(closure(EXPECTED_ANCHORS, support, rows)) == 64,
            "the certified five anchors do not complete")
    return {"sets_by_size": counts, "sets_checked_below_five": total,
            "certified_anchor_size": 5, "minimal_residual_count": 2,
            "scope": "single-original-row reversible propagation"}


def row_residual(words, t):
    return (words[t] - sigma1(words[t - 2]) - words[t - 7]
            - sigma0(words[t - 15]) - words[t - 16]) & MASK


def solve_target(words, t, target, inverse0, inverse1):
    require(target not in words, "solve target was already assigned")
    other = set(recurrence_rows()[t]) - {target}
    require(other <= set(words), "solve row has another unknown")
    if target == t:
        value = (sigma1(words[t - 2]) + words[t - 7]
                 + sigma0(words[t - 15]) + words[t - 16]) & MASK
    elif target == t - 2:
        image = (words[t] - words[t - 7] - sigma0(words[t - 15])
                 - words[t - 16]) & MASK
        value = inverse1(image)
    elif target == t - 7:
        value = (words[t] - sigma1(words[t - 2]) - sigma0(words[t - 15])
                 - words[t - 16]) & MASK
    elif target == t - 15:
        image = (words[t] - sigma1(words[t - 2]) - words[t - 7]
                 - words[t - 16]) & MASK
        value = inverse0(image)
    elif target == t - 16:
        value = (words[t] - sigma1(words[t - 2]) - words[t - 7]
                 - sigma0(words[t - 15])) & MASK
    else:
        raise ValueError("target absent from row")
    words[target] = value
    require(row_residual(words, t) == 0, "reverse solve did not satisfy its row")


def reconstruct(coordinates, certificate, inverse0, inverse1):
    words = dict(coordinates)
    required = set(EXPECTED_SUPPORT) | set(EXPECTED_ANCHORS)
    require(set(words) == required, "wrong reconstruction coordinate domain")
    for t, target in certificate["solve_steps"]:
        solve_target(words, t, target, inverse0, inverse1)
    require(set(words) == set(range(64)), "reconstruction did not assign 64 words")
    return [words[i] for i in range(64)]


def expand(block):
    require(len(block) == 16, "input block length")
    words = [value & MASK for value in block]
    for t in range(16, 64):
        words.append((sigma1(words[t - 2]) + words[t - 7]
                      + sigma0(words[t - 15]) + words[t - 16]) & MASK)
    require(all(row_residual(words, t) == 0 for t in range(16, 64)),
            "forward expansion failed its own rows")
    return words


def words_hash(words):
    return hashlib.sha256(b"".join(value.to_bytes(4, "big") for value in words)).hexdigest()


def roundtrip(certificate, inverse0, inverse1):
    blocks = [
        [0] * 16,
        list(range(16)),
        [((0x9E3779B9 * (i + 1)) ^ (0xA5A5A5A5 >> (i % 7))) & MASK for i in range(16)],
        [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A,
         0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19,
         0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5,
         0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5],
    ]
    fixed = set(EXPECTED_SUPPORT) | set(EXPECTED_ANCHORS)
    records = []
    schedules = []
    for number, block in enumerate(blocks):
        schedule = expand(block)
        coordinates = {index: schedule[index] for index in fixed}
        rebuilt = reconstruct(coordinates, certificate, inverse0, inverse1)
        require(rebuilt == schedule, "actual schedule roundtrip mismatch")
        residuals = {str(t): row_residual(rebuilt, t) for t in EXPECTED_RESIDUALS}
        require(set(residuals.values()) == {0}, "actual schedule residual is nonzero")
        records.append({"fixture": number, "input_sha256": words_hash(block),
                        "schedule_sha256": words_hash(schedule),
                        "residuals_hex": {key: f"{value:08x}" for key, value in residuals.items()}})
        schedules.append(schedule)
    return records, schedules


def verify_damaged_inverse(function, columns):
    damaged = list(columns)
    damaged[0] ^= 1
    require(any(function(damaged[bit]) != 1 << bit for bit in range(32)),
            "damaged inverse column escaped basis composition")


def negative_controls(certificate, inverse0, inverse1, inverse0_columns, schedules):
    controls = []

    damaged = copy.deepcopy(certificate)
    damaged["solve_steps"][0][1] = 18
    try:
        validate_structure(damaged)
    except ValueError as error:
        controls.append({"name": "known_coordinate_as_solve_target", "rejected": True,
                         "reason": str(error)})
    else:
        raise ValueError("damaged solve target accepted")

    damaged = copy.deepcopy(certificate)
    damaged["residual_rows"].pop()
    try:
        validate_structure(damaged)
    except ValueError as error:
        controls.append({"name": "omit_residual_row", "rejected": True,
                         "reason": str(error)})
    else:
        raise ValueError("omitted residual accepted")

    try:
        verify_damaged_inverse(sigma0, inverse0_columns)
    except ValueError as error:
        raise ValueError("inverse damage control implementation failed: " + str(error))
    controls.append({"name": "alter_sigma0_inverse_column", "rejected": True,
                     "reason": "basis composition differs from identity"})

    schedule = schedules[-1]
    fixed = set(EXPECTED_SUPPORT) | set(EXPECTED_ANCHORS)
    coordinates = {index: schedule[index] for index in fixed}
    coordinates[10] ^= 1
    rebuilt = reconstruct(coordinates, certificate, inverse0, inverse1)
    try:
        require(rebuilt == schedule, "roundtrip no longer equals the source schedule")
    except ValueError as error:
        controls.append({"name": "alter_fixed_roundtrip_coordinate", "rejected": True,
                         "reason": str(error)})
    else:
        raise ValueError("damaged roundtrip coordinate accepted")
    require(len(controls) == 4 and all(item["rejected"] for item in controls),
            "negative control count")
    return controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    support_path = ROOT / "supports-v2.json"
    certificate_path = HERE / "COORDINATE-CERTIFICATE.json"
    require(digest(support_path) == SUPPORT_HASH, "frozen support source changed")
    source = json.loads(support_path.read_text())
    require(source["supports"][12] == EXPECTED_SUPPORT, "support-12 source mismatch")
    certificate = json.loads(certificate_path.read_text())

    structure = validate_structure(certificate)
    minimality = exhaustive_minimality()
    inverse0_columns, inverse0 = inverse_columns(sigma0)
    inverse1_columns, inverse1 = inverse_columns(sigma1)
    roundtrips, schedules = roundtrip(certificate, inverse0, inverse1)
    controls = negative_controls(certificate, inverse0, inverse1, inverse0_columns, schedules)

    report = {
        "schema": "CRYPTO3-support12-independent-base-review-v8",
        "status": "PASS",
        "phase": "PRE-AUTHOR",
        "support_source_sha256": digest(support_path),
        "certificate_sha256": digest(certificate_path),
        "checker_sha256": digest(Path(__file__).resolve()),
        "structure": structure,
        "minimality": minimality,
        "sigma_permutations": {
            "sigma0_inverse_columns_hex": [f"{value:08x}" for value in inverse0_columns],
            "sigma1_inverse_columns_hex": [f"{value:08x}" for value in inverse1_columns],
            "basis_compositions_checked": 128
        },
        "actual_schedule_roundtrips": roundtrips,
        "negative_controls": controls,
        "author_files_read_or_imported": False,
        "claim": "exact five-anchor/two-residual base interpolation equivalence; minimal in the stated one-row reversible propagation class",
        "not_claimed": ["residual solvability", "actual active pair data", "full message pair",
                        "distance-13 attainability", "distance at least 14", "Lean formalization"]
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
