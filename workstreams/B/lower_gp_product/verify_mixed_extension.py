"""Independent original-graph checks of the mixed-family construction."""
from itertools import combinations
from collections import deque,Counter
from extend_mixed import construct
import random,json,platform,time
rng=random.Random(202610101138);start=time.monotonic();modes=Counter();factor_entries=0;product_entries=0;total_checked=0

def build(n,intersection):
 V=list(combinations(range(n),2));I={e:i for i,e in enumerate(V)};adj=[set() for _ in V]
 for i,j in combinations(range(len(V)),2):
  common=any(a==b for a in V[i] for b in V[j])
  if common==intersection:adj[i].add(j);adj[j].add(i)
 D=[]
 for root in range(len(V)):
  row=[-1]*len(V);row[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if row[v]<0:row[v]=row[u]+1;q.append(v)
  D.append(row)
 return V,I,adj,D

def gp(M):
 return all(M[i][j]+M[j][k]!=M[i][k] and M[i][k]+M[k][j]!=M[i][j] and M[j][i]+M[i][k]!=M[j][k] for i,j,k in combinations(range(len(M)),3))

rows=[]
for n,m,k in ((7,10,4),(9,10,4),(9,12,5),(13,16,5)):
 A,ai,aa,DA=build(n,True);B,bi,ab,DB=build(m,False);factor_entries+=len(A)**2+len(B)**2;W=len(B);N=len(A)*len(B)
 def matrix(S):return [[DA[ai[a]][ai[c]]+DB[bi[b]][bi[d]] for c,d in S] for a,b in S]
 E=[(0,1),(1,2),(2,3)]+[(2*j,2*j+1) for j in range(2,k-1)]
 F=[(0,j) for j in range(1,k+1)]
 repeat=([(0,1),(2,3)]*3)[:k]
 cases=[list(zip(E,F)),list(zip(repeat,F))];attempts=0;used=set()
 while len(cases)<2500:
  attempts+=1;S=[(A[z//W],B[z%W]) for z in rng.sample(range(N),k)]
  if gp(matrix(S)):cases.append(S)
 for S in cases:
  assert len(set(S))==k and gp(matrix(S));z,mode=construct(n,m,S)
  assert z not in S and z[0] in ai and z[1] in bi and gp(matrix(S+[z]))
  modes[mode]+=1;total_checked+=1
  if mode not in used:
   used.add(mode);root=ai[z[0]]*W+bi[z[1]];ds=[-1]*N;ds[root]=0;q=deque([root])
   while q:
    w=q.popleft();x,y=divmod(w,W)
    for v in [u*W+y for u in aa[x]]+[x*W+u for u in ab[y]]:
     if ds[v]<0:ds[v]=ds[w]+1;q.append(v)
   assert all(ds[x*W+y]==DA[ai[z[0]]][x]+DB[bi[z[1]]][y] for x in range(len(A)) for y in range(W));product_entries+=N
 # Adjacency-role reversal and selected-point duplication are detected.
 assert DA[ai[(0,1)]][ai[(0,2)]]==1 and DB[bi[(0,1)]][bi[(0,2)]]==2
 assert len(set(cases[0]+[cases[0][0]]))!=k+1
 rows.append(dict(n=n,m=m,k=k,checked=len(cases),attempts=attempts,modes=sorted(used)))
S=[((0,1),(0,1)),((0,2),(0,2)),((0,3),(0,3)),((0,4),(0,4))]
for n,m in ((8,10),(7,9)):
 try:construct(n,m,S)
 except AssertionError:pass
 else:raise AssertionError('invalid strict factor premise accepted')
print(json.dumps(dict(status='PASS',python=platform.python_version(),rows=rows,product_gp_sets_extended=total_checked,construction_modes=dict(modes),factor_bfs_entries=factor_entries,product_bfs_entries=product_entries,negative_controls=4,seconds=time.monotonic()-start,scope='original-definition regressions of universal mixed-family proof; independent review pending'),sort_keys=True))
