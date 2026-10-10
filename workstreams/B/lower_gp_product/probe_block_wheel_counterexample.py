"""Discovery construction from feasible five-point signature system, exact integers."""
from itertools import combinations
from collections import deque
from pathlib import Path
import json,time
P=Path(__file__).parent;start=time.monotonic()
def distances(n,E):
 adj=[set() for _ in range(n)]
 for a,b in E:adj[a].add(b);adj[b].add(a)
 D=[]
 for s in range(n):
  r=[-1]*n;r[s]=0;q=deque([s])
  while q:
   a=q.popleft()
   for b in adj[a]:
    if r[b]<0:r[b]=r[a]+1;q.append(b)
  D.append(r)
 return D
G=[e for e in combinations(range(11),2) if 0 in e or (e[0]<=5)==(e[1]<=5)]
# G: hub0, clique1..5, clique6..10. H: landmarks0..4,
# universal hub2, C4 on0,3,1,4, and6true twins on each C4 edge.
H=[e for e in combinations(range(5),2) if e not in [(0,1),(3,4)]]
quadrants=[(0,3),(0,4),(1,3),(1,4)]
for q,(a,b) in enumerate(quadrants):
 block=list(range(5+6*q,11+6*q));H+=list(combinations(block,2));H +=[(u,v) for u in block for v in (2,a,b)]
H=sorted(tuple(sorted(e)) for e in H);DG=distances(11,G);DH=distances(29,H)
S=[(1,0),(1,1),(0,2),(6,3),(6,4)]
def dist(a,b):return DG[a[0]][b[0]]+DH[a[1]][b[1]]
def col(a,b,c):return dist(a,b)+dist(b,c)==dist(a,c) or dist(a,c)+dist(c,b)==dist(a,b) or dist(b,a)+dist(a,c)==dist(b,c)
assert all(not col(a,b,c) for a,b,c in combinations(S,3))
cover={}
for g in range(11):
 for h in range(29):
  z=(g,h)
  if z in S:continue
  pair=next(((i,j) for i,j in combinations(range(5),2) if col(S[i],S[j],z)),None)
  assert pair is not None,(g,h);cover[f'{g},{h}']=pair
checks={}
for name,D in [('G',DG),('H',DH)]:
 n=len(D);full=(1<<n)-1;lines={}
 for a,b in combinations(range(n),2):
  lines[a,b]=sum(1<<u for u in range(n) if D[a][u]+D[u][b]==D[a][b] or abs(D[u][a]-D[u][b])==D[a][b])
 gpcounts={};tested=0
 for k in range(1,6):
  gps=0
  for T in combinations(range(n),k):
   tested+=1
   if any(lines[a,b]>>c&1 for a,b,c in combinations(T,3)):continue
   gps+=1;blocked=sum(1<<u for u in T)
   for a,b in combinations(T,2):blocked|=lines[a,b]
   assert blocked!=full,(name,T)
  gpcounts[k]=gps
 checks[name]=dict(order=n,edges=len(G if name=='G' else H),subsets_tested=tested,gp_counts=gpcounts)
result=dict(status='EXACT_ORIGINAL_COUNTEREXAMPLE_CANDIDATE',G=dict(order=11,edges=G),H=dict(order=29,edges=H),S=S,product_order=319,unselected_vertices_covered=len(cover),cover=cover,factor_checks=checks,seconds=time.monotonic()-start,scope='original lowerGP product conjecture: factor lowerGP>=6, maximal productGP5; independent review pending')
(P/'block_wheel_candidate.json').write_text(json.dumps(result,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('G','H','cover')}),flush=True)
