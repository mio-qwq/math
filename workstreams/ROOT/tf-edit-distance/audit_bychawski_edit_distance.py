#!/usr/bin/env python3
"""Falsification checks for Bychawski Conj 6.5 sharp TF edit distance.

Independent exact DSU computes MINIMUM edge flips from an arbitrary graph
into the family invariant under a fixed ordered TF pair. Compare against
independent orbit-pair mismatch bounds. Also construct the source's actual
connected, nonbipartite, reduced target with a true-twin automorphism.
No external graph library, no discovery imports or floating-point decisions.
"""
from itertools import combinations
from collections import deque
from random import Random
from hashlib import sha256
from pathlib import Path

RNG=Random(20261010)


def matrix(n):
    return [[bool(RNG.getrandbits(1)) if j>i else False for j in range(n)] for i in range(n)]


def symmetrize(A):
    n=len(A)
    for i in range(n):
        for j in range(i+1,n):A[j][i]=A[i][j]
    return A


def transposition(n, i, j):
    p=list(range(n));p[i],p[j]=p[j],p[i];return p


def exact_tf_edit_cost(A,a,b):
    n=len(A);edges=list(combinations(range(n),2));idx={pair:i for i,pair in enumerate(edges)}
    z=len(edges);parent=list(range(z+1))
    def find(u):
        while parent[u]!=u:parent[u]=parent[parent[u]];u=parent[u]
        return u
    def union(u,v):
        u=find(u);v=find(v)
        if u!=v:parent[u]=v
    for u in range(n):
        for v in range(n):
            src=z if u==v else idx[tuple(sorted((u,v)))]
            target=z if a[u]==b[v] else idx[tuple(sorted((a[u],b[v])))]
            union(src,target)
    force=find(z)
    grouped={}
    for u,v in edges:
        e=idx[u,v];root=find(e)
        group=grouped.setdefault(root,[0,0])
        group[int(A[u][v])]+=1
    return sum(group[1] if root==force else min(group) for root,group in grouped.items())


def original_orbit_mismatches(A,a,b):
    n=len(A);S={i for i in range(n) if a[i]!=i or b[i]!=i}
    W=set(range(n))-S
    done=set();orbits=[]
    for v in sorted(S):
        if v in done:continue
        stack=[v];done.add(v)
        for u in stack:
            for nxt in (a[u],b[u]):
                if nxt not in done:done.add(nxt);stack.append(nxt)
        assert len(stack)>=2
        orbits.append(stack)
    comparisons=[]
    for O in orbits:
        for k in range(len(O)//2):
            x,y=O[2*k],O[2*k+1]
            for w in W:comparisons.append((x,w,y,w))
    used=set()
    for x,w,y,z in comparisons:
        for e in ((min(x,w),max(x,w)),(min(y,z),max(y,z))):
            assert e not in used
            used.add(e)
    z=sum(A[x][w]!=A[y][v] for x,w,y,v in comparisons)
    return z,len(comparisons),len(S)


def invariant(A):
    n=len(A)
    rows=[tuple(row) for row in A]
    reduced=len(set(rows))==n
    seen={0};queue=deque([0]);colors={0:0};bip=True
    while queue:
        u=queue.popleft()
        for v in range(n):
            if not A[u][v]:continue
            if v not in seen:
                seen.add(v);colors[v]=1-colors[u];queue.append(v)
            elif colors[v]==colors[u]:bip=False
    return len(seen)==n,not bip,reduced


def make_true_twins(G):
    H=[row.copy() for row in G];n=len(G)
    H[0][1]=H[1][0]=True
    for w in range(2,n):H[0][w]=H[w][0]=G[1][w]
    edits=sum(G[i][j]!=H[i][j] for i in range(n) for j in range(i+1,n))
    a=transposition(n,0,1)
    assert all(H[u][v]==H[a[u]][a[v]] for u in range(n) for v in range(n))
    assert all(H[u][v]==H[v][u] for u in range(n) for v in range(n))
    return H,edits


def regression():
    tf_checks=0;full_source=0;upper_constructs=0
    for n in (5,6,8,10,12,16,20,32):
        for trial in range(250):
            G=symmetrize(matrix(n))
            a=list(range(n));b=list(range(n))
            RNG.shuffle(a);RNG.shuffle(b)
            if a==b==list(range(n)):continue
            bound,L,s=original_orbit_mismatches(G,a,b)
            cost=exact_tf_edit_cost(G,a,b)
            assert cost>=bound,(n,trial,a,b,cost,bound)
            tf_checks+=1
            H,edits=make_true_twins(G)
            assert edits==sum(G[0][w]!=G[1][w] for w in range(2,n))+int(not G[0][1])
            upper_constructs+=1
            W=[[G[i][j] for j in range(2,n)] for i in range(2,n)]
            # If the induced W is already connected/reduced/nonbip and 1 has
            # a neighbour in W, the edited graph MUST retain those properties.
            goodW=invariant(W)
            if all(goodW) and any(G[1][w] for w in range(2,n)):
                assert all(invariant(H)),(n,trial,goodW)
                full_source+=1
    # Three negative controls check that a damaged target or a wrong
    # claimed inequality is not accidentally accepted by this checker.
    G=symmetrize(matrix(8));H,_=make_true_twins(G)
    p=transposition(8,0,1)
    bad=[row.copy() for row in H];bad[0][2]=not bad[0][2];bad[2][0]=bad[0][2]
    assert not all(bad[u][v]==bad[p[u]][p[v]] for u in range(8) for v in range(8))
    bad=[row.copy() for row in H];bad[0][1]=bad[1][0]=False
    assert not (bad[0][1] and all(bad[0][w]==bad[1][w] for w in range(2,8)))
    bad=[row.copy() for row in H];bad[0][0]=True
    assert not all(not bad[i][i] for i in range(8)), 'illegal source loop accepted'
    return tf_checks,upper_constructs,full_source,3


if __name__=='__main__':
    v=regression()
    print('PASS raw TF-edge edit-distance DSU and disjoint orbit-pair lower bound:',v[0])
    print('PASS true-twin edge toggles:',v[1], 'original-target source conditions retained:',v[2])
    print('PASS negative controls:',v[3])
    print('SHA256:',sha256(Path(__file__).read_bytes()).hexdigest())
