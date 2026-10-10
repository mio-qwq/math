"""Second diagnostic: metric distortion by unequal edge subdivisions.
Uses exact terminal search from first discovery, not claimed independent checking.
"""
from probe_cubic import distances,search
from pathlib import Path
from itertools import combinations
from collections import Counter
import random,json,time
P=Path(__file__).parent;rng=random.Random(202610101056);records=[];stats=Counter();start=time.monotonic()
cores=[(4,list(combinations(range(4),2))),(5,list(combinations(range(5),2))),(6,list(combinations(range(6),2)))]
for core_n,core_e in cores:
 for trial in range(30):
  n=core_n;edges=[];lengths=[]
  for u,v in core_e:
   length=rng.choice((1,2,3,4));lengths.append(length);path=[u]
   for _ in range(length-1):path.append(n);n+=1
   path.append(v);edges.extend(zip(path,path[1:]))
  adj,D=distances(n,edges)
  if max(map(max,D))<4 or all((D[0][u]-D[0][v])%2 for u,v in edges):continue
  status,S,nodes=search(D,cap=300000)
  record=dict(core_order=core_n,subdivision_lengths=lengths,order=n,edges=edges,diameter=max(map(max,D)),status=status,selected=S,nodes=nodes)
  records.append(record);stats[status]+=1
  if status=='NO_TERMINAL_SET':(P/'candidate_subdivision.json').write_text(json.dumps(record,indent=2)+'\n');break
  if time.monotonic()-start>60:break
 print(json.dumps(dict(core_order=core_n,stats=dict(stats),max_nodes=max((r['nodes'] for r in records),default=0),seconds=time.monotonic()-start)),flush=True)
 if stats['NO_TERMINAL_SET'] or time.monotonic()-start>60:break
(P/'subdivision_probe.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(dict(status='DIAGNOSTIC_COMPLETE',graphs=len(records),stats=dict(stats),seconds=time.monotonic()-start)))
