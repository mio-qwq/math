#!/usr/bin/env python3
"""Compare frozen author artifacts with an already reconstructed checker.

Imports only the reviewer-owned checker. The discoverer's check.py is
hashed as bytes, never imported, parsed as Python, or executed.
"""
import argparse
import copy
import json
from pathlib import Path

from check_independent import HERE, ROOT, REPRESENTATIVES, certify_map, digest, require

CANDIDATE = ROOT / "shift-reduction-v3"
REVIEWED_BASE = "b7eb3becacf474a6978b6acb2879fce3d505e395"
AUTHOR_MAPS = [(0, 1, 9), (1, 1, 0), (2, 2, 0), (4, 3, 0),
               (6, 1, 12), (13, 2, 12), (7, 3, 12),
               (0, -1, 1), (0, -2, 2), (0, -3, 4)]


def compare_results(results: dict, supports: list[set[int]]) -> list[dict]:
    require(results["representative_supports"] == REPRESENTATIVES, "wrong representative cover")
    claims = []
    require(len(results["implications"]) == 10, "wrong number of author maps")
    observed = []
    for item in results["implications"]:
        direction = item["direction"]
        require(direction in ("left", "right"), "invalid shift direction")
        offset = item["shift"] * (1 if direction == "left" else -1)
        observed.append((item["source"], offset, item["target"]))
        independent = certify_map(supports, item["source"], offset, item["target"])
        source_rows = item["tail"] if offset > 0 else item["prefix"]
        require(len(source_rows) == len(independent["boundary_rows"]), "boundary count mismatch")
        for row, verified in zip(source_rows, independent["boundary_rows"]):
            require(row["t"] == verified["original_recurrence_index"], "recurrence index mismatch")
            key = "lags" if offset > 0 else "rhs_indices"
            require(row[key] == [term["index"] for term in verified["terms"]], "dependency mismatch")
            require(row["active_dependencies"] == [], "author claims active boundary dependencies")
            require(verified["conclusion"] == "zero", "boundary not proven equal")
            if offset < 0:
                require(row["new_shared_index"] == verified["new_old_index"], "inverse index mismatch")
        claims.append(independent)
    require(observed == AUTHOR_MAPS, "author's stated support maps differ")
    return claims


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest = json.loads((CANDIDATE / "manifest.json").read_text())
    for name, expected in manifest["files_sha256"].items():
        require(digest(CANDIDATE / name) == expected, "candidate file hash mismatch: " + name)
    require((CANDIDATE / "supports-v2.json").read_bytes() == (ROOT / "supports-v2.json").read_bytes(),
            "support copies differ")
    supports = [set(s) for s in json.loads((ROOT / "supports-v2.json").read_text())["supports"]]
    results = json.loads((CANDIDATE / "RESULTS.json").read_text())
    require(json.loads((CANDIDATE / "check.log").read_text()) == results, "author log differs from result")
    reviewed = compare_results(results, supports)
    special = certify_map(supports, 3, 2, 14)
    require(special["deleted_active_original_indices"] == [1], "special map cropped wrong active word")
    require(special["added_active_old_indices"] == [64], "special map added wrong active word")
    require(special["boundary_rows"][0]["terms"][1]["index"] == 57, "special identity term")
    require(special["boundary_rows"][0]["terms"][1]["symbol"] == "d", "special term is not direct")
    require(special["boundary_rows"][0]["conclusion"] == "nonzero", "special tail64 not active")
    require(special["boundary_rows"][1]["conclusion"] == "zero", "special tail65 not equal")
    negative = []
    for label, change in [
        ("damaged_author_target", lambda r: r["implications"][0].__setitem__("target", 0)),
        ("damaged_author_tail_dependency", lambda r: r["implications"][0]["tail"][0]["lags"].__setitem__(0, 61)),
        ("damaged_author_representative_list", lambda r: r["representative_supports"].pop()),
        ("damaged_author_backward_index", lambda r: r["implications"][-1]["prefix"][-1].__setitem__("new_shared_index", -4)),
    ]:
        damaged = copy.deepcopy(results)
        change(damaged)
        try:
            compare_results(damaged, supports)
        except ValueError as error:
            negative.append({"name": label, "rejected": True, "reason": str(error)})
        else:
            raise ValueError("damaged author record accepted: " + label)
    source_paths = [ROOT / "supports-v2.json"]
    source_paths += sorted(CANDIDATE.iterdir())
    reviewed_sources = [{"path": str(p.relative_to(ROOT.parent)), "bytes": p.stat().st_size,
                         "sha256": digest(p)} for p in source_paths if p.is_file()]
    independent = json.loads((HERE / "INDEPENDENT_RUN.json").read_text())
    require(independent["checker_source_sha256"] == digest(HERE / "check_independent.py"),
            "independent run belongs to another checker version")
    data = {
        "schema": "crypto3-shift-independent-review-receipt-v4",
        "reviewer": "separate AI sub-agent /root/shift_review; not external human peer review",
        "reviewed_base_commit": REVIEWED_BASE,
        "candidate_path": "workstreams/CRYPTO3-20261012/sha256-word-distance/shift-reduction-v3",
        "review_status": "ACCEPTED_WITH_EXPLICIT_INHERITED_PREMISES",
        "source_hashes": reviewed_sources,
        "reviewer_checker_sha256": digest(HERE / "check_independent.py"),
        "comparison_checker_sha256": digest(Path(__file__).resolve()),
        "independent_run_sha256": digest(HERE / "INDEPENDENT_RUN.json"),
        "independent_written_proof_sha256": digest(HERE / "INDEPENDENT_PROOF.md"),
        "candidate_manifest_verified": True,
        "candidate_log_matches_frozen_results": True,
        "candidate_checker_imported_or_executed": False,
        "reconstruction_preceded_candidate_proof_read": True,
        "accepted_author_maps": reviewed,
        "accepted_special_map": special,
        "accepted_universal_statements": [
            "unique bilateral extension of any actual sixteen-word input",
            "any translated sixteen-word window re-expands to the translated sequence",
            "two distinct original sixteen-word inputs stay distinct under every time translation",
            "six-representative existence equivalence conditional on fifteen-support classification and exclusion of support14",
        ],
        "inherited_premises_not_reproved_here": [
            "global distance lower bound thirteen and complete fifteen-support classification",
            "unconditional impossibility of support14",
        ],
        "original_support3_exclusion_is_not_needed_for_coverage": True,
        "negative_comparison_controls": negative,
        "independent_boundary_negative_controls": len(independent["negative_controls"]),
        "author_random_tests_not_accepted_as_proof": True,
        "independent_concrete_tests_scope": independent["implementation_crosschecks"],
        "extra_safe_maps": [m for m in independent["exhaustive_safe_maps"]
                            if (m["source"], m["offset"], m["target"]) not in AUTHOR_MAPS + [(3, 2, 14)]],
        "extra_maps_reduce_representative_count": False,
        "unaccepted_or_unclaimed": [
            "existence of an actual distance13 message pair",
            "distance lower bound14",
            "unconditional reverse implications from support9 or support12",
            "candidate check.py code correctness or replay of its historical executions",
            "formal proof-assistant certification or full SHA-256 hash security assertion",
            "historical novelty or external human peer review",
        ],
    }
    rendered = json.dumps(data, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
