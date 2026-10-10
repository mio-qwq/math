"""Original adjacency/potential certificates for bipartite maximum-degree-three family.
No imports from the discovery or earlier ratio checker.
"""
from collections import deque
from bisect import bisect_left
from itertools import combinations
import hashlib,json,time,platform
start=time.monotonic();digest=hashlib.sha256()
def build(depth,ascending=False):
 k=1<<depth;a=2*k;N=(k-1)*(k-2)//2;L=a+3*N+3;T=2*k-1;H=T+k*L;M=H+k;n=M+k-1;A=[set() for _ in range(n)]
 def track(j,t):return k-1+j if t==0 else T+(t-1)*k+j
 def edge(x,y):A[x].add(y);A[y].add(x)
 for x in range(1,T):edge(x,(x-1)//2)
 for j in range(k):
  for t in range(L):edge(track(j,t),track(j,t+1))
  edge(track(j,a),H+j)
 for j in range(k-1):edge(H+j,M+j);edge(M+j,H+j+1)
 def bfs(u):
  D=[-1]*n;D[u]=0;q=deque([u])
  while q:
   x=q.popleft()
   for y in A[x]:
    if D[y]<0:D[y]=D[x]+1;q.append(y)
  assert min(D)>=0;return D
 u=track(0,a);initial=bfs(u)
 assert all(initial[track(j,a)]==2*j+2 for j in range(1,k))
 peaks=[];incoming=[[] for _ in range(k)]
 for j in range(2,k):
  for i in range(1,j):
   before=sum(h-1 for h in (range(2,j) if ascending else range(j+1,k)));s=before+j-1-i;p=a+2+3*s
   edge(track(i,p),track(j,p+1));peaks.append(track(j,p));incoming[j].append(p)
 potential=initial.copy()
 for j in range(k):
  incoming[j].sort()
  for t in range(1,L+1):potential[track(j,t)]-=2*bisect_left(incoming[j],t)
 return A,track,bfs,u,initial,potential,peaks,(k,a,N,L,T,H,M,n)
def valid(A,u,p):
 return p[u]==0 and all(x==u or p[x]>0 for x in range(len(A))) and all(abs(p[x]-p[y])<=1 for x in range(len(A)) for y in A[x]) and all(x==u or any(p[y]==p[x]-1 for y in A[x]) for x in range(len(A)))
rows=[]
for depth in (2,3,4,5):
 A,track,bfs,u,old,p,peaks,data=build(depth);k,a,N,L,T,H,M,n=data;du=bfs(u);dv=bfs(0)
 assert valid(A,u,p) and du==p
 assert max(map(len,A))==3 and all(x not in A[x] and all(x in A[y] for y in A[x]) for x in range(n))
 assert all((dv[x]-dv[y])%2==1 for x in range(n) for y in A[x])
 assert all(dv[track(j,t)]==depth+t for j in range(k) for t in range(L+1))
 assert all(dv[H+j]==depth+a+1 for j in range(k)) and all(dv[M+j]==depth+a+2 for j in range(k-1))
 # Explicit2k rooted-geodesic cover: kfull tracks, kbackbone branches.
 cover=set();paths=[]
 for j in range(k):
  treepath=[];x=track(j,0)
  while x:treepath.append(x);x=(x-1)//2
  treepath=[0]+list(reversed(treepath));paths.append(treepath+[track(j,t) for t in range(1,L+1)])
  branch=treepath+[track(j,t) for t in range(1,a+1)]+[H+j]
  if j<k-1:branch.append(M+j)
  paths.append(branch)
 for path in paths:
  assert path[0]==0 and all(y in A[x] and dv[y]==dv[x]+1 for x,y in zip(path,path[1:]));cover.update(path)
 assert len(paths)==2*k and len(cover)==n
 # 2k-root position witness: allHvertices and upper endpoints.
 Sv=[H+j for j in range(k)]+[track(j,L) for j in range(k)];assert len(set(Sv))==2*k
 for x in Sv:
  # Any ascending continuation from an Hvertex stops at an unselected Mvertex.
  for y in A[x]:
   if dv[y]>dv[x]:assert y not in Sv and all(dv[z]<=dv[y] for z in A[y])
 Su=peaks+[track(j,L) for j in range(k)];assert len(set(Su))==N+k
 assert all(all(du[y]<du[x] for y in A[x]) for x in Su)
 direct=0;extra=0
 if depth<=3:
  for D,S in ((dv,Sv),(du,Su)):
   for pos,x in enumerate(S):
    dx=bfs(x);extra+=n
    for y in S[pos+1:]:assert D[x]+dx[y]!=D[y] and D[y]+dx[y]!=D[x];direct+=1
 corrupt=p.copy();corrupt[peaks[0]]+=1;assert not valid(A,u,corrupt)
 # DirectH-H edge would violate the proven bipartition and is rejected.
 assert (dv[H]-dv[H+1])%2==0
 assert len(Sv)>2*k-1
 digest.update(str((depth,du,Sv,sorted(Su))).encode())
 rows.append(dict(depth=depth,k=k,vertices=n,edges=sum(map(len,A))//2,maximum_degree=3,bipartite=True,root_position_exact=2*k,other_root_position_lower=N+k,ratio_lower=f'{N+k}/{2*k}',initial_and_two_root_bfs_entries=3*n,direct_position_pairs=direct,extra_pair_bfs_entries=extra))
A,track,bfs,u,old,p,peaks,data=build(3,ascending=True);assert not valid(A,u,p) and bfs(u)!=p
print(json.dumps(dict(status='PASS',python=platform.python_version(),rows=rows,witness_sha256=digest.hexdigest(),negative_controls=4,seconds=time.monotonic()-start,scope='all-depth bipartite subcubic ratio divergence proved in SUBCUBIC_PROOF.md; actual finite adjacency checks; independent review pending'),sort_keys=True))
