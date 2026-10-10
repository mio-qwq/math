#!/usr/bin/env python3
"""Check the multi-colour insertion construction on independently generated regular graphs.
For d=4 roots exist by Haxell's theorem; finite runs use separate backtracking.
"""
from itertools import combinations

def matchings(vertices,forbidden):
    if not vertices:
        yield ()
        return
    a=min(vertices)
    for b in sorted(vertices-{a}):
        if frozenset((a,b)) in forbidden:continue
        yield from (((a,b),)+tail for tail in matchings(vertices-{a,b},forbidden))

def direct_check(V,edges,order,degree):
    if len(edges)!=len(order) or len(set(edges))!=len(edges) or set(edges)!=set(order):return False
    seq={v:[] for v in V}
    for a,b,c in order:
        seq[a].append(c);seq[b].append(c)
    if any(len(seq[v])!=degree or len(set(seq[v]))!=degree for v in V):return False
    return all(seq[a]!=seq[b] for a,b,c in edges)

def make_order(V,edges,degree):
    # Reconstruct original colour-specific adjacency, rejecting malformed input.
    by_color={v:{} for v in V}
    for a,b,c in edges:
        if c in by_color[a] or c in by_color[b]:raise ValueError('not proper')
        by_color[a][c]=b;by_color[b][c]=a
    assert all(set(by_color[v])==set(range(degree)) for v in V)
    assert len({(min(a,b),max(a,b)) for a,b,c in edges})==len(edges)
    cycles=[];unused=set(V)
    while unused:
        start=min(unused)
        component=[];node=start;color=0
        while node not in component:
            component.append(node);unused.discard(node)
            node=by_color[node][color]
            color=1-color
        assert node==start and len(component)>=4 and len(component)%2==0
        cycles.append(component)
    # Independent roots, with a second exact backtracking implementation.
    forbidden={frozenset((a,b)) for a,b,c in edges if c>=2}
    def roots_search(i,roots):
        if i==len(cycles):return roots
        for v in cycles[i]:
            if all(frozenset((v,w)) not in forbidden for w in roots):
                answer=roots_search(i+1,roots+[v])
                if answer is not None:return answer
        return None
    root_list=roots_search(0,[])
    assert root_list is not None,('independent transversal missing',cycles)
    roots=set(root_list)
    ordered_cycles=[];pos={}
    for cid,comp in enumerate(cycles):
        root=root_list[cid]
        cur=root;col=0;cyc=[]
        while cur not in cyc:
            cyc.append(cur);cur=by_color[cur][col];col=1-col
        assert cur==root and len(cyc)==len(comp)
        ordered_cycles.append(cyc)
        for j,v in enumerate(cyc):pos[v]=(cid,j)
    slots={v:[] for v in V}
    for a,b,c in edges:
        if c<2:continue
        owner=a if a in roots else b if b in roots else min((a,b),key=pos.get)
        slots[owner].append((min(a,b),max(a,b),c))
    result=[]
    for cyc in ordered_cycles:
        for j,v in enumerate(cyc):
            nxt=cyc[(j+1)%len(cyc)]
            result.append((min(v,nxt),max(v,nxt),j%2))
            result.extend(sorted(slots[v],key=lambda edge:edge[2]))
    assert direct_check(V,edges,result,degree)
    return result

def run():
    tally={}
    for parts in ((8,),(4,4)):
        comps=[];start=0
        for n in parts:
            comps.append(list(range(start,start+n)));start+=n
        base=[]
        for comp in comps:
            base.extend((min(comp[i],comp[(i+1)%len(comp)]),max(comp[i],comp[(i+1)%len(comp)]),i%2) for i in range(len(comp)))
        blocked={frozenset((a,b)) for a,b,c in base}
        count=0
        for M2 in matchings(set(range(start)),blocked):
            blocked_more=blocked|{frozenset(pair) for pair in M2}
            for M3 in matchings(set(range(start)),blocked_more):
                edges=base+[(a,b,2) for a,b in M2]+[(a,b,3) for a,b in M3]
                make_order(set(range(start)),edges,4)
                count+=1
        tally[str(parts)]=count
    # K4 Cartesian K2: 8-vertex connected nonbipartite 4-regular graph.
    pairs={0:((0,1),(2,3)),1:((0,2),(1,3)),2:((0,3),(1,2))}
    edges=[(a+4*i,b+4*i,c) for i in (0,1) for c,P in pairs.items() for a,b in P]
    edges += [(a,a+4,3) for a in range(4)]
    make_order(set(range(8)),edges,4)
    # A 5-regular K6 properly five-edge-coloured (all two-colour cycles length 6).
    K6=[]
    for c in range(5):
        for a,b in ((5,c),((c+1)%5,(c-1)%5),((c+2)%5,(c-2)%5)):
            K6.append((min(a,b),max(a,b),c))
    make_order(set(range(6)),K6,5)
    result=make_order(set(range(6)),K6,5)
    assert not direct_check(set(range(6)),K6,result[:-1],5)
    print('PASS 4-regular complete two-factor/matching enumeration',tally,
          'plus nonbipartite K4xK2, 5-regular K6, negative control')

if __name__=='__main__':run()
