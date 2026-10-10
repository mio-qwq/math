"""Discovery: can fifth color be confined to length2 connector interiors?
Restricted UNSAT is not original UNSAT. Never reinterpret a timeout.
"""
from itertools import combinations,product
from collections import deque,Counter
from pathlib import Path
import json,time

def graph(n,E,L):
 A=[set() for _ in range(3*n)];ports=[0]*n;allowed=[]
 def edge(u,v):A[u].add(v);A[v].add(u)
 for i in range(n):
  for u,v in combinations(range(3*i,3*i+3),2):edge(u,v)
 for (u,v),l in zip(E,L):
  x=3*u+ports[u];ports[u]+=1;y=3*v+ports[v];ports[v]+=1
  for _ in range(l-1):
   z=len(A);A.append(set());edge(x,z);x=z
   if l==2:allowed.append(z)
  edge(x,y)
 assert all(len(ns)<=3 and (len(ns)!=3 or sum(len(A[v])==3 for v in ns)<=2) for ns in A)
 return A,allowed

def solve(A,allowed,limit=.25):
 n=len(A);D=[]
 for s in range(n):
  d=[-1]*n;d[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in A[u]:
    if d[v]<0:d[v]=d[u]+1;q.append(v)
  D.append(d)
 F=[[[w for w in range(n) if w!=v and D[v][w]<=s] for s in [2,2,2,2,3]] for v in range(n)]
 nodes=0;deadline=time.monotonic()+limit
 def rec(ds):
  nonlocal nodes
  nodes+=1
  if nodes%256==0 and time.monotonic()>deadline:raise TimeoutError
  free=[v for v in range(n) if ds[v].bit_count()>1]
  if not free:return [x.bit_length()-1 for x in ds]
  v=min(free,key=lambda v:(ds[v].bit_count(),-sum(map(len,F[v]))))
  for c in range(5):
   bit=1<<c
   if not ds[v]&bit:continue
   nd=ds[:];nd[v]=bit;q=[v];ok=True
   while q and ok:
    u=q.pop();b=nd[u];co=b.bit_length()-1
    for w in F[u][co]:
     if nd[w]&b:
      nd[w]^=b
      if not nd[w]:ok=False;break
      if nd[w].bit_count()==1:q.append(w)
   if ok:
    ans=rec(nd)
    if ans is not None:return ans
  return None
 try:ans=rec([31 if v in allowed else 15 for v in range(n)])
 except TimeoutError:return 'UNKNOWN',None,nodes
 if ans is not None:assert all(ans[u]!=ans[v] or D[u][v]>[2,2,2,2,3][ans[u]] for u in range(n) for v in range(u))
 return ('SAT' if ans is not None else 'UNSAT'),ans,nodes

if __name__=='__main__':
 E=list(combinations(range(4),2));stats=Counter()
 for L in product([2,3],repeat=6):
  A,allowed=graph(4,E,L);st,col,nodes=solve(A,allowed);stats[st]+=1
  if st!='SAT':
   unrestricted=solve(A,list(range(len(A))),1)
   out={'core':E,'lengths':L,'restricted':st,'restricted_nodes':nodes,'original':unrestricted[0],'original_coloring':unrestricted[1],'allowed_exception_vertices':allowed}
   print(json.dumps(out),flush=True)
   if st=='UNSAT':Path(__file__).with_name('mixed_matching_obstacle.json').write_text(json.dumps(out,indent=2)+'\n');break
 print(json.dumps({'stats':dict(stats),'scope':'restricted fifth-color location, K4 core only'}))
