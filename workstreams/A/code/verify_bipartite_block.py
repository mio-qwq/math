#!/usr/bin/env python3
"""Exact construction and verifier for bipartite sequencing. Standard library only."""
from itertools import permutations

def validate(U,V,edges):
    U,V=set(U),set(V)
    if not U or not V or U&V: raise ValueError('bad bipartition')
    incident={x:[] for x in U|V}
    seen=set()
    for u,v,c in edges:
        if u not in U or v not in V: raise ValueError('wrong endpoint part')
        if (u,v) in seen: raise ValueError('multiedge')
        seen.add((u,v))
        incident[u].append((u,v,c));incident[v].append((u,v,c))
    for x,es in incident.items():
        palette=[e[2] for e in es]
        if len(set(palette))!=len(palette): raise ValueError('not proper')
    if any(len(incident[u])<3 for u in U):raise ValueError('left degree too small')
    return incident

def construct(U,V,edges):
    I=validate(U,V,edges)
    forbidden={
        v:tuple(e[2] for u in sorted(U) for e in I[v] if e[0]==u)
        for v in V
    }
    out=[]
    for u in sorted(U):
        by_color={e[2]:e for e in I[u]}
        bad={forbidden[v] for _,v,_ in I[u]}
        choice=next((p for p in permutations(sorted(by_color)) if p not in bad),None)
        assert choice is not None
        out.extend(by_color[c] for c in choice)
    return out

def independent_check(U,V,edges,order):
    """Rebuild incident ordered colour sequences from actual global order."""
    want={(u,v,c) for u,v,c in edges}
    if len(order)!=len(want) or set(order)!=want:return False
    seq={x:[] for x in set(U)|set(V)}
    for u,v,c in order:
        seq[u].append(c);seq[v].append(c)
    return all(seq[u]!=seq[v] for u,v,c in edges)

def cases():
    k=0
    for m in range(3,13):
        for d in range(3,min(m,7)+1):
            U=[f'u{i}' for i in range(m)];V=[f'v{i}' for i in range(m)]
            edges=[(f'u{i}',f'v{(i+j)%m}',j) for i in range(m) for j in range(d)]
            order=construct(U,V,edges)
            assert independent_check(U,V,edges,order)
            assert not independent_check(U,V,edges,sorted(edges,key=lambda e:e[2]))
            k+=1
            if d>=4:
                removed={(f'u{i}',f'v{(i+d-1)%m}',d-1) for i in range(0,m,2)}
                less=[e for e in edges if e not in removed]
                assert independent_check(U,V,less,construct(U,V,less))
                k+=1
    U=['u0','u1','u2'];V=['v0','v1','v2']
    e=[(u,v,i+j*3) for i,u in enumerate(U) for j,v in enumerate(V)]
    assert independent_check(U,V,e,construct(U,V,e))
    k+=1
    for invalid in [e+[(e[0][0],e[0][1],44)],[(u,v,0) for u,v,c in e],e[:2]]:
        try:construct(U,V,invalid)
        except ValueError:pass
        else:raise AssertionError('bad graph or colouring accepted')
    good=construct(U,V,e)
    assert not independent_check(U,V,e,good[:-1])
    assert not independent_check(U,V,e,good+[good[0]])
    print(f'PASS {k} graph/colouring cases; invalid/negative checks PASS')

if __name__=='__main__':cases()
