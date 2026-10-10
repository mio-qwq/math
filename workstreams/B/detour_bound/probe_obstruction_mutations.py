"""Targeted third mechanism: repair one missing vertex in a longest-path obstruction.
The input has a detour-irredundant triple on a global longest path but saturates,
rather than violates, the numerical bound. Edge additions/vertex deletions may
close this gap; every resulting claim is recomputed from original simple paths.
"""
from probe_general import inspect
from itertools import combinations
from pathlib import Path
import json,time
P=Path(__file__).parent
source=json.loads((P/'strong_lemma_obstruction.json').read_text());n=source['order'];E={tuple(e) for e in source['edges']};S=set(source['selected']);start=time.monotonic();counts={}
variants=[]
for e in combinations(range(n),2):
 if e not in E:variants.append(('add_edge',n,sorted(E|{e})))
for v in range(n):
 if v in S:continue
 vertices=[u for u in range(n) if u!=v];mapping={u:i for i,u in enumerate(vertices)}
 edges=[(mapping[u],mapping[w]) for u,w in E if v not in (u,w)]
 seen={0}
 while True:
  expanded=seen|{w for u,w in edges if u in seen}|{u for u,w in edges if w in seen}
  if expanded==seen:break
  seen=expanded
 if len(seen)==n-1:variants.append(('delete_vertex',n-1,edges))
for mode,k,edges in variants:
 witness,strong,data=inspect(k,edges);counts[mode]=counts.get(mode,0)+1
 if witness:
  data['selected']=witness;data['origin_mutation']=mode
  (P/'candidate_mutation.json').write_text(json.dumps(data,indent=2)+'\n')
  print(json.dumps(dict(status='CANDIDATE',mode=mode,order=k,selected=witness,diameter=data['detour_diameter'],counts=counts,seconds=time.monotonic()-start)));break
else:print(json.dumps(dict(status='NO_CANDIDATE_IN_WINDOW',counts=counts,seconds=time.monotonic()-start)))
