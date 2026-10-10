"""Independent semantics only: no block decomposition or construction imports."""
from collections import deque

def verify(adj,colors):
 n=len(adj);assert len(colors)==n and all(c in (0,1,2) for c in colors)
 for u,ns in enumerate(adj):
  assert u not in ns and len(ns)<=3
  assert all(0<=v<n and u in adj[v] for v in ns)
  if len(ns)==3:assert any(w in adj[v] for v in ns for w in ns if w!=v)
 heavy=[len(ns)==3 and all(len(adj[v])==3 for v in ns) for ns in adj]
 assert all(not(heavy[u] and heavy[v]) for u,ns in enumerate(adj) for v in ns)
 pairs=0
 for r in range(n):
  d=[None]*n;d[r]=0;q=deque([r])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if d[v] is None:d[v]=d[u]+1;q.append(v)
  for v in range(r):
   pairs+=1
   assert colors[r]!=colors[v] or d[v] is None or d[v]>(1,1,2)[colors[r]]
 return pairs
