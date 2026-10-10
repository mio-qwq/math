"""Original adjacency/BFS regression of the universal extension construction.
Imports the proposed constructor only; neither discovery program is imported.
All returned points are checked against independently rebuilt product distances.
"""
from collections import deque,Counter
from itertools import combinations,product
import json,platform
from extend_triple import extend_three

def bfs(n,E):
 adj=[set() for _ in range(n)]
 for u,v in E:assert 0<=u<v<n;adj[u].add(v);adj[v].add(u)
 D=[]
 for root in range(n):
  row=[None]*n;row[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if row[v] is None:row[v]=row[u]+1;q.append(v)
  D.append(row)
 return D

def direct_gp(D,S):
 for a,b,c in combinations(S,3):
  if D[a][b] is None or D[a][c] is None or D[b][c] is None:continue
  if D[a][b]+D[b][c]==D[a][c] or D[b][a]+D[a][c]==D[b][c] or D[a][c]+D[c][b]==D[a][b]:return False
 return True

def has_extension(D,S):return any(u not in S and direct_gp(D,S+[u]) for u in range(len(D)))
def lower(D):
 for k in range(len(D)+1):
  for S in combinations(range(len(D)),k):
   if direct_gp(D,list(S)) and not has_extension(D,list(S)):return k
 raise AssertionError

def cartesian(g,E,h,F):
 return [(u*h+b,v*h+b) for u,v in E for b in range(h)]+[(a*h+u,a*h+v) for a in range(g) for u,v in F]

def blowup(n,E):
 E={tuple(sorted(e)) for e in E}
 return 2*n,[(u,v) for u,v in combinations(range(2*n),2) if u//2==v//2 or tuple(sorted((u//2,v//2))) in E]
fixtures=[(4,list(combinations(range(4),2))),(7,[(u,v) for u,v in combinations(range(7),2) if u<3]),blowup(3,[(0,1),(1,2)]),blowup(4,[(0,1),(1,2),(2,3)]),blowup(5,[(i,(i+1)%5) for i in range(5)])]
modes=Counter();count=0;hypotheses=0;bfs_entries=0
for g,E in fixtures:
 A=bfs(g,E);bfs_entries+=g*g
 for k in range(1,4):
  for S in combinations(range(g),k):
   if direct_gp(A,list(S)):assert has_extension(A,list(S));hypotheses+=1
 D=bfs(g*g,cartesian(g,E,g,E));bfs_entries+=g**4
 # This equality is checked, not assumed, in the original-graph verifier.
 for u in range(g*g):
  for v in range(g*g):assert D[u][v]==A[u//g][v//g]+A[u%g][v%g]
 for triple in combinations(range(g*g),3):
  if not direct_gp(D,list(triple)):continue
  S=[divmod(u,g) for u in triple];z,mode=extend_three(A,A,S);w=z[0]*g+z[1]
  assert 0<=z[0]<g and 0<=z[1]<g and w not in triple
  assert direct_gp(D,list(triple)+[w]);modes[mode]+=1;count+=1
# Opposite-middle algebra: collect all distinct equality signatures in a small
# integer-metric regression domain. This is not a finite-to-universal inference.
patterns={}
for x,y in product(range(1,4),repeat=2):
 for ds in product(range(1,9),repeat=3):
  A=[[0,x,x+y],[x,0,y],[x+y,y,0]]
  if any(abs(ds[i]-ds[j])>A[i][j] or ds[i]+ds[j]<A[i][j] for i,j in combinations(range(3),2)):continue
  M=[row+[ds[i]] for i,row in enumerate(A)]+[list(ds)+[0]]
  if not direct_gp(M,[0,2,3]):continue
  signature=tuple((ds[i]+ds[j]==A[i][j],ds[i]+A[i][j]==ds[j],ds[j]+A[i][j]==ds[i]) for i,j in combinations(range(3),2))
  patterns.setdefault(signature,M)
assert len(patterns)==7
algebra=0;third_needed=0
for A,B0 in product(patterns.values(),repeat=2):
 perm=[0,2,1,3];B=[[B0[i][j] for j in perm] for i in perm]
 S=[(0,0),(1,1),(2,2)];T=[(3,0),(0,3),(3,3)]
 D=[[A[u//4][v//4]+B[u%4][v%4] for v in range(16)] for u in range(16)]
 assert direct_gp(D,[0,5,10]);ok=[direct_gp(D,[0,5,10,a*4+b]) for a,b in T]
 assert any(ok);algebra+=1;third_needed+=not any(ok[:2])
# Disconnected cases: direct enumeration, not use of the component lower bound.
boundaries=0
for g,E,h,F in [(3,[(0,1)],3,[(0,1)]),(2,[],2,[]),(1,[],3,[(0,1),(1,2)]),(0,[],3,[(0,1),(1,2)])]:
 A=bfs(g,E);B=bfs(h,F);D=bfs(g*h,cartesian(g,E,h,F))
 assert lower(D)>=min(4,lower(A),lower(B));boundaries+=1
# Three deliberate false premises/conclusions.
D=bfs(16,cartesian(4,list(combinations(range(4),2)),4,list(combinations(range(4),2))))
assert not direct_gp(D,[0,1,5])
assert direct_gp(D,[0,5,10]) and not direct_gp(D,[0,5,10,1])
assert lower(bfs(3,[(0,1),(1,2)]))==2
print(json.dumps(dict(status='PASS',python=platform.python_version(),fixtures=len(fixtures),factor_extension_hypotheses=hypotheses,original_bfs_entries=bfs_entries,product_gp_triples_extended=count,extension_cases=dict(modes),metric_signatures=len(patterns),signature_pairs=algebra,third_candidate_required=third_needed,disconnected_or_boundary_fixtures=boundaries,negative_controls=3,scope='finite semantic regressions of complete written universal proof; independent review pending'),sort_keys=True))
