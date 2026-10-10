#!/usr/bin/env python3
"""Exact, independent reconstruction from Mizzi's generalized claw definition.
Prove a graph-isomorphism invariant distinguishes the even-r/odd-n
reflection twist from the source, without black-box graph isomorphism.
"""
import json,hashlib,argparse
from pathlib import Path
from collections import deque


def source(r,n):
    assert r>=2 and n>=3 and r%2==0 and n%2==1
    h=r*n; N=3*h+n
    e=[set() for _ in range(N)]
    def edge(a,b):
        assert a!=b
        e[a].add(b);e[b].add(a)
    for i in range(2*h):edge(i,(i+1)%(2*h))
    for p in range(h):
        leaf=2*h+p
        edge(leaf,p);edge(leaf,p+h);edge(leaf,3*h+p%n)
    assert sum(map(len,e))==10*h
    return e


def reflect_perm(r,n):
    h=r*n
    return ([(-i)%(2*h) for i in range(2*h)]+
            [2*h+(-p)%h for p in range(h)]+
            [3*h+(-j)%n for j in range(n)])


def twist(A,P):
    N=len(A)
    assert sorted(P)==list(range(N))
    assert all(P[P[i]]==i for i in range(N))
    assert all({P[j] for j in A[i]}==A[P[i]] for i in range(N))
    B=[{j for j in range(N) if P[j] in A[i]} for i in range(N)]
    assert all(i not in B[i] for i in range(N))
    assert all((i in B[j])==(j in B[i]) for i in range(N) for j in range(N))
    # Full CDC isomorphism: (i,0)->(i,0), (i,1)->(P(i),1).
    assert all((j in B[i])==(P[j] in A[i]) for i in range(N) for j in range(N))
    return B


def connected_and_odd_cycle(A):
    n=len(A);color=[-1]*n;color[0]=0;queue=deque([0]);odd=False
    while queue:
        i=queue.popleft()
        for j in A[i]:
            if color[j]<0:
                color[j]=1-color[i];queue.append(j)
            elif color[j]==color[i]:odd=True
    return all(c>=0 for c in color), odd


def invariant(A,r,n):
    h=r*n;N=len(A)
    # No hard-coded vertex labels: reconstruct types from vertex degrees and neighbours.
    center={i for i in range(N) if len(A[i])==r}
    assert len(center)==n and r!=3
    leaves={i for i in range(N) if i not in center and any(c in center for c in A[i])}
    rings=set(range(N))-center-leaves
    assert len(leaves)==h and len(rings)==2*h
    assert all(len(A[i]&rings)==2 for i in leaves)
    assert all(len(A[i]&rings)==2 for i in rings)
    assert all(len(A[i]&leaves)==r for i in center)
    # Canonical traverse of the unique intrinsic ring cycle.
    start=min(rings);neighbors=sorted(A[start]&rings)
    assert len(neighbors)==2
    path=[start];prev=start;cur=neighbors[0]
    while cur!=start:
        assert cur not in path and cur in rings
        path.append(cur)
        other=(A[cur]&rings)-{prev}
        assert len(other)==1
        prev,cur=cur,next(iter(other))
    assert len(path)==2*h and set(path)==rings
    pos={v:i for i,v in enumerate(path)}
    # Each leaf attaches an antipodal ring pair: record its unique slot mod h.
    slots={}
    for leaf in leaves:
        x,y=sorted(pos[v] for v in A[leaf]&rings)
        assert (y-x)==h
        slots[leaf]=x%h
    # Each center's incident leaf slots mod n: cardinality is invariant under
    # any dihedral relabelling of the intrinsic 2h-ring, so graph isomorphism.
    signatures=[tuple(sorted({slots[leaf]%n for leaf in A[c]&leaves})) for c in center]
    hist={str(k):sum(len(s)==k for s in signatures) for k in (1,2,3)}
    assert all(len(s) in (1,2) for s in signatures)
    return hist, sorted(signatures), len(rings), len(leaves),len(center)


def strict_check(r,n):
    A=source(r,n)
    P=reflect_perm(r,n)
    B=twist(A,P)
    a_conn,a_nonbip=connected_and_odd_cycle(A)
    b_conn,b_nonbip=connected_and_odd_cycle(B)
    assert a_conn and b_conn and a_nonbip and b_nonbip
    assert len(set(map(frozenset,A)))==len(A)
    assert len(set(map(frozenset,B)))==len(B)
    a_hist,a_sig,*_=invariant(A,r,n)
    b_hist,b_sig,*_=invariant(B,r,n)
    assert a_hist['1']==n and a_hist['2']==0
    assert b_hist['1']==1 and b_hist['2']==n-1, (r,n,a_hist,b_hist)
    return {'r':r,'n':n,'vertices':len(A),'edges':sum(map(len,A))//2,
            'source_center_signatures':a_hist,'twisted_center_signatures':b_hist,
            'nonisomorphism_certified':True,'CDC_isomorphism_certified':True,
            'both_connected_nonbip_twinfree':True}


def negative_controls():
    r,n=2,3;A=source(r,n);P=reflect_perm(r,n)
    bad=P.copy();bad[0]=bad[1]
    try:twist(A,bad)
    except AssertionError:pass
    else:raise AssertionError('accepted nonbijective permutation')
    bad=[s.copy() for s in A];bad[0].add(0)
    try:twist(bad,P)
    except AssertionError:pass
    else:raise AssertionError('accepted source loop')
    bad=[s.copy() for s in A];bad[0].remove(1);bad[1].remove(0)
    try:twist(bad,P)
    except AssertionError:pass
    else:raise AssertionError('accepted damaged symmetry')
    return 3


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',default='reflection_even_r_results.json')
    args=ap.parse_args()
    tests=negative_controls()
    records=[strict_check(r,n) for r in (2,4,6,8,10,12) for n in (3,5,7,9)]
    payload={'result':'PASS','source':'Mizzi 2603.27559v3 Remark 6.2 generalized claw CG_r(n)',
             'number_of_cases':len(records),'negative_tests':tests,'cases':records}
    out=Path(args.out);out.write_text(json.dumps(payload,indent=2)+'\n')
    print('PASS',len(records),'even r, odd n models, direct full CDC maps and nonisomorphism invariant')
    print('every source histogram: one-residue on ALL n centers')
    print('every twisted histogram: one-residue on 1 center, two-residue on n-1 centers')
    print('negative controls:',tests)
    print('source sha256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print('result sha256',hashlib.sha256(out.read_bytes()).hexdigest())

if __name__=='__main__':main()
