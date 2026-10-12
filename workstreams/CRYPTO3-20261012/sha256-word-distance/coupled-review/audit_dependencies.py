#!/usr/bin/env python3
"""Rebuild the needed low-12 kernel and every original support substitution.

Only standard-library arithmetic. No import or execution of the prior
local checker, support checker, SAT builder, or enumeration program.
"""
from collections import Counter, defaultdict
import argparse
import copy
import hashlib
import json
from pathlib import Path

MASK = 0xFFFFFFFF
LOW = 0xFFF
K = 0xFBCA7000


def g(value):
    return (((value >> 17) | (value << 15)) & MASK) ^ \
           (((value >> 19) | (value << 13)) & MASK) ^ (value >> 10)


def reduce_rows(rows):
    """Full row elimination, unlike the supplied certificate's column method."""
    rows = list(rows)
    pivots = []
    rank = 0
    for column in range(32):
        chosen = next((j for j in range(rank, len(rows)) if (rows[j] >> column) & 1), None)
        if chosen is None:
            continue
        rows[rank], rows[chosen] = rows[chosen], rows[rank]
        for j in range(len(rows)):
            if j != rank and (rows[j] >> column) & 1:
                rows[j] ^= rows[rank]
        pivots.append(column)
        rank += 1
    return rows[:rank], pivots


def span(basis):
    result = {0}
    for value in basis:
        result |= {old ^ value for old in list(result)}
    return result


def audit_low12(certificate):
    assert certificate['definition'] == {'bits': 32, 'rotr': [17, 19], 'shr': 10,
                                         'outer_operation': 'addition modulo 2^32'}
    low12 = certificate['low12']
    rows = [1 << i for i in range(12)]
    for i in range(12):
        rows.append((1 << ((i+17) % 32)) ^ (1 << ((i+19) % 32)) ^ (1 << (i+10)))
    reduced, pivots = reduce_rows(rows)
    basis = []
    for free in sorted(set(range(32)) - set(pivots)):
        vector = 1 << free
        for row, pivot in zip(reduced, pivots):
            if (row >> free) & 1:
                vector |= 1 << pivot
        basis.append(vector)
    assert len(pivots) == 24 and len(basis) == 8
    masks = span(basis) - {0}
    assert len(masks) == 255
    assert all(((d | g(d)) & LOW) == 0 for d in masks)
    assert low12['low_bits'] == 12 and low12['map_rank'] == 24
    assert low12['kernel_dimension'] == 8 and low12['nonzero_masks_checked'] == 255
    supplied_basis = [int(v, 16) for v in low12['kernel_basis']]
    assert len(supplied_basis) == 8 and span(supplied_basis) == masks | {0}
    columns = [((1 << i) & LOW) | ((g(1 << i) & LOW) << 12) for i in range(32)]
    assert low12['map_columns'] == [f'{v:08x}' for v in columns]
    expected = {}
    for d in masks:
        e = g(d)
        bad = (d ^ e) & (~((d | e) << 1) & MASK)
        first = (bad & -bad).bit_length()-1 if bad else None
        expected[d] = (e, first)
    seen_masks = set()
    seen_selectors = set()
    for case in low12['cases']:
        d, e = int(case['xor_mask'], 16), int(case['sigma1_mask'], 16)
        selector = case['selector']
        assert type(selector) is int and 1 <= selector < 256 and selector not in seen_selectors
        selected = 0
        for i, vector in enumerate(supplied_basis):
            if (selector >> i) & 1:
                selected ^= vector
        assert selected == d and d not in seen_masks
        assert expected[d] == (e, case['first_obstruction_bit'])
        seen_masks.add(d); seen_selectors.add(selector)
    assert seen_masks == masks and seen_selectors == set(range(1, 256))
    survivors = sorted(d for d, (_, failure) in expected.items() if failure is None)
    assert survivors == [K] and g(K) == 0x763E9000
    assert low12['surviving_masks'] == [f'{d:08x}' for d in survivors]
    histogram = Counter('none' if failure is None else str(failure) for _, failure in expected.values())
    return {'matrix_rows': len(rows), 'rank': len(pivots), 'kernel_dimension': len(basis),
            'independently_rebuilt_basis': [f'{v:08x}' for v in basis],
            'all_nonzero_masks_checked': len(masks), 'rejected_masks': 254,
            'surviving_mask': f'{K:08x}', 'surviving_image': f'{g(K):08x}',
            'complete_supplied_table_matches': True, 'first_obstruction_histogram': dict(histogram)}


def audit_power_dependency(certificate):
    # Used only for the signed-power corollary stated in SUPPORT5.md.
    interval_images = []
    count = 0
    for first in range(32):
        for last in range(first, 32):
            count += 1
            d = (1 << (last+1)) - (1 << first)
            e = g(d)
            matches = [j for j in range(first, 32)
                       if e == (1 << (j+1)) - (1 << first)]
            for j in matches:
                interval_images.append({'k': first, 'last': last, 'image_last': j,
                                        'xor_mask': f'{d:08x}', 'sigma1_mask': f'{e:08x}'})
    assert count == 528
    assert interval_images == certificate['power_of_two']['same_start_interval_images']
    assert interval_images == [{'k': 0, 'last': 31, 'image_last': 21,
                                'xor_mask': 'ffffffff', 'sigma1_mask': '003fffff'}]
    values = []
    for x, y in [(0x7FFFFFFF, 0x80000000), (0xFFFFFFFF, 0)]:
        hx, hy = (x+g(x)) & MASK, (y+g(y)) & MASK
        assert hx != hy
        values.append({'x': f'{x:08x}', 'y': f'{y:08x}', 'h_x': f'{hx:08x}', 'h_y': f'{hy:08x}'})
    return {'input_intervals_checked': count, 'same_start_interval_images': interval_images,
            'two_remaining_input_pairs': values}


def reduced_recurrence(t, support):
    assert 16 <= t < 64
    full = [('d', t, 1), ('g', t-2, -1), ('d', t-7, -1),
            ('f', t-15, -1), ('d', t-16, -1)]
    reduced = defaultdict(int)
    for kind, index, coefficient in full:
        if index in support:
            reduced[kind, index] += coefficient
    return full, sorted((kind, index, coefficient) for (kind, index), coefficient in reduced.items() if coefficient)


def audit_bridges(data, support5_orientation=(-1, -1)):
    supports = data['supports']
    rows = []
    for sid, u in [(0, 30), (1, 31), (2, 32), (4, 33), (8, 29), (9, 29)]:
        support = set(supports[sid])
        p, q, r = u+7, u+14, u+22
        assert {u, p, q, r} <= support
        expected = [(p, [('d', p, 1), ('d', u, -1)]),
                    (q, [('d', q, 1), ('d', p, -1)]),
                    (u+16, [('g', q, -1), ('d', u, -1)]),
                    (r, [('d', r, 1), ('f', p, -1)]),
                    (u+29, [('d', r, -1), ('f', q, -1)])]
        for t, wanted in expected:
            full, reduced = reduced_recurrence(t, support)
            assert reduced == sorted(wanted)
            rows.append({'support': sid, 't': t, 'full_equation_terms': full,
                         'surviving_terms': reduced})
    s5 = set(supports[5])
    assert {8, 17} <= s5
    additional = [(24, [('d', 17, -1), ('d', 8, -1)]),
                  (19, [('d', 19, 1), ('g', 17, -1)]),
                  (26, [('d', 26, 1), ('d', 19, -1)]),
                  (33, [('d', 26, -1), ('d', 17, -1)]),
                  (23, [('d', 16, -1), ('f', 8, -1)]),
                  (32, [('f', 17, -1), ('d', 16, -1)])]
    for t, wanted in additional:
        full, reduced = reduced_recurrence(t, s5)
        assert reduced == sorted(wanted)
        rows.append({'support': 5, 't': t, 'full_equation_terms': full,
                     'surviving_terms': reduced})
    # Formal coefficients: d8=-D, F8=F17. Reversing index 8 gives dp=D, Fp=-F17.
    assert support5_orientation[0] * (-1) == 1
    assert support5_orientation[1] * 1 == -1
    assert len(rows) == 36
    return {'supports': [0, 1, 2, 4, 5, 8, 9], 'original_recurrences_checked': len(rows),
            'support5_pair_orientation': {'p': "W'[8]", 'p_prime': 'W[8]', 'q': 'W[17]', 'q_prime': "W'[17]"},
            'all_active_D_coordinates_verified': True, 'rows': rows}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    root = here.parent
    certificate_path = root/'local-review/independent_certificate.json'
    supports_path = root/'supports-v2.json'
    certificate = json.loads(certificate_path.read_text())
    supports = json.loads(supports_path.read_text())
    result = {'status': 'PASS', 'low12': audit_low12(certificate),
              'signed_power_dependency': audit_power_dependency(certificate),
              'bridges': audit_bridges(supports)}
    variants = []
    changed = copy.deepcopy(certificate); changed['low12']['cases'].pop()
    variants.append(('missing_mask_case', audit_low12, (changed,)))
    changed = copy.deepcopy(certificate); changed['low12']['cases'][0]['first_obstruction_bit'] = 0
    variants.append(('wrong_obstruction_bit', audit_low12, (changed,)))
    changed = copy.deepcopy(certificate); changed['low12']['kernel_basis'][0] = '00000001'
    variants.append(('wrong_kernel_basis', audit_low12, (changed,)))
    changed = copy.deepcopy(certificate); changed['low12']['surviving_masks'] = []
    variants.append(('removed_surviving_mask', audit_low12, (changed,)))
    changed = copy.deepcopy(supports); changed['supports'][0].remove(30)
    variants.append(('removed_active_D_coordinate', audit_bridges, (changed,)))
    variants.append(('reverse_input_but_not_sigma', audit_bridges, (supports, (-1, 1))))
    variants.append(('reverse_sigma_but_not_input', audit_bridges, (supports, (1, -1))))
    controls = []
    for name, procedure, arguments in variants:
        try:
            procedure(*arguments)
        except (AssertionError, KeyError):
            controls.append({'case': name, 'rejected': True})
        else:
            raise AssertionError('accepted damaged dependency: '+name)
    result['negative_controls'] = controls
    paths = [certificate_path, root/'local-review/INDEPENDENT_PROOF.md', supports_path,
             root/'coupled-boundary/SUPPORT5.md', root/'coupled-boundary/check_support5.py']
    result['source_hashes'] = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    result['prior_checkers_imported_or_executed'] = False
    if args.record:
        args.record.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': result['status'], 'low12': result['low12'],
                      'power_intervals': result['signed_power_dependency']['input_intervals_checked'],
                      'support_recurrences': len(result['bridges']['rows']),
                      'supports': result['bridges']['supports'],
                      'negative_controls': controls, 'source_hashes': result['source_hashes']}, indent=2))


if __name__ == '__main__':
    main()
