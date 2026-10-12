#!/usr/bin/env python3
"""Compare the frozen independent classification to the author certificate."""

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-v16-general-v9"
MASK = (1 << 32) - 1


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma(x, which):
    if which == 0:
        return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def h(text):
    return int(text, 16)


def validate_fixture(q, fixture):
    d = q << 16
    x, xp = h(fixture["x"]), h(fixture["x_plus_D"])
    y, yp = h(fixture["y"]), h(fixture["y_plus_D"])
    need((xp - x) & MASK == d and (yp - y) & MASK == d,
         f"q={q}: author fixture input difference")
    need((x ^ xp) == h(fixture["xor_x"]) and
         (y ^ yp) == h(fixture["xor_y"]),
         f"q={q}: author fixture XOR mask")
    fx = (sigma(xp, 0) - sigma(x, 0)) & MASK
    fy = (sigma(yp, 0) - sigma(y, 0)) & MASK
    gx = (sigma(xp, 1) - sigma(x, 1)) & MASK
    gy = (sigma(yp, 1) - sigma(y, 1)) & MASK
    need(fx == fy == h(fixture["common_F"]), f"q={q}: author fixture F")
    need(gx == h(fixture["G_x"]) and gy == h(fixture["G_y"]),
         f"q={q}: author fixture G values")
    need((gy - gx) & MASK == h(fixture["G_gap"]) == ((2 * d) & MASK),
         f"q={q}: author fixture G gap")

    # Independently evaluate the exact pair-reversed negative orientation.
    nd = (-d) & MASK
    rfx = (sigma(x, 0) - sigma(xp, 0)) & MASK
    rfy = (sigma(y, 0) - sigma(yp, 0)) & MASK
    rgx = (sigma(x, 1) - sigma(xp, 1)) & MASK
    rgy = (sigma(y, 1) - sigma(yp, 1)) & MASK
    need((x - xp) & MASK == nd and (y - yp) & MASK == nd,
         f"q={q}: reversed input difference")
    need(rfx == rfy == ((-fx) & MASK), f"q={q}: reversed F")
    need((rgy - rgx) & MASK == ((2 * nd) & MASK), f"q={q}: reversed G")


def main():
    independent_path = HERE / "PRE_AUTHOR_RUN.json"
    author_path = AUTHOR / "CERTIFICATE.json"
    independent = json.loads(independent_path.read_text())
    author = json.loads(author_path.read_text())
    need(author["schema"] == "CRYPTO3-support12-v16-q1-31-v9", "author schema")
    need(independent["status"] == author["status"] == "PASS", "statuses")
    need(author["q_domain"] == list(range(1, 32, 2)), "author q domain")
    need(len(independent["full32"]) == len(author["cases"]) == 16, "case count")

    independent_low = {row["q"]: row for row in independent["low31_control"]}
    case_comparison = []
    total_author_fixtures = 0
    total_independent_fixtures = 0
    for ours, theirs in zip(independent["full32"], author["cases"]):
        q = ours["q"]
        need(theirs["q"] == q, "case order")
        need(theirs["D"] == f"{q << 16:08x}", f"q={q}: D")
        need(theirs["input_classes"] == ours["input_class_count"],
             f"q={q}: input class count")
        author_hist = {str(size): count for size, count in
                       sorted(Counter(theirs["class_sizes"]).items())}
        need(author_hist == ours["input_class_size_histogram"],
             f"q={q}: complete class-size histogram")
        need(sum(theirs["class_sizes"]) == 1 << 16,
             f"q={q}: author upper-half cover")
        need(theirs["sigma0_leaves"] == ours["sigma0_leaves"],
             f"q={q}: sigma0 leaf count")
        need(theirs["low31_twin_leaves"] ==
             independent_low[q]["low31_twin_leaves"],
             f"q={q}: low31 twin leaf count")
        need(theirs["full32_twin_leaves"] == ours["twin_leaves"],
             f"q={q}: full twin leaf count")

        author_fixtures = theirs["unique_recovered_fixtures"]
        need(len(author_fixtures) == theirs["full32_twin_leaves"],
             f"q={q}: author fixture/leaf count")
        need(len({json.dumps(x, sort_keys=True) for x in author_fixtures}) ==
             len(author_fixtures), f"q={q}: duplicate author fixtures")
        for fixture in author_fixtures:
            validate_fixture(q, fixture)

        author_masks = Counter((f["xor_x"], f["xor_y"])
                               for f in author_fixtures)
        independent_masks = Counter((f"{f['xor_x']:08x}", f"{f['xor_y']:08x}")
                                    for f in ours["representatives"])
        need(author_masks == independent_masks,
             f"q={q}: surviving affine class-pair distribution")
        total_author_fixtures += len(author_fixtures)
        total_independent_fixtures += len(ours["representatives"])
        case_comparison.append({
            "q": q,
            "input_classes": ours["input_class_count"],
            "sigma0_leaves": ours["sigma0_leaves"],
            "low31_twin_leaves": independent_low[q]["low31_twin_leaves"],
            "full32_twin_leaves": ours["twin_leaves"],
            "surviving_mask_multiset_match": True,
            "all_author_fixtures_directly_checked": True,
        })

    excluded = [row["q"] for row in independent["full32"]
                if row["twin_leaves"] == 0]
    surviving = [row["q"] for row in independent["full32"]
                 if row["twin_leaves"] != 0]
    need(author["excluded_positive_q"] == excluded, "excluded q list")
    need(author["surviving_positive_q"] == surviving, "surviving q list")
    need(total_author_fixtures == total_independent_fixtures == 21,
         "total fixture count")
    need(author["controls"]["basis_rows_checked"] == 64, "basis control")
    need(author["controls"]["damaged_fixture_fields_rejected"] == 84,
         "author damaged-fixture control")
    need(author["controls"]["excluded_with_low31_frontier"] == [],
         "unexpected excluded low31 frontier")

    result = {
        "schema": "CRYPTO3-support12-v16-author-comparison-v9",
        "status": "PASS",
        "verdict": "ACCEPT",
        "author_certificate_sha256": hashlib.sha256(author_path.read_bytes()).hexdigest(),
        "author_checker_sha256": hashlib.sha256((AUTHOR / "check.py").read_bytes()).hexdigest(),
        "independent_run_sha256": hashlib.sha256(independent_path.read_bytes()).hexdigest(),
        "independent_checker_sha256": hashlib.sha256((HERE / "check_independent.py").read_bytes()).hexdigest(),
        "cases": case_comparison,
        "excluded_positive_q": excluded,
        "surviving_positive_q": surviving,
        "total_surviving_leaves": total_author_fixtures,
        "author_replay_observed": {
            "command": "python -B workstreams/CRYPTO3-20261012/sha256-word-distance/support12-v16-general-v9/check.py --negative",
            "status": "PASS",
            "elapsed_seconds": 190.3482551410052,
            "certificate_sha256": "f74dd80590b0e6b9c3f2ccb4841e9c39b94dd03a53c065dd16f3e48252854bd5"
        },
        "scope": "selected twin local condition only; no third pair, reciprocal edge, support assignment, message pair, or distance-14 proof",
        "comparison_checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output = HERE / "COMPARISON.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in (
        "status", "verdict", "excluded_positive_q", "surviving_positive_q",
        "total_surviving_leaves", "author_certificate_sha256")}, sort_keys=True))


if __name__ == "__main__":
    main()
