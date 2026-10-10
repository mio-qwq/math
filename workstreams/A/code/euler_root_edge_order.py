#!/usr/bin/env python3
"""Independent root-selector implementation for fixed d-colour, d-regular graphs.

Unlike verify_all_regular.py, THIS constructor never uses an auxiliary
multigraph sinkless orientation or Hall matching. It selects roots using
balanced_partitions.balanced_colouring on two genuine vertex partitions.
It imports only the original-definition final-order verifier from the old
research module. No Lean proof or independent mathematical review implied.
"""
from collections import deque
from balanced_partitions import balanced_colouring
from verify_all_regular import validate


def construct_euler_root_order(vertices, edges, d):
    """Return (order, certificate) for proper d-colouring of a simple d-regular G.

    Certificate contains the actual bipartition, Q components, balanced
    incidence colouring, exact non-saturation roots, and ordered Q root forest.
    """
    V = set(vertices)
    E = [(min(a, b), max(a, b), c) for a, b, c in edges]
    assert d >= 3 and V and len(E) == len(set(E))
    assert len({(a, b) for a, b, c in E}) == len(E)
    adjacency = {v:{} for v in V}
    for a,b,c in E:
        assert a in V and b in V and a != b and c in range(d)
        assert c not in adjacency[a] and c not in adjacency[b]
        adjacency[a][c] = b
        adjacency[b][c] = a
    assert all(set(adjacency[v]) == set(range(d)) for v in V)

    # Construct the P partition from the two-colour 2-factor itself.
    cycles=[]; unvisited=set(V)
    while unvisited:
        start=min(unvisited); current=start; col=0; cycle=[]
        while current not in cycle:
            cycle.append(current)
            unvisited.remove(current)
            current=adjacency[current][col]
            col ^= 1
        assert current==start and len(cycle)>=4 and len(cycle)%2==0
        cycles.append(cycle)
    # Construct the S partition as actual components of the leftover graph Q.
    Q = [e for e in E if e[2]>=2]
    leftover={v:[] for v in V}
    for a,b,c in Q:
        leftover[a].append((b,c)); leftover[b].append((a,c))
    assert all(len(leftover[v]) == d-2 for v in V)
    S=[];visited=set()
    for seed in sorted(V):
        if seed in visited: continue
        component=set([seed]);visited.add(seed);queue=[seed]
        while queue:
            a=queue.pop()
            for b,c in leftover[a]:
                if b not in visited:
                    visited.add(b); component.add(b);queue.append(b)
        assert len(component)>=2
        S.append(sorted(component))
    # A separate Eulerian bipartite-incidence splitter; no old orientation routine.
    colouring = balanced_colouring(cycles, S)
    assert set(colouring)==V
    assert all(abs(sum(colouring[v]==0 for v in B)-sum(colouring[v]==1 for v in B))<=1
               for B in cycles+S)
    R = [next(v for v in C if colouring[v]==0) for C in cycles]
    rootset=set(R)
    assert len(rootset)==len(cycles)
    assert all(len(set(B)-rootset)>=len(B)//2 for B in S)

    # Order the roots toward their Q[R] boundary vertices.
    root_adj={r:[] for r in R};boundary=set()
    for a,b,c in Q:
        if a in rootset and b in rootset:
            root_adj[a].append(b);root_adj[b].append(a)
        elif a in rootset:boundary.add(a)
        elif b in rootset:boundary.add(b)
    ordered_roots=[];visited_roots=set()
    for start in R:
        if start in visited_roots:continue
        component={start};stack=[start];visited_roots.add(start)
        while stack:
            u=stack.pop()
            for v in root_adj[u]:
                if v not in visited_roots:
                    visited_roots.add(v);component.add(v);stack.append(v)
        edge_boundary=component & boundary
        assert edge_boundary
        base=min(edge_boundary)
        distances={base:0};queue=deque([base])
        while queue:
            u=queue.popleft()
            for v in root_adj[u]:
                if v not in distances:
                    distances[v]=distances[u]+1;queue.append(v)
        ordered_roots.extend(sorted(component,key=lambda v:(-distances[v],v)))
    assert set(ordered_roots)==rootset
    rank={r:i for i,r in enumerate(ordered_roots)}
    assert all(any(b not in rootset or rank[b]>rank[r] for b,c in leftover[r]) for r in R)

    # Rotate each two-colour cycle to its root, with colour 0 first.
    ordered_cycles=[];position={}
    for cid,r in enumerate(ordered_roots):
        vertices=[];v=r;col=0
        while v not in vertices:
            vertices.append(v);v=adjacency[v][col];col^=1
        assert v==r and len(vertices)>=4 and len(vertices)%2==0
        ordered_cycles.append(vertices)
        for j,x in enumerate(vertices):position[x]=(cid,j)
    slots={v:[] for v in V}
    for a,b,c in Q:
        if a in rootset and b in rootset:
            owner=min((a,b),key=position.get)
        elif a in rootset:owner=a
        elif b in rootset:owner=b
        else:owner=min((a,b),key=position.get)
        slots[owner].append((a,b,c))
    assert all(slots[r] for r in R)
    order=[]
    for cycle in ordered_cycles:
        for j,a in enumerate(cycle):
            b=cycle[(j+1)%len(cycle)]
            order.append((min(a,b),max(a,b),j%2))
            order.extend(sorted(slots[a],key=lambda e:e[2]))
    # Independent original-definition check: one complete edge order, fixed w.
    assert validate(V,E,order,d)
    cert={'cycles':cycles,'leftover_components':S,'two_colour_map':colouring,
          'rootset':sorted(rootset),'ordered_roots':ordered_roots,
          'blue_component_margins':[len(set(C)-rootset) for C in S]}
    return order,cert
