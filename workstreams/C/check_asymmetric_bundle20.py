#!/usr/bin/env python3
"""Exact raw-edge checker for a 20-vertex *asymmetric* TF cycle-bundle.

Independent of the networkx discovery program. Certifies asymmetry via
isomorphism-invariant iterative vertex colours, all graph hypotheses, full
ordered-pair TF relation, and every edge of three listed disjoint cycles.
A finite witness is not a proof of the universal conjecture.
"""
from collections import deque
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import platform


def graph(raw):
    n=raw['n']
    assert type(n)==int and 1<=n<=100
    A=[[False]*n for _ in range(n)]
    for e in raw['edges']:
        assert type(e)==list and len(e)==2
        u,v=e
        assert type(u)==type(v)==int and 0<=u<v<n
        assert not A[u][v], 'duplicate undirected edge'
        A[u][v]=A[v][u]=True
    return A


def invariant_colors(A):
    n=len(A)
    deg=[sum(A[i]) for i in range(n)]
    tri=[sum(A[i][j] and A[i][k] and A[j][k]
             for j in range(n) for k in range(j+1,n)) for i in range(n)]
    keys=list(zip(deg,tri))
    colours=[{x:j for j,x in enumerate(sorted(set(keys)))}[x] for x in keys]
    rounds=0
    while True:
        enriched=[(colours[i],tuple(sorted(colours[j] for j in range(n) if A[i][j])))
                  for i in range(n)]
        lookup={key:c for c,key in enumerate(sorted(set(enriched)))}
        nxt=[lookup[key] for key in enriched]
        rounds+=1
        if nxt==colours:
            return colours,rounds
        colours=nxt


def connected_nonbipartite(A):
    n=len(A); colours=[-1]*n
    components=0;odd_edge=False
    for root in range(n):
        if colours[root]>=0:continue
        components+=1
        colours[root]=0
        queue=deque([root])
        while queue:
            u=queue.popleft()
            for v in range(n):
                if not A[u][v]:continue
                if colours[v]==-1:
                    colours[v]=colours[u]^1
                    queue.append(v)
                elif colours[v]==colours[u]: odd_edge=True
    return components==1,odd_edge


def check(raw):
    A=graph(raw);n=len(A)
    assert n==20 and sum(map(sum,A))==160
    connected,nonbip=connected_nonbipartite(A)
    assert connected and nonbip
    # Any graph automorphism must preserve degree, local triangle count,
    # and every refinement round. Unique final colours force it to be id.
    colors,rounds=invariant_colors(A)
    assert len(set(colors))==n, 'asymmetry not certified by colour refinement'
    assert len({tuple(row) for row in A})==n, 'not vertex determining'
    alpha=raw['alpha']
    assert isinstance(alpha,list) and len(alpha)==n
    assert all(type(x)==int for x in alpha) and sorted(alpha)==list(range(n))
    orbit_lengths=raw['orbit_lengths']
    assert orbit_lengths==[5,5,5,5]
    assert all(alpha[5*j+x]==5*j+(x+1)%5
               for j in range(4) for x in range(5))
    beta=[-1]*n
    for u,v in enumerate(alpha):beta[v]=u
    assert any(alpha[i]!=i for i in range(n))
    assert all(A[u][v]==A[alpha[u]][beta[v]]
               for u in range(n) for v in range(n)), 'TF condition false'
    allv=[];cycles=raw['expected_bundle_cycles']
    assert [len(c) for c in cycles]==[3,6,6]
    for c in cycles:
        assert all(type(v)==int and 0<=v<n for v in c)
        assert len(c)==len(set(c))
        assert all(A[c[i]][c[(i+1)%len(c)]] for i in range(len(c)))
        allv.extend(c)
    assert len(set(allv))==len(allv),'cycles are not vertex-disjoint'
    # The first three 5-cycles of alpha are exactly covered by the bundle.
    assert set(allv)==set(range(15))
    return {'n':n,'edges':sum(map(sum,A))//2,'asymmetric':True,
            'unstable_TF':True,'connected':True,'nonbipartite':True,
            'distinct_vertex_colours':len(set(colors)),
            'colour_refinement_rounds':rounds,
            'disjoint_cycle_lengths':list(map(len,cycles))}


def negative_controls(raw):
    tests=[]
    x=deepcopy(raw);x['edges'].pop(0);tests.append(('delete_edge',x))
    x=deepcopy(raw);x['alpha'][0]=x['alpha'][1];tests.append(('broken_permutation',x))
    x=deepcopy(raw);x['expected_bundle_cycles'][1][0]=x['expected_bundle_cycles'][0][0]
    tests.append(('overlap_cycles',x))
    x=deepcopy(raw);x['edges'].append([0,0]);tests.append(('loop',x))
    x=deepcopy(raw);x['edges'].append(x['edges'][0]);tests.append(('duplicate_edge',x))
    for label,altered in tests:
        try:check(altered)
        except AssertionError:continue
        raise AssertionError('corrupt case ACCEPTED: '+label)
    return len(tests)


def main():
    here=Path(__file__).parent
    p=here/'asymmetric_order5_bundle_raw.json'
    data=json.loads(p.read_text())
    result=check(data)
    count=negative_controls(data)
    print('PASS:',json.dumps(result,sort_keys=True))
    print('negative_controls_rejected:',count)
    print('Python:',platform.python_version())
    for path in (Path(__file__),p):
        print('sha256',path.name,sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':main()
