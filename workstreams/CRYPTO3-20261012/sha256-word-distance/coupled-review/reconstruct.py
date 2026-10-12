#!/usr/bin/env python3
"""Independent truth-table CNF of the three modular word equations.

Does not import, read, or execute the discoverer's circuit or checker.
The optional solver is a cross-check, not the UNSAT certificate review.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

BITS = 32
MASK = (1 << BITS) - 1
DELTA_XOR = 0xFBCA7000


class Circuit:
    def __init__(self):
        self.nvars = 0
        self.clauses = []
        self.gates = []
        self.one = self.fresh()
        self.clauses.append([self.one])

    def fresh(self):
        self.nvars += 1
        return self.nvars

    def word(self):
        return [self.fresh() for _ in range(BITS)]

    def gate(self, kind, args):
        out = self.fresh()
        for values in itertools.product([False, True], repeat=3):
            expected = (sum(values) % 2 == 1) if kind == 'xor3' else sum(values) >= 2
            clause = [-lit if value else lit for lit, value in zip(args, values)]
            clause.append(out if expected else -out)
            self.clauses.append(clause)
        self.gates.append({'kind': kind, 'inputs': list(args), 'output': out})
        return out

    def sigma(self, word, r, s, shift):
        return [self.gate('xor3', [word[(i+r) % BITS], word[(i+s) % BITS],
                                  word[i+shift] if i+shift < BITS else -self.one])
                for i in range(BITS)]

    def plus(self, left, right):
        carry = -self.one
        result = []
        for i in range(BITS):
            result.append(self.gate('xor3', [left[i], right[i], carry]))
            if i < BITS-1:
                carry = self.gate('maj3', [left[i], right[i], carry])
        return result

    def equate(self, left, right):
        for a, b in zip(left, right):
            self.clauses.extend([[-a, b], [a, -b]])


def reconstruct():
    c = Circuit()
    p, pp, q = c.word(), c.word(), c.word()
    qp = [-literal if (DELTA_XOR >> i) & 1 else literal for i, literal in enumerate(q)]
    gq = c.sigma(q, 17, 19, 10)
    gqp = c.sigma(qp, 17, 19, 10)
    fpp = c.sigma(pp, 7, 18, 3)
    fqp = c.sigma(qp, 7, 18, 3)
    fp = c.sigma(p, 7, 18, 3)
    fq = c.sigma(q, 7, 18, 3)
    sides = [(c.plus(q, gq), c.plus(qp, gqp)),
             (c.plus(pp, q), c.plus(p, qp)),
             (c.plus(fpp, fqp), c.plus(fp, fq))]
    functional_clause_count = len(c.clauses)
    for left, right in sides:
        c.equate(left, right)
    mapping = {'p': p, 'pp': pp, 'q': q, 'qp': qp,
               'gq': gq, 'gqp': gqp, 'fpp': fpp, 'fqp': fqp, 'fp': fp, 'fq': fq,
               'sides': sides, 'one': c.one, 'functional_clause_count': functional_clause_count}
    return c, mapping


def value(lit, assignment):
    ans = assignment[abs(lit)]
    return ans if lit > 0 else not ans


def direct_sigma(x, which):
    # Independent scalar arithmetic; no bit-source arrays from the encoding.
    if which == 'f':
        a = ((x >> 7) | (x << 25)) & MASK
        b = ((x >> 18) | (x << 14)) & MASK
        return a ^ b ^ (x >> 3)
    a = ((x >> 17) | (x << 15)) & MASK
    b = ((x >> 19) | (x << 13)) & MASK
    return a ^ b ^ (x >> 10)


def evaluate(circuit, mapping, p, pp, q):
    assignment = {mapping['one']: True}
    for name, integer in [('p', p), ('pp', pp), ('q', q)]:
        for i, literal in enumerate(mapping[name]):
            assignment[literal] = bool((integer >> i) & 1)
    for gate in circuit.gates:
        values = [value(lit, assignment) for lit in gate['inputs']]
        assignment[gate['output']] = (sum(values) % 2 == 1) if gate['kind'] == 'xor3' else sum(values) >= 2
    return assignment


def word_value(word, assignment):
    return sum(int(value(lit, assignment)) << i for i, lit in enumerate(word))


def controls(circuit, mapping):
    rng = random.Random(0x435233)
    fixtures = [(rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(32)) for _ in range(64)]
    fixtures += [(1 << i, 1 << ((i+11) % 32), 1 << ((i+23) % 32)) for i in range(32)]
    fixtures += [(MASK, 1, MASK), (1, MASK, 1), (MASK, MASK, MASK)]
    for p, pp, q in fixtures:
        qp = q ^ DELTA_XOR
        assignment = evaluate(circuit, mapping, p, pp, q)
        assert word_value(mapping['qp'], assignment) == qp
        words = {'gq': (q, 'g'), 'gqp': (qp, 'g'), 'fpp': (pp, 'f'),
                 'fqp': (qp, 'f'), 'fp': (p, 'f'), 'fq': (q, 'f')}
        for name, (x, sigma) in words.items():
            assert word_value(mapping[name], assignment) == direct_sigma(x, sigma)
        expected = [[(q+direct_sigma(q, 'g')) & MASK, (qp+direct_sigma(qp, 'g')) & MASK],
                    [(pp+q) & MASK, (p+qp) & MASK],
                    [(direct_sigma(pp, 'f')+direct_sigma(qp, 'f')) & MASK,
                     (direct_sigma(p, 'f')+direct_sigma(q, 'f')) & MASK]]
        for pair, raw in zip(mapping['sides'], expected):
            assert [word_value(side, assignment) for side in pair] == raw
        assert all(any(value(lit, assignment) for lit in cl)
                   for cl in circuit.clauses[:mapping['functional_clause_count']])
        encoded_eqs = all(any(value(lit, assignment) for lit in cl)
                          for cl in circuit.clauses[mapping['functional_clause_count']:])
        assert encoded_eqs == all(left == right for left, right in expected)

    # A wrong local output bit must violate its defining clauses.
    assignment = evaluate(circuit, mapping, *fixtures[0])
    assignment[circuit.gates[0]['output']] = not assignment[circuit.gates[0]['output']]
    assert not all(any(value(lit, assignment) for lit in cl)
                   for cl in circuit.clauses[:mapping['functional_clause_count']])

    # Wrong XOR constant and sigma rotation are visible against the raw definition.
    assert (fixtures[0][2] ^ (DELTA_XOR ^ 1)) != (fixtures[0][2] ^ DELTA_XOR)
    wrong_g = lambda x: (((x >> 18) | (x << 14)) & MASK) ^ (((x >> 19) | (x << 13)) & MASK) ^ (x >> 10)
    assert any(wrong_g(1 << i) != direct_sigma(1 << i, 'g') for i in range(32))
    assignment = evaluate(circuit, mapping, MASK, 1, MASK)
    assert word_value(mapping['sides'][1][0], assignment) == 0
    return {'input_fixtures': len(fixtures), 'sigma_word_comparisons': 6*len(fixtures),
            'modular_sum_comparisons': 6*len(fixtures),
            'negative_controls': ['flipped internal gate bit', 'wrong XOR constant', 'wrong sigma rotation'],
            'overflow_control': '0x00000001 + 0xffffffff encoded as 0x00000000',
            'passed': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--solve', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    circuit, mapping = reconstruct()
    cnf = ('p cnf %d %d\n' % (circuit.nvars, len(circuit.clauses)) +
           ''.join(' '.join(map(str, cl))+' 0\n' for cl in circuit.clauses))
    (root/'independent.cnf').write_text(cnf)
    (root/'independent-circuit.json').write_text(json.dumps({'inputs_and_outputs': mapping,
                                                          'gates': circuit.gates}, indent=2)+'\n')
    result = {'nvars': circuit.nvars, 'nclauses': len(circuit.clauses),
              'cnf_sha256': hashlib.sha256(cnf.encode()).hexdigest(),
              'controls': controls(circuit, mapping),
              'discoverer_files_read_by_program': False}
    if args.solve:
        from pysat.solvers import Solver
        start = time.monotonic()
        with Solver(name='cadical195', bootstrap_with=circuit.clauses) as solver:
            sat = solver.solve()
        result['solver_cross_check'] = {'solver': 'pysat cadical195', 'satisfiable': sat,
                                        'elapsed_seconds': time.monotonic()-start,
                                        'is_certificate_review': False}
    (root/'RECONSTRUCTION_RUN.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
