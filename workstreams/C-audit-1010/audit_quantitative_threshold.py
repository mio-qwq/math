#!/usr/bin/env python3
"""Exact-arithmetic spot checks of elementary inequalities in the proof of
an explicit labelled nontrivial-CDC-instability asymptotic error bound.

The adjacent monotonicity and symbolic all-n proof live in the companion
research manuscript. This script is a falsification diagnostic, not a proof
that checking finitely many integers establishes an infinite statement.
"""
from fractions import Fraction
from hashlib import sha256
from math import comb
from pathlib import Path


def one(n):
    assert n >= 1024
    assert n**100 <= 1 << n # log2(n) <= n/100
    assert Fraction(19, 8800)*n >= Fraction(67,32) # dense term rate
    assert 16*n*n+48 <= 1 << (n//2) # bad base/attachments
    assert 192*(1 << 9) <= 1 << (n//2) # s=4,t=1
    assert n**4*(1 << 21) <= 1 << (n//2) # pair overlap
    assert Fraction(13,100)*n >= 16 # s=5,6 error terms
    assert Fraction(1,40)*n >= 3 # absorb six error terms
    assert Fraction(n*n,110) >= Fraction(n,2) # dense vs linear
    m=n-4
    # Bound elementary disconnected/twin probability + A/B empty
    from math import comb
    numerator=16*n*n+48
    assert numerator * (1 << (n//2)) <= 1 << n
    return n, Fraction(19*n*n, 8800), Fraction(67*n,32)


def main():
    rs=[one(n) for n in range(1024,1200)]+[one(n) for n in (1536,2048,4096,8192)]
    # minimal local direct original formulas
    for n in (8,16,40):
        m=n-4
        assert 3*comb(n,4)*(1 << (comb(m,2)+2*m+1)) == 3*comb(n,4)*(1 << (comb(n,2)-2*n+3))
    print('PASS',len(rs),'exact threshold arithmetic cases; n>=1024 samples only')
    print('base n=1024 dense slack:',rs[0][1]-rs[0][2])
    print('candidate labelled bound for all n>=1024: relative error <= 2^(-9n/20)')
    print('SHA256',sha256(Path(__file__).read_bytes()).hexdigest())

if __name__=='__main__':main()
