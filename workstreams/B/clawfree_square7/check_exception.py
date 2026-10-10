"""Original-definition finite exception and local-bound checker; stdlib only."""
import itertools,json
from collections import deque

def clawfree(a):
 return all(any(v in a[u] for u,v in itertools.combinations(ns,2)) for ns in a if len(ns)==3)
def square(a):
 return [(ns|set().union(*(a[v] for v in ns)))-{u} for u,ns in enumerate(a)]
def distances(a,r):
 d=[None]*len(a);d[r]=0;q=deque([r])
 while q:
  u=q.popleft()
  for v in a[u]:
   if d[v] is None:d[v]=d[u]+1;q.append(v)
 return d

def cubic_graphs(n):
 a=[set() for _ in range(n)]
 def rec():
  todo=[u for u in range(n) if len(a[u])<3]
  if not todo:
   yield [ns.copy() for ns in a];return
  u=todo[0];need=3-len(a[u]);avail=[v for v in range(u+1,n) if len(a[v])<3 and v not in a[u]]
  for chosen in itertools.combinations(avail,need):
   for v in chosen:a[u].add(v);a[v].add(u)
   yield from rec()
   for v in chosen:a[u].remove(v);a[v].remove(u)
 yield from rec()

all_cubic=cf=connected=0;diameters={}
for a in cubic_graphs(8):
 all_cubic+=1
 if not clawfree(a):continue
 cf+=1
 if None in distances(a,0):continue
 connected+=1;D=[distances(a,u) for u in range(8)];diam=max(map(max,D));assert diam>=3
 diameters[diam]=diameters.get(diam,0)+1
small=0
for n in range(7):
 es=list(itertools.combinations(range(n),2))
 for mask in range(1<<len(es)):
  a=[set() for _ in range(n)]
  for i,(u,v) in enumerate(es):
   if mask>>i&1:a[u].add(v);a[v].add(u)
  if any(len(ns)>3 for ns in a) or not clawfree(a):continue
  sq=square(a);assert all(len(ns)<=7 for ns in sq)
  assert all(len(sq[u])<=6 for u in range(n) if len(a[u])<=2)
  small+=1
cube=[{u^1,u^2,u^4} for u in range(8)];assert not clawfree(cube)
K4=[set(range(4))-{u} for u in range(4)];assert clawfree(K4) and all(len(ns)==3 for ns in square(K4))
print(json.dumps({'cubic_order8':all_cubic,'clawfree_order8':cf,'connected_clawfree_order8':connected,'diameters':diameters,'small_local_bound_cases':small,'controls':'PASS','status':'PASS'},sort_keys=True))
