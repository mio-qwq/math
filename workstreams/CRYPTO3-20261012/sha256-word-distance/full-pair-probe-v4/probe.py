#!/usr/bin/env python3
"""One bounded full independent-active-pair query, not a message search."""
import hashlib
import json
from pathlib import Path
import sys
import threading
import time

HERE = Path(__file__).resolve().parent
MASK = (1 << 32) - 1
SUPPORT_SHA = '02a12d8caa3ee3b78ec140f20fc0ad253835a6d32273247d20d22e0d8818edaf'


class Circuit:
    def __init__(self):
        self.n = 1
        self.zero = 1
        self.clauses = [[-1]]
        self.gates = []
        self.inputs = {}

    def fresh(self):
        self.n += 1
        return self.n

    def word(self, name):
        value = [self.fresh() for _ in range(32)]
        self.inputs[name] = value
        return value

    def gate(self, op, a, b):
        z = self.fresh()
        if op == 'xor':
            self.clauses.extend([[-a, -b, -z], [a, b, -z], [a, -b, z], [-a, b, z]])
        elif op == 'and':
            self.clauses.extend([[-a, -b, z], [a, -z], [b, -z]])
        elif op == 'or':
            self.clauses.extend([[a, b, -z], [-a, z], [-b, z]])
        else:
            raise ValueError(op)
        self.gates.append([op, a, b, z])
        return z

    def add(self, a, b):
        output, carry = [], self.zero
        for i in range(32):
            half = self.gate('xor', a[i], b[i])
            output.append(self.gate('xor', half, carry))
            if i != 31:
                both = self.gate('and', a[i], b[i])
                carried = self.gate('and', half, carry)
                carry = self.gate('or', both, carried)
        return output

    def sigma(self, x, kind):
        r, s, h = ((7, 18, 3), (17, 19, 10))[kind]
        return [self.gate('xor', self.gate('xor', x[(i+r) % 32], x[(i+s) % 32]),
                          x[i+h] if i+h < 32 else self.zero) for i in range(32)]

    def total(self, words):
        if not words:
            return [self.zero] * 32
        value = words[0]
        for word in words[1:]:
            value = self.add(value, word)
        return value

    def equal(self, a, b):
        for u, v in zip(a, b):
            self.clauses.extend([[-u, v], [u, -v]])


def build(support):
    c = Circuit()
    pair = {i: [c.word(f'w{i}'), c.word(f'wp{i}')] for i in support}
    sigma = {(i, prime, kind): c.sigma(pair[i][prime], kind)
             for i in support for prime in (0, 1) for kind in (0, 1)}
    unequal = {}
    for i in support:
        unequal[i] = [c.gate('xor', u, v) for u, v in zip(*pair[i])]
        c.clauses.append(unequal[i])
    for t in range(16, 64):
        left, right = [], []
        if t in pair:
            left.append(pair[t][1]); right.append(pair[t][0])
        for lag, kind in ((2, 1), (7, None), (15, 0), (16, None)):
            i = t-lag
            if i in pair:
                left.append(pair[i][0] if kind is None else sigma[i, 0, kind])
                right.append(pair[i][1] if kind is None else sigma[i, 1, kind])
        if left:
            c.equal(c.total(left), c.total(right))
    # v2(d17)=11 iff the low eleven input bits agree and bit eleven differs.
    for bit in range(11):
        c.clauses.append([-unequal[17][bit]])
    c.clauses.append([unequal[17][11]])
    return c


def sigma_bits(x, kind):
    r, s, shift = ((7, 18, 3), (17, 19, 10))[kind]
    result = 0
    for i in range(32):
        bit = ((x >> ((i+r) % 32)) ^ (x >> ((i+s) % 32))) & 1
        if i+shift < 32:
            bit ^= (x >> (i+shift)) & 1
        result |= bit << i
    return result


def check_pairs(pairs, support):
    assert sorted(pairs) == sorted(support)
    d, f, g = {}, {}, {}
    for i, (x, xp) in pairs.items():
        assert 0 <= x <= MASK and 0 <= xp <= MASK and x != xp
        d[i] = (xp-x) & MASK
        f[i] = (sigma_bits(xp, 0)-sigma_bits(x, 0)) & MASK
        g[i] = (sigma_bits(xp, 1)-sigma_bits(x, 1)) & MASK
    assert d[17] & 0xfff == 0x800
    assert d[8] == (-d[17]) & MASK
    residuals = [(d.get(t, 0)-g.get(t-2, 0)-d.get(t-7, 0)
                  -f.get(t-15, 0)-d.get(t-16, 0)) & MASK for t in range(16, 64)]
    assert residuals == [0] * 48
    return {'all_48_original_difference_equations': True, 'unequal_pairs': len(pairs),
            'D': f'{d[17]:08x}', 'valuation': 11, 'base_completion_checked': False}


def main():
    import pysat
    from pysat.solvers import Solver
    source = HERE.parent/'supports-v2.json'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SUPPORT_SHA
    support = json.loads(source.read_text())['supports'][5]
    c = build(support)
    dimacs = f'p cnf {c.n} {len(c.clauses)}\n' + ''.join(
        ' '.join(map(str, row))+' 0\n' for row in c.clauses)
    (HERE/'query.cnf').write_text(dimacs)
    circuit = {'schema': 'crypto3-support5-full-pair-circuit-v4', 'support': support,
               'variables': c.n, 'zero': c.zero, 'inputs': c.inputs, 'gates': c.gates,
               'valuation': {'index': 17, 'exact': 11}, 'base_constraints': False}
    (HERE/'circuit.json').write_text(json.dumps(circuit, indent=2)+'\n')
    result = {'schema': 'crypto3-support5-full-pair-probe-v4', 'support': 5,
              'model': 'all actual-pair difference recurrences; base completion absent',
              'valuation': {'index': 17, 'exact': 11}, 'conflict_budget': 50000,
              'wall_budget_seconds': 45, 'python': sys.version, 'pysat': pysat.__version__,
              'solver': 'Glucose3', 'variables': c.n, 'clauses': len(c.clauses),
              'cnf_sha256': hashlib.sha256(dimacs.encode()).hexdigest(),
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with Solver(name='g3', bootstrap_with=c.clauses, with_proof=True) as solver:
        solver.conf_budget(50000)
        timer = threading.Timer(45, solver.interrupt)
        timer.start()
        start = time.monotonic()
        try:
            answer = solver.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        result.update(status={True: 'sat', False: 'unsat', None: 'unknown'}[answer],
                      seconds=time.monotonic()-start, statistics=solver.accum_stats())
        if answer is True:
            model = set(solver.get_model())
            words = {name: sum((lit in model) << i for i, lit in enumerate(bits))
                     for name, bits in c.inputs.items()}
            pairs = {i: [words[f'w{i}'], words[f'wp{i}']] for i in support}
            result['direct_check'] = check_pairs(pairs, support)
            result['pairs'] = {str(i): values for i, values in pairs.items()}
        elif answer is False:
            proof = '\n'.join(solver.get_proof())+'\n'
            (HERE/'query.drup').write_text(proof)
            result['drup_sha256'] = hashlib.sha256(proof.encode()).hexdigest()
            result['certificate_checked'] = False
    (HERE/'RUN.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'pairs'}, indent=2))


if __name__ == '__main__':
    main()
