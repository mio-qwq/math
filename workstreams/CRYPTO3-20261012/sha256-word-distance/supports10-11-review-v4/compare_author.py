#!/usr/bin/env python3
"""Read author JSON as data only, then compare independently reconstructed facts."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

from check_independent import (HERE, BASE, WORD, PINNED, f, g, nullspace,
                              map_rows, full_span, derive)

AUTHOR = BASE / "supports10-11-v4"
PINNED_MANIFEST = "e85f54f94e7ca95271bd09f48a39814b509599eccb531a697b76a60912bb3dc5"


def valuation(value):
    return 32 if value == 0 else (value & -value).bit_length() - 1


def inspect_fixture(fixture):
    assert fixture["m"] in (1, 2)
    words = fixture["words"]
    x, xp, y, yp = (words[k] for k in ("x", "x_prime", "y", "y_prime"))
    assert all(isinstance(v, int) and 0 <= v <= WORD for v in (x, xp, y, yp))
    assert x != xp and y != yp
    A = (xp - x) & WORD
    C = (g(xp) - g(x)) & WORD
    E = (fixture["m"] * A + C) & WORD
    assert fixture["interfaces"] == {"A": A, "C": C, "E": E}
    assert A != 0 and E != 0
    residuals = [(yp - y + f(xp) - f(x)) & WORD,
                 (f(yp) - f(y) + fixture["m"] * A + C) & WORD]
    assert residuals == [0, 0]
    valuations = [valuation(A), valuation(E)]
    assert min(valuations) == 15
    return {"m": fixture["m"], "words": words, "interfaces": fixture["interfaces"],
            "actual_residuals": residuals, "valuations": valuations,
            "scope": "two actual ordered word pairs; not a full message or support assignment"}


def inspect_certificate(cert, independently):
    assert cert["schema"] == "supports10-11-two-pair-joint-valuation-v1"
    assert cert["definitions"] == {"bits": 32, "f_rotations": [7, 18], "f_shift": 3,
                                   "g_rotations": [17, 19], "g_shift": 10}
    assert cert["source_support_sha256"] == PINNED and cert["k"] == 16
    assert cert["kernel_X_rank"] == 31 and cert["kernel_Y_rank"] == 16
    assert [int(x, 16) for x in cert["kernel_X_basis"]] == independently["K_basis"]
    y_basis = [int(x, 16) for x in cert["kernel_Y_basis"]]
    assert len(y_basis) == 16
    assert all(f(x) & 65535 == 0 for x in y_basis)
    assert full_span(y_basis) == full_span(independently["L_basis"])
    assert int(cert["FX_xor_mask"], 16) == independently["fK"]
    assert cert["first_candidates"] == 65536
    assert cert["first_empty_histogram"] == independently["first_failure_histogram"]
    assert [int(x, 16) for x in cert["first_survivors"]] == independently["first_survivors"]
    for m in (1, 2):
        expected = {f"{row['L']:08x}": row["first_impossible_bit"]
                    for row in independently["second_exclusions"][str(m)]}
        assert cert["second_first_empty_bits"][str(m)] == expected
    assert [(b["support_index"], b["m"]) for b in cert["bridges"]] == [(10, 1), (11, 2)]
    for actual, bridge in zip(independently["bridges"], cert["bridges"]):
        assert bridge["active_indices"] == [18, 26, 34]
        equations = {}
        for equation in bridge["equations"]:
            t = str(equation["t"])
            assert t in actual["rows"]
            converted = {q.upper() + str(i) if q != "d" else q + str(i): c
                         for q, i, c in equation["terms"]}
            assert converted == actual["rows"][t]
            assert t not in equations
            equations[t] = converted
        def combo(weights):
            result = {}
            for t, coefficient in weights.items():
                for symbol, value in equations[t].items():
                    result[symbol] = result.get(symbol, 0) + coefficient * value
            return {symbol: value for symbol, value in result.items() if value}
        assert combo(bridge["core1_combination"]) == {"d26": 1, "F18": 1}
        assert combo(bridge["core2_combination"]) == {"F26": 1, "d18": bridge["m"], "G18": 1}
        assert combo(bridge["E_combination"]) == {"d34": 1, "d18": -bridge["m"], "G18": -1}
    assert [w["m"] for w in cert["boundary_fixtures"]] == [1, 2]
    return [inspect_fixture(w) for w in cert["boundary_fixtures"]]


def controls(cert, facts):
    mutations = [
        ("wrong_f_shift", lambda c: c["definitions"].update(f_shift=4)),
        ("wrong_stratum", lambda c: c.update(k=15)),
        ("wrong_X_rank", lambda c: c.update(kernel_X_rank=30)),
        ("wrong_Y_rank", lambda c: c.update(kernel_Y_rank=15)),
        ("missing_Y_basis", lambda c: c["kernel_Y_basis"].pop()),
        ("wrong_survivor", lambda c: c["first_survivors"].__setitem__(0, "4804ddd7")),
        ("wrong_second_failure", lambda c: c["second_first_empty_bits"]["2"].update({"4804ddd6": 26})),
        ("wrong_bridge_m", lambda c: c["bridges"][1].update(m=1)),
        ("wrong_core2_sign", lambda c: c["bridges"][1]["core2_combination"].update({"18": -1})),
        ("wrong_support_row", lambda c: c["bridges"][1]["equations"][2]["terms"].pop()),
        ("damaged_fixture", lambda c: c["boundary_fixtures"][0]["words"].update(x=0)),
        ("false_fixture_interface", lambda c: c["boundary_fixtures"][1]["interfaces"].update(E=0)),
    ]
    result = []
    for name, mutation in mutations:
        damaged = copy.deepcopy(cert)
        mutation(damaged)
        try:
            inspect_certificate(damaged, facts)
        except (AssertionError, KeyError):
            result.append(name)
        else:
            raise AssertionError("damaged certificate accepted: " + name)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true")
    args = parser.parse_args()
    manifest_bytes = (AUTHOR / "manifest.json").read_bytes()
    assert hashlib.sha256(manifest_bytes).hexdigest() == PINNED_MANIFEST
    manifest = json.loads(manifest_bytes)
    hashes = {name: hashlib.sha256((AUTHOR / name).read_bytes()).hexdigest()
              for name in manifest["files"]}
    assert hashes == manifest["files"]
    facts = json.loads((HERE / "RESULTS.json").read_text())
    cert = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    fixtures = inspect_certificate(cert, facts)
    output = {"status": "PASS", "independent_reconstruction_preceded_author_comparison": True,
              "author_manifest_sha256": PINNED_MANIFEST, "author_source_sha256": hashes,
              "complete_Y_kernel_sets_equal": True, "first_survivors_equal": True,
              "all_second_failures_equal": True, "all_original_bridge_rows_equal": True,
              "actual_local_sharpness": fixtures, "negative_controls": controls(cert, facts),
              "acceptance": "Written local joint-valuation theorem and both two-pair sharpness fixtures only"}
    if args.save:
        (HERE / "AUTHOR_COMPARISON.json").write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
