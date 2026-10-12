#!/usr/bin/env python3
"""Compare the frozen pre-author audit with the q=33..63 author package."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-v16-q33-63-v10"
MASK = (1 << 32) - 1
QS = tuple(range(33, 64, 2))


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def sigma(x, which):
    if which == 0:
        return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def parse_hex_fixture(item):
    return {key: int(value, 16) for key, value in item.items()}


def direct_check(q, item):
    d = q << 16
    x, xp, y, yp = (item[k] for k in ("x", "x_plus_D", "y", "y_plus_D"))
    need((xp - x) & MASK == d and (yp - y) & MASK == d,
         f"q={q}: author fixture has wrong D")
    need(x ^ xp == item["xor_x"] and y ^ yp == item["xor_y"],
         f"q={q}: author fixture has wrong xor mask")
    fx = (sigma(xp, 0) - sigma(x, 0)) & MASK
    fy = (sigma(yp, 0) - sigma(y, 0)) & MASK
    gx = (sigma(xp, 1) - sigma(x, 1)) & MASK
    gy = (sigma(yp, 1) - sigma(y, 1)) & MASK
    need(fx == fy == item["common_F"], f"q={q}: author fixture F mismatch")
    need(gx == item["G_x"] and gy == item["G_y"],
         f"q={q}: author fixture G mismatch")
    need((gy - gx) & MASK == item["G_gap"] == (2 * d) & MASK,
         f"q={q}: author fixture gap mismatch")
    # Pair reversal: an actual arithmetic check, not a symbolic assertion.
    nd = (-d) & MASK
    rfx = (sigma(x, 0) - sigma(xp, 0)) & MASK
    rfy = (sigma(y, 0) - sigma(yp, 0)) & MASK
    rgx = (sigma(x, 1) - sigma(xp, 1)) & MASK
    rgy = (sigma(y, 1) - sigma(yp, 1)) & MASK
    need(rfx == rfy == (-item["common_F"]) & MASK,
         f"q={q}: reversed author fixture F mismatch")
    need((rgy - rgx) & MASK == (2 * nd) & MASK,
         f"q={q}: reversed author fixture gap mismatch")


def main():
    pre = json.loads((HERE / "PRE_AUTHOR_RUN.json").read_text())
    cert = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    manifest = json.loads((AUTHOR / "SHA256.json").read_text())

    need(pre["status"] == cert["status"] == "PASS", "non-PASS input")
    need(tuple(pre["range"]["q_values"]) == QS, "independent range mismatch")
    need(tuple(cert["q_domain"]) == QS, "author range mismatch")
    need(len(cert["cases"]) == len(QS), "author case count mismatch")
    need(tuple(case["q"] for case in cert["cases"]) == QS,
         "author cases not exact ordered q range")

    manifest_checked = 0
    for name, expected in sorted(manifest["files"].items()):
        actual = hashlib.sha256((AUTHOR / name).read_bytes()).hexdigest()
        need(actual == expected, f"author manifest mismatch: {name}")
        manifest_checked += 1

    independent = {row["q"]: row for row in pre["results"]}
    comparisons = []
    author_fixture_count = 0
    author_negative_count = 0
    independent_fixture_count = 0
    exact_fixture_matches = 0
    leaf_signature_matches = 0
    for case in cert["cases"]:
        q = case["q"]
        own = independent[q]
        need(case["input_classes"] == own["input_classes"],
             f"q={q}: input class count disagreement")
        need(case["sigma0_leaves"] == own["sigma0_leaves"],
             f"q={q}: F leaf disagreement")
        need(case["full32_twin_leaves"] == own["full32_twin_leaves"],
             f"q={q}: twin leaf disagreement")
        author_hist = {str(k): v for k, v in sorted(Counter(case["class_sizes"]).items())}
        need(author_hist == own["class_size_histogram"],
             f"q={q}: class-size histogram disagreement")
        author_fixtures = [parse_hex_fixture(x)
                           for x in case["unique_recovered_fixtures"]]
        need(len(author_fixtures) == case["full32_twin_leaves"],
             f"q={q}: author fixture/leaf mismatch")
        need(len(own["fixtures"]) == own["full32_twin_leaves"],
             f"q={q}: independent fixture/leaf mismatch")
        for item in author_fixtures:
            direct_check(q, item)
            author_fixture_count += 1
            author_negative_count += 1
        independent_fixture_count += len(own["fixtures"])
        # Different elimination pivots/free-zero conventions may choose
        # different points of the same affine leaf.  The mask pair is the
        # stable leaf signature here; actual words are checked separately.
        author_keys = {tuple(sorted(x.items())) for x in author_fixtures}
        own_keys = {tuple(sorted(x.items())) for x in own["fixtures"]}
        exact_fixture_matches += len(author_keys.intersection(own_keys))
        author_signatures = {(x["xor_x"], x["xor_y"]) for x in author_fixtures}
        own_signatures = {(x["xor_x"], x["xor_y"]) for x in own["fixtures"]}
        need(len(author_signatures) == len(author_fixtures),
             f"q={q}: duplicate author leaf signature")
        need(len(own_signatures) == len(own["fixtures"]),
             f"q={q}: duplicate independent leaf signature")
        need(author_signatures == own_signatures,
             f"q={q}: affine leaf signatures disagree")
        leaf_signature_matches += len(author_signatures)
        comparisons.append({
            "q": q,
            "input_classes": case["input_classes"],
            "class_size_histogram_equal": True,
            "sigma0_leaves": case["sigma0_leaves"],
            "full32_twin_leaves": case["full32_twin_leaves"],
            "leaf_signature_set_equal": True,
            "exact_word_fixture_set_equal": author_keys == own_keys,
        })

    excluded = tuple(q for q in QS if independent[q]["full32_twin_leaves"] == 0)
    surviving = tuple(q for q in QS if independent[q]["full32_twin_leaves"] != 0)
    need(tuple(cert["excluded_positive_q"]) == excluded,
         "excluded-q summary disagreement")
    need(tuple(cert["surviving_positive_q"]) == surviving,
         "surviving-q summary disagreement")

    result = {
        "schema": "CRYPTO3-support12-v16-q33-63-author-comparison-v10",
        "status": "PASS",
        "q_values_compared": list(QS),
        "q_case_count": len(QS),
        "comparisons": comparisons,
        "excluded_positive_q": list(excluded),
        "surviving_positive_q": list(surviving),
        "author_manifest_files_checked": manifest_checked,
        "author_fixtures_directly_checked": author_fixture_count,
        "author_negative_reversals_directly_checked": author_negative_count,
        "independent_fixture_count": independent_fixture_count,
        "exact_fixture_matches": exact_fixture_matches,
        "leaf_signature_matches": leaf_signature_matches,
        "scope": "bounded selected twin condition only; not a third pair, support, message pair, distance-14 proof, or Lean formalization",
    }
    (HERE / "COMPARISON.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
