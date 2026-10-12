#!/usr/bin/env python3
"""Exact support-12 base interpolation chart; see PROOF.md."""

MASK = (1 << 32) - 1
SUPPORT = (10, 11, 13, 15, 18, 20, 26, 28, 29, 34, 42, 43, 57)
PARAMETERS = (9, 12, 14, 19, 22)
RESIDUAL_INDICES = (33, 57)
ORDER = (
    (26, 24), (28, 21), (29, 27), (34, 32), (36, 36), (43, 41),
    (27, 25), (41, 39), (25, 23), (30, 30), (39, 37), (44, 44),
    (37, 35), (42, 40), (35, 33), (40, 38), (45, 45), (38, 31),
    (46, 46), (47, 47), (48, 48), (49, 49), (50, 50), (51, 51),
    (52, 52), (53, 53), (54, 54), (55, 55), (56, 56), (58, 58),
    (59, 59), (60, 60), (61, 61), (62, 62), (63, 63), (31, 16),
    (32, 17), (24, 8), (23, 7), (22, 6), (21, 5), (20, 4),
    (19, 3), (18, 2), (17, 1), (16, 0),
)


def rotr(word, count):
    return ((word >> count) | (word << (32 - count))) & MASK


def sigma0(word):
    return rotr(word, 7) ^ rotr(word, 18) ^ (word >> 3)


def sigma1(word):
    return rotr(word, 17) ^ rotr(word, 19) ^ (word >> 10)


def inverse_map(fn):
    basis = {}
    for j in range(32):
        value, preimage = fn(1 << j), 1 << j
        while value:
            pivot = (value & -value).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = value, preimage
                break
            value ^= basis[pivot][0]
            preimage ^= basis[pivot][1]
        else:
            raise ValueError("small sigma is singular")
    if len(basis) != 32:
        raise ValueError("incomplete inverse basis")

    def inverse(value):
        result = 0
        while value:
            pivot = (value & -value).bit_length() - 1
            value ^= basis[pivot][0]
            result ^= basis[pivot][1]
        return result
    return inverse


INV0 = inverse_map(sigma0)
INV1 = inverse_map(sigma1)


def complete(active, parameters):
    """Construct all words satisfying 46 rows and return both residuals."""
    if set(active) != set(SUPPORT) or set(parameters) != set(PARAMETERS):
        raise ValueError("wrong interpolation coordinates")
    values = list(active.values()) + list(parameters.values())
    if any(type(value) is not int or not 0 <= value <= MASK for value in values):
        raise ValueError("values must be unsigned 32-bit words")
    words = [None] * 64
    for i, value in list(active.items()) + list(parameters.items()):
        words[i] = value
    identity = lambda x: x
    for t, target in ORDER:
        inputs = ((t - 2, sigma1, INV1), (t - 7, identity, identity),
                  (t - 15, sigma0, INV0), (t - 16, identity, identity))
        positions = [t] + [position for position, _, _ in inputs]
        if [position for position in positions if words[position] is None] != [target]:
            raise ValueError("invalid elimination dependency")
        if target == t:
            words[target] = sum(fn(words[position]) for position, fn, _ in inputs) & MASK
        else:
            others = sum(fn(words[position]) for position, fn, _ in inputs
                         if position != target)
            inverse = next(inv for position, _, inv in inputs if position == target)
            words[target] = inverse((words[t] - others) & MASK)
    if any(value is None for value in words):
        raise ValueError("incomplete elimination")
    residuals = {
        t: (words[t] - sigma1(words[t - 2]) - words[t - 7]
            - sigma0(words[t - 15]) - words[t - 16]) & MASK
        for t in RESIDUAL_INDICES
    }
    return words, residuals

