#!/usr/bin/env python3
"""Global-size-tight simultaneous balancing of two finite set partitions.

Strengthens balanced_partitions.py: within every block of BOTH partitions,
red/blue counts differ by at most one; GLOBALLY red has exactly floor(|X|/2)
elements and blue has ceil(|X|/2). Constructive Eulerian augmentation pairs
odd block-vertices within each side, with at most one cross-side dummy edge.
The augmented graph need not be bipartite; the original incidence graph is.
Time/space O(|X|) on integer-indexed adjacency lists with hash maps for labels.
"""


def global_balanced(P, S):
    P=[tuple(part) for part in P]
    S=[tuple(part) for part in S]
    if any(len(part)==0 for part in P+S):
        raise ValueError('partition blocks must be nonempty')
    lp={};rp={}
    for i,part in enumerate(P):
        for x in part:
            if x in lp:raise ValueError('duplicate in P')
            lp[x]=i
    for j,part in enumerate(S):
        for x in part:
            if x in rp:raise ValueError('duplicate in S')
            rp[x]=j
    if set(lp)!=set(rp):raise ValueError('different underlying sets')
    n=len(lp);k=len(P);h=len(S)
    elements=list(lp)
    ends=[];adj=[[] for _ in range(k+h)]
    def add(a,b):
        eid=len(ends);ends.append((a,b));adj[a].append(eid);adj[b].append(eid)
        return eid
    for x in elements:add(lp[x],k+rp[x])
    oddL=[i for i in range(k) if len(adj[i])%2]
    oddR=[k+j for j in range(h) if len(adj[k+j])%2]
    # |oddL| and |oddR| have the same parity because both degree sums are n.
    assert (len(oddL)-len(oddR))%2==0
    for side in (oddL,oddR):
        for z in range(0,len(side)-1,2):
            add(side[z],side[z+1])
    if len(oddL)%2:
        add(oddL[-1],oddR[-1])
    assert all(len(a)%2==0 for a in adj)

    # Hierholzer, recovering explicit edge directions of every Euler tour.
    used=[False]*len(ends)
    orient=[None]*len(ends)
    for start in range(len(adj)):
        if not adj[start]:continue
        vertex_stack=[start]
        step_stack=[]
        circuit=[]
        while vertex_stack:
            v=vertex_stack[-1]
            while adj[v] and used[adj[v][-1]]:adj[v].pop()
            if not adj[v]:
                vertex_stack.pop()
                if step_stack:circuit.append(step_stack.pop())
            else:
                e=adj[v].pop()
                if used[e]:continue
                used[e]=True
                a,b=ends[e];w=b if a==v else a
                step_stack.append((e,v,w))
                vertex_stack.append(w)
        for e,a,b in reversed(circuit):
            assert orient[e] is None
            orient[e]=(a,b)
    assert all(used) and all(x is not None for x in orient)
    colors={x:(0 if orient[i]==ends[i] else 1) for i,x in enumerate(elements)}
    # Since P vertices' dummy edges are paired within the P side except at
    # most one P-S dummy, the global original imbalance is 0 (even n) or ±1.
    nred=sum(c==0 for c in colors.values())
    assert abs(2*nred-n)<=1,('global discrepancy not minimal',nred,n)
    if nred > n//2:colors={x:1-c for x,c in colors.items()}
    assert sum(c==0 for c in colors.values())==n//2
    assert validate_global(P,S,colors)
    return colors


def validate_global(P,S,colors):
    """Independent literal set-count test, unrelated to Euler traversal."""
    P=[tuple(p) for p in P];S=[tuple(s) for s in S]
    if any(not b for b in P+S):return False
    if set(colors)!={x for b in P for x in b}:return False
    if set(colors)!={x for b in S for x in b}:return False
    if sum(map(len,P))!=len(colors) or sum(map(len,S))!=len(colors):return False
    if any(c not in (0,1) for c in colors.values()):return False
    n=len(colors)
    if sum(c==0 for c in colors.values())!=n//2:return False
    return all(abs(sum(colors[x]==0 for x in b)-sum(colors[x]==1 for x in b))<=1
               for b in P+S)
