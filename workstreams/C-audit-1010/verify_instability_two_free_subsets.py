#!/usr/bin/env python3
"""Independent exact verifier for the Hujdurovic-Mitrovic four-added-vertex
construction with BOTH subsets A,B free, and both cross perfect matchings.
Checks 450 instances on K4 (all nonempty subsets) from original adjacency,
plus an all-m≥12 union-bound rational endpoint / monotonic finite gate.
"""
from fractions import Fraction
from math import comb, factorial
from hashlib import sha256
from pathlib import Path


def source_augmented(m, aset, bset, crossed):
    n=m+4
    g=[set() for _ in range(n)]
    def edge(u,v):
        assert u != v
        g[u].add(v);g[v].add(u)
    for u in range(m):
        for v in range(u+1,m):edge(u,v)
    a1,a2,b1,b2=m,m+1,m+2,m+3
    for u in range(m):
        if aset & (1<<u):edge(a1,u);edge(a2,u)
        if bset & (1<<u):edge(b1,u);edge(b2,u)
    if crossed:
        edge(a1,b2);edge(a2,b1)
    else:
        edge(a1,b1);edge(a2,b2)
    return g


def cover(g):
    h=[set() for _ in range(2*len(g))]
    for i,row in enumerate(g):
        for j in row:
            h[2*i].add(2*j+1);h[2*i+1].add(2*j)
    return h


def perm(m):
    N=m+4;p=list(range(2*N))
    a1,a2,b1,b2=m,m+1,m+2,m+3
    p[2*a1],p[2*a2]=p[2*a2],p[2*a1]
    p[2*b1+1],p[2*b2+1]=p[2*b2+1],p[2*b1+1]
    return p


def auto(h,p):
    return sorted(p)==list(range(len(h))) and all(
        {p[j] for j in h[i]}==h[p[i]] for i in range(len(h)))


def good_original(g):
    n=len(g);visited={0};que=[0]
    for x in que:
        for y in g[x]:
            if y not in visited:visited.add(y);que.append(y)
    if len(visited)!=n or len({frozenset(row) for row in g})!=n:
        return False
    # Nonbip follows from the original K_m triangle when m>=3.
    return all(len(g[i])>=1 for i in range(n)) and 0 in g[1] and 1 in g[2] and 2 in g[0]


def bound(m):
    # Three original union bounds, plus A=empty or B=empty.
    disc=Fraction(m,2**(m-1))+Fraction(2**4,2**m)
    twins=Fraction(comb(m,2),2**(m-1))
    bip=Fraction(2**(m+(m*m)//4),2**comb(m,2))
    empty=Fraction(2,2**m)
    return disc+twins+bip+empty


def main():
    m=4;seen=set();passed=0
    for A in range(1,1<<m):
        for B in range(1,1<<m):
            for twist in (0,1):
                g=source_augmented(m,A,B,twist)
                edges=tuple((i,j) for i,row in enumerate(g) for j in sorted(row) if i<j)
                assert edges not in seen;seen.add(edges)
                assert good_original(g)
                h=cover(g);p=perm(m)
                assert auto(h,p)
                # This fixes all old vertices in BOTH layers, yet moves a_i
                # on one layer and b_i on the other, so it is unexpected.
                assert p[0]==0 and p[1]==1 and p[2*m]!=2*m
                passed+=1
    assert passed==2*((1<<m)-1)**2==450
    # Negative controls directly mutate the source graph and the 2N mapping.
    g=source_augmented(m,1,2,0);p=perm(m)
    bad=[r.copy() for r in g];a,b=m,m+2
    bad[a].remove(b);bad[b].remove(a)
    assert not auto(cover(bad),p)
    bad=[r.copy() for r in g];bad[m].remove(0);bad[0].remove(m)
    assert not auto(cover(bad),p)
    q=p.copy();q[0]=q[2]
    assert not auto(cover(g),q)
    # Fraction arithmetic, no floating point in assertions.
    assert bound(12)==Fraction(11137,262144)
    assert bound(12)<Fraction(1,20)
    assert all(bound(i)>bound(i+1) for i in range(12,65))
    N=16;t=N-4
    lower=Fraction(19,20)*Fraction(2**(comb(t,2)+2*t+1),factorial(N))
    assert lower>0
    print('PASS 450 distinct labelled nontrivially-unstable graphs from K4')
    print('PASS 3 corrupted-input controls rejected')
    print('PASS m=12..65 exact rational bound; m12',bound(12),'N16 lower',lower)
    print('SHA256',sha256(Path(__file__).read_bytes()).hexdigest())

if __name__=='__main__':main()
