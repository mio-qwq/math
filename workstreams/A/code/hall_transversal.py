#!/usr/bin/env python3
"""Independent deterministic Hall-matching certificate for two large-block partitions.

No graph library. This is deliberately disjoint from the prior auxiliary
multigraph orientation in verify_all_regular.py.
"""
from collections import defaultdict


def check_partition(parts, universe, k=2):
    blocks = [frozenset(block) for block in parts]
    if not blocks or any(len(b) < k for b in blocks):
        raise ValueError('every nonempty partition block must have at least k elements')
    seen = set()
    for b in blocks:
        if seen & b:
            raise ValueError('overlapping partition blocks')
        seen.update(b)
    if seen != set(universe):
        raise ValueError('partition must cover universe exactly')
    return blocks


def hall_transversal(parts, other_parts):
    """Select one from each P block without saturating any S block.

    Both P and S partitions of the same nonempty universe must have block size >=2.
    Returns selected set and an independently checkable injection witness mapping
    each dangerous S block to a distinct P block. P/S block indices are 0-based.
    """
    universe = set().union(*(set(b) for b in parts)) if parts else set()
    P=check_partition(parts, universe)
    S=check_partition(other_parts, universe)
    chosen_pairs=[tuple(sorted(b, key=repr)[:2]) for b in P]
    candidates={x for a,b in chosen_pairs for x in (a,b)}
    owner={x:i for i,pair in enumerate(chosen_pairs) for x in pair}
    dangerous=[]
    adj={}
    for j,component in enumerate(S):
        if not component<=candidates: continue
        indices=[owner[x] for x in component]
        if len(indices)!=len(set(indices)): continue
        dangerous.append(j)
        adj[j]=sorted(set(indices))
        assert len(adj[j])==len(component)>=2
    # S components form disjoint blocks. Every P block contributes two candidates
    # to their total union, so Hall's cardinality condition is guaranteed.
    assigned_part={}
    def augment(j,seen):
        for i in adj[j]:
            if i in seen:continue
            seen.add(i)
            if i not in assigned_part or augment(assigned_part[i],seen):
                assigned_part[i]=j
                return True
        return False
    for j in dangerous:
        if not augment(j,set()):
            raise AssertionError('matching failure contradicts the Hall count')
    match={j:i for i,j in assigned_part.items()}
    selected=[]
    for i,pair in enumerate(chosen_pairs):
        requiring=assigned_part.get(i)
        if requiring is None:
            selected.append(pair[0])
        else:
            valid=[x for x in pair if x not in S[requiring]]
            assert valid
            selected.append(valid[0])
    R=frozenset(selected)
    assert len(R)==len(P)
    assert all(len(R & block)==1 for block in P)
    assert all(not block<=R for block in S)
    return R,match,chosen_pairs


def verify_independently(parts,other_parts,roots):
    P=[set(b) for b in parts]
    S=[set(b) for b in other_parts]
    return (len(roots)==len(P) and all(len(set(b)&set(roots))==1 for b in P)
            and all(not set(b)<=set(roots) for b in S))
