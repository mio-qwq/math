"""Probe long cyclic phase compatibility, a distinct restricted mechanism."""
from explore import *
import random
r=random.Random(20261010);counts=Counter();out=[];start=time.monotonic()
for m in [7,9,11,13,15,17,19,21]:
 for j in range(32):
  gaps=tuple(2 if j==0 else 3 if j==1 else r.choice([2,3]) for _ in range(m));g=graph(gaps,'cycle')
  for seq in [(1,2,3,3),(1,2,2,4),(2,2,2,2,4),(1,2,3,4,5)]:
   status,c,nodes=solve(g.a,seq,limit=1);counts[str(seq)+':'+status]+=1
   if status!='SAT':out.append({'gaps':gaps,'sequence':seq,'state':status,'nodes':nodes})
print(json.dumps({'elapsed':time.monotonic()-start,'seed':20261010,'counts':dict(counts),'exceptions':out},indent=2))
