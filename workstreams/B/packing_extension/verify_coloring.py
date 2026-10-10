#!/usr/bin/env python3
"""Check an explicit graph/coloring directly against Conjecture 1's definitions.

Python standard library only. No tile templates, decomposition assumptions,
SAT solver, or discovery search is used in the validation logic.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import platform
import sys


def verify(data):
    rows = data['adjacency']
    colors = data['colors']
    if not isinstance(rows, list) or not isinstance(colors, list):
        raise ValueError('adjacency and colors must be lists')
    n = len(rows)
    if len(colors) != n:
        raise ValueError('one color per vertex is required')
    adj = []
    for v, row in enumerate(rows):
        if not isinstance(row, list) or any(type(w) is not int for w in row):
            raise ValueError('adjacency entries must be integer lists')
        if len(row) != len(set(row)) or any(w < 0 or w >= n or w == v for w in row):
            raise ValueError('graph must be finite and simple')
        adj.append(set(row))
    if any(v not in adj[w] for v in range(n) for w in adj[v]):
        raise ValueError('adjacency must be symmetric')
    if any(len(row) > 3 for row in adj):
        raise ValueError('maximum degree exceeds three')
    if any(type(c) is not int or not 1 <= c <= 4 for c in colors):
        raise ValueError('colors must be integers 1,2,3,4')
    branch = {v for v in range(n) if len(adj[v]) == 3}
    if any(adj[v] & branch for v in branch):
        raise ValueError('degree-three vertices are not independent')
    local_girth = {}
    for v in branch:
        # Shortest cycle through v = 2 + shortest path between distinct
        # neighbors in G-v. This reconstructs the local-girth hypothesis.
        best = n + 1
        for s in adj[v]:
            dist = {s: 0}
            q = deque([s])
            while q:
                x = q.popleft()
                for y in adj[x]:
                    if y != v and y not in dist:
                        dist[y] = dist[x] + 1
                        q.append(y)
            for t in adj[v] - {s}:
                if t in dist:
                    best = min(best, dist[t] + 2)
        if best > 4:
            raise ValueError(f'vertex {v} has no cycle of length at most four')
        local_girth[v] = best
    checked_pairs = 0
    components = 0
    seen = set()
    for s in range(n):
        dist = {s: 0}
        q = deque([s])
        while q:
            x = q.popleft()
            for y in adj[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    q.append(y)
        if s not in seen:
            components += 1
            seen.update(dist)
        for t, distance in dist.items():
            if s < t and colors[s] == colors[t]:
                checked_pairs += 1
                if distance <= colors[s]:
                    raise ValueError(f'color {colors[s]} repeated at distance {distance}: {s},{t}')
    return {'vertices': n, 'edges': sum(map(len, adj)) // 2,
            'components': components, 'degree_three_vertices': len(branch),
            'max_degree_three_local_girth': max(local_girth.values(), default=None),
            'same_color_connected_pairs_checked': checked_pairs,
            'hypotheses': 'PASS', 'packing_coloring': 'PASS'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('certificate')
    args = p.parse_args()
    path = Path(args.certificate)
    raw = path.read_bytes()
    answer = verify(json.loads(raw))
    answer.update(certificate_sha256=hashlib.sha256(raw).hexdigest(),
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  python=sys.version, platform=platform.platform())
    print(json.dumps(answer, indent=2))


if __name__ == '__main__':
    main()
