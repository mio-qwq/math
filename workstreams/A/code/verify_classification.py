#!/usr/bin/env python3
"""Exhaustive small-order audit from original edge-order definition. Stdlib only."""
from itertools import product,permutations

def proper(V,E,c):
    for v in V:
        x=[c[i] for i,(a,b) in enumerate(E) if v==a or v==b]
        if len(x)!=len(set(x)):return False
    return True

def has_order(V,E,c):
    incidence={v:[] for v in V}
    for i,(u,v) in enumerate(E):
        incidence[u].append(i);incidence[v].append(i)
    for order in permutations(range(len(E))):
        pos={e:k for k,e in enumerate(order)}
        f={v:tuple(c[i] for i in sorted(incidence[v],key=pos.get)) for v in V}
        if all(f[u]!=f[v] for u,v in E):return True
    return False

def run():
    res=[]
    for n in (4,6,8):
        V=list(range(n));E=[(i,(i+1)%n) for i in range(n)]
        count=bad=good=0
        for c in product(range(3),repeat=n):
            if not proper(V,E,c):continue
            ok=has_order(V,E,c)
            assert ok==(len(set(c))>=3),(n,c,ok)
            count+=1;good+=int(ok);bad+=int(not ok)
        res.append((n,count,bad,good))
    assert not has_order([0,1],[(0,1)],(0,))
    V=[0,1,2,3];E=[(0,1),(1,2),(2,3)]
    for c in product(range(4),repeat=3):
        if proper(V,E,c):assert has_order(V,E,c)
    print('PASS C4,C6,C8 all proper 3-colourings',res,'K2 and P4 controls PASS')

if __name__=='__main__':run()
