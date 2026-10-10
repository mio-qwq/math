#!/usr/bin/env python3
"""Full 10-vertex Petersen-family baseline for future CG(n) enumeration.
Enumerates all CDC automorphisms at n=1 and all strongly switching guides,
then performs the actual graph folding and classifies nonisomorphic results.
A completed enumeration for n=1 is NOT a result for n>=3.
"""
import networkx as nx
from claw_graph_gate import claw,cdc
from collections import Counter


def folding_graph(K,p):
    assert all(p[p[u]]==u and p[u]!=u and (u%2)!=(p[u]%2)
               and not K.has_edge(u,p[u]) for u in K.nodes())
    orbits={};pairs=[]
    for u in range(len(K)):
        if u in orbits:continue
        v=p[u]; z=len(pairs);pairs.append((u,v));orbits[u]=orbits[v]=z
    H=nx.Graph();H.add_nodes_from(range(len(pairs)))
    for u,v in K.edges():
        a,b=orbits[u],orbits[v]
        assert a!=b
        H.add_edge(a,b)
    return H

def main():
    G=claw(1);G2=claw(1,True);K=cdc(G)
    fold_graphs=[];guidecount=0;class_counts=Counter();aut_total=0
    for p in nx.algorithms.isomorphism.GraphMatcher(K,K).isomorphisms_iter():
        aut_total+=1
        if not all(p[2*i]%2==1 and p[2*i+1]%2==0 for i in range(len(K)//2)):continue
        if not all(p[p[u]]==u and not K.has_edge(u,p[u]) for u in K.nodes()):continue
        guidecount+=1
        H=folding_graph(K,p)
        assert H.number_of_nodes()==10 and H.number_of_edges()==15
        assert nx.is_connected(H)
        key=next((i for i,C in enumerate(fold_graphs) if nx.is_isomorphic(H,C)),None)
        if key is None:key=len(fold_graphs);fold_graphs.append(H)
        class_counts[key]+=1
    print('total CDC automorphisms',aut_total)
    print('switching strong guides',guidecount)
    print('nonisomorphic fold graph classes including original',len(fold_graphs))
    print('fold class guide multiplicities',dict(class_counts))
    print('class original CG1 index',next(i for i,H in enumerate(fold_graphs) if nx.is_isomorphic(H,G)))
    print('class companion CG1 prime index',next(i for i,H in enumerate(fold_graphs) if nx.is_isomorphic(H,G2)))
    assert aut_total==240 and guidecount==11 and len(fold_graphs)==2
    print('PASS: known CG(1) exactly ONE nonisomorphic TF cousin confirmed')
if __name__=='__main__':main()
