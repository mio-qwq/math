#!/usr/bin/env python3
"""Definition-first TF functional-equality entropy check.

For a chosen moving alpha vertex u and each later v, create an edge-bit
constraint X_{u,v} = X_{alpha(u),beta(v)} (or zero for a diagonal).
Because each source bit occurs at most once, these are edges of a directed
functional graph.  A component has at most one cycle, so the dimension loss
is at least half the number of nontrivial constraints.
"""
from itertools import permutations, combinations
from random import Random
from math import comb
from hashlib import sha256
from pathlib import Path


def one(n, alpha, beta):
    E=list(combinations(range(n),2)); ids={x:i for i,x in enumerate(E)}
    moved=[u for u in range(n) if alpha[u]!=u]
    order=moved+[u for u in range(n) if alpha[u]==u]
    A=len(moved)
    # Unique edge variable per source, and no self-loops by construction.
    arrows={}
    for i,u in enumerate(order):
        if alpha[u] == u:continue
        for v in order[i+1:]:
            src=ids[tuple(sorted((u,v)))]
            im=None if alpha[u]==beta[v] else ids[tuple(sorted((alpha[u],beta[v])))]
            if im is not None and im == src:continue
            assert src not in arrows
            arrows[src]=im
    q=len(arrows)
    M=A*(n-A)+comb(A,2)
    assert q>=M-A
    # Independent DSU on all ordered TF equations: count exact lost bits.
    zero=len(E);p=list(range(zero+1))
    def find(x):
        while p[x]!=x:p[x]=p[p[x]];x=p[x]
        return x
    def union(x,y):
        x=find(x);y=find(y)
        if x!=y:p[x]=y
    for u in range(n):
        for v in range(n):
            x=zero if u==v else ids[tuple(sorted((u,v)))]
            y=zero if alpha[u]==beta[v] else ids[tuple(sorted((alpha[u],beta[v])))]
            union(x,y)
    roots={find(z) for z in range(len(E))};roots.discard(find(zero))
    deficit=len(E)-len(roots)
    # Direct constraint-only DSU verifies actual functional-graph rank.
    fp=list(range(zero+1))
    def ffind(x):
        while fp[x]!=x:fp[x]=fp[fp[x]];x=fp[x]
        return x
    for src,target in arrows.items():
        x=ffind(src);y=ffind(zero if target is None else target)
        if x!=y:fp[x]=y
    constrained_loss=zero-len({ffind(z) for z in range(zero)}-{ffind(zero)})
    assert constrained_loss*2 >= q,(n,alpha,beta,q,constrained_loss)
    assert deficit>=constrained_loss
    # Sharper all-n inequality when alpha moves many vertices
    assert 2*deficit>=q>=M-A
    return (q,constrained_loss,deficit)


def main():
    runs=0;worst=(2,1);has_cycle=False
    for n in range(3,6):
        ps=list(permutations(range(n)))
        for a in ps:
            for b in ps:
                if a==b:continue
                q,l,d=one(n,a,b);runs+=1
                if q>0 and 2*l==q:has_cycle=True
    rng=Random(20261010)
    for n in (6,8,10,12,16,20,30,40):
        for i in range(500):
            a=list(range(n));b=list(range(n));rng.shuffle(a);rng.shuffle(b)
            q,l,d=one(n,a,b);runs+=1
            if q>0 and 2*l==q:has_cycle=True
    assert has_cycle
    # Negative/optimality edge-case: two constraints forming one 2-cycle.
    p=[1,0,2,3]
    q=[0,1,3,2]
    one(4,p,q)
    print('PASS functional entropy; exact full TF DSU and selected partial DSU; cases',runs)
    print('tight 2-cycle found:',has_cycle)
    print('SHA256',sha256(Path(__file__).read_bytes()).hexdigest())
if __name__=='__main__':main()
