#!/usr/bin/env python3
"""Linear-time 2-colouring of the elements of two block-size>=2 partitions.

Both partition families become vertices of a bipartite multigraph; elements
become *labelled* incidence edges. Parallel edges are preserved. Every
partition block sees both colours. No external dependencies.
"""
from collections import deque


def split_partitions(P, S):
    """Return map element->0/1 such that every P and S block sees both values."""
    P=[tuple(b) for b in P];S=[tuple(b) for b in S]
    if not P or not S or any(len(set(b))!=len(b) or len(b)<2 for b in P+S):
        raise ValueError('both partitions require pairwise distinct elements, block sizes >=2')
    parts={}
    for i,block in enumerate(P):
        for x in block:
            if x in parts:raise ValueError('P overlaps')
            parts[x]=i
    if set(parts)!={x for b in S for x in b} or sum(map(len,S))!=len(parts):
        raise ValueError('S differs from P universe or overlaps')
    ns=len(P)+len(S)
    edge_ids={x:eid for eid,x in enumerate(parts)}
    endpoints=[];adj=[[] for _ in range(ns)]
    for j,block in enumerate(S):
        for x in block:
            a=parts[x];b=len(P)+j;eid=edge_ids[x]
            endpoints.append((eid,a,b))
            adj[a].append(eid);adj[b].append(eid)
    E=[None]*len(edge_ids)
    for eid,a,b in endpoints:E[eid]=(a,b)
    assert all(len(A)>=2 for A in adj)
    def opposite(eid,v):
        a,b=E[eid];return b if a==v else a
    colours={}
    seen=set()
    for start in range(ns):
        if start in seen:continue
        # First discover this component and find an undirected edge-labelled cycle.
        state={};parent={};parentedge={};cycle=None
        def explore(root):
            nonlocal cycle
            stack=[(root,iter(adj[root]))];state[root]=1
            while stack:
                u,it=stack[-1]
                try:eid=next(it)
                except StopIteration:
                    state[u]=2;stack.pop();continue
                if parentedge.get(u)==eid:continue
                v=opposite(eid,u)
                if v not in state:
                    parent[v]=u;parentedge[v]=eid;state[v]=1
                    stack.append((v,iter(adj[v])))
                elif state[v]==1:
                    cycle=[eid];x=u
                    while x!=v:
                        cycle.append(parentedge[x]);x=parent[x]
                    return
        explore(start)
        if cycle is None:raise AssertionError('degree>=2 component with no cycle')
        assert len(cycle)%2==0 and len(set(cycle))==len(cycle)
        for i,eid in enumerate(cycle):colours[eid]=i%2
        cycle_vertices={v for eid in cycle for v in E[eid]}
        # BFS forest rooted simultaneously at every cycle vertex.
        order=list(sorted(cycle_vertices));used=set(order)
        q=deque(order);treeparent={}
        while q:
            u=q.popleft()
            for eid in adj[u]:
                v=opposite(eid,u)
                if v not in used:
                    used.add(v);treeparent[v]=eid;q.append(v);order.append(v)
        seen.update(used)
        # All nontree edges have a fixed arbitrary colour first.
        forest_edges=set(treeparent.values())
        for u in used:
            for eid in adj[u]:
                if eid not in colours and eid not in forest_edges:
                    colours[eid]=0
        # Work from tree leaves towards the cycle.
        for v in reversed(order):
            if v not in treeparent:continue
            pe=treeparent[v]
            precoloured=[eid for eid in adj[v] if eid!=pe and eid in colours]
            if not precoloured:raise AssertionError('min-degree-2 invariant broken')
            colours[pe]=1-colours[precoloured[0]]
    assert len(colours)==len(E)
    split={x:colours[eid] for x,eid in edge_ids.items()}
    assert all({split[x] for x in B}=={0,1} for B in P+S)
    return split


def transversal(P,S):
    split=split_partitions(P,S)
    result={next(x for x in b if split[x]==0) for b in P}
    assert len(result)==len(P)
    assert all(len(set(b)&result)==1 for b in P)
    assert all(not set(b)<=result for b in S)
    return result
