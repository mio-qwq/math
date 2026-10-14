"""Bounded independent definition checks; no imports from the candidate."""
from pathlib import Path
from math import comb
from fractions import Fraction as F
from itertools import product
from collections import deque
from datetime import datetime, timezone
import json, hashlib

root = Path(__file__).resolve().parent

def B(m,t):
    return comb(m,(m+t)//2) if abs(t)<=m and (m+t)%2==0 else 0

def T(a,b,c):
    return sum(B(a,t)*B(b,t)*B(c,t) for t in range(-min(a,b,c),min(a,b,c)+1))

def N(triple):
    a,b,c=triple
    if a%2==b%2==c%2:
        return T(a,b,c)
    pair=[d for d in triple if sum(v%2==d%2 for v in triple)==2]
    x,y=pair
    z=next(d for d in triple if d%2!=x%2)
    return z*T(x,y,z-1)+x*y*T(x-1,y-1,z)

def theta(triple):
    edges=[]
    next_vertex=2
    for length in triple:
        path=[0]+list(range(next_vertex,next_vertex+length-1))+[1]
        edges.extend(tuple(sorted(e)) for e in zip(path,path[1:]))
        next_vertex+=length-1
    assert len(edges)==len(set(edges))
    return next_vertex,edges

def count_labels(vertices,edges):
    adj=[[] for _ in range(vertices)]
    for u,v in edges:
        adj[u].append(v); adj[v].append(u)
    order=[0]; parent={0:None}
    for u in order:
        for v in adj[u]:
            if v not in parent:
                parent[v]=u; order.append(v)
    assert len(order)==vertices
    facets=admissible=0
    for increments in product((-1,0,1),repeat=vertices-1):
        f=[0]*vertices
        for v,inc in zip(order[1:],increments):
            f[v]=f[parent[v]]+inc
        if any(abs(f[u]-f[v])>1 for u,v in edges):
            continue
        admissible+=1
        sat=[[] for _ in range(vertices)]
        for u,v in edges:
            if abs(f[u]-f[v])==1:
                sat[u].append(v);sat[v].append(u)
        seen={0}; pending=[0]
        for u in pending:
            for v in sat[u]:
                if v not in seen:
                    seen.add(v);pending.append(v)
        facets+=len(seen)==vertices
    return {'facets':facets,'admissible':admissible,'tree_increment_candidates':3**(vertices-1)}

def h(s):
    return s*comb(s-1,(s-1)//2)

def M(n):
    assert n>=5
    k=(n+1)//2 if n%2 else n//2
    w=h(k)**2 if k%2 else h(k-1)*h(k+1)
    return w if n%2 else 2*w

def predicted(n):
    k=(n+1)//2 if n%2 else n//2
    if n%2:
        triple=(k-1,k-1,2) if k%2==0 else (k,k-2,2)
    else:
        triple=(k,k,1) if k%2==0 else (k+1,k-1,1)
    return tuple(sorted(triple))

def short1(p,q):
    return F(p*q+2,2)*B(p,0)*B(q,0)

def short2(x,y):
    return F(x*y+5,4)*B(x+1,0)*B(y+1,0)

receipt={'utc':datetime.now(timezone.utc).isoformat(),'scope':'finite checks only; universal proof independently reviewed in writing','definition_checks':[], 'counters':{}}
actual=[(1,2,2),(1,2,3),(1,3,3),(1,2,5),(1,3,4),(1,3,5),(1,2,6),(2,2,2),(2,2,3),(2,2,4),(2,2,5),(2,3,3),(2,3,4),(3,3,3)]
for triple in actual:
    vertices,edges=theta(triple)
    counts=count_labels(vertices,edges)
    assert counts['facets']==N(triple),(triple,counts,N(triple))
    assert counts['admissible']>counts['facets']
    receipt['definition_checks'].append({'triple':triple,'vertices':vertices,**counts})
print('Actual facet-label counts:',len(actual),'graphs')

counters={'legal_triples':0,'compression_orientations':0,'strict_compressions':0,'short_formulas':0,'same_parity_exclusions':0,'balancing_transfers':0,'bicyclic_block_data':0,'zero_row_vandermonde':0,'ratio_identities':0}
for p in range(17):
    for q in range(17):
        if (p-q)%2==0:
            assert sum(B(p,t)*B(q,t) for t in range(-min(p,q),min(p,q)+1))==B(p+q,0)
            counters['zero_row_vandermonde']+=1

for n in range(4,17):
    values=[]
    for a in range(1,n):
        for b in range(a,n):
            c=n+1-a-b
            triple=(a,b,c)
            if c<b or triple.count(1)>1:
                continue
            counters['legal_triples']+=1
            facets=N(triple)
            values.append((facets,triple))
            if n>=5:
                assert facets<M(n)
            if a%2==b%2==c%2:
                k=(n+1)//2 if n%2 else n//2
                dominant=(1,2*k-3,2) if n%2 else (2,2*k-2,1)
                assert facets<N(dominant)
                counters['same_parity_exclusions']+=1
            else:
                pair=[d for d in triple if sum(v%2==d%2 for v in triple)==2]
                z=next(d for d in triple if d%2!=pair[0]%2)
                for x,y in (pair,pair[::-1]):
                    if x%2==0:
                        compressed=(x,y+z-1,1)
                        strict=z>1
                    elif x>=3:
                        compressed=(x,y+z-2,2)
                        strict=z>2
                    else:
                        continue
                    assert facets<=N(compressed)
                    assert not strict or facets<N(compressed)
                    counters['compression_orientations']+=1
                    counters['strict_compressions']+=strict

    best=max(f for f,_ in values)
    winners=[t for f,t in values if f==best]
    assert winners==[predicted(n)],(n,winners,predicted(n))
    if n>=5:
        k=(n+1)//2 if n%2 else n//2
        numerator=(k*k-2*k+(6 if k%2==0 else 5)) if n%2 else (k*k+(2 if k%2==0 else 1))
        assert F(best,M(n))==F(numerator,k*(k+1))
        counters['ratio_identities']+=1
    receipt.setdefault('unique_maxima',[]).append({'n':n,'triple':winners[0],'N':best})

for p in range(2,17,2):
    for q in range(2,17,2):
        assert N((p,q,1))==short1(p,q)
        counters['short_formulas']+=1
        if p>=q+4:
            assert short1(p-2,q+2)>short1(p,q)
            assert short2(p-3,q+1)>short2(p-1,q-1)
            counters['balancing_transfers']+=2
for x in range(1,17,2):
    for y in range(1,17,2):
        if x==y==1:
            continue
        assert N((x,y,2))==short2(x,y)
        counters['short_formulas']+=1

for n in range(5,17):
    equality=[]
    for p in range(3,n+2):
        for q in range(p,n+2):
            t=n+1-p-q
            if t<0:
                continue
            cyclep=comb(p,p//2) if p%2==0 else h(p)
            cycleq=comb(q,q//2) if q%2==0 else h(q)
            facets=2**t*cyclep*cycleq
            assert facets<=M(n)
            if facets==M(n):
                assert p%2==q%2==1 and t==(0 if n%2 else 1) and q-p<=2
                equality.append((p,q,t))
            counters['bicyclic_block_data']+=1
    assert len(equality)==1
    receipt.setdefault('maximizing_block_data',[]).append({'n':n,'cycle_bridge_data':equality[0]})

# Independent semantic damage controls: disconnected saturated graphs are
# not counted, and a duplicated unit path is rejected as a simple graph.
try:
    theta((1,1,3))
except AssertionError:
    duplicate_rejected=True
else:
    duplicate_rejected=False
assert duplicate_rejected
assert N((2,2,1))==12 and N((1,3,2))==24
receipt['damage_controls']={'duplicate_unit_path_rejected':duplicate_rejected,'disconnected_admissible_labels_rejected':all(row['admissible']>row['facets'] for row in receipt['definition_checks'])}
receipt['counters']=counters
receipt['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
receipt['status']='PASS'
(root/'INDEPENDENT_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','counters':counters,'total_actual_tree_label_assignments':sum(row['tree_increment_candidates'] for row in receipt['definition_checks']),'damage_controls':receipt['damage_controls']},indent=2))
