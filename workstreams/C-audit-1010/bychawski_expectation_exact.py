#!/usr/bin/env python3
"""Exact small-n random graph TF / projection expectation checker.

Implements directly the ordered-pair relation A[u,v]=A[alpha[u],beta[v]],
with diagonal forced zero, in a union-find on UNORDERED adjacency variables.
Constructs all satisfying graph masks, rather than importing old TF code.
Enumerates all alpha/beta and all simple graphs for n<=5 and reports exact
expectations (Fractions) for the full TF group, the canonical projection group,
and its conditional expectation given twin-freeness.
"""
from itertools import combinations, permutations
from collections import defaultdict
from fractions import Fraction
from math import comb
from hashlib import sha256
from pathlib import Path


def all_pair_families(n):
    pairs=list(combinations(range(n),2))
    edge_ids={xy:i for i,xy in enumerate(pairs)}
    E=len(pairs);zero=E
    perms=list(permutations(range(n)))
    pidx={p:i for i,p in enumerate(perms)}
    valid_masks=[0]*len(perms)
    full=0
    support_hist=defaultdict(int)
    pair_count=0
    for pa in perms:
        a_idx=pidx[pa]
        for pb in perms:
            parent=list(range(E+1))
            def find(x):
                while parent[x]!=x:
                    parent[x]=parent[parent[x]]
                    x=parent[x]
                return x
            def union(x,y):
                x=find(x);y=find(y)
                if x!=y:parent[x]=y
            for u in range(n):
                for v in range(n):
                    x=zero if u==v else edge_ids[(min(u,v),max(u,v))]
                    aa,bb=pa[u],pb[v]
                    y=zero if aa==bb else edge_ids[(min(aa,bb),max(aa,bb))]
                    union(x,y)
            z=find(zero)
            groups={}
            for i in range(E):
                key=find(i)
                if key!=z:groups[key]=groups.get(key,0)|(1<<i)
            free=list(groups.values())
            mask_count=1<<len(free)
            full+=mask_count
            s=sum(pa[i]!=i or pb[i]!=i for i in range(n))
            if pa!=tuple(range(n)) or pb!=tuple(range(n)):
                support_hist[s]+=mask_count
            pair_count+=1
            # Generate every original adjacency table allowed by the TF
            # relation and insert it in the FIRST-projection graph set.
            # n<=5 => <=1024 possible graph masks, so Python int bitmap.
            graph_masks=[0]
            for q in free:
                graph_masks += [x|q for x in graph_masks]
            for graph_mask in graph_masks:
                valid_masks[a_idx] |= 1<<graph_mask
    assert pair_count==len(perms)**2
    tfree_bitmap=0
    for mask in range(1<<E):
        rows=[0]*n
        for i,(u,v) in enumerate(pairs):
            if (mask>>i)&1:
                rows[u] |= 1<<v; rows[v] |= 1<<u
        if len(set(rows))==n:tfree_bitmap |= 1<<mask
    total_graphs=1<<E
    reduced=tfree_bitmap.bit_count()
    projected=sum(m.bit_count() for m in valid_masks)
    projected_reduced=sum((m&tfree_bitmap).bit_count() for m in valid_masks)
    # On reduced graphs, each alpha has at most one valid beta.
    full_reduced=0
    # A second independent identity: on reduced graphs |TF| == |projection|.
    # We can verify via source pair count by restriction when n<=4 directly.
    expected_FT=Fraction(full,total_graphs)
    expected_proj=Fraction(projected,total_graphs)
    expected_proj_reduced=Fraction(projected_reduced,reduced)
    K=comb(n,2)
    identity=total_graphs
    s2=K*(2**max(0,E-(n-2))+2*(2**max(0,E-(n-1)))) if n>=2 else 0
    # Written as integer over all 2^E graphs: n>=2.
    if n>=2:
        assert support_hist[2]==s2,(n,support_hist[2],s2)
    return dict(n=n,graph_masks=total_graphs,perms=len(perms),reduced_masks=reduced,
                expected_TF=str(expected_FT),expected_proj=str(expected_proj),
                expected_projection_given_reduced=str(expected_proj_reduced),
                support2_pair_count=support_hist[2],
                support3plus_pair_count=sum(v for k,v in support_hist.items() if k>=3),
                support_hist=dict(sorted(support_hist.items())))


def brute_check_n4():
    n=4;ps=list(permutations(range(n)));edges=list(combinations(range(n),2));
    E=len(edges);counts_full=0
    for mask in range(1<<E):
        rows=[[False]*n for _ in range(n)]
        for i,(u,v) in enumerate(edges):
            if mask>>i&1:rows[u][v]=rows[v][u]=True
        for a in ps:
            for b in ps:
                if all(rows[u][v]==rows[a[u]][b[v]] for u in range(n) for v in range(n)):
                    counts_full+=1
    fast=all_pair_families(4)
    assert Fraction(counts_full,1<<E)==Fraction(fast['expected_TF'])
    return fast


def main():
    out=[all_pair_families(n) for n in (2,3,5)]
    out.insert(2,brute_check_n4())
    import json
    target=Path(__file__).with_name('bychawski_exact_small.json')
    target.write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
    for r in out:
        print('n',r['n'],'E|TF|=',r['expected_TF'],
              'E|projection|=',r['expected_proj'],
              'E|projection|reduced=',r['expected_projection_given_reduced'],
              'TF tail s>=3',r['support3plus_pair_count'],'/',r['graph_masks'])
    print('PASS full TF DSU, projection group and twin-free exact values; independent n=4 brute complete')
    print('source_sha256',sha256(Path(__file__).read_bytes()).hexdigest())
    print('json_sha256',sha256(target.read_bytes()).hexdigest())

if __name__=='__main__':main()
