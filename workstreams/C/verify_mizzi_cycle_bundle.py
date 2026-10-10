#!/usr/bin/env python3
"""Independent integer checker for a heterogeneous TF-orbit cycle-bundle.

Input is an EXPLICIT edge list. The tool reconstructs graph adjacency,
checks the entire directed TF biconditional, reconstructs an odd quotient
cycle and its edge-orbit supports, and verifies every edge and vertex
of one C_k plus floor((m_min-1)/2) disjoint C_{2k}'s.

A finite checker does not prove the universal statement in
mizzi_cycle_bundle_extension.md. No external dependencies.
"""
from __future__ import annotations
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from math import gcd, lcm
from pathlib import Path
import platform


def adjacency(doc):
    n=doc['n']
    assert type(n)==int and n>0
    A=[[False]*n for _ in range(n)]
    for edge in doc['edges']:
        assert isinstance(edge,list) and len(edge)==2
        a,b=edge
        assert type(a)==type(b)==int and 0<=a<b<n
        assert not A[a][b], 'duplicated undirected edge'
        A[a][b]=A[b][a]=True
    assert all(not A[u][u] for u in range(n))
    return A


def check_simple_cycle(A,cyc):
    assert len(cyc)>=3 and len(set(cyc))==len(cyc)
    assert all(A[cyc[i]][cyc[(i+1)%len(cyc)]]
               for i in range(len(cyc)))


def check(doc):
    n=doc['n']; A=adjacency(doc)
    ms=doc['orbit_sizes']; bases=doc['orbit_base']
    assert len(ms)==len(bases)==3
    assert all(type(m)==int and m>=3 and m%2==1 for m in ms)
    assert bases==[sum(ms[:j]) for j in range(len(ms))]
    assert sum(ms)==n
    alpha=doc['alpha']
    assert type(alpha)==list and len(alpha)==n
    assert all(type(u)==int for u in alpha)
    assert sorted(alpha)==list(range(n)), 'not a permutation'
    assert all(alpha[bases[j]+x]==bases[j]+(x+1)%ms[j]
               for j in range(3) for x in range(ms[j]))
    beta=[-1]*n
    for i,v in enumerate(alpha):beta[v]=i
    for i in range(n):
        for j in range(n):
            assert A[i][j]==A[alpha[i]][beta[j]], 'TF edge/nonedge violation'
    # Independently check selected edges and complete residue class of each.
    S=[]
    for j in range(3):
        q=(j+1)%3
        mi,mq=ms[j],ms[q]
        g=gcd(mi,mq)
        edges=[(x,y) for x in range(mi) for y in range(mq)
               if A[bases[j]+x][bases[q]+y]]
        assert edges, 'missing quotient edge'
        s=sum(edges[0])%g
        assert all(A[bases[j]+x][bases[q]+y]
                   for x in range(mi) for y in range(mq)
                   if (x+y-s)%g==0), 'incomplete TF orbit edge'
        S.append(s)
    L=lcm(*ms)
    h=pow(2,-1,L)
    # For odd k, z_0=(s_0-s_1+s_2)/2; z_{j+1}=s_j-z_j.
    z=[((S[0]-S[1]+S[2])*h)%L]
    for j in range(2):z.append((S[j]-z[j])%L)
    assert (z[2]+z[0]-S[2])%L==0
    def at(j,shift):return bases[j]+(z[j]+shift)%ms[j]
    odd=[at(j,0) for j in range(3)]
    all_cycles=[odd]
    for t in range(1,(min(ms)-1)//2+1):
        doubled=[at(step%3, t if step%2==0 else -t)
                 for step in range(6)]
        all_cycles.append(doubled)
    vertices=[]
    for c in all_cycles:
        check_simple_cycle(A,c)
        vertices.extend(c)
    assert len(set(vertices))==len(vertices),'cycle overlap'
    expected=doc['expected_cycles']
    assert len(odd)==expected['odd'] and len(all_cycles)-1==expected['doubled']
    assert expected['all_disjoint'] is True
    # Direct verifier independent of any closed-form edge multiplicity.
    return {'n':n,'edges':sum(sum(row) for row in A)//2,
            'orbit_sizes':ms,'chosen_edge_residues':S,
            'cyclic_solution':z,
            'cycle_lengths':list(map(len,all_cycles)),
            'cycles':all_cycles, 'pairwise_disjoint':True}


def negative_controls(doc):
    tests=[]
    bad=deepcopy(doc);bad['edges'].pop(0)
    tests.append(('missing_input_edge',bad))
    bad=deepcopy(doc);bad['alpha'][0]=bad['alpha'][1]
    tests.append(('not_permutation',bad))
    bad=deepcopy(doc);bad['edges'].append([0,0])
    tests.append(('loop',bad))
    bad=deepcopy(doc);bad['edges'].append(bad['edges'][0])
    tests.append(('duplicated_edge',bad))
    bad=deepcopy(doc);bad['expected_cycles']['doubled']+=1
    tests.append(('false_bundle_multiplicity',bad))
    for name,changed in tests:
        try:check(changed)
        except AssertionError:continue
        raise AssertionError('False input ACCEPTED: '+name)
    return len(tests)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('data',nargs='?',default=str(Path(__file__).with_name('cycle_bundle_example.json')))
    args=p.parse_args()
    path=Path(args.data)
    obj=json.loads(path.read_text())
    result=check(obj)
    negative=negative_controls(obj)
    print('PASS exact raw-edge bundle witness')
    print('Python',platform.python_version())
    print(json.dumps(result,indent=2))
    print('negative controls rejected:',negative)
    for item in (Path(__file__),path):
        print('SHA256',item.name,sha256(item.read_bytes()).hexdigest())

if __name__=='__main__':main()
