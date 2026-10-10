"""Independent intersection adjacency/BFS checks of the pure family proof.
No discovery imports. Constructor decisions are checked against original graphs.
"""
from itertools import combinations
from collections import deque,Counter
from extend_linegraph import construct
import random,json,platform,time
start=time.monotonic();rng=random.Random(202610101132);modes=Counter();checked=0;product_bfs_entries=0;factor_bfs_entries=0

def graph(n):
 V=list(combinations(range(n),2));index={e:i for i,e in enumerate(V)};adj=[set() for _ in V]
 for i,j in combinations(range(len(V)),2):
  if any(x==y for x in V[i] for y in V[j]):adj[i].add(j);adj[j].add(i)
 D=[]
 for root in range(len(V)):
  ds=[-1]*len(V);ds[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if ds[v]<0:ds[v]=ds[u]+1;q.append(v)
  D.append(ds)
 return V,index,adj,D

def gp(M):
 return all(M[i][j]+M[j][k]!=M[i][k] and M[i][k]+M[k][j]!=M[i][j] and M[j][i]+M[i][k]!=M[j][k] for i,j,k in combinations(range(len(M)),3))

def verify(n,m,k,target=2500,structured=False):
 global checked,product_bfs_entries,factor_bfs_entries
 A,ai,adjA,DA=graph(n);B,bi,adjB,DB=graph(m);factor_bfs_entries+=len(A)**2+len(B)**2
 W=len(B);total=len(A)*len(B);cases=[];attempts=0
 def matrix(S):return [[DA[ai[a]][ai[c]]+DB[bi[b]][bi[d]] for c,d in S] for a,b in S]
 if structured:
  # P4 plus isolated edges, exactly one unused symbol in the first factor.
  E=[(0,1),(1,2),(2,3)]+[(2*j,2*j+1) for j in range(2,k-1)]
  F=[(0,j) for j in range(1,k+1)]
  assert len(E)==len(F)==k
  cases.append(list(zip(E,F)))
  if k==4:cases.append(list(zip([(0,1),(0,2),(0,1),(0,2)],E)))
 while len(cases)<target:
  attempts+=1
  S=[(A[z//W],B[z%W]) for z in rng.sample(range(total),k)]
  if gp(matrix(S)):cases.append(S)
 tested_modes=set()
 for t,S in enumerate(cases):
  assert len(S)==len(set(S))==k and gp(matrix(S))
  z,mode=construct(n,m,S)
  assert z not in S and z[0] in ai and z[1] in bi
  assert gp(matrix(S+[z]));checked+=1;modes[mode]+=1
  if mode not in tested_modes:
   tested_modes.add(mode)
   # Original Cartesian adjacency BFS, rooted at this constructed vertex.
   root=ai[z[0]]*W+bi[z[1]];ds=[-1]*total;ds[root]=0;q=deque([root])
   while q:
    v=q.popleft();x,y=divmod(v,W)
    for w in [a*W+y for a in adjA[x]]+[x*W+b for b in adjB[y]]:
     if ds[w]<0:ds[w]=ds[v]+1;q.append(w)
   product_bfs_entries+=total
   assert all(ds[x*W+y]==DA[ai[z[0]]][x]+DB[bi[z[1]]][y] for x in range(len(A)) for y in range(W))
 # Wrong adjacency convention and duplicate-point extension are rejected.
 assert DA[ai[(0,1)]][ai[(0,2)]]==1 and DA[ai[(0,1)]][ai[(2,3)]]==2
 assert len(set(cases[0]+[cases[0][0]]))!=k+1
 return dict(n=n,m=m,k=k,checked=len(cases),generated_attempts=attempts,modes=sorted(tested_modes))

rows=[verify(7,7,4,structured=True),verify(7,9,4),verify(9,9,5,structured=True),verify(11,13,6,structured=True)]
# A false parameter premise is explicitly rejected: lowerGP(L(K8))=4, not>4.
matching=[(0,1),(2,3),(4,5),(6,7)]
try:construct(8,8,list(zip(matching,matching)))
except AssertionError:pass
else:raise AssertionError('failed to reject a non-strict factor premise')
print(json.dumps(dict(status='PASS',python=platform.python_version(),rows=rows,product_gp_sets_extended=checked,construction_modes=dict(modes),factor_bfs_entries=factor_bfs_entries,product_bfs_entries=product_bfs_entries,negative_controls=3,seconds=time.monotonic()-start,scope='semantic checks of complete elementary all-parameter proof; independent review pending'),sort_keys=True))
