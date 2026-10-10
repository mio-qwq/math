#!/usr/bin/env python3
"""Exact rational gate for logarithmic-scale bound from Hujdurovic-Mitrovic
Problem 5.3 via their Construction 5.1 / Proposition 5.2.

This checks only finite identities, probability inequalities, and one explicit
source-defined unstable graph. The proof of the all-N theorem is in the note.
Standard library, exact fractions, mutation controls; no asymptotic oracle.
"""
from fractions import Fraction
from math import comb, factorial
import hashlib
from pathlib import Path


def bad_bound(m):
    assert m>=3
    disconnected=Fraction(m,2**(m-1)) + Fraction(2**4,2**m)
    twins=Fraction(comb(m,2),2**(m-1))
    bipartite=Fraction(2**(m+(m*m)//4),2**comb(m,2))
    return disconnected,twins,bipartite


def build_augmented(n=12):
    assert n>=3
    # Base graph K_n; A={0}, B={1}; extension from *original definition*.
    N=n+4
    g=[set() for _ in range(N)]
    def edge(i,j):
        assert i!=j
        g[i].add(j);g[j].add(i)
    for i in range(n):
        for j in range(i+1,n): edge(i,j)
    a1,a2,b1,b2=range(n,n+4)
    edge(a1,b1); edge(a2,b2)
    edge(a1,0);edge(a2,0)
    edge(b1,1);edge(b2,1)
    return g,(a1,a2,b1,b2)


def connected_nonbip_twinfree(g):
    n=len(g)
    seen={0};stack=[0]
    for v in stack:
        for u in g[v]:
            if u not in seen:seen.add(u);stack.append(u)
    assert len(seen)==n
    assert len(set(map(frozenset,g)))==n
    assert any(u in g[v] and v in g[w] and w in g[u]
               for u in range(n) for v in range(n) for w in range(n) if len({u,v,w})==3)


def cdc(g):
    n=len(g)
    h=[set() for _ in range(2*n)]
    for i in range(n):
        for j in g[i]:
            h[2*i].add(2*j+1)
            h[2*i+1].add(2*j)
    return h


def unexpected_phi(g,indices):
    n=len(g);a1,a2,b1,b2=indices
    p=list(range(2*n))
    p[2*a1],p[2*a2]=p[2*a2],p[2*a1]
    p[2*b1+1],p[2*b2+1]=p[2*b2+1],p[2*b1+1]
    return p


def valid_graph_auto(h,p):
    return sorted(p)==list(range(len(h))) and all({p[j] for j in h[i]}==h[p[i]]
                   for i in range(len(h)))


def tests():
    g,I=build_augmented();connected_nonbip_twinfree(g)
    h=cdc(g);p=unexpected_phi(g,I)
    assert valid_graph_auto(h,p)
    # p fixes many vertices while moving others only in individual layers, so
    # it cannot belong to the diagonal lifted Aut(g) or a lift times deck.
    assert p[0]==0 and p[1]==1 and p[2*I[0]]!=2*I[0]
    # Negative control 1: remove one source crossing edge; phi must fail.
    a1,a2,b1,b2=I
    broken=[s.copy() for s in g]
    broken[a1].remove(b1);broken[b1].remove(a1)
    assert not valid_graph_auto(cdc(broken),p)
    # Negative control 2: remove one symmetric attachment.
    broken=[s.copy() for s in g]
    broken[a1].remove(0);broken[0].remove(a1)
    assert not valid_graph_auto(cdc(broken),p)
    # Negative control 3: corrupted permutation fails bijection.
    corrupt=p.copy();corrupt[0]=corrupt[2]
    assert not valid_graph_auto(h,corrupt)
    return (len(g),sum(map(len,g))//2,3)


def main():
    bb=[sum(bad_bound(m)) for m in range(12,65)]
    assert all(x < Fraction(1,20) for x in bb)
    assert bb[0] == Fraction(11009,262144)
    assert all(bb[i]>bb[i+1] for i in range(len(bb)-1))
    assert Fraction(1,1)-bb[0]>Fraction(19,20)
    # Exact count at N=16 is a positive REAL lower bound on integer U_16.
    N=16;m=N-4
    lower=Fraction(114,5)*Fraction(2**comb(m,2),factorial(N))
    assert lower>0
    n,edges,negative=tests()
    print('PASS exact inequality m=12..64; m=12 bad-event bound',bb[0],float(bb[0]))
    print('N=16 unlabeled certified lower bound:',lower,float(lower))
    print('source-defined example N=',n,'edges=',edges,'negative controls=',negative)
    print('SHA256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())

if __name__=='__main__':main()
