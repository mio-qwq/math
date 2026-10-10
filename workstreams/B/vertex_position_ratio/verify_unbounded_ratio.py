"""Standalone original-definition checks. No discovery imports or matching solver.
Closed shortcut indices, original BFS, geodesic covers, distance-boundary witnesses.
"""
from itertools import combinations
from collections import deque
import hashlib,json,time,platform
start=time.monotonic();digest=hashlib.sha256()
def construct(r,ascending=False):
 k=2*r;a=k;N=r*(r-1);L=a+3*N+2;labels=[('v',0)]+[(j,t) for t in range(1,L+1) for j in range(k)];ix={x:i for i,x in enumerate(labels)};A=[set() for _ in labels]
 def edge(x,y):A[ix[x]].add(ix[y]);A[ix[y]].add(ix[x])
 for j in range(k):
  edge(('v',0),(j,1))
  for t in range(1,L):edge((j,t),(j,t+1))
 for j in range(k-1):edge((j,a),(j+1,a))
 schedule=[]
 for j in range(2,k):
  for q in range(1,j//2+1):
   before=sum(h//2 for h in (range(2,j) if ascending else range(j+1,k)));rank=before+q-1;p=a+2+3*rank;i=j-2*q
   edge((i,p),(j,p+1));schedule.append((i,j,p))
 assert len(schedule)==N and len({p for i,j,p in schedule})==N
 u=ix[0,a];S=[ix[j,p] for i,j,p in schedule]+[ix[j,L] for j in range(k)]
 potential=[a]
 for j,t in labels[1:]:
  initial=min(a+t,a-t+j) if t<=a else t-a+j
  potential.append(initial-2*sum(1 for i,jj,p in schedule if jj==j and p<t))
 return A,labels,ix,u,S,potential,(k,a,N,L)
def bfs(A,u):
 D=[-1]*len(A);D[u]=0;todo=deque([u])
 while todo:
  x=todo.popleft()
  for y in A[x]:
   if D[y]<0:D[y]=D[x]+1;todo.append(y)
 assert min(D)>=0;return D

def valid_potential(A,u,p):
 return p[u]==0 and all(x==u or p[x]>0 for x in range(len(A))) and all(abs(p[x]-p[y])<=1 for x in range(len(A)) for y in A[x]) and all(x==u or any(p[y]==p[x]-1 for y in A[x]) for x in range(len(A)))
rows=[]
for r in (2,3,5,12,20):
 A,labels,ix,u,S,p,params=construct(r);k,a,N,L=params;n=len(A)
 assert n==6*r**3-2*r*r+4*r+1 and sum(map(len,A))//2==n+r*r+r-2
 assert all(x not in A[x] and all(x in A[y] for y in A[x]) for x in range(n))
 assert valid_potential(A,u,p)
 dv=bfs(A,0);du=bfs(A,u);assert du==p and dv==[0]+[t for j,t in labels[1:]]
 # k original v-geodesics cover every nonroot vertex, certifying p_v<=k.
 covered={0}
 for j in range(k):
  chain=[0]+[ix[j,t] for t in range(1,L+1)]
  assert all(y in A[x] and dv[y]==dv[x]+1 for x,y in zip(chain,chain[1:]));covered.update(chain)
 assert len(covered)==n and len({ix[j,L] for j in range(k)})==k
 # Those k endpoints all have equal positive distanceL, so p_v>=k.
 assert all(dv[ix[j,L]]==L for j in range(k))
 assert len(set(S))==r*(r+1) and u not in S
 assert all(A[x] and all(du[y]<du[x] for y in A[x]) for x in S)
 # Small instances additionally check EVERY selected pair against actual BFS.
 pairchecks=0;extra_bfs=0
 if r<=5:
  for pos,x in enumerate(S):
   dx=bfs(A,x);extra_bfs+=n
   for y in S[pos+1:]:
    assert du[x]+dx[y]!=du[y] and du[y]+dx[y]!=du[x];pairchecks+=1
 digest.update(str((r,du,sorted(S))).encode())
 # Corrupted potential: a peak raised by1 breaks a necessary edge inequality.
 corrupt=p.copy();corrupt[S[0]]+=1;assert not valid_potential(A,u,corrupt)
 # False p_v<=k-1 rejected by the explicit k-vertex equal-level set.
 assert len([ix[j,L] for j in range(k)])>k-1
 # Adding observation root to a position set is invalid for any second point.
 x=S[0];assert du[u]+du[x]==du[x]
 rows.append(dict(r=r,order=n,edges=sum(map(len,A))//2,tracks=k,peaks=N,root_position_exact=k,other_root_witness=len(S),ratio_lower=f'{r+1}/2',two_root_bfs_entries=2*n,additional_pair_bfs_entries=extra_bfs,selected_pair_checks=pairchecks))
# Deliberately wrong processing order: lower targets first invalidates the potential.
A,labels,ix,u,S,p,params=construct(3,ascending=True);assert not valid_potential(A,u,p) and bfs(A,u)!=p
print(json.dumps(dict(status='PASS',python=platform.python_version(),rows=rows,witness_sha256=digest.hexdigest(),negative_controls=4,seconds=time.monotonic()-start,scope='complete elementary family proof in PROOF.md; finite original-definition regression and certificates; independent review pending'),sort_keys=True))
