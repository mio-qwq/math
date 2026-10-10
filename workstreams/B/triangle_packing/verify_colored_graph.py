"""Direct full-graph checker, separate from finite-state construction."""
from collections import deque

def verify_original(cert):
 rows=cert['adjacency'];a=[set(row) for row in rows];cols=cert['colors'];seq=cert['sequence'];n=len(a)
 assert seq in ([1,2,3,3],[1,2,2,4],[1,2,3,4,5])
 assert len(cols)==n and all(type(c) is int and 0<=c<len(seq) for c in cols)
 for u,ns in enumerate(a):
  assert len(ns)==len(rows[u]) and u not in ns and len(ns)<=3
  assert all(type(v) is int and 0<=v<n and u in a[v] for v in ns)
  if len(ns)==3:
   assert sum(len(a[v])==3 for v in ns)<=1
   assert any(v!=w and w in a[v] for v in ns for w in ns)
  d=[-1]*n;d[u]=0;q=deque([u])
  while q:
   v=q.popleft()
   for w in a[v]:
    if d[w]<0:d[w]=d[v]+1;q.append(w)
  for v in range(u):
   if cols[u]==cols[v] and d[v]>=0:assert d[v]>seq[cols[u]]
 return True
