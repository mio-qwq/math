"""Independent new construction: descending-target diagonal shortcuts.
A closed potential proof is being prepared; exact BFS discovery checks only.
"""
from collections import deque
from pathlib import Path
import json,time
P=Path(__file__).parent;start=time.monotonic();results=[]
for k in (4,8,12,24,40):
 N=sum(j//2 for j in range(k));a=k;L=a+3*N+2;n=1+k*L
 def v(j,t):return 0 if t==0 else 1+(t-1)*k+j
 adj=[set() for _ in range(n)]
 def edge(x,y):adj[x].add(y);adj[y].add(x)
 for j in range(k):
  for t in range(L):edge(v(j,t),v(j,t+1))
 for j in range(k-1):edge(v(j,a),v(j+1,a))
 p=a+2;shortcuts=[];peaks=[]
 for j in range(k-1,1,-1):
  for i in range(j-2,-1,-2):
   edge(v(i,p),v(j,p+1));shortcuts.append((i,j,p));peaks.append(v(j,p));p+=3
 assert len(peaks)==N and p-2<=L
 u=v(0,a)
 def bfs(root):
  D=[-1]*n;D[root]=0;q=deque([root])
  while q:
   x=q.popleft()
   for y in adj[x]:
    if D[y]<0:D[y]=D[x]+1;q.append(y)
  return D
 D=bfs(u);V=bfs(0);assert V==[0]+[1+(x-1)//k for x in range(1,n)]
 target=peaks+[v(j,L) for j in range(k)]
 assert len(set(target))==N+k and all(all(D[y]<D[x] for y in adj[x]) for x in target)
 # Explicit potential, with every target's suffix lowered by2per incoming shortcut.
 potential=[a]
 for t in range(1,L+1):
  for j in range(k):
   base=min(a+t,a-t+j) if t<=a else t-a+j
   potential.append(base-2*sum(1 for i,jj,p in shortcuts if jj==j and t>=p+1))
 assert D==potential
 results.append(dict(k=k,peaks=N,level=L,order=n,edges=sum(map(len,adj))//2,root_lower_position=k,other_root_position_lower_bound=N+k,ratio_lower_bound=f'{N+k}/{k}',bfs_entries=2*n,shortcuts=shortcuts))
 print(json.dumps({kk:vv for kk,vv in results[-1].items() if kk!='shortcuts'}),flush=True)
(P/'descending_shortcuts_probe.json').write_text(json.dumps(dict(status='CANDIDATE_UNBOUNDED_FAMILY',rows=results,seconds=time.monotonic()-start),separators=(',',':'))+'\n')
