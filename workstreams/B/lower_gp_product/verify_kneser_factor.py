"""Exact Petersen boundary check for the cited factor formula; no discovery imports."""
from itertools import combinations
from collections import deque
import json
V=list(combinations(range(5),2));N=len(V);adj=[set() for _ in V]
for u,v in combinations(range(N),2):
 if set(V[u]).isdisjoint(V[v]):adj[u].add(v);adj[v].add(u)
D=[]
for r in range(N):
 ds=[-1]*N;ds[r]=0;q=deque([r])
 while q:
  u=q.popleft()
  for v in adj[u]:
   if ds[v]<0:ds[v]=ds[u]+1;q.append(v)
 D.append(ds)
def gp(S):
 return all(D[a][b]+D[b][c]!=D[a][c] and D[a][c]+D[c][b]!=D[a][b] and D[b][a]+D[a][c]!=D[b][c] for a,b,c in combinations(S,3))
counts={};witness=None
for k in range(1,5):
 count=0
 for S in combinations(range(N),k):
  if gp(S) and not any(u not in S and gp(S+(u,)) for u in range(N)):
   count+=1;witness=witness or [V[v] for v in S]
 counts[k]=count
assert counts=={1:0,2:0,3:0,4:5}
assert not gp((0,1,9)) # 01,02,34: 34 is the middle of a shortest two-edge path
print(json.dumps(dict(status='PASS',order=N,lower_gp=4,maximal_set_counts=counts,witness=witness,negative_controls=1,scope='known Petersen factor value checked, not a new result')))
