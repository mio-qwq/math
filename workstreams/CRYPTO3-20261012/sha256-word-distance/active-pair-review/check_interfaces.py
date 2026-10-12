#!/usr/bin/env python3
"""Read-only reconstruction of all S0 equations and elementary pair interfaces."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform


MOD = 1 << 32
MASK = MOD - 1
Q = [2 + 14 * j for j in range(5)]
P = [9 + 14 * j for j in range(4)]
R = [10 + 14 * j for j in range(4)]
SUPPORT = {2, 9, 10, 16, 23, 24, 30, 37, 38, 44, 51, 52, 58}
NAMES = {**{i: f"Q{j}" for j, i in enumerate(Q)},
         **{i: f"P{j}" for j, i in enumerate(P)},
         **{i: f"R{j}" for j, i in enumerate(R)}}


def row(*terms):
    result = Counter()
    for operator, index, coefficient in terms:
        result[f"{operator}{index}"] += coefficient
    return {key: value for key, value in result.items() if value}


def canonical(value):
    ordered = sorted((key, coefficient) for key, coefficient in value.items() if coefficient)
    if ordered and ordered[0][1] < 0:
        ordered = [(key, -coefficient) for key, coefficient in ordered]
    return tuple(ordered)


def original_rows():
    result = {}
    for t in range(16, 64):
        all_terms = [("d", t, 1), ("G", t - 2, -1), ("d", t - 7, -1),
                     ("F", t - 15, -1), ("d", t - 16, -1)]
        result[t] = row(*(item for item in all_terms if item[1] in SUPPORT))
    return result


def family_rows():
    """Separate family formulas, including all left and right endpoints."""
    result = {t: {} for t in range(16, 64)}
    chain = [P[0], Q[1], P[1], Q[2], P[2], Q[3], P[3], Q[4]]
    for k, (before, after) in enumerate(zip(chain, chain[1:])):
        result[16 + 7 * k] = row(("d", after, 1), ("d", before, -1))
    for j in range(4):
        result[17 + 14 * j] = row(("d", R[j], 1), ("F", Q[j], 1))
        result[18 + 14 * j] = row(("G", Q[j + 1], 1), ("d", Q[j], 1))
    for j in range(3):
        result[24 + 14 * j] = row(("d", R[j + 1], 1), ("F", P[j], -1))
        result[25 + 14 * j] = row(("G", P[j + 1], 1), ("F", R[j], 1), ("d", P[j], 1))
        result[26 + 14 * j] = row(("G", R[j + 1], 1), ("d", R[j], 1))
    return result


def check_rows(candidate):
    if set(candidate) != set(range(16, 64)):
        raise ValueError("the complete 16..63 equation range is required")
    expected = family_rows()
    for t in range(16, 64):
        if canonical(candidate[t]) != canonical(expected[t]):
            raise ValueError(f"incorrect equation or omitted interface at t={t}")
    return True


def collapse_common_difference(value):
    common = {f"d{i}" for i in P + Q[1:]}
    result = Counter()
    for key, coefficient in value.items():
        result["D" if key in common else key] += coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def sigma(word, a, b, s):
    answer = 0
    for i in range(32):
        x = (word >> ((i + a) % 32)) & 1
        y = (word >> ((i + b) % 32)) & 1
        z = ((word >> (i + s)) & 1) if i + s < 32 else 0
        answer |= (x ^ y ^ z) << i
    return answer


def f(word):
    return sigma(word, 7, 18, 3)


def g(word):
    return sigma(word, 17, 19, 10)


def inverse_basis(function):
    columns = [function(1 << i) for i in range(32)]
    augmented = [sum(((columns[c] >> r) & 1) << c for c in range(32)) | (1 << (32 + r))
                 for r in range(32)]
    for c in range(32):
        pivot = next((r for r in range(c, 32) if (augmented[r] >> c) & 1), None)
        if pivot is None:
            raise AssertionError("sigma is not invertible")
        augmented[c], augmented[pivot] = augmented[pivot], augmented[c]
        for r in range(32):
            if r != c and ((augmented[r] >> c) & 1):
                augmented[r] ^= augmented[c]
    assert all((r & MASK) == 1 << i for i, r in enumerate(augmented))
    basis = [sum((((row >> 32) & (1 << j)).bit_count() & 1) << i
                 for i, row in enumerate(augmented)) for j in range(32)]
    assert all(function(basis[j]) == 1 << j for j in range(32))
    return basis


def apply_basis(basis, word):
    result = 0
    for j in range(32):
        if (word >> j) & 1:
            result ^= basis[j]
    return result


def r_chain(first_pair, images, g_inverse):
    if first_pair[0] == first_pair[1] or len(images) != 3:
        raise ValueError("an unequal initial R pair and three image parameters are required")
    pairs = [tuple(first_pair)]
    for z in images:
        difference = (pairs[-1][1] - pairs[-1][0]) % MOD
        next_pair = (apply_basis(g_inverse, z), apply_basis(g_inverse, (z - difference) % MOD))
        assert next_pair[0] != next_pair[1]
        assert ((g(next_pair[1]) - g(next_pair[0])) + difference) % MOD == 0
        pairs.append(next_pair)
    return pairs


def low_residues(xor_mask):
    return sorted({((x ^ (xor_mask & 7)) - x) % 8 for x in range(8)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    actual = original_rows()
    assert set(NAMES) == SUPPORT and len(NAMES) == 13
    check_rows(actual)
    assert sum(bool(r) for r in actual.values()) == 24
    # The seven links make exactly eight d coordinates equal to D.
    link_times = list(range(16, 59, 7))
    assert len(link_times) == 7 and all(not collapse_common_difference(actual[t]) for t in link_times)
    assert sum(bool(collapse_common_difference(r)) for r in actual.values()) == 17
    # Original equations t45 and t54 cancel the R2 difference.
    cancellation = Counter(actual[54])
    for key, value in actual[45].items():
        cancellation[key] -= value
    assert canonical(cancellation) == canonical(row(("G", 52, 1), ("F", 30, -1)))
    inverse_f, inverse_g = inverse_basis(f), inverse_basis(g)
    images = [0, MASK, 0x76543210]
    pairs = r_chain((0x12345678, 0x9ABCDEF0), images, inverse_g)
    recovered_images = [g(pair[0]) for pair in pairs[1:]]
    assert recovered_images == images
    assert r_chain(pairs[0], recovered_images, inverse_g) == pairs
    f_mask, g_mask = f(0x889B945B), g(0x4314A785)
    assert f_mask == 0x4314A785 and g_mask == 0xC722CCC1
    assert low_residues(f_mask) == [3, 5] and low_residues(g_mask) == [1, 7]
    assert set(low_residues(f_mask)).isdisjoint(low_residues(g_mask))
    damaged = []
    for t in [16, 17, 18, 58, 59, 60]:
        candidate = {u: dict(r) for u, r in actual.items()}
        candidate[t] = {}
        try:
            check_rows(candidate)
        except ValueError as error:
            damaged.append({"control": f"omit_boundary_t{t}", "rejected": True, "reason": str(error)})
        else:
            raise AssertionError("a missing boundary was accepted")
    candidate = {u: dict(r) for u, r in actual.items()}
    candidate[54]["G52"] *= -1
    try:
        check_rows(candidate)
    except ValueError as error:
        damaged.append({"control": "wrong_reverse_g_sign_t54", "rejected": True, "reason": str(error)})
    else:
        raise AssertionError("a wrong reverse-g sign was accepted")
    try:
        r_chain((5, 5), images, inverse_g)
    except ValueError as error:
        damaged.append({"control": "equal_initial_R_pair", "rejected": True, "reason": str(error)})
    else:
        raise AssertionError("a zero difference was accepted")
    equations = []
    for t, reduced in actual.items():
        equations.append({"t": t, "full_original_terms": [["d", t, 1], ["G", t-2, -1],
                          ["d", t-7, -1], ["F", t-15, -1], ["d", t-16, -1]],
                          "active_terms": reduced, "after_common_D_substitution": collapse_common_difference(reduced)})
    result = {
        "status": "PASS", "python": platform.python_version(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "independent active-pair equations; no base schedule or complete fibre audit",
        "support": sorted(SUPPORT), "coordinate_names": NAMES,
        "all_48_equations": equations, "nontrivial_equations": 24, "tautologies": 24,
        "common_D_link_times": link_times, "remaining_interfaces": 17,
        "sigma_inverse_basis": {"f": [f"{w:08x}" for w in inverse_f], "g": [f"{w:08x}" for w in inverse_g]},
        "inverse_basis_checks": 64,
        "r_parameterization_fixture": [[f"{w:08x}" for w in pair] for pair in pairs],
        "r_image_parameters": [f"{w:08x}" for w in images],
        "forced_interface": "G52 = F30 from t45 and t54",
        "fixed_xor_mod8": {"Q_xor": "889b945b", "R_xor": "4314a785", "f_Q_xor": f"{f_mask:08x}",
                           "g_R_xor": f"{g_mask:08x}", "F30_residues": low_residues(f_mask),
                           "G52_residues": low_residues(g_mask), "disjoint": True},
        "negative_controls": damaged,
    }
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.record:
        args.record.write_text(encoded)
    print(encoded, end="")


if __name__ == "__main__":
    main()
