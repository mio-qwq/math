#!/usr/bin/env python3
"""Exact rank-sum-edge-order regression for graphs with a universal vertex; stdlib."""
from itertools import combinations

def greedy_colouring(edges,unique=False):
    used={v:set() for e in edges for v in e}
    output=[]
    for i,(u,v) in enumerate(edges):
        c=i if unique else next(x for x in range(len(edges)+1) if x not in used[u] and x not in used[v])
        output.append((u,v,c))
        used[u].add(c)
        used[v].add(c)
    return output

def rank_sum_order(coloured):
    return sorted(coloured,key=lambda e:(e[0]+e[1],e[0],e[1]))

def independently_verify(n,coloured,ordered):
    if len(coloured)!=len(ordered) or set(coloured)!=set(ordered):return False
    seq={v:[] for v in range(n)}
    for u,v,c in ordered:
        seq[u].append(c)
        seq[v].append(c)
    return len({tuple(x) for x in seq.values()})==n

def run():
    count=0
    for n in range(3,8):
        candidates=list(combinations(range(1,n),2))
        root=[(0,j) for j in range(1,n)]
        for mask in range(1<<len(candidates)):
            edges=root+[e for i,e in enumerate(candidates) if mask>>i&1]
            for unique in (False,True):
                coloured=greedy_colouring(edges,unique)
                assert independently_verify(n,coloured,rank_sum_order(coloured)),(n,mask,unique)
                count+=1
    sample=greedy_colouring([(0,1),(0,2),(0,3),(1,2),(2,3),(1,3)])
    assert not independently_verify(4,sample,rank_sum_order(sample)[:-1])
    assert count==67732
    print('PASS 67732 labelled universal-root graphs/proper-colouring samples through n=7, missing-edge negative control')

if __name__=='__main__':run()
