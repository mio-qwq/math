#!/usr/bin/env python3
"""Finite adversarial diagnostics on *heterogeneous* odd TF orbit families.

Randomly samples complete TF-invariant edge-orbit subsets from the original
ordered graph relation.  Explicitly checks: TF symmetry, quotient/bipartition
obstruction, cyclic plus/minus lifts, and all actual cycle edges.  This is
not a proof of the universal theorem; see mizzi_v3_asymmetric_theorem.md.
"""
from collections import deque
from hashlib import sha256
import itertools
from math import gcd, lcm
from pathlib import Path
from random import Random

SEED = 20261010
SIZES = [(3,5,7), (1,3,3,5,7), (3,3,5,5,7),
         (1,1,3,5,7,9), (1,3,9,3,5,5), (3,3,3,5,7)]
RUNS = 180


def generate(sizes, rng):
    off = [sum(sizes[:i]) for i in range(len(sizes))]
    n = sum(sizes)
    A = [[False]*n for _ in range(n)]
    for i in range(len(sizes)):
        for j in range(i+1,len(sizes)):
            m, k = sizes[i],sizes[j]
            g = gcd(m,k)
            chosen = [r for r in range(g) if rng.random() < rng.uniform(.25,.75)]
            for x in range(m):
                for y in range(k):
                    if (x+y)%g in chosen:
                        u,v=off[i]+x,off[j]+y
                        A[u][v] = A[v][u] = True
    alpha=[0]*n
    for i,m in enumerate(sizes):
        for x in range(m):alpha[off[i]+x]=off[i]+(x+1)%m
    inv=[0]*n
    for i,u in enumerate(alpha):inv[u]=i
    assert all(A[i][j]==A[alpha[i]][inv[j]] for i in range(n) for j in range(n))
    return A,off,alpha


def quotient(A,sz,off):
    inds=[i for i,m in enumerate(sz) if m>1]
    Q={i: set() for i in inds}
    for i,j in itertools.combinations(inds,2):
        if any(A[off[i]+x][off[j]+y] for x in range(sz[i]) for y in range(sz[j])):
            Q[i].add(j);Q[j].add(i)
    return Q


def find_odd_cycle(Q):
    # Exact search for shortest simple odd cycle with no repeat of a block.
    vertices=sorted(Q)
    for k in range(3,len(vertices)+1,2):
        for comb in itertools.combinations(vertices,k):
            root=min(comb)
            for perm in itertools.permutations([x for x in comb if x!=root]):
                cyc=(root,)+perm
                if all(cyc[(j+1)%k] in Q[cyc[j]] for j in range(k)):
                    return cyc
    return None


def check_bipartition_implies_ordinary_auto(A,sz,off,alpha,Q):
    color={}
    for seed in Q:
        if seed in color:continue
        color[seed]=0
        q=deque([seed])
        while q:
            i=q.popleft()
            for j in Q[i]:
                if j not in color:color[j]=1-color[i];q.append(j)
                else:assert color[j]!=color[i]
    p=list(range(len(A)))
    for i,mi in enumerate(sz):
        if mi>1:
            step=1 if color[i]==0 else -1
            for x in range(mi): p[off[i]+x]=off[i]+(x+step)%mi
    assert any(p[i]!=i for i in range(len(A)))
    assert all(A[i][j]==A[p[i]][p[j]] for i in range(len(A)) for j in range(len(A)))


def check_disjoint_cycle_lift(A,sz,off,Q,cyc):
    k=len(cyc)
    L=lcm(*(sz[i] for i in cyc))
    ss=[]
    for z in range(k):
        i,j=cyc[z],cyc[(z+1)%k]
        gi=gcd(sz[i],sz[j])
        all_orig=[(x,y) for x in range(sz[i]) for y in range(sz[j])
                  if A[off[i]+x][off[j]+y]]
        assert all_orig
        x,y=all_orig[0]
        s=(x+y)%gi
        assert all(A[off[i]+u][off[j]+v]
                   for u in range(sz[i]) for v in range(sz[j]) if (u+v)%gi==s)
        ss.append(s)
    half=pow(2,-1,L)
    # Independently solve by alternating recurrence from the source labels.
    D=sum((-1)**(k-1-i)*ss[i] for i in range(k))
    x0=(D*half)%L
    z=[x0]
    for j in range(k-1): z.append((ss[j]-z[-1])%L)
    assert (z[-1]+z[0]-ss[-1])%L == 0
    def vid(j,p):return off[cyc[j]]+(z[j]+p)%sz[cyc[j]]
    c=[vid(j,0) for j in range(k)]
    # Odd k => crossing path visits upper and lower labels at each block.
    dub=[]
    for t in range(2*k):
        j=t%k
        sign=1 if t%2==0 else -1
        dub.append(vid(j,sign*half))
    assert len(set(c))==k and len(set(dub))==2*k
    assert set(c).isdisjoint(dub)
    assert all(A[c[i]][c[(i+1)%k]] for i in range(k))
    assert all(A[dub[i]][dub[(i+1)%(2*k)]] for i in range(2*k))


def main():
    rng=Random(SEED)
    results=[]
    for sizes in SIZES:
        have_cycle=0
        bip_quotient=0
        for _ in range(RUNS):
            A,off,alpha=generate(sizes,rng)
            Q=quotient(A,sizes,off)
            odd=find_odd_cycle(Q)
            if odd is None:
                bip_quotient+=1
                check_bipartition_implies_ordinary_auto(A,sizes,off,alpha,Q)
            else:
                have_cycle+=1
                check_disjoint_cycle_lift(A,sizes,off,Q,odd)
        results.append((sizes,have_cycle,bip_quotient))
    for a,b,c in results:print('sizes',a,'lift_verified',b,'bipartite_forces_ordinary_auto',c)
    print('PASS sampled exact heterogeneous orbit checks',len(SIZES)*RUNS)
    print('SHA256',sha256(Path(__file__).read_bytes()).hexdigest())

if __name__=='__main__':main()
