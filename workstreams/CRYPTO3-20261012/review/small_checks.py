#!/usr/bin/env python3
"""Small independent checks of the SHA-256 word-distance prerequisites.

No import from the discovery code.  The sigma functions are reconstructed
bit by bit from FIPS 180-4 equations (4.6)-(4.7).  This does not enumerate
supports or replay the large lower-bound certificate.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

WIDTH = 32
MODULUS = 1 << WIDTH
MASK = MODULUS - 1
H = 1 << 31


def sigma(x: int, rotation_a: int, rotation_b: int, shift: int) -> int:
    """Output bit j uses input bits j+a, j+b (cyclic), and j+shift."""
    assert 0 <= x < MODULUS
    result = 0
    for j in range(WIDTH):
        bit = ((x >> ((j + rotation_a) % WIDTH)) & 1)
        bit ^= (x >> ((j + rotation_b) % WIDTH)) & 1
        if j + shift < WIDTH:
            bit ^= (x >> (j + shift)) & 1
        result |= bit << j
    return result


def s0(x: int) -> int:
    return sigma(x, 7, 18, 3)


def s1(x: int) -> int:
    return sigma(x, 17, 19, 10)


def invert_binary_map(fn):
    """Gauss-Jordan reduction of [A|I], with rows indexed by output bit."""
    columns = [fn(1 << j) for j in range(WIDTH)]
    rows = [sum(((columns[j] >> i) & 1) << j for j in range(WIDTH))
            | (1 << (WIDTH + i)) for i in range(WIDTH)]
    pivot_count = 0
    for col in range(WIDTH):
        pivot = next((i for i in range(pivot_count, WIDTH)
                      if (rows[i] >> col) & 1), None)
        if pivot is None:
            continue
        rows[pivot_count], rows[pivot] = rows[pivot], rows[pivot_count]
        for i in range(WIDTH):
            if i != pivot_count and (rows[i] >> col) & 1:
                rows[i] ^= rows[pivot_count]
        pivot_count += 1
    assert pivot_count == WIDTH
    assert [row & MASK for row in rows] == [1 << j for j in range(WIDTH)]
    inverse_rows = [row >> WIDTH for row in rows]
    def inverse(y: int) -> int:
        return sum(((row & y).bit_count() & 1) << j
                   for j, row in enumerate(inverse_rows))
    inverse_columns = [inverse(1 << j) for j in range(WIDTH)]
    assert all(fn(inverse_columns[j]) == 1 << j for j in range(WIDTH))
    assert all(inverse(fn(1 << j)) == 1 << j for j in range(WIDTH))
    return pivot_count, inverse, inverse_columns


def valuation(x: int, width: int = WIDTH) -> int:
    x %= 1 << width
    return width if x == 0 else (x & -x).bit_length() - 1


def require_equal(label: str, actual, expected):
    if actual != expected:
        raise ValueError(label)


def main():
    rank0, inv0, basis0 = invert_binary_map(s0)
    rank1, inv1, basis1 = invert_binary_map(s1)
    k = s0(H)
    h_preimage = inv1(H)
    require_equal("sigma0(H)", k, 0x11002000)
    require_equal("sigma1 inverse H", h_preimage, 0xC6EEAAD6)
    assert valuation(k) == 13
    assert valuation(h_preimage) == 1
    positions = [j for j in range(WIDTH) if (k >> j) & 1]
    possible_additive_differences = sorted({sum(sign << j for sign, j in zip(signs, positions)) & MASK
                                          for signs in itertools.product((-1, 1), repeat=len(positions))})
    assert len(possible_additive_differences) == 8
    assert all(valuation(d) == 13 for d in possible_additive_differences)
    assert all(valuation((-d) & MASK) == 13 for d in possible_additive_differences)
    # Added after disclosure of the complete v2 two-sigma0 proof: audit the
    # exact adjacent-quotient implication, including cyclic wraparound.
    carry_cases = 0
    for quotient in range(128):
        for sign in (-1, 1):
            alpha = quotient ^ ((quotient + sign) % 128)
            assert not (alpha & (1 << 6)) or bool(alpha & (1 << 5))
            carry_cases += 1
    assert all(d % (1 << 24) in (1 << 13, (1 << 24) - (1 << 13))
               for d in possible_additive_differences)
    # The weaker premise v2(delta_a)=13 alone would be invalid for the
    # second sigma0 link.  This exact example detects that overstatement.
    valuation_only_input = (1 << 13) + (1 << 19)
    assert valuation(valuation_only_input) == 13
    assert s0(valuation_only_input) % 4 == 2
    # Small exhaustive validation of the elementary valuation implementation;
    # the all-width statement has a written proof in review.md.
    low_width_pairs = 0
    for width in range(1, 8):
        for a in range(1 << width):
            for b in range(1 << width):
                assert valuation(b - a, width) == valuation(a ^ b, width)
                low_width_pairs += 1
    negative_controls = []
    for label, actual, expected in [
        ("corrupt_sigma0_constant", k, 0x11002001),
        ("corrupt_sigma1_inverse_constant", s1(h_preimage ^ 1), H),
        ("wrong_sigma0_rotation", sigma(H, 7, 17, 3), 0x11002000),
        ("wrong_sigma1_shift", sigma(h_preimage, 17, 19, 9), H),
    ]:
        try:
            require_equal(label, actual, expected)
        except ValueError:
            negative_controls.append({"case": label, "rejected": True})
        else:
            raise AssertionError(f"negative control accepted: {label}")
    print(json.dumps({
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "scope": "sigma bijectivity, constants, valuation obstruction; no support enumeration",
        "sigma0_rank": rank0,
        "sigma1_rank": rank1,
        "sigma0_H": f"0x{k:08x}",
        "sigma1_inverse_H": f"0x{h_preimage:08x}",
        "sigma0_inverse_basis": [f"0x{x:08x}" for x in basis0],
        "sigma1_inverse_basis": [f"0x{x:08x}" for x in basis1],
        "possible_sigma0_additive_differences_from_H": [f"0x{x:08x}" for x in possible_additive_differences],
        "valuation_sigma0_output": 13,
        "valuation_input_to_sigma1_output_H": 1,
        "adjacent_quotient_carry_cases": carry_cases,
        "valuation_only_premise_is_insufficient": {
            "a": "0x00000000",
            "a_prime": f"0x{valuation_only_input:08x}",
            "sigma0_difference": f"0x{s0(valuation_only_input):08x}",
            "sigma0_difference_mod4": 2,
        },
        "low_width_valuation_pairs_checked": low_width_pairs,
        "negative_controls": negative_controls,
        "passed": True,
    }, indent=2))


if __name__ == "__main__":
    main()
