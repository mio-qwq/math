#!/usr/bin/env python3
"""Post-freeze independent comparison with the author proof-v11 package."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / "support12-base-factor-normal-proof-v11"
AUTHOR_MANIFEST_SHA256 = "dc2c0a4d2f6bf9bf14c720c476a865d16d75aaf439c2d3a0de52fb63a5a7d8fe"
PRE_HASHES = {
    "PRE_AUTHOR_DERIVATION.md": "ae13e8b0b8371b5d0d30bd1f41003df9ed09081f0e90f58703558b79c5a19f1f",
    "PRE_AUTHOR_RUN.json": "d934e2e159265c72445d0609fe66b18f165b1bacb78d7c58965e8d6437ddfd50",
    "check_pre_author.py": "49006390aac3d6c87ee7709d57244e3a6f5fb1797ea9acb11be72cfdb9f84a90",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_pre():
    path = HERE / "check_pre_author.py"
    spec = importlib.util.spec_from_file_location("blind_v11", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def author_defs(pre, w, A):
    B = (-pre.d0(w[10], A)) & pre.M
    C = (-pre.d1(w[43], -B & pre.M)) & pre.M
    K = (-pre.d1(w[29], C)) & pre.M
    P = pre.d0(w[11], B)
    Q = pre.d0(w[13], C)
    L = pre.d0(w[15], K)
    T = pre.d1(w[26], (P + A) & pre.M)
    W = pre.d0(w[29], C)
    Z = pre.d0(w[42], (P + A) & pre.M)
    return {"a": A, "b": B, "c": C, "k": K, "p": P,
            "q": Q, "l": L, "s": T, "w": W, "z": Z}


def main():
    assert sha(AUTHOR / "SHA256.json") == AUTHOR_MANIFEST_SHA256
    manifest = json.loads((AUTHOR / "SHA256.json").read_text())
    assert set(manifest["files"]) == {"PROOF.md", "RUN.json", "check_symbolic.py"}
    for name, expected in manifest["files"].items():
        assert sha(AUTHOR / name) == expected
    assert {p.name for p in AUTHOR.iterdir() if p.is_file()} == {
        "PROOF.md", "RUN.json", "SHA256.json", "check_symbolic.py"
    }
    for name, expected in PRE_HASHES.items():
        assert sha(HERE / name) == expected

    rerun = subprocess.run(
        [sys.executable, "-B", str(AUTHOR / "check_symbolic.py")],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout
    assert rerun == (AUTHOR / "RUN.json").read_bytes()
    author_run = json.loads(rerun)

    pre = load_pre()
    author_eliminated = {
        "10F", "11F", "13F", "15F", "26G", "29F", "29G", "42F", "43G"
    }
    author_retained = (
        "15G", "18F", "18G", "20F", "20G", "26F", "28F", "28G",
        "34F", "34G", "42G", "43F", "57G",
    )
    assert author_run["symbolic_core"]["definitionally_zero_equations"] == [
        "10F", "11F", "13F", "15F", "26G", "29F", "29G", "42F", "43G"
    ]
    assert tuple(author_run["symbolic_core"]["retained_equations"]) == author_retained

    rng = random.Random(0xA1170B11)
    trials = 10000
    for _ in range(trials):
        inputs = {i: rng.getrandbits(32) for i in pre.T + pre.P}
        w = pre.chart(inputs)
        A = rng.getrandbits(32)
        values = author_defs(pre, w, A)
        eq = pre.local22(w, values)
        assert len(eq) == 22
        assert all(eq[name] == 0 for name in author_eliminated)
        assert tuple(name for name in eq if name not in author_eliminated) == author_retained
        assert all(value == 0 for value in pre.diff_rows(pre.difference_table(values)))
        classes = [values["a"], values["b"], values["c"], values["k"],
                   (values["p"] + values["a"]) & pre.M,
                   (values["q"] + values["s"]) & pre.M, values["z"]]
        ds = [pre.difference_table(values)[i][0] for i in pre.S]
        assert all(classes) == all(ds)
        # The retained word-57 equation is evaluated at the chart-forced H.
        assert eq["57G"] == (
            pre.d1(w[57], values["z"]) - values["b"]
        ) & pre.M

    audit = {
        "schema": "CRYPTO3-support12-base-factor-normal-review-v11-author-comparison",
        "status": "ACCEPT",
        "author_manifest_sha256": AUTHOR_MANIFEST_SHA256,
        "author_files_exact": True,
        "author_symbolic_rerun_byte_exact": True,
        "pre_author_freeze_intact": True,
        "independent_numeric_definition_trials": trials,
        "common_source_object": {
            "active_positions": list(pre.S),
            "original_factor_equalities": 22,
            "base_residuals_after_sink_merge": [33],
            "exact_support_nonzero_classes": ["a", "b", "c", "k", "p+a", "q+s", "z"],
        },
        "blind_chart": {
            "extra_free_factor_word": "z",
            "eliminated_factor_parameters": ["b", "k", "a", "c", "p", "q", "l", "s", "w"],
            "retained_factor_equations": list(pre.REMAINING),
        },
        "author_chart": {
            "extra_free_factor_word": "a",
            "definitionally_eliminated_equations": sorted(author_eliminated),
            "retained_factor_equations": list(author_retained),
        },
        "claims_accepted": {
            "bidirectional_exact_support12_schedule_pair_equivalence": True,
            "free_words": 18,
            "factor_equalities_22_to_13": True,
            "total_equalities_including_R33": 14,
            "exact_support_inequalities": 7,
            "H_and_R33_independent_of_temporary_u57": True,
            "position57_same_endpoint_condition": "D1(H,Z)=B",
            "first_16_words_are_message_blocks": True,
        },
        "claims_not_made_or_accepted": [
            "normal-form satisfiable", "normal-form unsatisfiable",
            "distance-13 message pair exists", "distance at least 14",
            "Lean formalisation", "human peer review",
        ],
        "scope": "Exact reformulation only; independent AI acceptance, not Lean or human certification.",
    }
    print(json.dumps(audit, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
