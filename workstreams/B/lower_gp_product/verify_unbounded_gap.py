"""Original-adjacency regression checks of the elementary unbounded-gap family."""
from itertools import combinations
from collections import deque
import hashlib,json,time,platform
start=time.monotonic();digest=hashlib.sha256()
def graph(n,blocks):
 A=[set() for _ in range(n)]
 for B in blocks:
  for a,b in combinations(B,2):A[a].add(b);A[b].add(a)
 return A

def bfs(A,root):
 d=[-1]*len(A);d[root]=0;q=deque([root])
 while q:
  a=q.popleft()
  for b in A[a]:
   if d[b]<0:d[b]=d[a]+1;q.append(b)
 assert min(d)>=0;return d

def product_graph(G,H):
 h=len(H);P=[set() for _ in range(len(G)*h)]
 for a in range(len(G)):
  for b in range(h):P[a*h+b].update(u*h+b for u in G[a]);P[a*h+b].update(a*h+v for v in H[b])
 return P

def col(a,b,c):return a+b==c or a+c==b or b+c==a
rows=[]
for r in (6,7,12,31):
 g=2*r-1;h=4*r+5;G=graph(g,[[0]+list(range(1,r)),[0]+list(range(r,g))]);corners=[(0,3),(0,4),(1,3),(1,4)]
 H=graph(h,[[2,a,b]+list(range(5+r*q,5+r*(q+1))) for q,(a,b) in enumerate(corners)])
 assert len(G[0])==g-1 and len(H[2])==h-1
 for q in range(4):
  Q=list(range(5+r*q,5+r*(q+1)));assert all(H[x]|{x}==H[Q[0]]|{Q[0]} for x in Q)
 P=product_graph(G,H);S=[h+0,h+1,2,r*h+3,r*h+4];D=[bfs(P,s) for s in S]
 assert all(not col(D[a][S[b]],D[b][S[c]],D[a][S[c]]) for a,b,c in combinations(range(5),3))
 covered=0
 for x in range(g*h):
  if x in S:continue
  pair=next(((a,b) for a,b in combinations(range(5),2) if col(D[a][S[b]],D[a][x],D[b][x])),None)
  assert pair is not None;covered+=1;digest.update(f'{r}:{x}:{pair};'.encode())
 # Exact factor distances from landmarks, sufficient for the six GP extension cases.
 HD=[bfs(H,s) for s in range(5)];base=[(0,1),(3,4),(0,2,3),(0,2,4),(1,2,3),(1,2,4)]
 for T in base:
  assert any(all(not col(HD[a][b],HD[a][x],HD[b][x]) for a,b in combinations(T,2)) for x in range(5,h))
 # Removing a selected point leaves an extendible set, rejecting false maximality.
 assert all(not col(D[a][S[b]],D[a][S[4]],D[b][S[4]]) for a,b in combinations(range(4),2))
 rows.append(dict(r=r,factor_orders=[g,h],product_order=g*h,selected_bfs_entries=5*g*h,factor_landmark_bfs_entries=5*h,outside_vertices_blocked=covered))
# Small complete-factor equality witnesses: all smaller GP sets explicitly extend.
small=[]
for r in range(1,6):
 A=graph(r,[list(range(r))]);P=product_graph(A,A);D=[bfs(P,s) for s in range(r*r)]
 def gp(T):return all(not col(D[a][b],D[a][c],D[b][c]) for a,b,c in combinations(T,3))
 row=list(range(r))
 assert gp(row) and all(not gp(row+[x]) for x in range(r,r*r))
 tested=0
 for k in range(1,r):
  for T in combinations(range(r*r),k):
   if not gp(T):continue
   useda={x//r for x in T};usedb={x%r for x in T};a=next(x for x in range(r) if x not in useda);b=next(x for x in range(r) if x not in usedb);assert gp(list(T)+[a*r+b]);tested+=1
 small.append(dict(r=r,small_gp_sets_extended=tested))
print(json.dumps(dict(status='PASS',python=platform.python_version(),family_rows=rows,small_complete_cases=small,witness_digest=digest.hexdigest(),negative_controls='false four-point maximality rejected in all four family instances',seconds=time.monotonic()-start,scope='semantic regressions of elementary all-r family; proof not inferred from samples; independent review pending'),sort_keys=True))
