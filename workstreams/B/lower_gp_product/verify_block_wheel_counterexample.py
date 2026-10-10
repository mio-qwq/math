"""Definition-first counterexample verifier. No discovery or metric-sum imports.
Rebuild factors as unions of cliques and the original Cartesian adjacency.
"""
from itertools import combinations
from collections import deque
import hashlib,json,time,platform
start=time.monotonic()
def clique_union(n,blocks):
 A=[set() for _ in range(n)]
 for block in blocks:
  for a,b in combinations(block,2):A[a].add(b);A[b].add(a)
 return A
G=clique_union(11,[[0]+list(range(1,6)),[0]+list(range(6,11))])
corners=[(0,3),(0,4),(1,3),(1,4)]
H=clique_union(29,[[2,a,b]+list(range(5+6*q,11+6*q)) for q,(a,b) in enumerate(corners)])
for A in (G,H):assert all(i not in A[i] and all(i in A[j] for j in A[i]) for i in range(len(A)))
assert sum(map(len,G))==60 and sum(map(len,H))==280
P=[set() for _ in range(319)]
for g in range(11):
 for h in range(29):
  P[29*g+h].update(29*u+h for u in G[g]);P[29*g+h].update(29*g+v for v in H[h])
assert sum(map(len,P))==4820

def bfs(A):
 D=[]
 for root in range(len(A)):
  ds=[-1]*len(A);ds[root]=0;q=deque([root])
  while q:
   a=q.popleft()
   for b in A[a]:
    if ds[b]<0:ds[b]=ds[a]+1;q.append(b)
  assert min(ds)>=0;D.append(ds)
 return D
DG,DH,DP=map(bfs,(G,H,P));assert max(map(max,DG))==max(map(max,DH))==2 and max(map(max,DP))==4

def bad(D,a,b,c):
 # Check each potential middle explicitly against original BFS distances.
 return any(D[x][y]+D[y][z]==D[x][z] for x,y,z in ((a,b,c),(a,c,b),(b,a,c)))
def gp(D,T):return all(not bad(D,a,b,c) for a,b,c in combinations(T,3))
def extension(D,T,x):return x not in T and all(not bad(D,a,b,x) for a,b in combinations(T,2))
def maximal(D,T):return gp(D,T) and not any(extension(D,T,x) for x in range(len(D)) if x not in T)
selected=[29*1+0,29*1+1,29*0+2,29*6+3,29*6+4]
assert len(set(selected))==5 and gp(DP,selected) and maximal(DP,selected)
cover=hashlib.sha256();covered=0
for x in range(319):
 if x in selected:continue
 a,b=next((i,j) for i,j in combinations(range(5),2) if bad(DP,selected[i],selected[j],x));covered+=1;cover.update(f'{x}:{a},{b};'.encode())
assert covered==314

# Different verification algorithm from discovery's union-of-line masks:
# every small GP set receives an explicit valid extension from original distances.
factor_rows=[];factor_digest=hashlib.sha256()
for name,D in (('G',DG),('H',DH)):
 tested=0;counts={}
 for k in range(1,6):
  count=0
  for T in combinations(range(len(D)),k):
   tested+=1
   if not gp(D,T):continue
   count+=1;x=next((x for x in range(len(D)) if extension(D,T,x)),None)
   assert x is not None,(name,T)
   factor_digest.update(f'{name}:{T}:{x};'.encode())
  counts[k]=count
 factor_rows.append(dict(factor=name,order=len(D),subsets_tested=tested,gp_sets_extended=counts))
# Exact G=6 upper witness, independent of the lower enumeration.
assert maximal(DG,list(range(6)))
# True-twin premise and all maximal landmark GP subsets checked directly.
for q in range(4):
 block=range(5+6*q,11+6*q);neighborhoods=[H[x]|{x} for x in block];assert all(N==neighborhoods[0] for N in neighborhoods)
landmark_max=[]
for k in range(1,6):
 for T in combinations(range(5),k):
  if gp(DH,T) and not any(extension(DH,T,x) for x in range(5) if x not in T):
   assert any(extension(DH,T,x) for x in range(5,29));landmark_max.append(T)
assert set(landmark_max)=={(0,1),(3,4),(0,2,3),(0,2,4),(1,2,3),(1,2,4)}
# Three intentional corruptions: non-GP selected set; false maximality; false G lower>=7.
bad_set=next(selected[:-1]+[x] for x in range(319) if x not in selected and not gp(DP,selected[:-1]+[x]))
assert not gp(DP,bad_set)
assert not maximal(DP,selected[:-1]) and extension(DP,selected[:-1],selected[-1])
assert len(range(6))<7 and maximal(DG,list(range(6)))
print(json.dumps(dict(status='PASS',python=platform.python_version(),factor_orders=[11,29],factor_edges=[30,140],product_order=319,product_edges=2410,original_bfs_entries=11**2+29**2+319**2,selected_product_vertices=[divmod(x,29) for x in selected],selected_gp_triples=10,unselected_product_vertices_blocked=covered,product_cover_sha256=cover.hexdigest(),factor_rows=factor_rows,factor_extension_sha256=factor_digest.hexdigest(),true_twin_classes=4,landmark_maximal_sets=landmark_max,negative_controls=3,seconds=time.monotonic()-start,conclusion='original product conjecture refuted: gp^-(G square H)<=5<6<=min(gp^-G,gp^-H); independent review pending'),sort_keys=True))
