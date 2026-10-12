#!/usr/bin/env python3
"""Exact author-version comparison after the independent reconstruction."""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import check_valuation_independent as independent

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
EXPECTED = {
    "mechanism/VALUATION_BOUND.md": "1edca147825bae48618e56d65730b5cf62ab7ebf50faf085f9226f5f1d95c574",
    "mechanism/STRUCTURAL-CERTIFICATE.json": "6fb30742ea7a520e0ce61d57c1ccb1f443ddb51dead591c46728804a701bef1d",
    "mechanism/check_structural.py": "e1659b38a9b2f1e4949a53239e5a8de289128f8f969953e6ab316bb09c962077",
    "mechanism/RUNS.json": "29d81e8cfac78a606c6f031258b5d9fa45c4fa028ee03deed7e3b587d507f123",
    "mechanism/TWIN-V21-HALF-CARRY.json": "2e7f5d467d613f4778db912b713c141c3209a92b4103702fd52c069ce0ef5b9a",
    "mechanism/TWIN-RUN.json": "b0de2acb8ad6e63082dfa7b9cc89e00cc4f6612849b8db420474037ec79df918",
    "supports-v2.json": "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hashes() -> None:
    for name, expected in EXPECTED.items():
        independent.require(sha(PARENT / name) == expected, "changed unreviewed author bytes: " + name)


def verify_structural(cert: dict, own: dict) -> dict:
    need = independent.require
    f, g, hx = independent.f, independent.g, independent.hx
    need(cert["bits"] == 32 and cert["forbidden_divisibility_exponent"] == 21, "author object")
    need(cert["schema"] == "sha256-twin-divisibility-obstruction-v1", "author schema")
    desired_cases = [{"index": i, "shift": x-19, "x": x, "y": y, "r": r}
                     for i, x, y, r in independent.COORDINATES]
    need(cert["support_cases"] == desired_cases, "same four support coordinates")
    masks = [g((1 << (end+1)) - (1 << 21)) for end in range(21, 32)]
    need(cert["sigma1_masks_hex"] == [hx(mask) for mask in masks], "all eleven sigma1 masks")
    need(2 * max(masks[:-1]) < (1 << 22), "author non-top mask magnitude bound")
    need(len(cert["gap_bits"]) == 10, "complete author gap list")
    gaps = []
    for end, mask, h in zip(range(21, 31), masks[:-1], cert["gap_bits"]):
        need(type(h) is int and 1 <= h < 22, "gap below target bit")
        need(not ((mask | masks[-1]) >> (h-1)) & 1, "both preceding bits zero")
        need(((mask ^ masks[-1]) >> h) & 1 == 1, "one active gap bit")
        need(2 * ((1 << (h-1))-1) < (1 << h), "strict lower-contribution bound")
        gaps.append({"end": end, "sigma1_mask": hx(mask), "gap_bit": h})
    full = own["remaining_interval"]
    need(cert["alpha_hex"] == full["input_mask"], "common full interval")
    need(cert["sigma0_alpha_hex"] == full["f_mask"], "common sigma0 mask")
    need(cert["sigma1_alpha_hex"] == full["g_mask"], "common sigma1 mask")
    identity = own["parity_contradiction"]
    raw = sum(1 << i for i in cert["identity_raw_bits"])
    ff = sum(1 << i for i in cert["identity_sigma0_bits"])
    gg = sum(1 << i for i in cert["identity_sigma1_bits"])
    gg ^= 1 << cert["identity_target_sigma1_bit"]
    need((hx(raw), hx(ff), hx(gg)) == (identity["z_mask"], identity["f_mask"], identity["g_mask"]),
         "identical independently found parity identity")
    for i in range(32):
        z = 1 << i
        total = (z & raw).bit_count() + (f(z) & ff).bit_count() + (g(z) & gg).bit_count()
        need(total % 2 == 0, "author identity on each basis word")
    return {"support_coordinates_agree": True, "sigma1_masks_agree": 11,
            "author_sigma1_gap_obstructions": gaps,
            "independent_sigma0_gap_obstructions": own["mixed_interval_exclusions"],
            "universal_parity_identity_agrees": True,
            "original_recurrence_substitutions": 44, "integer_target_identities": 20}


def witness(words: dict, expected_delta: int | None = None) -> dict:
    need = independent.require
    f, g, hx, mask = independent.f, independent.g, independent.hx, independent.MASK
    a, ap, b, bp = [words[key] for key in ("x", "xp", "y", "yp")]
    need(all(type(v) is int and 0 <= v <= mask for v in (a, ap, b, bp)), "witness word range")
    delta = (ap-a) & mask
    need(delta and (bp-b) & mask == delta, "matching nonzero input differences")
    if expected_delta is not None:
        need(delta == expected_delta, "expected witness difference")
    fa, fb = (f(ap)-f(a)) & mask, (f(bp)-f(b)) & mask
    ga, gb = (g(ap)-g(a)) & mask, (g(bp)-g(b)) & mask
    need(fa == fb and (gb-ga) & mask == (2*delta) & mask, "exact twin equations")
    return {"words_hex": {key: hx(words[key]) for key in ("x", "xp", "y", "yp")},
            "delta": hx(delta), "F": hx(fa), "G_x": hx(ga), "G_y": hx(gb),
            "G_y_minus_G_x": hx((gb-ga) & mask),
            "ordinary_G_x": g(ap)-g(a), "ordinary_G_y": g(bp)-g(b),
            "scope": "two independent pairs; no third pair or complete schedule supplied"}


def main() -> None:
    check_hashes()
    source = (PARENT / "supports-v2.json").read_bytes()
    own = independent.rebuild(source)
    cert = json.loads((PARENT / "mechanism/STRUCTURAL-CERTIFICATE.json").read_text())
    structural = verify_structural(cert, own)
    half = json.loads((PARENT / "mechanism/TWIN-V21-HALF-CARRY.json").read_text())
    half_witnesses = [witness(case["witness"], 0x80200000) for case in half["cases"] if case["witness"]]
    independent.require(len(half_witnesses) == 12, "all twelve supplied positive half-stratum witnesses")
    explicit = witness({"x": 2147483648, "xp": 2097152,
                        "y": 697319424, "yp": 2846900224}, 0x80200000)
    independent.require(explicit == half_witnesses[0], "written witness matches supplied object")
    generic = json.loads((PARENT / "mechanism/TWIN-RUN.json").read_text())
    generic_checked = witness(generic["words"], generic["delta"])
    argv = [sys.executable, "-B", str(PARENT / "mechanism/check_structural.py"),
            str(PARENT / "supports-v2.json"), "--negative"]
    start = time.monotonic()
    run = subprocess.run(argv, text=True, capture_output=True)
    actual_run = {"argv": argv, "exit_code": run.returncode,
                  "elapsed_seconds": time.monotonic()-start,
                  "stdout": run.stdout, "stderr": run.stderr}
    independent.require(run.returncode == 0, "actual author structural checker execution")
    author_result = json.loads(run.stdout)
    independent.require(len(author_result["rejected_controls"]) == 6, "six author damaged controls")
    check_hashes()
    result = {
        "schema": "CRYPTO3-independent-irregular-valuation-review-v1",
        "status": "PASS",
        "review_kind": "independent AI reconstruction before reading author proof, then precise-version comparison; not human peer review",
        "python": platform.python_version(),
        "author_sha256": EXPECTED,
        "independent_sha256": {name: sha(HERE / name) for name in (
            "RECONSTRUCTION.md", "check_valuation_independent.py", "independent_valuation_certificate.json",
            "INDEPENDENT_RUN.json", "compare_valuation.py")},
        "structural_comparison": structural,
        "omitted_third_equation_boundary_witness": explicit,
        "all_supplied_half_stratum_witnesses": half_witnesses,
        "generic_twin_witness": generic_checked,
        "author_structural_checker_actual_rerun": actual_run,
        "accepted_statement": "For each exact support 6,7,12,13, the stated nonzero common difference D satisfies v2(D)<=20.",
        "limitations": [
            "A conditional valuation restriction; none of the four supports is completely excluded.",
            "The old potential certificate and support-classification completeness were not re-enumerated.",
            "The exploratory 121-case traversal and SAT/UNSAT results are not proof dependencies and were not rerun.",
            "Positive stored boundary word pairs were directly checked; unsupplied or null traversal cases make no claim here.",
            "No Lean compilation, novelty claim, external human review, or increased global schedule distance bound."
        ],
    }
    target = HERE / "REVIEW_RECEIPT.json"
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "receipt_sha256": sha(target),
                      "reviewed_proof_sha256": EXPECTED["mechanism/VALUATION_BOUND.md"],
                      "author_checker_exit_code": run.returncode,
                      "author_gap_cases": 10, "independent_gap_cases": 10,
                      "boundary_witnesses_directly_verified": len(half_witnesses)+1,
                      "scope": result["accepted_statement"]}, indent=2))


if __name__ == "__main__":
    main()
