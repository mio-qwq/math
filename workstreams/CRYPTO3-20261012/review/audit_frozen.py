#!/usr/bin/env python3
"""Bounded frozen-input audit; no support search or Bellman replay.

Run with a read-only snapshot of the CRYPTO2 workstream and the repository
checkout.  This imports only this reviewer's sigma implementation.
"""
from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import zlib

from small_checks import H, MASK, invert_binary_map, s0, s1

POTENTIAL_SHA256 = "1f04aa2b5ac13c5144e677cf75eb6d6af323d518abf96ec65a44a96fa07df23c"
CRYPTO2_SHA = "80b71cb3b6a67c8f8aae80d9cd8b6ed87d74bd51"
MAIN_SHA = "61488e05c9fe41984f483853f99e79f5715dc893"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_commit_bytes(repo, commit, prefix, disk_root, names):
    result = subprocess.run(["git", "ls-tree", "-rz", commit, "--", prefix],
                            cwd=repo, check=True, capture_output=True)
    blobs = {}
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        metadata, name = record.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        if kind == b"blob":
            blobs[name.decode()] = oid.decode()
    checked = []
    for name in names:
        data = (disk_root / name).read_bytes()
        oid = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        require(blobs.get(prefix + "/" + name) == oid, "snapshot bytes differ from frozen commit")
        checked.append({"path": name, "git_blob": oid, "sha256": hashlib.sha256(data).hexdigest()})
    return checked


def recurrence_terms(support, t):
    require(16 <= t <= 63, "recurrence outside standard range")
    # Move the four FIPS inputs to the left-hand side.
    raw = [("d", t, 1), ("G", t - 2, -1), ("d", t - 7, -1),
           ("F", t - 15, -1), ("d", t - 16, -1)]
    return {(name, position): sign for name, position, sign in raw
            if position in support}


def expected_exclusion(support, offset):
    u, x, a, r, b = (v + offset for v in (27, 34, 42, 43, 57))
    require(all(i in support for i in (u, x, a, r, b)), "missing active pivot")
    targets = [
        (x, {("d", x): 1, ("d", u): -1}),
        (r, {("d", r): 1, ("d", u): -1}),
        (r + 7, {("d", r): -1, ("d", x): -1}),
        (x + 15, {("d", a): -1, ("F", x): -1}),
        (b, {("d", b): 1, ("F", a): -1}),
        (b + 2, {("G", b): -1, ("d", r): -1}),
    ]
    result = []
    for t, target in targets:
        actual = recurrence_terms(support, t)
        require(actual == target, "reduced recurrence mismatch")
        result.append({"t": t, "terms": [[k, i, v] for (k, i), v in sorted(actual.items())]})
    return result


def check_tail(pairs):
    require(set(pairs) == {"x", "a", "r", "b"}, "tail labels")
    delta, fdiff, gdiff = {}, {}, {}
    for key, pair in pairs.items():
        require(len(pair) == 2 and all(type(x) is int and 0 <= x <= MASK for x in pair),
                "tail word format")
        w, wp = pair
        delta[key] = (wp - w) & MASK
        fdiff[key] = (s0(wp) - s0(w)) & MASK
        gdiff[key] = (s1(wp) - s1(w)) & MASK
        require(delta[key] != 0, "tail inactive pair")
    require((delta["r"] + delta["x"]) & MASK == 0, "tail cancellation")
    require(fdiff["r"] == fdiff["x"], "tail sigma0 matching")
    require((delta["a"] + fdiff["x"]) & MASK == 0, "tail first link")
    require(delta["b"] == fdiff["a"], "tail second link")
    require(gdiff["b"] == delta["x"], "tail final link")
    require(delta["x"] != H, "tail contradicts forced-H scope")
    return {key: f"0x{value:08x}" for key, value in delta.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crypto2-root", required=True, type=Path)
    parser.add_argument("--repo", required=True, type=Path)
    args = parser.parse_args()
    sha_root = args.crypto2_root / "projects/sha256-schedule-distance"
    v2 = sha_root / "v2"
    previous = json.loads((sha_root / "certificate.json").read_text())
    supplied = json.loads((v2 / "supports.json").read_text())
    supports = supplied["supports"]
    require(len(supports) == 15, "supplied list length")
    for support in supports:
        require(len(support) == 13 and support == sorted(set(support)), "support format")
        require(all(type(i) is int and 0 <= i <= 63 for i in support), "support range")
        require(any(i < 16 for i in support), "different inputs")
        for t in range(16, 64):
            require(sum(i in support for i in (t, t - 2, t - 7, t - 15, t - 16)) != 1,
                    "supplied support violates no-singleton")
    for i, fn in enumerate((s0, s1)):
        _, _, basis = invert_binary_map(fn)
        require(previous["sigma_inverse_columns"][i] == basis, "v1 inverse basis differs")
    raw = zlib.decompress(base64.b64decode(previous["potentials_zlib_base64"], validate=True))
    require(len(raw) == 49 * 65536, "potential length")
    require(hashlib.sha256(raw).hexdigest() == POTENTIAL_SHA256, "potential frozen hash")
    equations = {
        "3": expected_exclusion(set(supports[3]), 0),
        "14": expected_exclusion(set(supports[14]), -2),
    }
    tail = json.loads((v2 / "TAIL.json").read_text())
    tail_deltas = check_tail(tail["pairs"])
    negatives = []
    bad_support = set(supports[3]) | {32}
    try:
        expected_exclusion(bad_support, 0)
    except ValueError as exc:
        negatives.append({"case": "extra_active_sigma1_source", "rejected": str(exc)})
    else:
        raise ValueError("bad recurrence control accepted")
    bad_tail = copy.deepcopy(tail["pairs"])
    bad_tail["x"][0] ^= 1
    try:
        check_tail(bad_tail)
    except ValueError as exc:
        negatives.append({"case": "one_bit_tail_corruption", "rejected": str(exc)})
    else:
        raise ValueError("bad tail control accepted")
    structure_root = args.repo / "workstreams/ROOT/cryptographic-structures"
    provenance = json.loads((structure_root / "provenance.json").read_text())
    main_hashes = []
    for item in provenance["files"]:
        actual = sha256(structure_root / item["path"])
        require(actual == item["output_sha256"], "integrated artifact hash mismatch")
        main_hashes.append({"path": item["path"], "sha256": actual})
    source_names = ["PROOF.md", "certificate.json", "check.py", "v2/PROOF.md", "v2/check.py",
                    "v2/SOURCE-GATE.md", "v2/supports.json", "v2/exclusions.json", "v2/TAIL.json"]
    frozen_blobs = verify_commit_bytes(args.repo, CRYPTO2_SHA,
        "workstreams/CRYPTO2-20261011-7f3c/projects/sha256-schedule-distance", sha_root, source_names)
    main_blobs = verify_commit_bytes(args.repo, MAIN_SHA,
        "workstreams/ROOT/cryptographic-structures", structure_root,
        ["README.md", "VERIFICATION.json", "provenance.json"] + [item["path"] for item in provenance["files"]])
    print(json.dumps({
        "schema": "CRYPTO3-bounded-independent-review-v1",
        "passed": True,
        "checker_sha256": sha256(Path(__file__)),
        "sigma_implementation_sha256": sha256(Path(__file__).with_name("small_checks.py")),
        "frozen_crypto2_commit": CRYPTO2_SHA,
        "main_commit": MAIN_SHA,
        "source_file_sha256": {name: sha256(sha_root / name) for name in source_names},
        "snapshot_to_git_blob_checks": {"CRYPTO2": frozen_blobs, "main": main_blobs},
        "listed_supports_checked": 15,
        "no_singleton_tests_on_listed_supports": 15 * 48,
        "classification_completeness_traversal_rerun": False,
        "full_potential_inequalities_rerun": False,
        "potential_sha256": POTENTIAL_SHA256,
        "potential_bytes": len(raw),
        "inverse_columns_independently_recomputed": 64,
        "verified_exclusion_equations": equations,
        "tail_deltas": tail_deltas,
        "tail_scope": "Only the supplied five-equation boundary witness; no search and no actual expansion witness",
        "negative_controls": negatives,
        "integrated_main_output_hashes_checked": main_hashes,
        "lean_rerun": False,
    }, indent=2))


if __name__ == "__main__":
    main()
