"""Independent original-distance check of a restricted route obstruction."""
from collections import deque
from itertools import product
import json
core=[(u,v) for u in range(3) for v in range(3,6)]
a=[set() for _ in range(18)];used=[0]*6
for u in range(6):
 for i,j in [(0,1),(0,2),(1,2)]:a[3*u+i].add(3*u+j);a[3*u+j].add(3*u+i)
for u,v in core:
 x=3*u+used[u];used[u]+=1;y=3*v+used[v];used[v]+=1;a[x].add(y);a[y].add(x)
D=[]
for r in range(18):
 d=[99]*18;d[r]=0;q=deque([r])
 while q:
  u=q.popleft()
  for v in a[u]:
   if d[v]==99:d[v]=d[u]+1;q.append(v)
 D.append(d)
count=0
for ports in product(range(3),repeat=3):
 chosen=[3*u+ports[u] for u in range(3)];count+=1
 assert any(D[u][v]<=4 for i,u in enumerate(chosen) for v in chosen[i+1:])
# Contrast control: the same fixed core class DOES admit a 3-packing.
chosen=[0,4,8]
assert all(D[u][v]>3 for i,u in enumerate(chosen) for v in chosen[i+1:])
assert not all(D[u][v]>4 for i,u in enumerate(chosen) for v in chosen[i+1:])
print(json.dumps({'fixed_core_class':'one side of K3,3','transversals_checked':count,'valid_4pack_transversals':0,'scope':'route obstacle only, not original UNSAT'}))
