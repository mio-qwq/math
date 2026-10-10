"""Definition-first checks for the universal random-block upper-bound proof.
Full original adjacency/BFS, finite block encodings, independent exhaustive
Ka(t,2) GP subsets, and exact permutation incidence. No discovery imports.
"""
from itertools import product,permutations,combinations
from collections import deque,Counter
import json,platform,math

def kautz(m,k):
 W=[w for w in product(range(m),repeat=k) if all(w[i]!=w[i+1] for i in range(k-1))]
 index={w:i for i,w in enumerate(W)}
 adj=[[index[w[1:]+(x,)] for x in range(m) if x!=w[-1]] for w in W]
 return W,index,adj

def bfs(adj,s):
 d=[-1]*len(adj);d[s]=0;q=deque([s])
 while q:
  u=q.popleft()
  for v in adj[u]:
   if d[v]<0:d[v]=d[u]+1;q.append(v)
 assert min(d)>=0
 return d

base=[];controls=0
for t in (3,4):
 W,ix,a=kautz(t,2);D=[bfs(a,s) for s in range(len(W))]
 forbidden=[]
 for tri in combinations(range(len(W)),3):
  if any(D[u][v]+D[v][w]==D[u][w] for u,v,w in permutations(tri)):
   forbidden.append(sum(1<<u for u in tri))
 maximum=0;valid=0
 for mask in range(1<<len(W)):
  if any(mask&x==x for x in forbidden):continue
  valid+=1;maximum=max(maximum,mask.bit_count())
 assert maximum==t*t//3
 base.append(dict(t=t,all_subsets=1<<len(W),valid=valid,maximum=maximum))

bridges=[]
for m in (6,7,8,9):
 t=m//2;blocks=[(2*i,2*i+1) for i in range(t)]
 W,ix,a=kautz(m,4);V,jx,b=kautz(t,2)
 images=[ix[blocks[u]+blocks[v]] for u,v in V]
 Dsmall=[bfs(b,i) for i in range(len(V))]
 Dbig=[bfs(a,s) for s in images]
 for i in range(len(V)):
  for j in range(len(V)):
   assert Dbig[i][images[j]]==2*Dsmall[i][j]
 # A claim that the map preserves distances without scaling is false.
 i=0;j=next(j for j in range(len(V)) if Dsmall[i][j]==1)
 assert Dbig[i][images[j]]!=Dsmall[i][j];controls+=1
 # Original forbidden triple from a block triangle, checked using full BFS.
 tri=[jx[(0,1)],jx[(1,2)],jx[(2,0)]]
 u,v,w=tri
 assert Dbig[u][images[v]]+Dbig[v][images[w]]==Dbig[u][images[w]]
 controls+=1
 bridges.append(dict(m=m,full_vertices=len(W),bfs_rows=len(images),scaled_pairs=len(V)**2,bfs_distance_entries=len(images)*len(W)))

# Exact inclusion multiplicities for ALL 6! permutations; no formula used to count.
freq=Counter()
for p in permutations(range(6)):
 B=[p[2*i:2*i+2] for i in range(3)]
 for i in range(3):
  for j in range(3):
   if i!=j:freq[B[i]+B[j]]+=1
assert len(freq)==360 and set(freq.values())=={12}
assert 12*math.prod(range(3,7))==math.factorial(6)*3*2
for m in range(6,101):
 n=m*(m-1)**3;distinct=math.prod(range(m-3,m+1))
 assert n-distinct==m*(m-1)*(3*m-5)
 # Digon + DAG inequality across every allowed split of t.
 t=m//2
 for q in range(t//2+1):
  r=t-2*q
  assert 2*q+r*r//3<=t*t//3
print(json.dumps(dict(status='PASS',python=platform.python_version(),base_GP_checks=base,original_metric_bridges=bridges,permutations_counted=720,distinct_words=360,inclusion_multiplicity=12,finite_algebra_m_values=95,negative_controls=controls,scope='finite checks supplement the universal written proof; no independent peer review'),sort_keys=True))
