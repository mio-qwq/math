#!/usr/bin/env python3
"""Compare an exact discoverer version after the independent reconstruction.

No discoverer Python module is imported. The root checker is separately run
as a subprocess to retain its actual result, in addition to independent data
comparison against check_independent.py.
"""

from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

import check_independent as independent

HERE = Path(__file__).resolve().parent
PARENT = HERE.parent
EXPECTED = {
    "LOCAL_PROOF.md": "608752c21bbdc43ad5540a3b7f34ce1e2f55c0531df66864b68aa6c53943598b",
    "build_local_certificate.py": "43e10b848c0b72981ec0944d64e4f3419248b1c3d2f13fceacf0d312aa1e9ffe",
    "check_local.py": "9d10e42aacd2704afb927411fa1bba62a23cd2abe00e769868b974d3ae63a5dc",
    "local_certificate.json": "fe8f32f4dfababf27438aad8470ef10671afb2c3ef21fc28e96284065cc7ed11",
    "LOCAL_RUNS.json": "2140c80edfd479868729c8fcc9865b26082488d9894cbafedff2f257904d3517",
    "supports-v2.json": "02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_hashes() -> None:
    for name, expected in EXPECTED.items():
        actual = sha(PARENT / name)
        if actual != expected:
            raise ValueError(f"unreviewed changed version: {name}: {actual}")


def independent_bridges(cert: dict, supports: list[list[int]]) -> list[dict]:
    result = []
    for item in cert["support_bridges"]:
        index, u = item["index"], item["u"]
        support = set(supports[index])
        assert item["support"] == supports[index]
        assert {u, u+7, u+14} <= support
        expected = [
            {("d", u+7): 1, ("d", u): -1},
            {("d", u+14): 1, ("d", u+7): -1},
            {("g", u+14): -1, ("d", u): -1},
        ]
        rows = []
        for t, target in zip((u+7, u+14, u+16), expected):
            assert 16 <= t < 64
            terms = [("d", t, 1), ("g", t-2, -1),
                     ("d", t-7, -1), ("f", t-15, -1),
                     ("d", t-16, -1)]
            row = {(kind, position): coefficient
                   for kind, position, coefficient in terms if position in support}
            assert row == target
            rows.append({"t": t, "terms": [{"kind": key[0], "index": key[1],
                         "coefficient": coefficient} for key, coefficient in row.items()]})
        result.append({"support_index": index, "u": u,
                       "h_collision_word": u+14, "recurrences": rows})
    assert [(r["support_index"], r["u"]) for r in result] == [
        (0, 30), (1, 31), (2, 32), (4, 33), (8, 29), (9, 29)]
    return result


def main() -> None:
    check_hashes()
    own = independent.rebuild()
    cert = json.loads((PARENT / "local_certificate.json").read_text())
    assert cert["sigma1"] == {"rotations": [17, 19], "right_shift": 10}
    assert cert["projection_rank"] == own["low13"]["map_rank"] == 26
    their_masks = {r["alpha"]: (r["beta"], r["first_empty_bit"])
                   for r in cert["carry_exclusions"]}
    our_masks = {int(r["xor_mask"], 16):
                 (int(r["sigma1_mask"], 16), r["first_obstruction_bit"])
                 for r in own["low13"]["cases"]}
    assert len(their_masks) == 63 and their_masks == our_masks
    assert independent.rank(cert["kernel_basis"]) == 6
    assert all(v in our_masks for v in cert["kernel_basis"])
    histogram = dict(sorted(Counter(first for _, first in their_masks.values()).items()))

    match = own["power_of_two"]["same_start_interval_images"][0]
    assert cert["power2_interval_matches"] == [{
        "k": match["k"], "input_last": match["last"],
        "output_last": match["image_last"],
        "alpha": int(match["xor_mask"], 16),
        "beta": int(match["sigma1_mask"], 16)}]
    assert cert["power2_boundary_pairs"] == [[0x7fffffff, 0x80000000], [0xffffffff, 0]]
    sharp = cert["local_sharpness"]
    witness = independent.witness_record(sharp["x"], sharp["y"])
    assert sharp["delta"] == int(witness["additive_delta_y_minus_x"], 16)
    assert sharp["sigma1_x"] == int(witness["sigma1_x"], 16)
    assert sharp["sigma1_y"] == int(witness["sigma1_y"], 16)
    assert sharp["h"] == int(witness["h_x"], 16)
    assert witness["xor_mask"] == own["low12"]["surviving_masks"][0]
    boundary_sigma_deltas = []
    for x, y in cert["power2_boundary_pairs"]:
        boundary_sigma_deltas.append(independent.hx(
            (independent.sigma1(y)-independent.sigma1(x)) & independent.MASK))
    assert boundary_sigma_deltas == ["0000a001", "ffc00001"]

    supports = json.loads((PARENT / "supports-v2.json").read_text())["supports"]
    bridges = independent_bridges(cert, supports)
    argv = [sys.executable, "-B", str(PARENT / "check_local.py"), "--negative"]
    start = time.monotonic()
    run = subprocess.run(argv, text=True, capture_output=True)
    actual_run = {"argv": argv, "exit_code": run.returncode,
                  "elapsed_seconds": time.monotonic()-start,
                  "stdout": run.stdout, "stderr": run.stderr}
    assert run.returncode == 0
    actual = json.loads(run.stdout)
    assert actual["status"] == "PASS"
    assert len(actual["negative_controls"]) == 11
    check_hashes()
    result = {
        "schema": "CRYPTO3-independent-local-review-receipt-v1",
        "status": "PASS",
        "review_kind": "independent AI reconstruction followed by exact-version comparison; not human peer review",
        "python": platform.python_version(),
        "discoverer_sha256": EXPECTED,
        "independent_sha256": {name: sha(HERE / name) for name in (
            "check_independent.py", "independent_certificate.json", "INDEPENDENT_PROOF.md",
            "INDEPENDENT_RUN.json", "RECONSTRUCTION.md", "compare_discoverer.py")},
        "common_nonzero_low13_masks": 63,
        "complete_low13_alpha_beta_first_failure_agreement": True,
        "failure_histogram": histogram,
        "complete_power2_interval_agreement": True,
        "discoverer_witness_independently_recomputed": witness,
        "boundary_sigma_deltas": boundary_sigma_deltas,
        "post_reconstruction_conditional_bridge_checks": bridges,
        "discoverer_checker_actual_rerun": actual_run,
        "independent_additional_lemma": "Among all 255 nonzero low12 kernel masks, only fbca7000 survives the necessary carry obstruction.",
        "limitations": [
            "No new full-schedule distance bound or complete support exclusion.",
            "The six bridge checks are conditional on the supplied exact supports; the old support classification and potential certificate were not replayed here.",
            "No Lean compilation, external human peer review, or novelty claim.",
            "Subsequent changes to any reviewed discoverer bytes require a new precise-version receipt."
        ],
    }
    target = HERE / "REVIEW_RECEIPT.json"
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "receipt_sha256": sha(target),
                      "reviewed_proof_sha256": EXPECTED["LOCAL_PROOF.md"],
                      "discoverer_run_exit": run.returncode,
                      "common_masks": len(their_masks), "conditional_recurrences": 18,
                      "root_witness": witness}, indent=2))


if __name__ == "__main__":
    main()
