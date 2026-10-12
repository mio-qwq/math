#!/usr/bin/env python3
"""Optional SciPy generation of the fixed six-letter exact hypergraph certificate.

The verifier uses the Python standard library only, with no optimizer.
"""
from itertools import product,combinations
from collections import Counter
from pathlib import Path
import json
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_array
from model import candidate_orbits

HERE=Path(__file__).resolve().parent
L=[1,2,0,1,2,0, 0,1,2,1,1,0, 2,0,1,2,2,1,
   1,2,1,1,0,0, 1,0,2,1,0,0, 1,0,2,2,2,2]
N=6

def main():
    orbs=candidate_orbits(N,L)
    forced=sorted(o[0] for o in orbs if len(o)==1)
    index={w:i for i,w in enumerate(forced)}
    triple_to_witness={}
    for x in product(range(N),repeat=8):
        ids=[index.get(x[i:i+4]) for i in range(5)]
        for s in combinations(range(5),3):
            if all(ids[i] is not None for i in s):
                key=tuple(sorted(set(ids[i] for i in s)))
                if key not in triple_to_witness:
                    triple_to_witness[key]={'word8':list(x),'starts':list(s)}
    edges=sorted(triple_to_witness)
    cols=[];rows=[]
    for j,e in enumerate(edges):
        for i in e:rows.append(i);cols.append(j)
    A=coo_array((np.ones(len(rows)),(np.array(rows,dtype=np.int32),np.array(cols,dtype=np.int32))),shape=(len(forced),len(edges))).tocsr()
    r=milp(-np.ones(len(edges)), integrality=np.ones(len(edges),dtype=np.int32),bounds=Bounds(0,1),constraints=LinearConstraint(A,0,1),options={'mip_rel_gap':0.0,'time_limit':60})
    assert r.status==0
    match=[edges[j] for j,v in enumerate(r.x) if v>.5]
    print('matching',len(match))
    assert len(match)==64
    rows2=[];cols2=[]
    for i,e in enumerate(edges):
        for j in e:rows2.append(i);cols2.append(j)
    A2=coo_array((np.ones(len(rows2)),(np.array(rows2,dtype=np.int32),np.array(cols2,dtype=np.int32))),shape=(len(edges),len(forced))).tocsr()
    s=milp(np.ones(len(forced)),integrality=np.ones(len(forced),dtype=np.int32),bounds=Bounds(0,1),constraints=LinearConstraint(A2,1,np.inf),options={'mip_rel_gap':0.0,'time_limit':60})
    assert s.status==0
    cover=[forced[i] for i,v in enumerate(s.x) if v>.5]
    print('cover',len(cover))
    assert len(cover)==64
    data={'schema':'GP2-forced-cover-v1','n':N,'levels':L,
          'viable_orbits':len(orbs),'forced_words':len(forced),
          'hyperedge_count':len(edges), 'cover':[list(w) for w in sorted(cover)],
          'disjoint_matching':[
              {'forbidden_words':[list(forced[i]) for i in edge], **triple_to_witness[edge]}
              for edge in sorted(match)],
          'rank_histogram':dict(sorted(Counter(map(len,edges)).items()))}
    (HERE/'forced_cover_certificate.json').write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print('written',HERE/'forced_cover_certificate.json')

if __name__=='__main__':main()
