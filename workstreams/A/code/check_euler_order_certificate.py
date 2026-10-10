#!/usr/bin/env python3
"""Independent original-definition checker for an Euler-root edge-order certificate.

No import from Euler-root constructor, original generator or original validator.
Reconstructs the true two-colour cycles, leftover components, root placement,
full edge order and per-vertex incident colour lists from INPUT data only.
"""
from collections import deque


def check_certificate(vertices, edges, d, ordered_edges, certificate):
    try:
        V=set(vertices)
        if not V or d<3:return False
        E=[(min(a,b),max(a,b),c) for a,b,c in edges]
        O=[(min(a,b),max(a,b),c) for a,b,c in ordered_edges]
        if any(a==b or a not in V or b not in V or not 0<=c<d for a,b,c in E):return False
        if len(E)!=len(set(E)) or len({(a,b) for a,b,c in E})!=len(E):return False
        if len(O)!=len(E) or set(O)!=set(E) or len(set(O))!=len(O):return False
        inc={v:{} for v in V};seq={v:[] for v in V}
        for a,b,c in E:
            if c in inc[a] or c in inc[b]:return False
            inc[a][c]=b; inc[b][c]=a
        if any(set(inc[v])!=set(range(d)) for v in V):return False
        for a,b,c in O:
            seq[a].append(c);seq[b].append(c)
        if any(seq[a]==seq[b] for a,b,c in E):return False
        # Reconstruct the genuine alternating cycles as a partition of V.
        unseen=set(V);actual=[]
        while unseen:
            start=min(unseen);cyc=[];x=start;colour=0
            while x not in cyc:
                cyc.append(x);unseen.discard(x)
                x=inc[x][colour];colour^=1
            if x!=start or len(cyc)<4 or len(cyc)%2:return False
            actual.append(frozenset(cyc))
        claimed_cycles=certificate['cycles']
        if len(claimed_cycles)!=len(actual):return False
        if sorted(map(frozenset,claimed_cycles),key=lambda x:tuple(sorted(x)))!=sorted(actual,key=lambda x:tuple(sorted(x))):return False
        # Reconstruct Q connected components without using generator's code.
        graph={v:set() for v in V}
        for a,b,c in E:
            if c>=2:graph[a].add(b);graph[b].add(a)
        remaining=set(V);components=[]
        while remaining:
            root=min(remaining);component={root};q=deque([root]);remaining.remove(root)
            while q:
                x=q.popleft()
                for y in graph[x]:
                    if y in remaining:remaining.remove(y);component.add(y);q.append(y)
            components.append(frozenset(component))
        S=certificate['leftover_components']
        if sorted(map(frozenset,S),key=lambda x:tuple(sorted(x)))!=sorted(components,key=lambda x:tuple(sorted(x))):return False
        colouring=certificate['two_colour_map']
        if set(colouring)!=V or any(colouring[v] not in (0,1) for v in V):return False
        for block in claimed_cycles+S:
            reds=sum(colouring[v]==0 for v in block)
            if abs(2*reds-len(block))>1:return False
        roots=certificate['rootset'];R=set(roots)
        if len(R)!=len(claimed_cycles) or len(roots)!=len(R):return False
        if any(colouring[r]!=0 for r in R):return False
        if any(len(R & set(c))!=1 for c in claimed_cycles):return False
        if any(len(set(comp)-R)<len(comp)//2 for comp in S):return False
        if certificate['blue_component_margins'] != [len(set(comp)-R) for comp in S]:return False
        root_order=certificate['ordered_roots']
        if set(root_order)!=R or len(root_order)!=len(R):return False
        idx={v:i for i,v in enumerate(root_order)}
        if any(not any(w not in R or idx[w]>idx[v] for w in graph[v]) for v in R):return False
        return True
    except (AssertionError,ValueError,TypeError,IndexError,KeyError,NameError):
        return False
