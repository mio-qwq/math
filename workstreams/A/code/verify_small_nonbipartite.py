#!/usr/bin/env python3
"""Exact small NONBIPARTITE cubic search; exhaustive but only two graphs."""
from itertools import combinations, permutations, product

def proper(n,edges,cs):
    incident=[set() for _ in range(n)]
    for (u,v),c in zip(edges,cs):
        if c in incident[u] or c in incident[v]:return False
        incident[u].add(c);incident[v].add(c)
    return True

def witness(n,edges,cs):
    incident=[[] for _ in range(n)]
    for e,(u,v) in enumerate(edges):incident[u].append(e);incident[v].append(e)
    for order in permutations(range(len(edges))):
        pos={e:i for i,e in enumerate(order)}
        seq=[tuple(cs[e] for e in sorted(incident[v],key=pos.get)) for v in range(n)]
        if all(seq[u]!=seq[v] for u,v in edges):return order
    return None

def main():
    tests=[
        ('K4',4,list(combinations(range(4),2))),
        ('triangular-prism',6,[(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)]),
    ]
    for name,n,edges in tests:
        valid=0;fail=0;first=None
        for cs in product(range(3),repeat=len(edges)):
            if not proper(n,edges,cs):continue
            valid+=1
            order=witness(n,edges,cs)
            if order is None:fail+=1
            elif first is None:first=(cs,order)
        print(name,'proper-colorings=',valid,'no-good-global-order=',fail,'first=',first)
        assert valid==6 and fail==0
if __name__=='__main__':main()
