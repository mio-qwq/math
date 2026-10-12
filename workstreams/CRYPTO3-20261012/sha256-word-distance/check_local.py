#!/usr/bin/env python3
"""Stdlib-only exact dependencies of LOCAL_PROOF.md.

Written separately from the constructor, using direct bit equations and
low-pivot elimination. This separation is not itself independent-agent review.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

SOURCE_HASH = '02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf'
MODULUS = 1 << 32


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sigma1(word):
    require(type(word) is int and 0 <= word < MODULUS, 'unsigned word')
    bits = [(word >> j) & 1 for j in range(32)]
    result = []
    for j in range(32):
        out = bits[(j + 17) % 32] ^ bits[(j + 19) % 32]
        if j + 10 < 32:
            out ^= bits[j + 10]
        result.append(out)
    return sum(value << bit for bit, value in enumerate(result))


def rank(words):
    rows = list(words)
    at = 0
    for bit in range(32):
        pivot = next((j for j in range(at, len(rows)) if (rows[j] >> bit) & 1), None)
        if pivot is None:
            continue
        rows[at], rows[pivot] = rows[pivot], rows[at]
        for j in range(at + 1, len(rows)):
            if (rows[j] >> bit) & 1:
                rows[j] ^= rows[at]
        at += 1
    return at


def carry_failure(alpha, beta):
    # Signed changed-bit contributions are relaxed to independent signs.
    # A final carry at bit32 is allowed: the equality is modular.
    reachable = {0}
    for bit in range(13, 32):
        left = (-1, 1) if (alpha >> bit) & 1 else (0,)
        right = (-1, 1) if (beta >> bit) & 1 else (0,)
        following = set()
        for carry in reachable:
            for a in left:
                for b in right:
                    total = carry + a + b
                    if total % 2 == 0:
                        following.add(total // 2)
        reachable = following
        if not reachable:
            return bit
    return None


def recurrence(support, t):
    require(16 <= t < 64, 'recurrence boundary')
    terms = [('d', t, 1), ('g', t-2, -1), ('d', t-7, -1),
             ('f', t-15, -1), ('d', t-16, -1)]
    return {(kind, index): sign for kind, index, sign in terms if index in support}


def check(cert, source_bytes):
    require(cert['schema'] == 'crypto3-sigma1-local-cancellation-v1', 'schema')
    require(cert['word_bits'] == 32 and cert['common_low_bits'] == 13, 'word/low-bit width')
    require(cert['sigma1'] == {'rotations': [17, 19], 'right_shift': 10}, 'FIPS constants')
    require(hashlib.sha256(source_bytes).hexdigest() == SOURCE_HASH == cert['source_support_sha256'],
            'frozen support hash')
    basis = cert['kernel_basis']
    require(len(basis) == 6 and rank(basis) == 6, 'kernel basis independence')
    for word in basis:
        require(word % 8192 == 0 and sigma1(word) % 8192 == 0, 'kernel membership')
    rows = [1 << bit for bit in range(13)]
    for bit in range(13):
        row = sum(((sigma1(1 << variable) >> bit) & 1) << variable for variable in range(32))
        rows.append(row)
    require(rank(rows) == cert['projection_rank'] == 26, 'complete kernel dimension')
    supplied = cert['carry_exclusions']
    require(len(supplied) == 63 and [r['selection'] for r in supplied] == list(range(1, 64)),
            'complete carry list')
    failure_histogram = {}
    for row in supplied:
        alpha = 0
        for bit, value in enumerate(basis):
            if (row['selection'] >> bit) & 1:
                alpha ^= value
        beta = sigma1(alpha)
        require(row['alpha'] == alpha and row['beta'] == beta and alpha != 0, 'carry mask')
        rejected_at = carry_failure(alpha, beta)
        require(rejected_at is not None and row['first_empty_bit'] == rejected_at, 'carry obstruction')
        failure_histogram[rejected_at] = failure_histogram.get(rejected_at, 0) + 1

    # Exactly 528 input interval masks, with all output endpoints checked.
    matches = []
    for start in range(32):
        alpha = 0
        for last in range(start, 32):
            alpha += 1 << last
            image = sigma1(alpha)
            output = 0
            for output_last in range(start, 32):
                output += 1 << output_last
                if image == output:
                    matches.append(dict(k=start, input_last=last, output_last=output_last,
                                        alpha=alpha, beta=image))
    require(matches == cert['power2_interval_matches'] == [dict(k=0, input_last=31,
            output_last=21, alpha=0xffffffff, beta=0x003fffff)], 'complete power2 masks')
    require(cert['power2_boundary_pairs'] == [[0x7fffffff, 0x80000000], [0xffffffff, 0]],
            'complete power2 boundary pairs')
    for x, y in cert['power2_boundary_pairs']:
        require((y-x) % MODULUS == 1 and x ^ y == 0xffffffff, 'increment boundary')
        require((sigma1(y)-sigma1(x)) % MODULUS != MODULUS-1, 'boundary contradiction')

    sharp = cert['local_sharpness']
    x, y = sharp['x'], sharp['y']
    gx, gy = sigma1(x), sigma1(y)
    delta = (y-x) % MODULUS
    require(x != y and delta % 4096 == 0 and delta % 8192 != 0, 'sharpness valuation')
    require(sharp['sigma1_x'] == gx and sharp['sigma1_y'] == gy, 'sharpness sigma values')
    require((x+gx) % MODULUS == (y+gy) % MODULUS == sharp['h'], 'local collision')
    require(delta == sharp['delta'], 'sharpness delta')
    require(sharp['scope'] == 'one local word pair only; not an expanded message pair', 'sharpness scope')

    supports = json.loads(source_bytes)['supports']
    bridges = cert['support_bridges']
    require([(b['index'], b['u']) for b in bridges] == [(0,30),(1,31),(2,32),(4,33),(8,29),(9,29)],
            'support bridge coverage')
    for bridge in bridges:
        u, support = bridge['u'], set(bridge['support'])
        require(bridge['support'] == supports[bridge['index']], 'source support binding')
        require({u, u+7, u+14}.issubset(support), 'nonzero bridge words')
        identities = [(u+7, {('d',u+7):1, ('d',u):-1}),
                      (u+14, {('d',u+14):1, ('d',u+7):-1}),
                      (u+16, {('g',u+14):-1, ('d',u):-1})]
        for t, expected in identities:
            require(recurrence(support,t) == expected, 'exact recurrence bridge')
    return dict(status='PASS', kernel_rank=26, kernel_dimension=6, carry_masks_rejected=63,
                failure_histogram=failure_histogram, interval_masks=528, exceptional_boundary_pairs=2,
                schedule_bridges=6, recurrence_identities=18, local_sharpness_delta=delta,
                actual_schedule_distance_lower_bound=13,
                limitation='No actual 16-word message pair or complete 13-support exclusion is claimed.')


def negatives(cert, source):
    cases = []
    def add(label, change):
        bad = copy.deepcopy(cert)
        change(bad)
        cases.append((label, bad, source))
    add('wrong rotation', lambda c: c['sigma1']['rotations'].__setitem__(0,18))
    add('corrupt kernel basis', lambda c: c['kernel_basis'].__setitem__(0,c['kernel_basis'][0]^8192))
    add('omit carry mask', lambda c: c['carry_exclusions'].pop())
    add('fake carry rejection', lambda c: c['carry_exclusions'][0].__setitem__('first_empty_bit',31))
    add('wrong sigma image', lambda c: c['carry_exclusions'][0].__setitem__('beta',0))
    add('omit interval exception', lambda c: c['power2_interval_matches'].clear())
    add('damaged sharpness input', lambda c: c['local_sharpness'].__setitem__('x',c['local_sharpness']['x']^8192))
    add('alter claimed sigma value', lambda c: c['local_sharpness'].__setitem__('sigma1_y',0))
    add('wrong recurrence index', lambda c: c['support_bridges'][0].__setitem__('u',31))
    add('false global scope', lambda c: c['local_sharpness'].__setitem__('scope','full schedule'))
    cases.append(('damaged dependency', cert, source+b' '))
    results = []
    for label, bad, bad_source in cases:
        try:
            check(bad,bad_source)
        except ValueError as exc:
            results.append(dict(control=label,rejection=str(exc)))
        else:
            raise ValueError('negative control accepted: '+label)
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('local_certificate.json'))
    parser.add_argument('--supports', type=Path, default=Path(__file__).with_name('supports-v2.json'))
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    cert = json.loads(args.certificate.read_text())
    source = args.supports.read_bytes()
    result = check(cert,source)
    if args.negative:
        result['negative_controls'] = negatives(cert,source)
    print(json.dumps(result,sort_keys=True))
