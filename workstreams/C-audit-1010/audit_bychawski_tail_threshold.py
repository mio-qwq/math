#!/usr/bin/env python3
"""Exact-integer diagnostics for universal TF expected-size tail at n>=1024.

The SYMBOLIC mathematical proof in BYCHAWSKI_C66_EFFECTIVE_BOUND.md proves
all-n inequalities; a finite check cannot establish asymptotic theorems.
"""
from math import comb
from hashlib import sha256
from pathlib import Path


def check(n):
    assert n>=1024
    # log2 n <= n/100 and n<=2^(n/100) using stronger easy integer test.
    assert n**100 <= 1 << n
    # s=5,6 contribution <=2*n^12*2^(-3n+18) <= 2*n^4*2^(-2n)
    assert n**8 * (1<<18) <= 1<<n
    # s>=7: n*2^(-497 n/200) <= 2^(-2n)
    assert n**200 <= 1 << (97*n)
    # dense contribution <=2^(-9 n^2 /800 +3n/32) <= 2^(-2n)
    assert 9*n*32 >= 800*(64+3)
    # probability random labelled graph is nonreduced <1/2
    b=comb(n,2)
    assert b <= (1 << (n-2))
    # total bound coefficient <=2^13
    assert 384+6144+2+1+1 <= (1<<13)
    # conditioning error factor with a conservative 2^16 coefficient
    assert 2*(1+(1<<13)) <= (1<<16)
    return n


def main():
    values=[check(n) for n in range(1024,1224)]+[check(n) for n in (2048,4096,8192)]
    assert len(values)==203
    print('PASS',len(values),'exact integer threshold diagnostics at n>=1024')
    print('Uniform TF-pair tail n>=1024 <= 2^13*n^4*2^(-2n)')
    print('Reduced conditional projection error n>=1024 <=2^16*n^4*2^(-2n)')
    print('SHA256',sha256(Path(__file__).read_bytes()).hexdigest())

if __name__=='__main__':main()
