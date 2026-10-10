#!/usr/bin/env python3
"""Exhaustive finite model verification for selected TF-cousin permutation classes.
This enumerates every union of admissible pair-orbits for each explicit T, not
all 10- or 12-vertex graphs. No universal nonexistence claim is intended.
"""
from itertools import combinations
from time import perf_counter
from tf_pair_probe import make_perm,edge_orbits,graph_from_mask,nxg,property_holds
import networkx as nx
import json,sys

CLASSES=[(4,4,2),(4,2,2,2),(4,4,4),(4,4,2,2),(6,3,3)]

def run(parts):
    T=make_perm(parts);n=len(T);orbs,invalid=edge_orbits(T); r=len(orbs)
    assert r<=14, 'keep initial census bounded'
    count={'total_labelled_edge_models':1<<r,'connected_both':0,'nonbipartite_both':0,
      'vertex_determining_both':0,'nonisomorphic_TF_cousins':0,'conjecture_satisfied':0,'potential_exception':0}
    t=perf_counter()
    for mask in range(1<<r):
        A,B=graph_from_mask(n,T,orbs,mask)
        G,H=nxg(A),nxg(B)
        if min(G.number_of_edges(),H.number_of_edges())<n:continue
        if not nx.is_connected(G) or not nx.is_connected(H):continue
        count['connected_both']+=1
        if nx.is_bipartite(G) or nx.is_bipartite(H):continue
        count['nonbipartite_both']+=1
        if len({tuple(row) for row in A})<n or len({tuple(row) for row in B})<n:continue
        count['vertex_determining_both']+=1
        if nx.is_isomorphic(G,H):continue
        count['nonisomorphic_TF_cousins']+=1
        valid,k,which=property_holds(A,B)
        if valid:count['conjecture_satisfied']+=1
        else:
            count['potential_exception']+=1
            with open('/mnt/data/c_next_study/exact_candidate.json','w') as f:
                json.dump({'class':parts,'mask':mask,'T':T,'G':list(G.edges()),'H':list(H.edges())},f,indent=2)
            raise RuntimeError('A possible violation requires independent check')
    count['time_s']=round(perf_counter()-t,3)
    count['parts']=parts;count['edge_orbits']=r;count['invalid_edge_orbits']=invalid
    return count

def main():
    all_results=[]
    for parts in CLASSES:
        output=run(parts)
        print(json.dumps(output,sort_keys=True),flush=True)
        all_results.append(output)
    assert all(x['potential_exception']==0 for x in all_results)
    with open('/mnt/data/c_next_study/exhaustive_results.json','w') as f:json.dump(all_results,f,indent=2)
    print('ALL EXACT MODEL FAMILIES PASSED; no global open-problem resolution')
if __name__=='__main__':main()
