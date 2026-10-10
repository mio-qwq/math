#!/usr/bin/env python3
"""Original-TF equality-graph entropy certificate and adversarial tests.
Independently rebuilds relations among UNDIRECTED edge variables from
A_uv=A_{alpha(u),beta(v)}. Greedy disjoint constraints are explicit.
This tests finite instances; theorem in GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md.
"""
from itertools import combinations
from random import Random
from collections import Counter
from hashlib import sha256
from pathlib import Path
import json

def one_case(n,alpha,beta):
    moved=[u for u in range(n) if alpha[u]!=u]
    a=len(moved)
    if a==0: return None
    order=moved+[u for u in range(n) if alpha[u]==u]
    constraints=[]
    for x in range(n):
        u=order[x]
        if alpha[u]==u:continue
        for y in range(x+1,n):
            v=order[y]
            source=tuple(sorted((u,v)))
            target=None if alpha[u]==beta[v] else tuple(sorted((alpha[u],beta[v])))
            if target==source:continue
            constraints.append((source,target))
    M=a*(n-a)+a*(a-1)//2
    assert len(constraints)>=M-a
    incidence=Counter()
    for src,tgt in constraints:
        incidence[src]+=1
        if tgt is not None:incidence[tgt]+=1
    assert max(incidence.values(), default=0)<=3
    used=set();picked=[]
    for src,tgt in constraints:
        involved={src} if tgt is None else {src,tgt}
        if not (used & involved):
            used |= involved;picked.append((src,tgt))
    assert len(picked)*6>=len(constraints)
    assert len(picked)*6>=M-a
    # Count the full TF degrees of freedom via independent DSU on all ordered pair constraints.
    edges=list(combinations(range(n),2)); ids={e:i for i,e in enumerate(edges)}
    z=len(edges);parent=list(range(z+1))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    def union(i,j):
        x,y=find(i),find(j)
        if x!=y:parent[x]=y
    for i in range(n):
        for j in range(n):
            left=z if i==j else ids[tuple(sorted((i,j)))]
            a,b=alpha[i],beta[j]
            right=z if a==b else ids[tuple(sorted((a,b)))]
            union(left,right)
    roots=set(find(i) for i in range(z));roots.discard(find(z))
    deficit=z-len(roots)
    assert deficit>=len(picked)
    return {'n':n,'alpha_support':a,'nontrivial_constraints':len(constraints),
            'maximum_incidence':max(incidence.values()),
            'greedy_independent_constraints':len(picked),'actual_entropy_deficit':deficit}

def main():
    rng=Random(20261010)
    out=[]
    for n in (8,10,12,16,20):
        for i in range(90):
            a=list(range(n));b=list(range(n))
            rng.shuffle(a);rng.shuffle(b)
            z=one_case(n,a,b)
            out.append(z)
        for k in (2,3,4,5):
            if k>n:continue
            # Low moved-support corner, with beta on a disjoint or overlapping support.
            a=list(range(n));b=list(range(n))
            for j in range(k):a[j]=(j+1)%k
            if k<n:
                b[k-1],b[k]=b[k],b[k-1]
            out.append(one_case(n,a,b))
    assert len(out)==5*(90+4)
    assert all(x['greedy_independent_constraints']<=x['actual_entropy_deficit'] for x in out)
    path=Path(__file__).with_name('dense_entropy_exact_results.json')
    data={'cases':len(out),'minimal_deficit':min(x['actual_entropy_deficit'] for x in out),
          'max_incidence':max(x['maximum_incidence'] for x in out),
          'sample_first':out[:8], 'sample_last':out[-8:]}
    path.write_text(json.dumps(data,indent=2)+'\n')
    print('PASS',len(out),'original ordered-TF constraint systems, degree<=3')
    print('PASS independent greedy constraints <= actual lost bits')
    print('max incidence',data['max_incidence'],'minimum exact entropy deficit',data['minimal_deficit'])
    print('source sha256',sha256(Path(__file__).read_bytes()).hexdigest())
    print('results sha256',sha256(path.read_bytes()).hexdigest())
if __name__=='__main__':main()
