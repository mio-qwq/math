#!/usr/bin/env python3
"""Exact-integer threshold diagnostics for the proposed effective unlabelled
CDC-instability asymptotic. The mathematical note, not finite tests, contains
the all-n counting proof. No numeric approximations or sample fitting.
"""
from math import factorial
from fractions import Fraction
from hashlib import sha256
from pathlib import Path


def check(n):
    assert n>=4096
    m=n-4
    # log2 n <= n/100, and already valid for n-s, n-s >= 3n/4.
    assert n**100 <= (1 << n)
    assert (3*n//4)**100 <= (1 << (3*n//4))
    # Dense ratio: -n^2/800 + (67/32)n <= -n^2/2000.
    assert Fraction(3,4000)*n >= Fraction(67,32)
    # Unlabelled 2-pattern overcount Q/H <= 2^(-n/2).
    C=10*factorial(8)**4
    assert C*n**4*(1 << 21) <= 1 << (n//2)
    # K_n Q/H <= 2^(-2n/5), from K<=n^4.
    assert n**4*(1 << (2*n//5)) <= 1 << (n//2)
    # Six error terms that are exp(-n/3) or better fit exp(-n/4).
    assert (1 << (n//4))*8 <= (1 << ((m//3)))
    return (n,m)


def main():
    cases=[check(n) for n in range(4096,4120)]+[check(n) for n in (4608,5120,8192,16384)]
    print('PASS',len(cases),'exact integer bounds at n>=4096 (diagnostic only)')
    print('candidate all-n theorem: unlabelled relative error <= 2^(-n/4), n>=4096')
    print('SHA256',sha256(Path(__file__).read_bytes()).hexdigest())
if __name__=='__main__':main()
