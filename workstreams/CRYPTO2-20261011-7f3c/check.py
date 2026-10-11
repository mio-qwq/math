#!/usr/bin/env python3
"""Standalone certificate checker, no import of construction or quotient solver.

Carryless product then polynomial long division (different field algorithm);
nontriviality and relatedness checked directly, and matrix inverse verified
by exact column elimination. This is implementation separation by the same
author, not independent-agent review. Python standard library only.
"""
import argparse
import copy
import json
from pathlib import Path


def require(ok, why):
    if not ok:
        raise ValueError(why)


def remainder(a, p):
    while a and a.bit_length() >= p.bit_length():
        a ^= p << (a.bit_length() - p.bit_length())
    return a


def product(a, b, p):
    z = 0
    for i in range(b.bit_length()):
        if (b >> i) & 1:
            z ^= a << i
    return remainder(z, p)


def gcd(a, b):
    while b:
        a, b = b, remainder(a, b)
    return a


def irreducible(p):
    m = p.bit_length()-1
    if m < 1 or not p & 1:
        return False
    x = remainder(2, p)
    y = x
    for k in range(1, m+1):
        y = product(y, y, p)
        if k <= m//2 and gcd(y ^ x, p) != 1:
            return False
    return y == x


def inverse(a, p):
    require(a != 0, 'zero inverse')
    u, v, g, h = a, p, 1, 0
    while u != 1:
        require(u != 0, 'nonunit')
        shift = u.bit_length()-v.bit_length()
        if shift < 0:
            u, v, g, h = v, u, h, g
            shift = -shift
        u ^= v << shift
        g ^= h << shift
    return remainder(g, p)


def nonsingular(A, p):
    # Column operations, as opposed to the constructor's row RREF.
    A = [r[:] for r in A]
    n = len(A)
    for i in range(n):
        j = next((j for j in range(i, n) if A[i][j]), None)
        if j is None:
            return False
        for row in A:
            row[i], row[j] = row[j], row[i]
        q = inverse(A[i][i], p)
        for k in range(n):
            A[k][i] = product(A[k][i], q, p)
        for j in range(i+1, n):
            t = A[i][j]
            for k in range(n):
                A[k][j] ^= product(t, A[k][i], p)
    return True


def raw_matrix(a):
    # Build columns by physical right rotation, not quotient indexing.
    cols = [a[:]]
    for _ in range(1, len(a)):
        cols.append(cols[-1][-1:] + cols[-1][:-1])
    return [list(r) for r in zip(*cols)]


def raw_apply(A, x, p):
    out = []
    for row in A:
        value = 0
        for a, b in zip(row, x):
            value ^= product(a, b, p)
        out.append(value)
    return out


def related(x, y, p):
    return all(product(product(a, b, p), a ^ b, p) == 0 for a, b in zip(x, y))


def check(cert):
    p, a, u, v = [cert[k] for k in ('modulus', 'column', 'u', 'v')]
    require(isinstance(p, int) and irreducible(p), 'reducible modulus')
    n, q = len(a), 1 << (p.bit_length()-1)
    require(n >= 3, 'dimension outside theorem')
    for row in (a, u, v, cert['Mu'], cert['Mv']):
        require(len(row) == n and all(type(x) is int and 0 <= x < q for x in row), 'bad encoding')
    require(any(u) and any(v) and u != v, 'trivial pair')
    A = raw_matrix(a)
    require(nonsingular(A, p), 'singular matrix')
    U, V = raw_apply(A, u, p), raw_apply(A, v, p)
    require(U == cert['Mu'] and V == cert['Mv'], 'wrong claimed output')
    require(any(U) and any(V) and U != V, 'trivial output')
    require(related(u, v, p), 'inputs not related')
    require(related(U, V, p), 'outputs not related')
    quotient = cert.get('quotient')
    if quotient is not None:
        d = quotient['dimension']
        require(isinstance(d, int) and d >= 3 and n % d == 0, 'bad divisor')
        b = quotient['column']
        require(len(b) == d, 'bad quotient dimension')
        B = raw_matrix(b)
        require(nonsingular(B, p), 'singular quotient')
        # Direct intertwining check on every basis vector.
        for j in range(d):
            x = [int(i == j) for i in range(d)]
            lhs = raw_apply(A, x*(n//d), p)
            rhs = raw_apply(B, x, p)*(n//d)
            require(lhs == rhs, 'wrong quotient intertwining')
        require(u == quotient['u']*(n//d) and v == quotient['v']*(n//d), 'wrong lift')
    return True


def negative_controls(cert):
    corrupt = []
    c = copy.deepcopy(cert); c['v'] = c['u'][:]; corrupt.append(('equal vectors', c))
    c = copy.deepcopy(cert); c['u'] = [0]*len(c['u']); corrupt.append(('zero vector', c))
    c = copy.deepcopy(cert); c['Mu'][0] ^= 1; corrupt.append(('wrong output', c))
    c = copy.deepcopy(cert); c['column'][0] ^= 1; corrupt.append(('matrix alteration', c))
    c = copy.deepcopy(cert); c['modulus'] = 5; corrupt.append(('reducible polynomial', c))
    c = copy.deepcopy(cert); c['u'][0] = 1 << (c['modulus'].bit_length()-1); corrupt.append(('invalid element', c))
    if cert.get('quotient') is not None:
        c = copy.deepcopy(cert); c['quotient']['column'][0] ^= 1; corrupt.append(('wrong quotient', c))
        c = copy.deepcopy(cert); c['quotient']['u'][0] ^= 1; corrupt.append(('wrong lift', c))
    for name, c in corrupt:
        try:
            check(c)
        except (ValueError, KeyError, TypeError):
            pass
        else:
            raise AssertionError('accepted corrupt certificate: ' + name)
    return len(corrupt)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--negative', action='store_true')
    args = ap.parse_args()
    obj = json.loads(args.certificate.read_text())
    certs = obj if isinstance(obj, list) else [obj]
    for cert in certs:
        check(cert)
    negatives = negative_controls(certs[0]) if args.negative else 0
    print(json.dumps({'status': 'PASS', 'certificates': len(certs), 'negative_controls': negatives}))
