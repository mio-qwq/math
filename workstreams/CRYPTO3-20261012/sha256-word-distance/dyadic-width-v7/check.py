#!/usr/bin/env python3
"""Definition-based check of the shared-term width lemma; no solver."""
import copy
import hashlib
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parent
N = 1 << 32
MASK = N-1
LOW = (1 << 22)-1


def row(j):
    out = {(j+17) % 32, (j+19) % 32}
    if j+10 < 32:
        out.symmetric_difference_update({j+10})
    return sorted(out)


def g(x):
    return (((x >> 17) | (x << 15)) ^ ((x >> 19) | (x << 13)) ^ (x >> 10)) & MASK


def g_bits(x):
    return sum((sum((x >> i) & 1 for i in row(j)) % 2) << j for j in range(32))


def expected():
    cases = []
    for k in range(10, 19):
        cases.append({'k': k, 'modulus': 1 << (k+14), 'common': 1 << (k+13),
                      'unchanged_rows': [[j, row(j)] for j in range(22, k+13)],
                      'flipping_row': [k+13, row(k+13)],
                      'maximum_odd_q': (1 << (22-k))-1,
                      'lifts': 1 << (18-k), 'positive_count': 1 << (39-2*k),
                      'signed_count': 1 << (40-2*k)})
    return {'schema': 'crypto3-shared-term-width-v7', 'cases': cases,
            'integer_q_bound': LOW, 'shared_term_bound': 4*LOW,
            'reversal_lift': '(-h) mod lifts'}


def validate(packet):
    assert packet == expected(), 'exact row/domain certificate differs'
    for case in packet['cases']:
        k, modulus = case['k'], case['modulus']
        assert modulus <= N and N % modulus == 0
        assert 4*LOW < modulus
        for j, bits in case['unchanged_rows']:
            assert bits == [j-15, j-13] and max(bits) < k
        assert case['flipping_row'] == [k+13, [k-2, k]]
        assert case['common']*2 == modulus
        max_q = case['maximum_odd_q']
        assert max_q*(1 << k) <= LOW < (max_q+1)*(1 << k)
        assert max_q % 2 == 1
        assert case['lifts']*modulus == N
        assert ((max_q+1)//2)*case['lifts'] == case['positive_count']
        assert 2*case['positive_count'] == case['signed_count']
        assert 2*LOW < modulus, 'signed intervals must be disjoint'
        for h in range(case['lifts']):
            negated_h = (-h) % case['lifts']
            for q in (1, max_q):
                d = (-q*(1 << k)+h*modulus) & MASK
                reverse = (q*(1 << k)+negated_h*modulus) & MASK
                assert (-d) & MASK == reverse
                assert d != 0 and d & -d == 1 << k


def samples():
    rng = random.Random(20261012)
    count = 0
    for k in range(10, 19):
        modulus, common = 1 << (k+14), 1 << (k+13)
        for unused in range(16):
            delta = (rng.randrange(1 << (32-k)) | 1) << k
            for sign in (1, -1):
                x = rng.randrange(N)
                xp = (x+sign*delta) & MASK
                assert (x ^ xp) & ((1 << k)-1) == 0
                assert ((x ^ xp) >> k) & 1
                u, up = g(x), g(xp)
                assert u == g_bits(x) and up == g_bits(xp)
                q = (up & LOW)-(u & LOW)
                assert -LOW <= q <= LOW
                assert (up-u-common-q) % modulus == 0
                count += 1
    return count


def controls(packet):
    faults = []
    p = copy.deepcopy(packet); p['cases'][0]['k'] = 9; faults.append(p)
    p = copy.deepcopy(packet); p['cases'][7]['flipping_row'][1][0] += 1; faults.append(p)
    p = copy.deepcopy(packet); p['cases'][6]['lifts'] //= 2; faults.append(p)
    p = copy.deepcopy(packet); p['reversal_lift'] = 'h'; faults.append(p)
    for p in faults:
        try:
            validate(p)
        except AssertionError:
            continue
        raise AssertionError('damaged certificate accepted')
    modulus = 1 << 23
    qx, qy, qr = -4194303, -4193279, 513
    assert all(-LOW <= q <= LOW for q in (qx, qy, qr))
    a, b = qy-qr, qy-qx
    d = a % modulus
    assert d & -d == 1 << 9
    assert (a-d) % modulus == (b-2*d) % modulus == 0
    assert b-2*a == modulus and abs(a) <= LOW
    # The zero-multiple step fails, though the signed domain formula
    # at k9 would already cover every exact valuation9 residue.
    assert ((1 << (22-9))//2)*2*(1 << (18-9)) == 1 << (31-9)
    assert d <= LOW or modulus-d <= LOW
    return len(faults)


def main():
    path = ROOT/'CERTIFICATE.json'
    packet = json.loads(path.read_text())
    validate(packet)
    count = samples()
    negative = controls(packet)
    print(json.dumps({'status': 'PASS', 'valuation_layers': len(packet['cases']),
                      'original_bit_rows': 32, 'actual_decomposition_samples': count,
                      'samples_are_core_witnesses': False, 'controls_rejected': negative,
                      'certificate_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'uses_solver': False}, sort_keys=True))


if __name__ == '__main__':
    main()
