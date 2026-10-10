#!/usr/bin/env python3
"""Exhaustive independent original-definition check of a component-avoiding transversal.
The solver/lemma proof is in verify_general_all_regular.py; brute enumerator is separate.
"""
from itertools import combinations,product
from verify_all_regular import choose_nonsaturated_roots


def components(V,E):
    adj={v:set() for v in V}
    for u,v in E:adj[u].add(v);adj[v].add(u)
    seen=set();out=[]
    for v in V:
        if v in seen:continue
        S={v};seen.add(v);work=[v]
        while work:
            u=work.pop()
            for q in adj[u]:
                if q not in seen:S.add(q);seen.add(q);work.append(q)
        out.append(S)
    return out


def main():
    V=set(range(6));edges=list(combinations(range(6),2))
    partitions=[[[0,1],[2,3],[4,5]],[[0,1,2],[3,4,5]],[[0,1],[2,3,4,5]]]
    total=0; roots_checked=0
    for mask in range(1<<len(edges)):
        E=[e for i,e in enumerate(edges) if mask>>i&1]
        deg={v:0 for v in V}
        for u,v in E:deg[u]+=1;deg[v]+=1
        if not all(deg.values()):continue
        Q=[(u,v,2) for u,v in E]
        comps=components(V,E)
        for parts in partitions:
            root,_,_=choose_nonsaturated_roots(parts,Q,V)
            assert len(root)==len(parts)
            assert all(not S<=set(root) for S in comps)
            assert any(all(not S<=set(r) for S in comps) for r in product(*parts))
            roots_checked+=1
        total+=1
    empty_comps=components(V,[])
    assert not any(all(not S<=set(r) for S in empty_comps) for r in product(*partitions[0]))
    print(f'PASS all six-vertex graphs with min degree>=1: {total} graphs; {roots_checked} partitioned cases; empty-Q negative test')
if __name__=='__main__':main()
