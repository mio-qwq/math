#!/usr/bin/env python3
"""Independent post-freeze audit of the author factor-signature package."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / "support12-factor-signature-v9"
MASK32 = (1 << 32) - 1
MASK26 = (1 << 26) - 1
NAMES = ("a", "b", "c", "k", "p", "q", "l", "s", "w", "z")


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK32


def sigma0(x, first=7):
    return rotr(x, first) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def sigma_bits(x, which, first=7):
    r1, r2, shift = (first, 18, 3) if which == 0 else (17, 19, 10)
    out = 0
    for bit in range(32):
        v = ((x >> ((bit + r1) % 32)) & 1) ^ ((x >> ((bit + r2) % 32)) & 1)
        if bit + shift < 32:
            v ^= (x >> (bit + shift)) & 1
        out |= v << bit
    return out


def word(raw):
    assert isinstance(raw, str) and len(raw) == 8
    value = int(raw, 16)
    assert 0 <= value <= MASK32
    return value


def ctz(value):
    assert value
    return (value & -value).bit_length() - 1


def add(*values):
    return sum(values) & MASK26


def neg(value):
    return (-value) & MASK26


def table(v):
    return {
        10: ("PF", v["a"], neg(v["b"]), None),
        11: ("PF", v["b"], v["p"], None),
        13: ("PF", v["c"], v["q"], None),
        15: ("J", v["k"], v["l"], neg(v["a"])),
        18: ("J", v["b"], neg(add(v["p"], v["a"])), neg(add(v["b"], v["c"]))),
        20: ("J", neg(v["b"]), neg(add(v["q"], v["s"])), neg(v["k"])),
        26: ("J", add(v["p"], v["a"]), neg(v["b"]), v["s"]),
        28: ("J", add(v["q"], v["s"]), neg(v["b"]), neg(v["l"])),
        29: ("J", v["c"], v["w"], neg(v["k"])),
        34: ("J", v["b"], neg(add(v["p"], v["a"])), add(v["b"], neg(v["c"]))),
        42: ("J", add(v["p"], v["a"]), v["z"], neg(add(v["w"], v["q"], v["s"]))),
        43: ("J", neg(v["b"]), neg(add(v["p"], v["a"])), neg(v["c"])),
        57: ("PG", v["z"], None, v["b"]),
    }


def check_certificate(data, sigma0_first=7):
    assert data["schema"] == "support12-factor-signature-v9-certificate-v1"
    low = data["low26"]
    assert low["width"] == 26 and word(low["fixed_b_residue"]) == 1 << 16
    assert set(low["scalars"]) == set(NAMES)
    values = {name: word(raw) for name, raw in low["scalars"].items()}
    assert all(value <= MASK26 for value in values.values())
    assert values["b"] == 1 << 16
    factors = table(values)
    assert set(map(int, low["pairs"])) == set(factors)
    rows = []
    for index, (kind, need_d, need_f, need_g) in factors.items():
        rec = low["pairs"][str(index)]
        assert set(rec) == {"kind", "x", "y"} and rec["kind"] == kind
        x, y = word(rec["x"]), word(rec["y"])
        f0x, f0y = sigma0(x, sigma0_first), sigma0(y, sigma0_first)
        f1x, f1y = sigma1(x), sigma1(y)
        assert f0x == sigma_bits(x, 0, sigma0_first)
        assert f0y == sigma_bits(y, 0, sigma0_first)
        assert f1x == sigma_bits(x, 1) and f1y == sigma_bits(y, 1)
        got = ((y - x) & MASK32, (f0y - f0x) & MASK32, (f1y - f1x) & MASK32)
        needs = (need_d, need_f, need_g)
        for actual, needed in zip(got, needs):
            if needed is not None:
                assert needed != 0 and (actual & MASK26) == needed
        alpha = x ^ y
        assert ctz(alpha) == ctz(got[0]) == ctz(need_d)
        if need_f is not None:
            assert (f0x ^ f0y) == sigma0(alpha, sigma0_first)
            assert ctz(sigma0(alpha, sigma0_first)) == ctz(got[1]) == ctz(need_f)
        if need_g is not None:
            assert (f1x ^ f1y) == sigma1(alpha)
            assert ctz(sigma1(alpha)) == ctz(got[2]) == ctz(need_g)
        rows.append({
            "index": index, "kind": kind,
            "d32": f"{got[0]:08x}", "F32": f"{got[1]:08x}", "G32": f"{got[2]:08x}",
            "d26": f"{got[0] & MASK26:08x}", "F26": f"{got[1] & MASK26:08x}",
            "G26": f"{got[2] & MASK26:08x}",
            "high6": [got[0] >> 26, got[1] >> 26, got[2] >> 26],
        })

    exact = data["exact_two_factor"]
    a, b, c, p = (word(exact[n]) for n in ("a", "b", "c", "p"))
    common_f = word(exact["common_F"])
    assert ctz(b) == 16 and common_f == (-(p + a)) & MASK32
    exact_rows = {}
    for index in (34, 43):
        x, y = (word(exact["pairs"][str(index)][n]) for n in ("x", "y"))
        assert sigma0(x) == sigma_bits(x, 0) and sigma0(y) == sigma_bits(y, 0)
        assert sigma1(x) == sigma_bits(x, 1) and sigma1(y) == sigma_bits(y, 1)
        exact_rows[index] = ((y - x) & MASK32,
                             (sigma0(y) - sigma0(x)) & MASK32,
                             (sigma1(y) - sigma1(x)) & MASK32)
    assert exact_rows[34] == (b, common_f, (b - c) & MASK32)
    assert exact_rows[43] == ((-b) & MASK32, common_f, (-c) & MASK32)
    return values, rows, {str(k): [f"{x:08x}" for x in v] for k, v in exact_rows.items()}


def reject_controls(pristine):
    controls = []
    cases = [
        ("wrong_fixed_b", lambda d: d["low26"]["scalars"].__setitem__("b", "00030000"), 7),
        ("damaged_pair18", lambda d: d["low26"]["pairs"]["18"].__setitem__("y", "dc00ddf8"), 7),
        ("damaged_shared_p", lambda d: d["low26"]["scalars"].__setitem__("p", "02621700"), 7),
        ("wrong_factor_kind", lambda d: d["low26"]["pairs"]["57"].__setitem__("kind", "PF"), 7),
        ("wrong_sigma0_rotation", lambda d: None, 8),
        ("damaged_exact_pair43", lambda d: d["exact_two_factor"]["pairs"]["43"].__setitem__("y", "56132ab6"), 7),
        ("damaged_exact_common_F", lambda d: d["exact_two_factor"].__setitem__("common_F", "c8877211"), 7),
    ]
    for name, mutate, first in cases:
        trial = copy.deepcopy(pristine); mutate(trial)
        try:
            check_certificate(trial, first)
        except (AssertionError, KeyError, ValueError):
            controls.append({"control": name, "rejected": True})
        else:
            raise AssertionError("negative control accepted: " + name)
    return controls


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest():
    manifest = json.loads((AUTHOR / "manifest.json").read_text())
    assert manifest["schema"] == "support12-factor-signature-v9-manifest-v1"
    for name, rec in manifest["files"].items():
        path = AUTHOR / name
        assert path.stat().st_size == rec["bytes"] and sha(path) == rec["sha256"]
    upstream = manifest["upstream"]
    assert sha(AUTHOR.parent / "support12-full-factor-v9" / "manifest.json") == upstream["support12_full_factor_v9_manifest_sha256"]
    assert sha(AUTHOR.parent / "support12-full-factor-v9" / "PROOF.md") == upstream["support12_full_factor_v9_proof_sha256"]
    assert sha(AUTHOR.parent / "support12-structure-v7" / "manifest.json") == upstream["support12_structure_v7_manifest_sha256"]
    return {"files": len(manifest["files"]), "upstream_bindings": len(upstream), "status": "PASS"}


def main():
    data = json.loads((AUTHOR / "CERTIFICATE.json").read_text())
    values, rows, exact = check_certificate(data)
    out = {
        "schema": "CRYPTO3-support12-factor-signature-review-v9-independent-audit",
        "status": "PASS",
        "scalars": {name: f"{value:08x}" for name, value in values.items()},
        "factor_count": len(rows),
        "factor_rows": rows,
        "direct_sigma_implementations_agree": True,
        "same_pair_J_factors": 9,
        "uncoupled_high_bits_per_projected_coordinate": 6,
        "exact_full32_factors_34_43": exact,
        "negative_controls": reject_controls(data),
        "manifest": check_manifest(),
        "scope": "low26 residue feasibility only, plus isolated exact full32 factors 34/43; no full32 13-factor, common-base, or message existence claim",
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
