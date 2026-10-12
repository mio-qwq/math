#!/usr/bin/env python3
"""Recognize all gates and clauses of the supplied circuit; do not import its builder.

This comparison follows the independently frozen word specification.
The previously built independent circuit uses different gate/CNF templates.
"""
from collections import Counter
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

from check_hints import read_cnf

EXPECTED_MASK = 0xFBCA7000


def canonical(clause):
    return tuple(sorted(clause))


def gate_clauses(op, a, b, z):
    if op == 'xor':
        clauses = []
        for av, bv in itertools.product([False, True], repeat=2):
            clauses.append([-a if av else a, -b if bv else b, z if av != bv else -z])
        return clauses
    if op == 'and':
        return [[-z, a], [-z, b], [-a, -b, z]]
    if op == 'or':
        return [[-a, z], [-b, z], [-z, a, b]]
    raise ValueError('unknown gate')


def audit(data, n, clauses):
    assert data['K'] == EXPECTED_MASK
    assert data['variables'] == n
    assert set(data['inputs']) == {'q', 'p', 'p_prime'}
    words = data['inputs']
    assert all(len(word) == 32 for word in words.values())
    free = [v for word in words.values() for v in word]
    assert all(type(v) is int and v > 0 for v in free)
    assert len(set(free)) == 96
    zero = data['zero']
    assert type(zero) is int and zero > 0 and zero not in free
    known = set(free) | {zero}
    expected_clauses = [[-zero]]
    truth_rows = 0
    for op, a, b, z in data['gates']:
        assert abs(a) in known and abs(b) in known and z not in known and z > 0
        # Check the gate-CNF template at all eight local truth assignments.
        template = gate_clauses(op, 1, 2, 3)
        for av, bv, zv in itertools.product([False, True], repeat=3):
            assignment = {1: av, 2: bv, 3: zv}
            cnf_value = all(any(assignment[abs(lit)] == (lit > 0) for lit in cl) for cl in template)
            function = (av != bv) if op == 'xor' else (av and bv) if op == 'and' else (av or bv)
            assert cnf_value == (zv == function)
            truth_rows += 1
        expected_clauses.extend(gate_clauses(op, a, b, z))
        known.add(z)
    assert known == set(range(1, n+1))

    cursor = 0

    def consume(op, a, b):
        nonlocal cursor
        gate = data['gates'][cursor]
        assert gate[:3] == [op, a, b]
        cursor += 1
        return gate[3]

    def sigma(word, r, s, shift):
        result = []
        for i in range(32):
            t = consume('xor', word[(i+r) % 32], word[(i+s) % 32])
            result.append(consume('xor', t, word[i+shift] if i+shift < 32 else zero))
        return result

    def add(left, right):
        carry = zero
        result = []
        for i in range(32):
            t = consume('xor', left[i], right[i])
            result.append(consume('xor', t, carry))
            if i != 31:
                both = consume('and', left[i], right[i])
                carried = consume('and', t, carry)
                carry = consume('or', both, carried)
        return result

    def equate(left, right):
        for a, b in zip(left, right):
            expected_clauses.extend([[-a, b], [a, -b]])

    q, p, pp = words['q'], words['p'], words['p_prime']
    qp = [q[i] * (-1 if ((EXPECTED_MASK >> i) & 1) else 1) for i in range(32)]
    gq = sigma(q, 17, 19, 10)
    gqp = sigma(qp, 17, 19, 10)
    lhs1, rhs1 = add(q, gq), add(qp, gqp)
    equate(lhs1, rhs1)
    lhs2, rhs2 = add(pp, q), add(p, qp)
    equate(lhs2, rhs2)
    fpp = sigma(pp, 7, 18, 3)
    fqp = sigma(qp, 7, 18, 3)
    fp = sigma(p, 7, 18, 3)
    fq = sigma(q, 7, 18, 3)
    lhs3, rhs3 = add(fpp, fqp), add(fp, fq)
    equate(lhs3, rhs3)
    assert cursor == len(data['gates'])
    assert Counter(map(canonical, expected_clauses)) == Counter(map(canonical, clauses))
    return {'gates_recognized': cursor, 'truth_rows_checked': truth_rows,
            'free_input_bits': len(free), 'six_modular_adders': True,
            'three_full_word_equalities': True, 'final_carries_unconstrained': True,
            'every_cnf_clause_accounted_for': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    source = here.parent/'coupled-boundary'
    data = json.loads((source/'circuit.json').read_text())
    n, clauses = read_cnf(source/'boundary.cnf')
    result = {'status': 'PASS', 'mapping': audit(data, n, clauses)}
    variants = []
    altered = copy.deepcopy(data); altered['K'] ^= 1
    variants.append(('wrong_xor_constant', altered, clauses))
    altered = copy.deepcopy(data); altered['gates'][0][1] += 1
    variants.append(('wrong_sigma_bit_source', altered, clauses))
    altered = copy.deepcopy(data); altered['inputs']['p_prime'][0] = altered['inputs']['p'][0]
    variants.append(('identified_independent_base_bits', altered, clauses))
    variants.append(('missing_gate_clause', data, clauses[:1] + clauses[2:]))
    variants.append(('extra_auxiliary_assumption', data, clauses + [[1]]))
    changed = copy.deepcopy(clauses); changed[-1][0] *= -1
    variants.append(('damaged_word_equality', data, changed))
    controls = []
    for name, mapping, cnf in variants:
        try:
            audit(mapping, n, cnf)
        except (AssertionError, IndexError, ValueError):
            controls.append({'case': name, 'rejected': True})
        else:
            raise AssertionError('negative control accepted: '+name)
    result['negative_controls'] = controls
    result['source_hashes'] = {name: hashlib.sha256((source/name).read_bytes()).hexdigest()
                               for name in ['PROOF.md', 'build_cnf.py', 'circuit.json', 'boundary.cnf']}
    result['imports_discoverer_builder'] = False
    if args.record:
        args.record.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
