#!/usr/bin/env python3
"""Check the finite ARC core over F_2[q], with no numeric specialization.

Coefficients are integer bit sets: bit i is the coefficient of q**i.
The input data is attributed to OpenAI family 199. The checker checks only
the explicitly enumerated finite identities, not the complete ARC theorem.
Python 3.9+; standard library only. Never run Python with -O for this file.
"""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def multiply(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result


def reference_multiply(a, b):
    """Independent sparse-exponent implementation of polynomial product."""
    powers_a = [i for i in range(a.bit_length()) if (a >> i) & 1]
    powers_b = [i for i in range(b.bit_length()) if (b >> i) & 1]
    powers = set()
    for i in powers_a:
        for j in powers_b:
            if i + j in powers:
                powers.remove(i + j)
            else:
                powers.add(i + j)
    return sum(1 << i for i in powers)


def vector_add(a, b):
    result = dict(a)
    for x, coefficient in b.items():
        result[x] = result.get(x, 0) ^ coefficient
        if not result[x]:
            del result[x]
    return result


def scale(vector, coefficient):
    return {
        x: product
        for x, value in vector.items()
        if (product := multiply(value, coefficient))
    }


def require(condition, label, witness=None):
    if not condition:
        raise ValueError(f"{label}: {witness!r}")


def verify(path):
    raw = path.read_bytes()
    data = json.loads(raw)
    require(data['format'] == 'arc-core-v1', 'data format')
    lower = data['lower_basis']
    basis = lower + lower.upper()
    radical = basis.replace('e', '').replace('f', '')
    require(len(set(basis)) == 20 and len(radical) == 18, 'basis sizes')

    # A bounded arithmetic implementation check is not the theorem proof;
    # the two formulas above implement polynomial convolution directly.
    for a, b in itertools.product(range(256), repeat=2):
        require(multiply(a, b) == reference_multiply(a, b),
                'polynomial multiplication implementation', (a, b))

    left = dict(data['left_corners'])
    right = dict(data['right_corners'])
    for x in lower:
        left[x.upper()] = right[x]
        right[x.upper()] = left[x]

    c_multiplication = {}
    for a, b in itertools.product(lower, repeat=2):
        value = {}
        if a in 'ef' and left[b] == a:
            value = {b: 1}
        if b in 'ef' and right[a] == b:
            value = {a: 1}
        c_multiplication[a, b] = value
    for word, outputs in data['nonunit_products'].items():
        value = {v: sum(1 << power for power in powers)
                 for v, powers in outputs.items()}
        c_multiplication[tuple(word)] = value

    multiplication = {}
    for a, b in itertools.product(basis, repeat=2):
        if a in lower and b in lower:
            value = c_multiplication[a, b]
        elif a in lower:
            value = {c.upper(): coefficient for c in lower
                     if (coefficient := c_multiplication[c, a].get(b.lower(), 0))}
        elif b in lower:
            value = {c.upper(): coefficient for c in lower
                     if (coefficient := c_multiplication[b, c].get(a.lower(), 0))}
        else:
            value = {}
        multiplication[a, b] = value

    def vector_multiply(a, b):
        result = {}
        for x, value_x in a.items():
            for y, value_y in b.items():
                result = vector_add(result, scale(multiplication[x, y],
                                                 multiply(value_x, value_y)))
        return result

    for a, b, c in itertools.product(basis, repeat=3):
        require(vector_multiply(multiplication[a, b], {c: 1}) ==
                vector_multiply({a: 1}, multiplication[b, c]),
                'associativity', (a, b, c))
    unit = {'e': 1, 'f': 1}
    for a in basis:
        require(vector_multiply(unit, {a: 1}) == {a: 1} ==
                vector_multiply({a: 1}, unit), 'unit', a)

    degrees = dict(data['degrees'])
    for x in lower:
        degrees[x.upper()] = 5 - degrees[x]
    for (a, b), value in multiplication.items():
        for v in value:
            require(degrees[v] == degrees[a] + degrees[b],
                    'homogeneous positive grading', (a, b, v))
    for a, b in itertools.product(basis, repeat=2):
        trace = multiplication[a, b].get('E', 0) ^ multiplication[a, b].get('F', 0)
        require(trace == (1 if b == a.swapcase() else 0),
                'symmetric nondegenerate trace', (a, b))
    require(vector_multiply(multiplication['u', 't'],
                            multiplication['u', 't']) == {'z': 6},
            'fourth radical product')

    cochain = {}
    for word, exponent in data['cochain_entries']:
        require(len(word) == 4 and exponent >= 0, 'cochain entry', word)
        a, b, c, v = word
        require((a, b, c) not in cochain, 'unique cochain input', word)
        cochain[a, b, c] = {v: 1 << exponent}
        require(a in radical and b in radical and c in radical, 'radical inputs', word)
        require(right[a] == left[b] and right[b] == left[c], 'composable inputs', word)
        require(left[a] == left[v] and right[c] == right[v], 'cochain corners', word)
        require(sum(x.isupper() for x in word[:3]) == int(v.isupper()) + 1,
                'weight minus one', word)
    require(len(cochain) == 179, 'cochain size')

    composable_words = 0
    for a, b, c, d in itertools.product(radical, repeat=4):
        if right[a] == left[b] and right[b] == left[c] and right[c] == left[d]:
            composable_words += 1
        value = vector_multiply({a: 1}, cochain.get((b, c, d), {}))
        for x, coefficient in multiplication[a, b].items():
            value = vector_add(value, scale(cochain.get((x, c, d), {}), coefficient))
        for x, coefficient in multiplication[b, c].items():
            value = vector_add(value, scale(cochain.get((a, x, d), {}), coefficient))
        for x, coefficient in multiplication[c, d].items():
            value = vector_add(value, scale(cochain.get((a, b, x), {}), coefficient))
        value = vector_add(value, vector_multiply(cochain.get((a, b, c), {}), {d: 1}))
        require(not value, 'Hochschild differential', (a, b, c, d, value))
    require(composable_words == 15250, 'composable four-word count', composable_words)

    gamma = set(data['boundary_gamma_q_letters'])
    for a, b in itertools.product(radical, repeat=2):
        lhs = [{}, {}]
        for w in radical:
            term = vector_multiply(cochain.get((a, b, w), {}), {w.swapcase(): 1})
            lhs[int(w.isupper())] = vector_add(lhs[int(w.isupper())], term)
        constant = scale(multiplication[a, b], 2 if b.isupper() and a in gamma else 0)
        linear = {}
        for v, coefficient in multiplication[a, b].items():
            gamma_sum = ((2 if b in gamma else 0) ^ (2 if v in gamma else 0)
                         ^ (2 if not b.isupper() and a in gamma else 0))
            if (product := multiply(gamma_sum, coefficient)):
                linear[v] = product
        require(lhs[0] == constant, 'twisted boundary constant coefficient', (a, b))
        require(lhs[1] == linear, 'twisted boundary H coefficient', (a, b))

    # Differential in s^r tensor bar(T) tensor s: outer faces vanish.
    cycle = [(('t', 'x', 'J'), 4), (('t', 'y', 'J'), 1)]
    differential = {}
    pairing = {}
    for (a, b, c), coefficient in cycle:
        require(left[a] == 'f' and right[c] == 'f', 'simple endpoints')
        for x, value in multiplication[a, b].items():
            differential = vector_add(differential, {(x, c): multiply(coefficient, value)})
        for x, value in multiplication[b, c].items():
            differential = vector_add(differential, {(a, x): multiply(coefficient, value)})
        pairing = vector_add(pairing, scale(cochain.get((a, b, c), {}), coefficient))
    require(not differential, 'bar cycle')
    require(pairing == {'f': 8}, 'nonzero cycle pairing')

    return {
        'status': 'verified exact polynomial identities',
        'scope': 'finite algebra, cocycle, twisted boundary and cycle only',
        'coefficient_ring': 'F_2[q], with indeterminate H in the boundary identity',
        'data_sha256': hashlib.sha256(raw).hexdigest(),
        'source_commit': data['source_commit'],
        'associativity_basis_triples': 20 ** 3,
        'Hochschild_radical_four_words': 18 ** 4,
        'composable_radical_four_words': composable_words,
        'boundary_radical_pairs': 18 ** 2,
        'cochain_entries': len(cochain),
        'nonzero_cycle_pairing': 'q^3 f',
        'complete_ARC_theorem_verified': False,
        'one_parameter_ARC_realization_independently_verified': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path,
                        default=Path(__file__).resolve().parents[1] / 'data' / 'arc-core.json')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    report = json.dumps(verify(args.data), indent=2) + '\n'
    if args.output:
        args.output.write_text(report, encoding='utf-8')
    print(report, end='')


if __name__ == '__main__':
    main()
