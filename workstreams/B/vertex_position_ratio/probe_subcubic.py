"""Post-freeze stronger family: binary root tree plus degree-three base comb."""
from collections import deque
from bisect import bisect_left
from pathlib import Path
import json,time
start=time.monotonic();rows=[]
for depth in (2,3,4,5,6):
 k=1<<depth;a=k;N=(k//2-1)**2;L=a+3*N+2;tree=2*k-1;back=tree+k*L;n=back+k;A=[set() for _ in range(n)]
 def at(j,t):return k-1+j if not t else tree+(t-1)*k+j
 def edge(x,y):A[x].add(y);A[y].add(x)
 for x in range(1,tree):edge(x,(x-1)//2)
 for j in range(k):
  for t in range(L):edge(at(j,t),at(j,t+1))
  edge(at(j,a),back+j)
  if j:edge(back+j-1,back+j)
 def bfs(root):
  D=[-1]*n;D[root]=0;q=deque([root])
  while q:
   x=q.popleft()
   for y in A[x]:
    if D[y]<0:D[y]=D[x]+1;q.append(y)
  assert min(D)>=0;return D
 u=at(0,a);old=bfs(u);incoming=[[] for _ in range(k)];peaks=[];p=a+2
 for j in range(k-1,2,-1):
  for i in range(j-2,0,-2):
   edge(at(i,p),at(j,p+1));incoming[j].append(p);peaks.append(at(j,p));p+=3
 assert len(peaks)==N
 D=bfs(u);V=bfs(0);potential=old.copy()
 for j in range(k):
  for t in range(1,L+1):potential[at(j,t)]-=2*bisect_left(incoming[j],t)
 assert potential==D and max(map(len,A))==3
 assert all(V[at(j,t)]==depth+t for j in range(k) for t in range(L+1))
 assert all(V[back+j]==depth+a+1 for j in range(k))
 S=peaks+[at(j,L) for j in range(k)];assert len(set(S))==N+k
 assert all(all(D[y]<D[x] for y in A[x]) for x in S)
 Sv=[back+j for j in range(k)]+[at(j,L) for j in range(k)];assert all(all(V[y]<=V[x] for y in A[x]) for x in Sv)
 rows.append(dict(depth=depth,k=k,order=n,edges=sum(map(len,A))//2,maxdegree=3,root_position=2*k,other_root_witness=N+k,ratio_lower=f'{N+k}/{2*k}',bfs_entries=3*n))
 print(json.dumps(rows[-1]),flush=True)
Path(__file__).with_name('subcubic_probe.json').write_text(json.dumps(dict(status='CANDIDATE_SUBCUBIC_UNBOUNDED',rows=rows,seconds=time.monotonic()-start),separators=(',',':'))+'\n')
