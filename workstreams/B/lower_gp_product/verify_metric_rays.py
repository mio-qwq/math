"""Exact double-description of MET5 from defining inequalities, no ray table input."""
from itertools import combinations
from math import gcd
from functools import reduce
import json,time
from pathlib import Path

def extreme_metric_rays(n=5,trace=False):
 edges=list(combinations(range(n),2));ix={e:i for i,e in enumerate(edges)};dimension=len(edges)
 constraints=[]
 for a,b,c in combinations(range(n),3):
  for u,v,w in ((a,b,c),(a,c,b),(b,a,c)):
   row=[0]*dimension
   row[ix[tuple(sorted((u,v)))]]+=1;row[ix[tuple(sorted((v,w)))]]+=1;row[ix[tuple(sorted((u,w)))]]-=1;constraints.append(tuple(row))
 # Begin with positive orthant, all coordinate inequalities already present.
 full=(1<<dimension)-1
 rays=[(tuple(int(i==j) for i in range(dimension)),full^(1<<j)) for j in range(dimension)]
 counts=[]
 for step,row in enumerate(constraints):
  val=[sum(a*b for a,b in zip(r,row)) for r,z in rays]
  pos=[i for i,x in enumerate(val) if x>0];neg=[i for i,x in enumerate(val) if x<0];zero=[i for i,x in enumerate(val) if x==0]
  bit=1<<(dimension+step);new={r:z|(bit if val[i]==0 else 0) for i,(r,z) in enumerate(rays) if val[i]>=0}
  for i in pos:
   for j in neg:
    common=rays[i][1]&rays[j][1]
    # Adjacent iff their common face contains no third old extreme ray.
    if any(k not in (i,j) and z&common==common for k,(r,z) in enumerate(rays)):continue
    v=tuple(val[i]*b-val[j]*a for a,b in zip(rays[i][0],rays[j][0]));g=reduce(gcd,v);v=tuple(x//g for x in v)
    assert all(x>=0 for x in v) and any(v)
    zeros=sum(1<<a for a,x in enumerate(v) if x==0)
    for a,old in enumerate(constraints[:step+1]):
     s=sum(x*y for x,y in zip(v,old));assert s>=0
     if not s:zeros|=1<<(dimension+a)
    new[v]=zeros
  rays=sorted(new.items());counts.append(len(rays))
  if trace:print(json.dumps(dict(step=step+1,rays=len(rays))),flush=True)
 result=sorted(r for r,z in rays)
 assert len(result)==25
 return edges,constraints,result,counts
if __name__=='__main__':
 start=time.monotonic();edges,constraints,rays,counts=extreme_metric_rays(trace=True)
 # Corrupt candidate violates an ORIGINAL triangle inequality.
 bad=[1]*len(edges);bad[0]=3
 assert any(sum(x*y for x,y in zip(bad,row))<0 for row in constraints)
 result=dict(status='PASS',edges=edges,constraints=constraints,rays=rays,stage_ray_counts=counts,negative_controls=1,seconds=time.monotonic()-start)
 Path(__file__).with_name('metric_rays_verified.json').write_text(json.dumps(result,separators=(',',':'))+'\n')
 print(json.dumps(dict(status='PASS',extreme_rays=len(rays),stage_ray_counts=counts,seconds=time.monotonic()-start)),flush=True)
