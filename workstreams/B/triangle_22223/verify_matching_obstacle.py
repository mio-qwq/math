"""Separate fixed-object replay, not importing the restricted discovery solver."""
from itertools import combinations
from collections import deque
import json
E=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)];L=[2,2,2,2,2,3];A=[set() for _ in range(12)];ports=[0]*4
edges=[]
for i in range(4):edges+=list(combinations(range(3*i,3*i+3),2))
for (u,v),length in zip(E,L):
 x=3*u+ports[u];ports[u]+=1;y=3*v+ports[v];ports[v]+=1
 for _ in range(length-1):z=len(A);A.append(set());edges.append((x,z));x=z
 edges.append((x,y))
for u,v in edges:A[u].add(v);A[v].add(u)
c=[0,1,2,1,0,2,0,1,2,0,1,2,3,3,3,3,3,3,4]
assert len(A)==len(c)==19
D=[]
for s in range(19):
 d=[-1]*19;d[s]=0;q=deque([s])
 while q:
  u=q.popleft()
  for v in A[u]:
   if d[v]<0:d[v]=d[u]+1;q.append(v)
 D.append(d)
for u in range(19):
 assert len(A[u])<=3
 if len(A[u])==3:assert sum(len(A[v])==3 for v in A[u])<=2 and any(A[v]&A[u] for v in A[u])
for u,v in combinations(range(19),2):assert c[u]!=c[v] or D[u][v]>[2,2,2,2,3][c[u]]
matchings=0
for mask in range(1<<5):
 selected=[E[i] for i in range(5) if mask>>i&1]
 if len(set(sum((list(e) for e in selected),[])))!=2*len(selected):continue
 matchings+=1;seen={0}
 for _ in range(4):
  for i,(u,v) in enumerate(E[:5]):
   if not mask>>i&1 and (u in seen or v in seen):seen.update([u,v])
 assert len(seen)==4
# Damaging the original coloring removes the valid fifth color and fails.
bad=c[:];bad[-1]=3;assert any(bad[u]==bad[v] and D[u][v]<=[2,2,2,2,3][bad[u]] for u,v in combinations(range(19),2))
print(json.dumps({'status':'PASS','vertices':19,'edges':len(edges),'matchings_checked':matchings,'original_palette':'SAT','restricted_placement':'structurally impossible','negative_controls':1}))
