#!/usr/bin/env python3
"""Independent exact validation of a nonisomorphic TF-cousin pair.

Only the literal RAW edge lists and T (not a discovery orbit mask) are used.
It checks source graph restrictions, a full two-layer cover isomorphism,
nonisomorphism via distinct exact invariant multisets, all certificate cycles,
and independently constructs the forced pair of C_k+C_k and C_(2k) from
an odd quotient cycle of EVEN-length permutation orbits.

This is a test of one finite witness, not a universal proof (see proof note).
"""
from collections import deque
from copy import deepcopy
from hashlib import sha256
from math import gcd
from pathlib import Path
import json, sys


def adjacency(n, raw):
    assert isinstance(n,int) and n>0 and not isinstance(n,bool)
    a=[[False]*n for _ in range(n)]
    seen=set()
    for edge in raw:
        assert isinstance(edge,list) and len(edge)==2
        u,v=edge
        assert type(u) is type(v) is int and 0<=u<v<n and (u,v) not in seen
        seen.add((u,v))
        a[u][v]=a[v][u]=True
    return a


def connected_bipartite(a):
    n=len(a);seen=[-1]*n; comps=0; bip=True
    for root in range(n):
        if seen[root]!=-1:continue
        comps+=1;seen[root]=0; todo=deque([root])
        while todo:
            i=todo.popleft()
            for j in range(n):
                if not a[i][j]:continue
                if seen[j]<0:seen[j]=seen[i]^1;todo.append(j)
                elif seen[j]==seen[i]:bip=False
    return comps==1,bip


def triangles(a):
    n=len(a)
    return sorted(sum(a[i][j] and a[j][k] and a[k][i]
                      for j in range(n) for k in range(j+1,n)) for i in range(n))


def decompose(T):
    n=len(T)
    assert type(T) is list and sorted(T)==list(range(n)) and all(type(t) is int for t in T)
    seen=set();out=[]
    for root in range(n):
        if root in seen:continue
        c=[];x=root
        while x not in seen:
            seen.add(x);c.append(x);x=T[x]
        assert x==root
        out.append(c)
    return out


def cover_edge(A,u,v):
    i,l=divmod(u,2);j,r=divmod(v,2)
    return l!=r and A[i][j]


def cover_bijection(A,B,T):
    n=len(A)
    inv=[0]*n
    for i,j in enumerate(T): inv[j]=i
    # Mapping G->H: layer0 unchanged, layer1 v becomes T^{-1}(v).
    phi=lambda x:(2*(x//2) if x%2==0 else 2*inv[x//2]+1)
    assert sorted(phi(x) for x in range(2*n))==list(range(2*n))
    for u in range(2*n):
        for v in range(2*n):
            assert cover_edge(A,u,v)==cover_edge(B,phi(u),phi(v)), (u,v)
    # Also verify the algebraic normal form from the separate raw H graph.
    assert all(B[u][v]==A[u][T[v]] for u in range(n) for v in range(n))


def simple_cycle(a,cycle):
    n=len(a)
    assert isinstance(cycle,list) and len(cycle)>=3
    assert all(type(x) is int and 0<=x<n for x in cycle)
    assert len(set(cycle))==len(cycle)
    assert all(a[cycle[i]][cycle[(i+1)%len(cycle)]] for i in range(len(cycle)))


def odd_cycle_in_quotient(A,orbits):
    # The full even-orbit quotient reconstructed from raw edges.
    even=[i for i,orb in enumerate(orbits) if len(orb)%2==0]
    adj={i:set() for i in even}
    for index,i in enumerate(even):
        for j in even[index+1:]:
            if any(A[u][v] for u in orbits[i] for v in orbits[j]):
                adj[i].add(j);adj[j].add(i)
    # DFS exhaustive, find one ODD SIMPLE quotient cycle, n small.
    def explore(path):
        a=path[0];end=path[-1]
        for v in sorted(adj[end]):
            if v==a and len(path)>=3 and len(path)%2==1:return list(path)
            if v not in path and v>=a:
                answer=explore(path+[v])
                if answer:return answer
        return None
    for root in even:
        result=explore([root])
        if result:return result
    return None


def orbit_cycle_construction(A,B,orbits,oddcycle):
    """Independent arithmetic reconstruction of Q_even odd-cycle lift."""
    k=len(oddcycle)
    assert k>=3 and k%2==1
    ms=[len(orbits[i]) for i in oddcycle]
    assert all(m>=2 and m%2==0 for m in ms)
    Gs=[];gs=[]
    for j in range(k):
        p,q=orbits[oddcycle[j]],orbits[oddcycle[(j+1)%k]]
        gg=gcd(len(p),len(q));gs.append(gg)
        pairs=[(u,v) for u in range(len(p)) for v in range(len(q)) if A[p[u]][q[v]]]
        assert pairs
        ss=(pairs[0][0]+pairs[0][1])%gg
        assert all(A[p[x]][q[y]] for x in range(len(p)) for y in range(len(q))
                   if (x+y)%gg==ss)
        assert all(B[p[x]][q[y]] for x in range(len(p)) for y in range(len(q))
                   if (x+y+1)%gg==ss)
        Gs.append(ss)
    D=sum(((-1)**(k-1-j))*Gs[j] for j in range(k))
    if D%2==0:
        good=A; doubling=B; evens=Gs; odds=[s-1 for s in Gs];side='G'
    else:
        good=B; doubling=A; evens=[s-1 for s in Gs]; odds=Gs;side='H'
    assert sum(((-1)**(k-1-j))*evens[j] for j in range(k))%2==0
    assert sum(((-1)**(k-1-j))*odds[j] for j in range(k))%2==1
    e=min(range(k),key=lambda e: ((gs[e]&-gs[e]).bit_length(),e))
    def fixed_cycle(S):
        d=sum(((-1)**(k-1-j))*S[j] for j in range(k))
        assert d%2==0
        x=[d//2]
        for j in range(k):x.append(S[j]-x[-1])
        assert x[-1]==x[0]
        return [orbits[oddcycle[j]][x[j]%ms[j]] for j in range(k)]
    c1=fixed_cycle(evens)
    modified=evens.copy();modified[e]+=gs[e]
    c2=fixed_cycle(modified)
    d=sum(((-1)**(k-1-j))*odds[j] for j in range(k))
    x=[(d-1)//2]
    for j in range(2*k):x.append(odds[j%k]-x[-1])
    assert x[-1]==x[0]
    cc=[orbits[oddcycle[j%k]][x[j]%ms[j%k]] for j in range(2*k)]
    simple_cycle(good,c1);simple_cycle(good,c2);simple_cycle(doubling,cc)
    assert set(c1).isdisjoint(c2)
    assert len(set(cc))==2*k
    return side,k,c1,c2,cc,gs,Gs


def verify(doc):
    n=doc['n']; A=adjacency(n,doc['G_edges']);B=adjacency(n,doc['H_edges'])
    assert len(doc['G_edges'])==len(doc['H_edges'])==20
    assert all(sum(a[i])==4 for a in [A,B] for i in range(n))
    assert all(connected_bipartite(a)==(True,False) for a in [A,B])
    assert all(len({tuple(row) for row in a})==n for a in [A,B])
    tg,th=triangles(A),triangles(B)
    assert tg==doc['G_triangle_incidence_multiset']
    assert th==doc['H_triangle_incidence_multiset']
    assert tg!=th, 'nonisomorphism not proven'
    T=doc['T'];orbits=decompose(T);cover_bijection(A,B,T)
    odd=odd_cycle_in_quotient(A,orbits)
    assert odd is not None
    side,k,c1,c2,c2k,gs,ss=orbit_cycle_construction(A,B,orbits,odd)
    assert side=='G' and k==doc['expected_odd_k']
    originalcycles=doc['two_disjoint_odd_cycles_in_G']
    assert len(originalcycles)==2
    for c in originalcycles:simple_cycle(A,c)
    assert set(originalcycles[0]).isdisjoint(originalcycles[1])
    simple_cycle(B,doc['doubled_cycle_in_H'])
    assert len(doc['doubled_cycle_in_H'])==2*k
    return {'order':n,'size_each':20,'T_orbit_sizes':[len(x) for x in orbits],
      'quotient_cycle':[len(orbits[j]) for j in odd],
      'gcds':gs,'selected_edge_residues':ss,
      'constructed_side_with_two_disjoint_Ck':side,'k':k,
      'constructed_two_cycles':[c1,c2],'constructed_C2k':c2k,
      'triangle_invariants':{'G':tg,'H':th}}


def mutated_inputs(doc):
    cases=[]
    bad=deepcopy(doc);bad['H_edges'].remove([0,4]);cases.append(('broken_cover_edge',bad))
    bad=deepcopy(doc);bad['T'][0],bad['T'][1]=bad['T'][1],bad['T'][0];cases.append(('broken_T_permutation',bad))
    bad=deepcopy(doc);bad['G_edges'].append([0,0]);cases.append(('illegal_loop',bad))
    bad=deepcopy(doc);bad['two_disjoint_odd_cycles_in_G'][1][0]=0;cases.append(('cycle_overlap',bad))
    bad=deepcopy(doc);bad['G_triangle_incidence_multiset'][0]=17;cases.append(('false_nonisomorphism_invariant',bad))
    for tag,data in cases:
        try:verify(data)
        except (AssertionError,ValueError):pass
        else:raise AssertionError('damaged witness unexpectedly accepted: '+tag)
    return [name for name,_ in cases]


def main():
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('mizzi_cousin_10_vertex.json')
    doc=json.loads(path.read_text(encoding='utf-8'))
    answer=verify(doc)
    errors=mutated_inputs(doc)
    print('PASS EXACT original-hypothesis TF-cousin certificate')
    print(json.dumps(answer,sort_keys=True))
    print('negative tests rejected',len(errors),errors)
    print('source_sha256',sha256(Path(__file__).read_bytes()).hexdigest())
    print('certificate_sha256',sha256(path.read_bytes()).hexdigest())
if __name__=='__main__':main()
