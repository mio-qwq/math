"""Direct construction and full-distance regression for the subfamily theorem."""
from collections import deque
import random,json

def make(n,edges,matching,lengths):
 a=[set() for _ in range(3*n)];inc=[[] for _ in range(n)]
 for i,(u,v) in enumerate(edges):inc[u].append(i);inc[v].append(i)
 assert all(len(es)==3 for es in inc)
 port={(u,e):3*u+j for u,es in enumerate(inc) for j,e in enumerate(es)}
 def edge(u,v):a[u].add(v);a[v].add(u)
 for u in range(n):
  for i,j in [(0,1),(0,2),(1,2)]:edge(3*u+i,3*u+j)
 mate={};hc={};col={}
 for e in matching:
  u,v=edges[e];assert u not in mate and v not in mate
  mate[u]=mate[v]=e;hc[u]=0;hc[v]=1
 assert len(mate)==n
 F=[[] for _ in range(n)]
 for e,(u,v) in enumerate(edges):
  if e not in matching:F[u].append((v,e));F[v].append((u,e))
 out={}
 for start in range(n):
  if start in out:continue
  u=start;prev=None
  while True:
   v,e=next((v,e) for v,e in F[u] if e!=prev)
   out[u]=e;u=v;prev=e
   if u==start:break
 for u in range(n):
  col[port[u,mate[u]]]=hc[u]
  for e in inc[u]:
   if e!=mate[u]:col[port[u,e]]=2 if e==out[u] else 1-hc[u]
 for e,(u,v) in enumerate(edges):
  x=port[u,e];y=port[v,e]
  if e in matching:
   p=len(a);a.extend([set() for _ in range(3)])
   for i,j in [(0,1),(0,2),(1,2)]:edge(p+i,p+j)
   edge(x,p);edge(y,p+1);col[p]=1-hc[u];col[p+1]=1-hc[v];col[p+2]=2
  else:
   path=[x]
   for _ in range(lengths[e]-1):w=len(a);a.append(set());edge(path[-1],w);path.append(w)
   edge(path[-1],y);path.append(y)
   if col[path[-1]]==2:path.reverse()
   for j in range(len(path)-2,0,-1):col[path[j]]=1-col[path[j+1]]
 return a,[col[v] for v in range(len(a))]

def check(a,c):
 heavy={u for u,ns in enumerate(a) if len(ns)==3 and all(len(a[v])==3 for v in ns)}
 assert all(len(ns)<=3 and (len(ns)!=3 or any(a[v]&ns for v in ns)) for ns in a)
 assert all(not(a[u]&heavy) for u in heavy)
 for root in range(len(a)):
  d=[99999]*len(a);d[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v in a[u]:
    if d[v]==99999:d[v]=d[u]+1;q.append(v)
  assert all(c[root]!=c[v] or d[v]>(1,1,2)[c[v]] for v in range(root))

if __name__=='__main__':
 rng=random.Random(30112);count=0
 for n in [4,6,8,10,12,20,40]:
  es=[(u,(u+1)%n) for u in range(n)]+[(u,u+n//2) for u in range(n//2)]
  for L in range(2,12):
   lens=[rng.randrange(2,30) if L==11 else L for _ in es]
   a,c=make(n,es,set(range(n,len(es))),lens);check(a,c);count+=1
 bad=c.copy();u=0;v=next(iter(a[u]));bad[v]=bad[u]
 try:check(a,bad)
 except AssertionError:pass
 else:raise AssertionError('corruption accepted')
 print(json.dumps({'graphs':count,'original_distance_checks':'PASS','corrupted_coloring':'rejected','scope':'full matched-heavy subfamily only'}))
