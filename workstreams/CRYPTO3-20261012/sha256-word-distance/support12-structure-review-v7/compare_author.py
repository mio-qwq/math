#!/usr/bin/env python3
"""Compare frozen author data with the previously frozen blind reconstruction.

No author-code imports. Read only unless --save writes this directory's RUN.json.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from check_signatures_independent import (HERE, SUPPORTS, PINNED_SUPPORTS, MASK,
    direct_f, sigma_rows, evaluate_rows, constraints, original_rows, combo,
    verify_packet)

AUTHOR = HERE.parent / "support12-structure-v7"
BLIND_MANIFEST_HASH = "3d2e2ab37250187ed2e9f643eb5475ee01e72ae7eca8a82c4485579f85410a2a"
AUTHOR_MANIFEST_HASH = "8a5d97b2f671ae416ed296267bc25df2835c053fa9d318b01bf5bc68c615288a"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def direct_g(x):
    r17 = ((x >> 17) | (x << 15)) & MASK
    r19 = ((x >> 19) | (x << 13)) & MASK
    return r17 ^ r19 ^ (x >> 10)


def v2(word):
    assert word != 0
    return (word & -word).bit_length()-1


def review_certificate(cert, packet):
    assert cert["schema"] == "CRYPTO3-support12-analytic-structure-v7"
    assert cert["definition"] == {"bits": 32, "f_rotations": [7, 18], "f_shift": 3,
                                   "g_rotations": [17, 19], "g_shift": 10}
    for index, transform in ((0, direct_f), (1, direct_g)):
        columns = cert["inverse_basis_columns"][str(index)]
        assert len(columns) == 32
        for bit, encoded in enumerate(columns):
            word = int(encoded, 16)
            assert 0 <= word <= MASK
            assert transform(word) == 1 << bit
    cases = cert["valuation_cases"]
    assert len(cases) == 1024
    indexed = {(case["a"], case["b"]): case for case in cases}
    assert len(indexed) == 1024
    assert set(indexed) == {(a, b) for a in range(32) for b in range(32)}
    rows = sigma_rows()
    reconstructed = [[False]*32 for _ in range(32)]
    for (a, b), case in indexed.items():
        equations = constraints(a, b, rows)
        if case["witness"] is not None:
            assert case["contradiction_rows"] is None
            word = int(case["witness"], 16)
            assert 0 < word <= MASK
            assert all((row & word).bit_count() % 2 == rhs for row, rhs in equations)
            assert v2(word) == a and v2(direct_f(word)) == b
            reconstructed[a][b] = True
        else:
            selected = case["contradiction_rows"]
            assert selected and len(selected) == len(set(selected))
            left = right = 0
            for i in selected:
                assert type(i) is int and 0 <= i < len(equations)
                left ^= equations[i][0]
                right ^= equations[i][1]
            assert left == 0 and right == 1
    assert reconstructed == packet["forward_signature_table"]
    allowed = [[a, b] for a in range(32) for b in range(32)
               if reconstructed[a][b] and reconstructed[b][a]]
    assert cert["necessary_transposed_signatures"] == allowed
    assert allowed == [[a, b] for a in range(32) for b in range(32)
                       if packet["anti_cycle_necessary_table"][a][b]]
    assert cert["consequences"] == {"allowed_count": 309, "maximum_individual": 23,
                                    "maximum_sum": 30}
    boundary_a16 = [b for a, b in allowed if a == 16]
    assert boundary_a16 == list(range(11)) + [12]
    half = cert["half_constants"]
    assert half == {"H": "80000000", "f_H": "11002000", "f_inv_H": "94857ee6",
                    "v_f_H": 13, "v_f_inv_H": 1}
    H = 1 << 31
    assert direct_f(H) == 0x11002000 and v2(direct_f(H)) == 13
    assert direct_f(0x94857EE6) == H and v2(0x94857EE6) == 1
    assert int(cert["inverse_basis_columns"]["0"][31], 16) == 0x94857EE6
    return {"all_1024_author_cases_match_blind_table": True,
            "all_64_inverse_basis_identities": True,
            "exact_309_transposed_entries_match": True, "a16_necessary_b_values": boundary_a16,
            "halfword_identities_and_valuation_mismatch": True}


def shifted_original_bridges(supports):
    results = []
    for sid, shift in ((12, 0), (6, 1), (7, 3), (13, 2)):
        support = supports[sid]
        assert support == [i + shift for i in supports[12]]
        rows = original_rows(support)
        assert combo(rows, {33+shift: -1}) == {f"d{26+shift}": 1, f"F{18+shift}": 1}
        assert combo(rows, {41+shift: -1, 34+shift: -1}) == {f"F{26+shift}": 1, f"d{18+shift}": 1}
        assert combo(rows, {42+shift: 1, 33+shift: -1}) == {f"d{42+shift}": 1, f"F{18+shift}": 1}
        results.append({"support_index": sid, "shift": shift,
                        "all_48_rows_reconstructed": True,
                        "reciprocal_and_d42_original_row_identities": True})
    return results


def negatives(cert, packet):
    impossible_index = next(i for i, case in enumerate(cert["valuation_cases"])
                            if case["witness"] is None)
    mutations = [
        ("missing_signature_case", lambda c: c["valuation_cases"].pop()),
        ("zero_positive_witness", lambda c: c["valuation_cases"][0].update(witness="00000000")),
        ("empty_infeasibility_xor", lambda c: c["valuation_cases"][impossible_index].update(contradiction_rows=[])),
        ("wrong_transposed_entry", lambda c: c["necessary_transposed_signatures"].append([31, 1])),
        ("wrong_f_inverse_column", lambda c: c["inverse_basis_columns"]["0"].__setitem__(31, "94857ee7")),
        ("wrong_g_inverse_column", lambda c: c["inverse_basis_columns"]["1"].__setitem__(0, "00000000")),
        ("false_halfword_valuation", lambda c: c["half_constants"].update(v_f_inv_H=13)),
    ]
    rejected = []
    for name, mutation in mutations:
        damaged = copy.deepcopy(cert)
        mutation(damaged)
        try:
            review_certificate(damaged, packet)
        except (AssertionError, KeyError):
            rejected.append(name)
        else:
            raise AssertionError("damaged author data accepted: " + name)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    blind_bytes = (HERE / "PRECOMPARISON_MANIFEST.json").read_bytes()
    assert digest(blind_bytes) == BLIND_MANIFEST_HASH
    for name, pinned in json.loads(blind_bytes)["files"].items():
        data = (HERE / name).read_bytes()
        assert len(data) == pinned["bytes"] and digest(data) == pinned["sha256"]
    packet = json.loads((HERE / "SIGNATURES.json").read_text())
    blind_result = verify_packet(packet)
    source = SUPPORTS.read_bytes()
    assert digest(source) == PINNED_SUPPORTS
    supports = json.loads(source)["supports"]
    author_bytes = (AUTHOR / "manifest.json").read_bytes()
    assert digest(author_bytes) == AUTHOR_MANIFEST_HASH
    manifest = json.loads(author_bytes)
    assert len(manifest["files"]) == 8
    hashes = {"manifest.json": AUTHOR_MANIFEST_HASH}
    for name, expected in manifest["files"].items():
        hashes[name] = digest((AUTHOR / name).read_bytes())
        assert hashes[name] == expected
    cert = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    checks = review_certificate(cert, packet)
    output = {"status": "PASS", "reviewer": "independent AI mathematical reviewer",
              "blind_manifest_sha256": BLIND_MANIFEST_HASH, "blind_snapshot_unchanged": True,
              "author_source_sha256": hashes, "independent_signature_results": blind_result,
              "author_comparison": checks, "all_four_support_bridges": shifted_original_bridges(supports),
              "negative_controls_rejected": negatives(cert, packet),
              "reviewer_comparison_source_sha256": digest(Path(__file__).read_bytes()),
              "written_claims_reviewed": {
                  "three_pair_I_D_membership_iff_selected_local_core": "PASS, third pair reversed with both output signs changed",
                  "four_pair_extra_D_in_R_A_iff_selected_local_equations": "PASS, additional forward-A preimage must exist; no base completion inferred",
                  "halfword_D_and_A_excluded_in_reciprocal_model": "PASS, valuation mismatch13 versus1 and f bijectivity",
                  "R_endpoints_disjoint_from_X_and_Y": "PASS conditional on fourth reciprocal coupling; not asserted for bare three-pair core",
                  "at_least_five_distinct_word_values": "PASS under selected four-pair model",
                  "reciprocal_f_model_has_nonzero_solution": "PASS for every permutation of an even cyclic group by finite-sum and collision argument"},
              "scope": "Exact selected-local image equivalences, reciprocal-pair necessary restrictions and structural consequences only.",
              "not_claimed": ["309 numerical reciprocal pairs are all realizable", "full support feasibility or exclusion", "actual16word message pair", "distance14", "Lean", "human review", "historical novelty", "publication"]}
    if args.save:
        (HERE / "RUN.json").write_text(json.dumps(output, indent=2, sort_keys=True)+"\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
