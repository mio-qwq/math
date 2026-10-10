"""Analyze radius-three-color location patterns in attachable two-port gadgets."""
from collections import deque
from itertools import combinations
import json

def gadget(lengths):
 a=[set() for _ in range(6)]
 def edge(u,v):a[u].add(v);a[v].add(u)
 for u,v in [(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)]:edge(u,v)
 for i,L in enumerate(lengths):
  x=i
  for _ in range(L-1):y=len(a);a.append(set());edge(x,y);x=y
  edge(x,3+i)
 return a

def analyze(a):
 n=len(a);D=[]
 for s in range(n):
  d=[99]*n;d[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in a[u]:
    if d[v]==99:d[v]=d[u]+1;q.append(v)
  D.append(d)
 def four(removed):
  V=[u for u in range(n) if u not in removed];c={}
  def rec():
   if len(c)==len(V):return True
   u=max((v for v in V if v not in c),key=lambda v:len({c[w] for w in c if D[v][w]<=2}))
   forbid={c[w] for w in c if D[u][w]<=2}
   for x in range(4):
    if x not in forbid:
     c[u]=x
     if rec():return True
     del c[u]
   return False
  return rec()
 feasible=[]
 for mask in range(1<<n):
  R=[v for v in range(n) if mask>>v&1]
  if any(D[u][v]<=3 for u,v in combinations(R,2)):continue
  if four(set(R)):feasible.append(R)
 return {'n':n,'feasible_special_sets':feasible,'boundary_distances':[[v,D[2][v],D[5][v]] for v in range(n)]}
if __name__=='__main__':
 for ls in [(2,2),(2,3),(2,4),(3,3),(3,4)]:
  print(json.dumps({'lengths':ls,**analyze(gadget(ls))}),flush=True)
