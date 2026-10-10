"""Bounded richer five-vertex boundary experiment for the first palette."""
from itertools import product
from collections import deque
from functools import lru_cache
import time,json
from pathlib import Path
radii=(1,2,3,3)
D0=[[0,1,2,2,3],[1,0,1,1,2],[2,1,0,1,2],[2,1,1,0,1],[3,2,2,1,0]]
S=[w for w in product(range(4),repeat=5) if all(w[i]!=w[j] or D0[i][j]>radii[w[i]] for i in range(5) for j in range(i))]
def relation(L):
 # vertices0,1,2 triangle left ports0,1;3,4,5 right ports3,4.
 a=[set() for _ in range(6)]
 def edge(u,v):a[u].add(v);a[v].add(u)
 for u,v in [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3)]:edge(u,v)
 path=[1]
 for _ in range(L-1):path.append(len(a));a.append(set())
 path.append(3)
 for u,v in zip(path,path[1:]):edge(u,v)
 left=len(a);a.append(set());edge(left,0)
 right=len(a);a.append(set());edge(4,right)
 n=len(a);D=[]
 for u in range(n):
  ds={u:0};q=[u]
  for v in q:
   for w in a[v]:
    if w not in ds:ds[w]=ds[v]+1;q.append(w)
  D.append(ds)
 slots1=(left,0,2,1,path[1]);slots2=(path[-2],3,5,4,right)
 rows=[]
 for s in S:
  row=0
  for j,t in enumerate(S):
   fixed={};ok=True
   for v,c in list(zip(slots1,s))+list(zip(slots2,t)):
    if v in fixed and fixed[v]!=c:ok=False;break
    fixed[v]=c
   if not ok:continue
   if any(c==d and D[u][v]<=radii[c] for u,c in fixed.items() for v,d in fixed.items() if u<v):continue
   free=[v for v in range(n) if v not in fixed]
   def rec(i):
    if i==len(free):return True
    u=free[i]
    for c in range(4):
     if all(c!=d or D[u][v]>radii[c] for v,d in fixed.items()):
      fixed[u]=c
      if rec(i+1):fixed.pop(u);return True
      fixed.pop(u)
    return False
   if rec(0):row|=1<<j
  rows.append(row)
 return tuple(rows)
def mul(A,B):
 out=[]
 for row in A:
  ans=0
  while row:
   bit=row&-row;row-=bit;ans|=B[bit.bit_length()-1]
  out.append(ans)
 return tuple(out)
def diag(A):return any(row>>i&1 for i,row in enumerate(A))
start=time.monotonic();R={}
for L in range(2,15):
 R[L]=relation(L);print('RELATION',L,'entries',sum(x.bit_count() for x in R[L]),'trace',diag(R[L]),flush=True)
Path(__file__).with_name('richer_relations.json').write_text(json.dumps({'states':S,'relations':R},indent=2)+'\n')
seen={A:(L,) for L,A in R.items()};queue=list(seen);bad=[];capped=False
for A in queue:
 if not diag(A):bad.append(seen[A]);print('BAD',seen[A],flush=True)
 for L,B in R.items():
  C=mul(A,B)
  if C not in seen:seen[C]=seen[A]+(L,);queue.append(C)
 if len(seen)>10000 or time.monotonic()-start>60:capped=True;break
print(json.dumps({'states':len(S),'relation_semigroup_seen':len(seen),'capped':capped,'bad_representatives':bad,'elapsed':time.monotonic()-start}),flush=True)
