#!/usr/bin/env python3
"""Construct the small local sigma1 certificate; no SMT is required."""
import argparse
import hashlib
import json
from pathlib import Path

MASK = (1 << 32) - 1


def rotr(word, count):
    return ((word >> count) | (word << (32 - count))) & MASK


def sigma1(word):
    return rotr(word, 17) ^ rotr(word, 19) ^ (word >> 10)


def kernel_basis(k):
    rows = [1 << j for j in range(k)]
    for j in range(k):
        rows.append(sum(((sigma1(1 << i) >> j) & 1) << i for i in range(32)))
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = row
                break
            row ^= pivots[pivot]
    basis = []
    for free in range(32):
        if free in pivots:
            continue
        word = 1 << free
        for pivot, row in sorted(pivots.items()):
            if (row & word).bit_count() % 2:
                word |= 1 << pivot
        basis.append(word)
    return basis, len(pivots)


def first_empty_carry(alpha, beta, k):
    carries = {0}
    for bit in range(k, 32):
        count = ((alpha >> bit) & 1) + ((beta >> bit) & 1)
        choices = (0,) if count == 0 else (-1, 1) if count == 1 else (-2, 0, 2)
        carries = {(carry + value) // 2 for carry in carries for value in choices
                   if (carry + value) % 2 == 0}
        if not carries:
            return bit
    return None


def build(support_bytes):
    basis, rank = kernel_basis(13)
    rejected = []
    for selection in range(1, 1 << len(basis)):
        alpha = 0
        for j, word in enumerate(basis):
            if (selection >> j) & 1:
                alpha ^= word
        beta = sigma1(alpha)
        rejected.append(dict(selection=selection, alpha=alpha, beta=beta,
                             first_empty_bit=first_empty_carry(alpha, beta, 13)))
    intervals = []
    for k in range(32):
        for last in range(k, 32):
            alpha = (1 << (last + 1)) - (1 << k)
            beta = sigma1(alpha)
            for output_last in range(k, 32):
                if beta == (1 << (output_last + 1)) - (1 << k):
                    intervals.append(dict(k=k, input_last=last, output_last=output_last,
                                          alpha=alpha, beta=beta))
    x, y = 0x5d130376, 0xa6d97376
    supports = json.loads(support_bytes)['supports']
    return {
        'schema': 'crypto3-sigma1-local-cancellation-v1',
        'status': 'candidate; independent written and finite verification recorded separately',
        'word_bits': 32, 'sigma1': {'rotations': [17, 19], 'right_shift': 10},
        'common_low_bits': 13, 'projection_rank': rank, 'kernel_basis': basis,
        'carry_exclusions': rejected, 'power2_interval_matches': intervals,
        'power2_boundary_pairs': [[0x7fffffff, 0x80000000], [0xffffffff, 0]],
        'local_sharpness': {'x': x, 'y': y, 'sigma1_x': sigma1(x), 'sigma1_y': sigma1(y),
                            'delta': (y - x) & MASK, 'h': (x + sigma1(x)) & MASK,
                            'scope': 'one local word pair only; not an expanded message pair'},
        'source_support_sha256': hashlib.sha256(support_bytes).hexdigest(),
        'support_bridges': [dict(index=i, u=u, support=supports[i])
                            for i, u in [(0, 30), (1, 31), (2, 32), (4, 33), (8, 29), (9, 29)]],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('supports', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = build(args.supports.read_bytes())
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'kernel_dimension': len(result['kernel_basis']),
                      'carry_masks': len(result['carry_exclusions']),
                      'all_rejected': all(r['first_empty_bit'] is not None for r in result['carry_exclusions'])}))
