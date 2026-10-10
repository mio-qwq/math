#!/usr/bin/env python3
"""Checks proof's *explicit construction* against every previously discovered
TF-cousin in five exhaustive 10/12-vertex restricted permutation models.
Discovery graph generation is reused but construction checker is separate.
This is a cross-check; not an exhaustive search over ALL graphs.
"""
from collections import Counter
from time import perf_counter
from tf_pair_probe import make_perm,edge_orbits,graph_from_mask,nxg
from check_mizzi_tf_cousin import decompose,odd_cycle_in_quotient,orbit_cycle_construction
import networkx as nx
import json
CLASSES=[(4,4,2),(4,2,2,2),(4,4,4),(4,4,2,2),(6,3,3)]

def run():
    cases=0;record=[];weights=Counter()
    for sizes in CLASSES:
        t0=perf_counter();T=make_perm(sizes);orbs,invalid=edge_orbits(T)
        n=len(T);total=1<<len(orbs);hits=0
        for mask in range(total):
            A,B=graph_from_mask(n,T,orbs,mask)
            G,H=nxg(A),nxg(B)
            if min(G.number_of_edges(),H.number_of_edges())<n:continue
            if not nx.is_connected(G) or not nx.is_connected(H):continue
            if nx.is_bipartite(G) or nx.is_bipartite(H):continue
            if len({tuple(row) for row in A})!=n or len({tuple(row) for row in B})!=n:continue
            if nx.is_isomorphic(G,H):continue
            odd=odd_cycle_in_quotient(A,decompose(T))
            assert odd,('lack of forced odd even-orbit cycle',sizes,mask)
            side,k,c1,c2,doubled,g,s=orbit_cycle_construction(A,B,decompose(T),odd)
            assert set(c1).isdisjoint(c2)
            assert len(set(doubled))==2*k
            hits+=1;weights[(sizes,side,k)]+=1
        cases+=hits;record.append({'T_cycle_type':sizes,'models':total,'cousins_checked':hits,'seconds':round(perf_counter()-t0,3)})
        print('DONE',record[-1],flush=True)
    print('ALL CONSTRUCTIVE CERTIFICATES PASS',cases,'tested pairs')
    print('side_k_stats',dict((str(k),v) for k,v in weights.items()))
    with open('/mnt/data/c_next_study/construction_replay_results.json','w') as f:json.dump({'records':record,'total':cases,'by_case':{str(k):v for k,v in weights.items()}},f,indent=2)
if __name__=='__main__':run()
