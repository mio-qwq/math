#!/usr/bin/env python3
"""Standard-library verifier for the factor-signature and low-26 witnesses."""

import argparse
import copy
import hashlib
import json
import platform
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORD_MASK = (1 << 32) - 1
LOW_WIDTH = 26
LOW_MASK = (1 << LOW_WIDTH) - 1
SCALAR_NAMES = ("a", "b", "c", "k", "p", "q", "l", "s", "w", "z")


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & WORD_MASK


def sigma0(x, damaged=False):
    first = 8 if damaged else 7
    return rotr(x, first) ^ rotr(x, 18) ^ (x >> 3)


def sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)


def parse_word(value):
    assert isinstance(value, str) and len(value) == 8
    result = int(value, 16)
    assert 0 <= result <= WORD_MASK
    return result


def ctz(value):
    assert value != 0
    return (value & -value).bit_length() - 1


def factors(v):
    mod = 1 << LOW_WIDTH
    neg = lambda x: (-x) % mod
    add = lambda *xs: sum(xs) % mod
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


def verify(data, damaged_sigma0=False):
    assert data["schema"] == "support12-factor-signature-v9-certificate-v1"
    low = data["low26"]
    assert low["width"] == LOW_WIDTH
    assert parse_word(low["fixed_b_residue"]) == 1 << 16
    assert set(low["scalars"]) == set(SCALAR_NAMES)
    values = {name: parse_word(raw) for name, raw in low["scalars"].items()}
    assert all(value <= LOW_MASK for value in values.values())
    assert values["b"] == 1 << 16
    expected = factors(values)
    assert set(map(int, low["pairs"])) == set(expected)

    signatures = {}
    for index, (kind, d_need, f_need, g_need) in expected.items():
        record = low["pairs"][str(index)]
        assert record["kind"] == kind
        x = parse_word(record["x"])
        y = parse_word(record["y"])
        d_got = (y - x) & WORD_MASK
        f_got = (sigma0(y, damaged_sigma0) - sigma0(x, damaged_sigma0)) & WORD_MASK
        g_got = (sigma1(y) - sigma1(x)) & WORD_MASK
        assert (d_got & LOW_MASK) == d_need
        assert d_need != 0
        if f_need is not None:
            assert (f_got & LOW_MASK) == f_need
            assert f_need != 0
        if g_need is not None:
            assert (g_got & LOW_MASK) == g_need
            assert g_need != 0

        # Since each constrained low residue is nonzero, its valuation is below
        # 26 and therefore equals the valuation of the full derivative.  This
        # same actual XOR mask witnesses the joint triple for every J factor.
        alpha = x ^ y
        assert ctz(alpha) == ctz(d_got) == ctz(d_need)
        row = [ctz(d_need)]
        if f_need is not None:
            assert sigma0(x, damaged_sigma0) ^ sigma0(y, damaged_sigma0) == sigma0(alpha, damaged_sigma0)
            assert ctz(sigma0(alpha, damaged_sigma0)) == ctz(f_got) == ctz(f_need)
            row.append(ctz(f_need))
        else:
            row.append(None)
        if g_need is not None:
            assert sigma1(x) ^ sigma1(y) == sigma1(alpha)
            assert ctz(sigma1(alpha)) == ctz(g_got) == ctz(g_need)
            row.append(ctz(g_need))
        else:
            row.append(None)
        signatures[str(index)] = row

    exact = data["exact_two_factor"]
    a = parse_word(exact["a"])
    b = parse_word(exact["b"])
    c = parse_word(exact["c"])
    p = parse_word(exact["p"])
    common_f = parse_word(exact["common_F"])
    assert ctz(b) == 16
    assert all(value != 0 for value in (a, b, c, p, (p + a) & WORD_MASK))
    assert (-(p + a)) & WORD_MASK == common_f
    exact_values = {}
    for index in (34, 43):
        pair = exact["pairs"][str(index)]
        x = parse_word(pair["x"])
        y = parse_word(pair["y"])
        exact_values[index] = (
            (y - x) & WORD_MASK,
            (sigma0(y, damaged_sigma0) - sigma0(x, damaged_sigma0)) & WORD_MASK,
            (sigma1(y) - sigma1(x)) & WORD_MASK,
        )
    assert exact_values[34] == (b, common_f, (b - c) & WORD_MASK)
    assert exact_values[43] == ((-b) & WORD_MASK, common_f, (-c) & WORD_MASK)
    assert (exact_values[34][2] - exact_values[43][2]) & WORD_MASK == b

    return {
        "status": "PASS",
        "python": platform.python_version(),
        "low_width": LOW_WIDTH,
        "factors_checked": len(expected),
        "full_joint_factors": sum(kind == "J" for kind, _, _, _ in expected.values()),
        "partial_factors": sum(kind != "J" for kind, _, _, _ in expected.values()),
        "fixed_low26_b": f"{values['b']:08x}",
        "exact_two_factor_b": f"{b:08x}",
        "exact_two_factor_v2_b": ctz(b),
        "signatures": signatures,
        "scope": "SAT witness for the exact low-26 quotient of all 13 factors, plus an exact two-factor valuation-16 witness; not a full 32-bit factor solution or message pair.",
    }


def negative_controls(data):
    controls = []

    def rejected(name, mutate, damaged_sigma0=False):
        trial = copy.deepcopy(data)
        mutate(trial)
        try:
            verify(trial, damaged_sigma0=damaged_sigma0)
        except (AssertionError, KeyError, ValueError):
            controls.append({"control": name, "rejected": True})
            return
        raise AssertionError(f"negative control accepted: {name}")

    rejected("wrong_fixed_b", lambda d: d["low26"]["scalars"].__setitem__("b", "00030000"))
    rejected("damaged_pair18", lambda d: d["low26"]["pairs"]["18"].__setitem__("y", "dc00ddf8"))
    rejected("damaged_shared_p", lambda d: d["low26"]["scalars"].__setitem__("p", "02621700"))
    rejected("wrong_factor_kind", lambda d: d["low26"]["pairs"]["57"].__setitem__("kind", "PF"))
    rejected("wrong_sigma0_rotation", lambda d: None, damaged_sigma0=True)
    rejected("damaged_exact_pair43", lambda d: d["exact_two_factor"]["pairs"]["43"].__setitem__("y", "56132ab6"))
    rejected("damaged_exact_common_F", lambda d: d["exact_two_factor"].__setitem__("common_F", "c8877211"))
    return controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    cert_path = HERE / "CERTIFICATE.json"
    data = json.loads(cert_path.read_text())
    result = verify(data)
    result["checker_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["certificate_sha256"] = hashlib.sha256(cert_path.read_bytes()).hexdigest()
    if args.negative:
        result["negative_controls"] = negative_controls(data)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
