#!/usr/bin/env python3
"""Separate stdlib checker. Reuses frozen v1 evidence, not discovery functions.

The universal implication is proved in PROOF.md. This checker verifies its
finite carry lemma, sigma constants/inverse, recurrence substitutions and
the completeness of equality-path enumeration. It is NOT a full proof assistant.
"""
import argparse
import base64
import copy
import hashlib
import json
from pathlib import Path
import zlib

HERE = Path(__file__).resolve().parent
POTENTIAL_HASH = '1f04aa2b5ac13c5144e677cf75eb6d6af323d518abf96ec65a44a96fa07df23c'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sigma(x, kind):
    # Direct bit equations; no rotation code from discovery/SMT is imported.
    p, q, s = ((7, 18, 3), (17, 19, 10))[kind]
    out = 0
    for j in range(32):
        bit = ((x >> ((j+p) % 32)) ^ (x >> ((j+q) % 32))) & 1
        if j+s < 32:
            bit ^= (x >> (j+s)) & 1
        out += bit * 2**j
    return out


def check(support_cert, chain_cert, previous):
    need(support_cert['schema'] == 'sha256-minimum-supports-v2', 'support schema')
    need(support_cert['bound'] == previous['bound'] == 13, 'bound')
    raw = zlib.decompress(base64.b64decode(previous['potentials_zlib_base64'], validate=True))
    need(len(raw) == 49*65536, 'potential length')
    need(hashlib.sha256(raw).hexdigest() == POTENTIAL_HASH, 'frozen potential hash')
    # Breadth-first masks, rebuilding state from the entire path rather than
    # mutating a 16-bit state as in the discovery DFS.
    frontier = {m for m in range(1, 65536) if m.bit_count()+raw[m] == 13}
    need(sorted(frontier) == support_cert['start_states'], 'complete initial states')
    visited = len(frontier)
    for t in range(16, 64):
        following = set()
        for mask in frontier:
            state = sum(((mask >> j) & 1) << (j-t+16) for j in range(t-16, t))
            for active in (False, True):
                cand = mask | (int(active) << t)
                if sum((cand >> j) & 1 for j in (t, t-2, t-7, t-15, t-16)) == 1:
                    continue
                nxt = sum(((cand >> j) & 1) << (j-t+15) for j in range(t-15, t+1))
                if raw[(t-16)*65536+state] == int(active)+raw[(t-15)*65536+nxt]:
                    following.add(cand)
        frontier = following
        visited += len(frontier)
    actual = {tuple(j for j in range(64) if (m >> j) & 1) for m in frontier}
    supplied = support_cert['supports']
    need(len(supplied) == len(actual) and {tuple(s) for s in supplied} == actual,
         'complete terminal supports')
    need(all(len(s) == 13 and s == sorted(set(s)) for s in supplied), 'support format')
    need(visited == support_cert['visited_nodes'] == 735, 'path count')

    need(chain_cert['schema'] == 'sha256-impossible-chain-v2', 'chain schema')
    need(chain_cert['word_bits'] == 32, 'word width')
    h = 1 << 31
    need(chain_cert['sigma0_half'] == sigma(h, 0) == 0x11002000, 'sigma0 half constant')
    inv = chain_cert['sigma1_inverse_half']
    need(inv == 0xc6eeaad6 and sigma(inv, 1) == h, 'sigma1 half inverse')
    # Verify the full right inverse, hence uniqueness of the asserted preimage.
    need(len(previous['sigma_inverse_columns'][1]) == 32, 'inverse length')
    for j, word in enumerate(previous['sigma_inverse_columns'][1]):
        need(sigma(word, 1) == 1 << j, 'complete sigma1 inverse')
    need(inv % 4 == 2, 'inverse valuation')
    # Adjacent 7-bit quotients cannot differ at bit6 alone among bits5,6.
    for quotient in range(128):
        for sign in (-1, 1):
            difference = quotient ^ ((quotient+sign) % 128)
            need(not (difference & 64) or bool(difference & 32), 'carry lemma')
    # Low 24 bits of the sigma0 output difference for a half-word input delta.
    for signs in range(8):
        delta = sum((1 if signs & (1 << j) else -1)*2**b
                    for j, b in enumerate((13, 24, 28)))
        need(delta % 2**24 in (2**13, 2**24-2**13), 'first delta reduction')

    def recurrence(support, t):
        need(16 <= t < 64, 'recurrence index')
        terms = [('d', t, 1), ('g', t-2, -1), ('d', t-7, -1),
                 ('f', t-15, -1), ('d', t-16, -1)]
        return {(k, i): sign for k, i, sign in terms if i in support}

    ids = []
    for case in chain_cert['cases']:
        idx = case['support_index']
        need(type(idx) is int and 0 <= idx < len(supplied), 'case index')
        S = set(supplied[idx])
        u, x, a, r, b = (case[k] for k in ('u', 'x', 'a', 'r', 'b'))
        need(all(j in S for j in (u, x, a, r, b)), 'nonzero assumption')
        identities = [
            (x, {('d', x): 1, ('d', u): -1}),
            (r, {('d', r): 1, ('d', u): -1}),
            (r+7, {('d', r): -1, ('d', x): -1}),
            (x+15, {('d', a): -1, ('f', x): -1}),
            (b, {('d', b): 1, ('f', a): -1}),
            (b+2, {('g', b): -1, ('d', r): -1}),
        ]
        for t, expected in identities:
            need(recurrence(S, t) == expected, 'recurrence substitution')
        ids.append(idx)
    need(sorted(ids) == [3, 14], 'excluded cases')
    need(chain_cert['remaining_indices'] == [i for i in range(15) if i not in ids],
         'remaining classification')
    return dict(supports=len(actual), visited_nodes=visited, carry_cases=256,
                excluded_indices=ids, remaining=len(actual)-len(ids),
                actual_distance_lower_bound=13,
                proof_scope='written universal proof plus checked finite dependencies; not Lean')


def negatives(s, c, old):
    bad = []
    ss = copy.deepcopy(s); ss['supports'].pop(); bad.append((ss, c))
    ss = copy.deepcopy(s); ss['supports'][0][0] = 0; bad.append((ss, c))
    ss = copy.deepcopy(s); ss['start_states'].pop(); bad.append((ss, c))
    cc = copy.deepcopy(c); cc['sigma1_inverse_half'] ^= 1; bad.append((s, cc))
    cc = copy.deepcopy(c); cc['cases'][0]['a'] = 43; bad.append((s, cc))
    cc = copy.deepcopy(c); cc['remaining_indices'].pop(); bad.append((s, cc))
    reasons = []
    for ss, cc in bad:
        try:
            check(ss, cc, old)
        except ValueError as e:
            reasons.append(str(e))
        else:
            raise ValueError('negative control accepted')
    return reasons


def check_tail(tail):
    need(tail['status'] == 'sat', 'tail witness status')
    pairs = tail['pairs']
    need(set(pairs) == set('xarb'), 'tail names')
    d, F, G = {}, {}, {}
    for name, pair in pairs.items():
        need(len(pair) == 2 and all(type(w) is int and 0 <= w < 2**32 for w in pair),
             'tail word range')
        u, v = pair
        d[name] = (v-u) % 2**32
        F[name] = (sigma(v, 0)-sigma(u, 0)) % 2**32
        G[name] = (sigma(v, 1)-sigma(u, 1)) % 2**32
        need(d[name] != 0, 'tail active word')
    need((d['r']+d['x']) % 2**32 == 0, 'tail raw cancellation')
    need(F['r'] == F['x'], 'tail matching sigma0 differences')
    need((d['a']+F['x']) % 2**32 == 0, 'tail first sigma0 link')
    need(d['b'] == F['a'] and G['b'] == d['x'], 'tail final links')
    need(d['x'] != 2**31, 'tail cannot contradict half-word theorem')
    return dict(delta_x=d['x'], equations=5,
                scope='counterexample to omitting forced H in tail exclusion; not an actual schedule')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    s, c, old = [json.loads(p.read_text()) for p in
                 (HERE/'supports.json', HERE/'exclusions.json', HERE.parent/'certificate.json')]
    result = check(s, c, old)
    tail = json.loads((HERE/'TAIL.json').read_text())
    result['tail'] = check_tail(tail)
    if args.negative:
        result['rejected_controls'] = negatives(s, c, old)
        bad = copy.deepcopy(tail)
        bad['pairs']['x'][0] ^= 1
        try:
            check_tail(bad)
        except ValueError as e:
            result['rejected_controls'].append(str(e))
        else:
            raise ValueError('corrupt tail accepted')
    print(json.dumps(result, sort_keys=True))
