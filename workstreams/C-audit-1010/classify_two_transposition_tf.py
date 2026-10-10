#!/usr/bin/env python3
"""Exhaust all 2^15 labelled simple graphs on six vertices against a
specified genuinely non-diagonal TF symmetry (alpha=(01), beta=(23)).
Checks necessity/sufficiency of the four-new-vertex normal form using direct
ordered-edge evaluation, with three intentionally damaged instances.
"""
from itertools import combinations
from hashlib import sha256
from pathlib import Path

N=6
EDGES=list(combinations(range(N),2))
ALPHA=(1,0,2,3,4,5)
BETA=(0,1,3,2,4,5)


def adjacency(mask):
    a=[[False]*N for _ in range(N)]
    for k,(u,v) in enumerate(EDGES):
        if mask>>k&1:a[u][v]=a[v][u]=True
    return a


def tf_automorphism(a):
    return all(a[u][v]==a[ALPHA[u]][BETA[v]] for u in range(N) for v in range(N))


def normal_form(a):
    # a0,a1 = 0,1 ; b0,b1 = 2,3 ; remaining old vertices 4,5.
    if a[0][1] or a[2][3]:return False
    if any(a[0][u]!=a[1][u] or a[2][u]!=a[3][u] for u in (4,5)):
        return False
    return a[0][2]==a[1][3] and a[0][3]==a[1][2]


def main():
    found=0;good_pattern=0;normal=0
    for mask in range(1<<len(EDGES)):
        a=adjacency(mask);t=tf_automorphism(a);nf=normal_form(a)
        assert t==nf,(mask,t,nf)
        if t:
            found+=1
            if a[0][2]!=a[0][3]:good_pattern+=1
        if nf:normal+=1
    assert found==normal==2**(1+2*2+2)==128
    assert good_pattern==64
    # A single forbidden a0-a1 edge, mismatched a-attachment, or cross
    # matching asymmetry must be rejected by the original TF definition.
    witness=adjacency(0)
    for i,j in ((0,2),(1,3)):
        witness[i][j]=witness[j][i]=True
    assert tf_automorphism(witness)
    for u,v in ((0,1),(0,4),(0,3)):
        wrong=[row.copy() for row in witness]
        wrong[u][v]=wrong[v][u]=True
        assert not tf_automorphism(wrong)
    print('PASS all 32768 labelled simple six-vertex graphs checked')
    print('TF-invariant normal form: 128 of 32768, valid cross matching patterns: 64')
    print('negative controls rejected: 3')
    print('SHA256',sha256(Path(__file__).read_bytes()).hexdigest())

if __name__=='__main__':main()
