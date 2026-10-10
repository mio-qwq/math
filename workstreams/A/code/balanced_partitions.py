#!/usr/bin/env python3
"""Simultaneously balance two finite set partitions using an Euler orientation.

Each element is a separately labelled incidence edge of a bipartite
multigraph. Parallel edges are preserved; no third-party dependencies.
"""


def partition_blocks(P, S):
    """Validate nonempty, disjoint blocks with the same underlying universe."""
    P = [tuple(b) for b in P]
    S = [tuple(b) for b in S]
    if any(not b for b in P + S):
        raise ValueError('empty partition block is not permitted')
    def owner_map(blocks):
        owners = {}
        for i, b in enumerate(blocks):
            for x in b:
                if x in owners:
                    raise ValueError('duplicate element in the same partition')
                owners[x] = i
        return owners
    left = owner_map(P)
    right = owner_map(S)
    if set(left) != set(right):
        raise ValueError('partitions must contain exactly the same finite set')
    return P, S, left, right


def balanced_colouring(P, S):
    """Output element->0/1, discrepancy<=1 in EVERY block of BOTH partitions.

    Singleton blocks are allowed and the empty universe produces {}.
    All adjacency and Eulerian traversal operations are linear in |X|.
    """
    P, S, owner_p, owner_s = partition_blocks(P, S)
    k, h = len(P), len(S)
    vertices = k + h
    elements = list(owner_p)
    edge_ends = [(owner_p[x], k + owner_s[x]) for x in elements]
    artificial = vertices
    adj = [[] for _ in range(vertices + 1)]
    def add_edge(a, b):
        eid = len(edge_ends)
        edge_ends.append((a, b))
        adj[a].append(eid)
        adj[b].append(eid)
        return eid
    for eid, (a, b) in enumerate(edge_ends):
        adj[a].append(eid)
        adj[b].append(eid)
    for v in range(vertices):
        if len(adj[v]) % 2:
            add_edge(v, artificial)
    if len(adj[artificial]) % 2:
        raise AssertionError('handshaking parity was violated')
    used = [False] * len(edge_ends)
    orientation = [None] * len(edge_ends)
    for start in range(vertices + 1):
        if not adj[start]:
            continue
        stack = [start]
        path_edges = []
        output = []
        while stack:
            v = stack[-1]
            while adj[v] and used[adj[v][-1]]:
                adj[v].pop()
            if not adj[v]:
                stack.pop()
                if path_edges:
                    output.append(path_edges.pop())
            else:
                eid = adj[v].pop()
                if used[eid]:
                    continue
                used[eid] = True
                a, b = edge_ends[eid]
                w = b if a == v else a
                path_edges.append((eid, v, w))
                stack.append(w)
        for eid, a, b in reversed(output):
            if orientation[eid] is not None:
                raise AssertionError('edge used twice')
            orientation[eid] = (a, b)
    assert all(used) and all(v is not None for v in orientation)
    result = {}
    for eid, x in enumerate(elements):
        left, right = edge_ends[eid]
        result[x] = 0 if orientation[eid] == (left, right) else 1
    if not verify_balance(P, S, result):
        raise AssertionError('Euler orientation did not balance incident edges')
    return result


def verify_balance(P, S, colour):
    """Independent original-block count check, not a replay of Euler traversal."""
    try:
        P, S, owner_p, owner_s = partition_blocks(P, S)
    except (TypeError, ValueError):
        return False
    if set(colour) != set(owner_p) or any(v not in (0, 1) for v in colour.values()):
        return False
    for block in P + S:
        n0 = sum(colour[x] == 0 for x in block)
        n1 = sum(colour[x] == 1 for x in block)
        if abs(n0 - n1) > 1:
            return False
    return True


def component_avoiding_transversal(P, S):
    """Select one red element per P block; each S block retains blue witnesses."""
    P, S = list(P), list(S)
    if any(len(b) < 2 for b in P + S):
        raise ValueError('this corollary requires all blocks >=2')
    colouring = balanced_colouring(P, S)
    R = {next(x for x in block if colouring[x] == 0) for block in P}
    if len(R) != len(P) or any(set(b) <= R for b in S):
        raise AssertionError('invalid root transversal')
    return R
