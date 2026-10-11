#!/usr/bin/env python3
"""Deterministic exact RD witness construction; standard library only.

Discovery-side code. check.py deliberately does not import this module.
Field elements encode polynomials over F2 as integers, low degree bit first.
Circulant input is the FIRST COLUMN, M[i][j] = a[(i-j) % n].
"""
import json
from pathlib import Path


class Field:
    def __init__(self, modulus):
        self.modulus = modulus
        self.degree = modulus.bit_length() - 1
        self.size = 1 << self.degree

    def mul(self, a, b):
        z = 0
        while b:
            if b & 1:
                z ^= a
            b >>= 1
            a <<= 1
            if a & self.size:
                a ^= self.modulus
        return z

    def inv(self, a):
        if not a:
            raise ValueError('zero inverse')
        z, e = 1, self.size - 2
        while e:
            if e & 1:
                z = self.mul(z, a)
            a = self.mul(a, a)
            e >>= 1
        return z


def xor_sum(xs):
    z = 0
    for x in xs:
        z ^= x
    return z


def matrix(a):
    n = len(a)
    return [[a[(i-j) % n] for j in range(n)] for i in range(n)]


def mv(A, x, f):
    return [xor_sum(f.mul(a, b) for a, b in zip(row, x)) for row in A]


def rref(A, f, ncols=None):
    A = [row[:] for row in A]
    ncols = len(A[0]) if ncols is None else ncols
    pivots = []
    for j in range(ncols):
        k = next((i for i in range(len(pivots), len(A)) if A[i][j]), None)
        if k is None:
            continue
        i = len(pivots)
        A[i], A[k] = A[k], A[i]
        t = f.inv(A[i][j])
        A[i] = [f.mul(t, x) for x in A[i]]
        for k in range(len(A)):
            if k != i and A[k][j]:
                t = A[k][j]
                A[k] = [x ^ f.mul(t, y) for x, y in zip(A[k], A[i])]
        pivots.append(j)
    return A, pivots


def kernel(A, f):
    R, pivots = rref(A, f)
    n = len(A[0])
    free = next((j for j in range(n) if j not in pivots), None)
    if free is None:
        return None
    x = [0] * n
    x[free] = 1
    for i, j in enumerate(pivots):
        x[j] = R[i][free]
    return x


def solve(A, b, f):
    n = len(A)
    R, pivots = rref([row + [v] for row, v in zip(A, b)], f, n)
    if len(pivots) != n:
        raise ValueError('singular solve')
    return [row[-1] for row in R]


def sub(A, I, J):
    return [[A[i][j] for j in J] for i in I]


def singular_minor_pair(A, I, J, f):
    n = len(A)
    Ic = [i for i in range(n) if i not in I]
    Jc = [j for j in range(n) if j not in J]
    s = kernel(sub(A, I, J), f)
    if s is None:
        raise ValueError('minor is not singular')
    u = [0] * n
    for j, x in zip(J, s):
        u[j] = x
    D = sub(A, Ic, Jc)
    t = kernel(D, f)
    route = 'both-complementary-minors-singular'
    if t is None:
        t = solve(D, [mv(A, u, f)[i] for i in Ic], f)
        route = 'complementary-minor-invertible'
    v = [0] * n
    for j, x in zip(Jc, t):
        v[j] = x
    return u, v, route


def odd_pair(a, f):
    n = len(a)
    S = [matrix(a)[(-i) % n] for i in range(n)]
    r = n // 2
    A, c, B = list(range(r)), r, list(range(r+1, n))
    H = sub(S, B, A)
    if kernel(H, f) is not None:
        return singular_minor_pair(S, B, A, f)
    p, q = [S[i][c] for i in B], [S[i][c] for i in A]
    x = solve(H, p, f)
    y = solve([list(z) for z in zip(*H)], q, f)
    if not any(x) and not any(y):
        return singular_minor_pair(S, [c], [A[0]], f)
    return x + [1] + [0]*r, [0]*r + [1] + y, 'symmetric-block'


def witness(a, modulus):
    f = Field(modulus)
    n = len(a)
    if n < 3 or any(not 0 <= x < f.size for x in a):
        raise ValueError('bad dimension or field encoding')
    M = matrix(a)
    if kernel(M, f) is not None:
        raise ValueError('singular input matrix is out of scope')
    quotient = None
    if n % 2:
        u, v, route = odd_pair(a, f)
    elif n % 4 == 0:
        u = [x if i % 2 == 0 else 0 for i, x in enumerate(a)]
        v = [x if i % 2 else 0 for i, x in enumerate(a)]
        route = 'even-odd-polynomials'
        if not any(u) or not any(v):
            j = next(j for j, x in enumerate(M[0]) if not x)
            u, v, route = singular_minor_pair(M, [0], [j], f)
    else:
        d = n//2
        b = [a[i] ^ a[i+d] for i in range(d)]
        x, y, base_route = odd_pair(b, f)
        u, v = x*2, y*2
        route = 'periodic-lift/' + base_route
        quotient = {'dimension': d, 'column': b, 'u': x, 'v': y}
    if not any(u) or not any(v) or u == v:
        raise ArithmeticError('trivial construction')
    return {'modulus': modulus, 'column': a, 'u': u, 'v': v,
            'Mu': mv(M, u, f), 'Mv': mv(M, v, f),
            'route': route, 'quotient': quotient}


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--modulus', type=lambda s: int(s, 0), default=0x11b)
    ap.add_argument('--column', type=lambda s: [int(x, 0) for x in s.split(',')], required=True)
    args = ap.parse_args()
    print(json.dumps(witness(args.column, args.modulus), indent=2))
