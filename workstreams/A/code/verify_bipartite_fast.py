#!/usr/bin/env python3
"""Polynomial-time block algorithm; exact independent induced-sequence verifier."""
def fast_order(U,V,E):
    U=set(U);V=set(V)
    if U&V or not U or not V:raise ValueError('bad bipartition')
    left={u:[] for u in U};right={v:[] for v in V};seen=set()
    for u,v,c in E:
        if u not in U or v not in V or (u,v) in seen:raise ValueError('not simple bipartite')
        seen.add((u,v));left[u].append((u,v,c));right[v].append((u,v,c))
    for u,es in left.items():
        if len(es)<3 or len({x[2] for x in es})!=len(es):raise ValueError('bad left degree/colours')
    for v,es in right.items():
        if len({x[2] for x in es})!=len(es):raise ValueError('bad right colours')
    Uorder=sorted(U)
    fixed={v:tuple(c for u in Uorder for a,b,c in right[v] if a==u) for v in V}
    out=[]
    for u in Uorder:
        color_edge={c:(a,b,c) for a,b,c in left[u]}
        colors=sorted(color_edge);d=len(colors)
        candidates=[tuple(colors[i:]+colors[:i]) for i in range(d)]
        candidates.append(tuple([colors[1],colors[0]]+colors[2:]))
        assert len(set(candidates))==d+1
        forbidden={fixed[v] for a,v,c in left[u]}
        chosen=next((p for p in candidates if p not in forbidden),None)
        assert chosen is not None
        out.extend(color_edge[c] for c in chosen)
    return out

def check_order(U,V,E,order):
    if len(E)!=len(order) or set(E)!=set(order):return False
    seq={v:[] for v in set(U)|set(V)}
    for u,v,c in order:seq[u].append(c);seq[v].append(c)
    return all(seq[u]!=seq[v] for u,v,c in E)

def run():
    count=0
    for m in range(3,41):
        for d in sorted({3,min(4,m),min(5,m),m}):
            U=[f'u{i}' for i in range(m)];V=[f'v{i}' for i in range(m)]
            E=[(f'u{i}',f'v{(i+j)%m}',j) for i in range(m) for j in range(d)]
            assert check_order(U,V,E,fast_order(U,V,E))
            count+=1
            if d>=4:
                E2=[e for e in E if not (int(e[0][1:])%2==0 and e[2]==d-1)]
                assert check_order(U,V,E2,fast_order(U,V,E2))
                count+=1
    U=['u0','u1','u2'];V=['v0','v1','v2']
    E=[(u,v,10*i+j) for i,u in enumerate(U) for j,v in enumerate(V)]
    assert check_order(U,V,E,fast_order(U,V,E))
    count+=1
    for bad in (E[:2],[(u,v,0) for u,v,c in E],E+[E[0]]):
        try:fast_order(U,V,bad)
        except ValueError:pass
        else:raise AssertionError('invalid case was accepted')
    print(f'PASS {count} graph/colouring cases; all independent final-order checks and negative controls passed')

if __name__=='__main__':run()
