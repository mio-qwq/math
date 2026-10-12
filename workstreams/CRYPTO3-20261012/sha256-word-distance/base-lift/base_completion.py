#!/usr/bin/env python3
"""Exact support-0 base interpolation; see PROJECTION.md for the theorem."""

MASK = (1 << 32) - 1
SUPPORT = (2, 9, 10, 16, 23, 24, 30, 37, 38, 44, 51, 52, 58)
PARAMETERS = (0, 1, 3, 4, 5, 7, 8, 11, 12, 15, 29, 43, 57)
RESIDUAL_INDICES = (28, 29, 35, 36, 42, 43, 49, 50, 56, 57)
ORDER = (
    (17, 17), (24, 22), (31, 31), (38, 36), (45, 45), (52, 50), (59, 59),
    (16, 14), (23, 21), (30, 28), (37, 35), (44, 42), (51, 49), (58, 56),
    (18, 18), (25, 25), (32, 32), (39, 39), (46, 46), (53, 53), (60, 60),
    (19, 19), (26, 26), (33, 33), (40, 40), (47, 47), (54, 54), (61, 61),
    (21, 6), (22, 20), (20, 13),
    (27, 27), (34, 34), (41, 41), (48, 48), (55, 55), (62, 62),
    (63, 63),
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
            raise ValueError("sigma matrix is singular")
    if len(basis) != 32:
        raise ValueError("incomplete sigma matrix")
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
    """Return a full sequence and the ten residuals; do not assert a lift."""
    if set(active) != set(SUPPORT) or set(parameters) != set(PARAMETERS):
        raise ValueError("wrong interpolation coordinates")
    if any(type(value) is not int or not 0 <= value <= MASK
           for value in list(active.values()) + list(parameters.values())):
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
            others = sum(fn(words[position]) for position, fn, _ in inputs if position != target)
            inverse = next(inv for position, _, inv in inputs if position == target)
            words[target] = inverse((words[t] - others) & MASK)
    if any(value is None for value in words):
        raise ValueError("incomplete elimination")
    residuals = {t: (words[t] - sigma1(words[t - 2]) - words[t - 7]
                     - sigma0(words[t - 15]) - words[t - 16]) & MASK
                 for t in RESIDUAL_INDICES}
    return words, residuals

