from collections import deque
from itertools import combinations,permutations
import json,platform,sys,hashlib,time
from pathlib import Path
R=Path(__file__).parent
counts={'graphs':0,'anchored_triples':0,'gp_triples':0,'ceiling_comparisons':0}
for n in range(5,91):
 for d in range(3,n):
  a=n%d
  if not 2<=a<=d-1:continue
  counts['graphs']+=1
  # Direct BFS gives all source distances by vertex-transitivity.
  dist=[-1]*n;dist[0]=0;Q=deque([0])
  while Q:
   v=Q.popleft()
   for step in range(1,d+1):
    w=(v+step)%n
    if dist[w]<0:dist[w]=dist[v]+1;Q.append(w)
  assert all(dist[x]==(x+d-1)//d for x in range(n))
  counts['ceiling_comparisons']+=n
  for x,y in combinations(range(1,n),2):
   counts['anchored_triples']+=1
   if any(dist[(w-u)%n]==dist[(v-u)%n]+dist[(w-v)%n] for u,v,w in permutations([0,x,y])):continue
   counts['gp_triples']+=1
   r=x%d or d;s=y%d or d
   assert 0<r<s<=d,(n,d,x,y,r,s,'order')
   assert s<a or (r>=a and s-r>=a),(n,d,x,y,r,s,'spacing')
result={'counts':counts,'result':'all assertions passed','python':sys.version,'platform':platform.platform(),'source_url':'https://arxiv.org/html/2604.15909v1#S3.SS1','note':'Independent direct BFS validates necessary residue inequalities on all anchored triples, n<=90. This is a computational check, not the general proof.'}
(R/'lemma_validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
