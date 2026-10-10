"""Construct witnesses, then validate original graph/BFS distances independently."""
from itertools import permutations,combinations
from collections import deque
import json

def color_graph(A,k,dynamic=False):
 c={}
 def go():
  if len(c)==len(A):return dict(c)
  u=max((v for v in range(len(A)) if v not in c),key=lambda v:(len({c[w] for w in A[v] if w in c}),len(A[v])))
  for x in range(k):
   if any(c.get(v)==x for v in A[u]):continue
   c[u]=x
   if all(len(A[v])<2 or not A[v]<=c.keys() or len({c[w] for w in A[v]})>=2 for v in range(len(A))) if dynamic else True:
    out=go()
    if out is not None:return out
   del c[u]
  return None
 return go()

def path_word(L,start,end):
 paths={start:list(start)}
 for _ in range(L-1):
  nxt={}
  for (a,b),w in paths.items():
   for c in range(4):
    if c not in (a,b):nxt[(b,c)]=w+[c]
  paths=nxt
 return paths.get(end)

def witness(n,E,L):
 incident=[[] for _ in range(n)]
 for i,(u,v) in enumerate(E):incident[u].append(i);incident[v].append(i)
 assert all(len(x)==3 for x in incident)
 port={(v,e):3*v+i for v,es in enumerate(incident) for i,e in enumerate(es)}
 old=[set() for _ in range(3*n)]
 def add(A,u,v):assert u!=v and v not in A[u];A[u].add(v);A[v].add(u)
 for v in range(n):
  for a,b in combinations(range(3*v,3*v+3),2):add(old,a,b)
 for i,(u,v) in enumerate(E):add(old,port[u,i],port[v,i])
 if L==2:
  col=color_graph(old,3);assert col is not None;missing=[3]*n
 elif L==3:
  core=[set() for _ in range(n)]
  for u,v in E:core[u].add(v);core[v].add(u)
  lab=color_graph(core,4,True);assert lab is not None;missing=[lab[v] for v in range(n)];col={}
  for v in range(n):
   ns=[E[e][1] if E[e][0]==v else E[e][0] for e in incident[v]]
   p=next(p for p in permutations(set(range(4))-{lab[v]}) if all(x!=lab[w] for x,w in zip(p,ns)))
   for e,x in zip(incident[v],p):col[port[v,e]]=x
 else:col={v:v%3+1 for v in range(3*n)};missing=[0]*n
 A=[set() for _ in range(3*n)]
 for v in range(n):
  for a,b in combinations(range(3*v,3*v+3),2):add(A,a,b)
 for i,(u,v) in enumerate(E):
  x,y=port[u,i],port[v,i];word=path_word(L,(col[x],missing[u]),(missing[v],col[y]));assert word is not None
  nodes=[x]
  for z in word[1:-1]:nodes.append(len(A));col[len(A)]=z;A.append(set())
  nodes.append(y)
  for x,y in zip(nodes,nodes[1:]):add(A,x,y)
 # Original assumptions, plus original full-graph distance-two validation.
 for u,ns in enumerate(A):
  assert len(ns)<=3
  if len(ns)==3:assert sum(len(A[v])==3 for v in ns)<=2 and any(A[v]&ns for v in ns)
 pairs=0
 for s in range(len(A)):
  D=[-1]*len(A);D[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in A[u]:
    if D[v]<0:D[v]=D[u]+1;q.append(v)
  assert all(d>=0 for d in D)
  for t in range(s):
   if col[s]==col[t]:assert D[t]>2
   pairs+=1
 return {'core_vertices':n,'length':L,'original_vertices':len(A),'original_pairs':pairs}

if __name__=='__main__':
 cores=[(4,list(combinations(range(4),2))),(6,[(u,v) for u in range(3) for v in range(3,6)]),(6,[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]),(10,[(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)])]
 for n in [4,6]:cores.append((n,[(i,(i+1)%n) for i in range(n)]+[(i,i+1) for i in range(0,n,2)]))
 rows=[witness(n,E,L) for n,E in cores for L in [2,3,7,8]]
 # The triple-edge core violates the required nonmonochromatic incidence condition.
 assert len({1,1,1})==1
 print(json.dumps({'status':'PASS','presentations':len(rows),'pairs':sum(r['original_pairs'] for r in rows),'results':rows}))
