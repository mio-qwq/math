"""Exact exhaustive verification for ORIGINAL Conjecture4.5 at order15.
No discovery imports. Enumerates all 128 inverse-closed connection sets and uses
triangles / full BFS / false-twin classes. Also checks ALL induced vertex subsets
in the surviving graphs, independently of induced-path DFS used in discovery.
"""
from itertools import combinations
from collections import deque,Counter
import json,platform
N=15
counts=Counter();survivors=[];subset_checks=0;negative_controls=0
for mask in range(1<<7):
 positive=[i+1 for i in range(7) if mask>>i&1]
 conn=set(positive)|{(-x)%N for x in positive}
 a=[{v for v in range(N) if v!=u and (v-u)%N in conn} for u in range(N)]
 assert all(u not in a[u] and all(u in a[v] for v in a[u]) for u in range(N))
 triangle=next((tri for tri in combinations(range(N),3) if all(v in a[u] for u,v in combinations(tri,2))),None)
 if triangle is not None:
  # Any induced path has no triangle as an induced subgraph.
  counts['triangle_obstruction']+=1;continue
 D=[]
 for s in range(N):
  ds=[-1]*N;ds[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in a[u]:
    if ds[v]<0:ds[v]=ds[u]+1;q.append(v)
  D.append(ds)
 if any(x<0 or x>2 for row in D for x in row) or max(map(max,D))!=2:
  counts['not_diameter_two']+=1;continue
 classes={}
 for u in range(N):classes.setdefault(tuple(sorted(a[u])),[]).append(u)
 twins=next((vs[:3] for vs in classes.values() if len(vs)>=3),None)
 assert twins is not None and all(v not in a[u] for u,v in combinations(twins,2))
 assert a[twins[0]]==a[twins[1]]==a[twins[2]]
 # Exhaustive independent algorithm: every subset inducing a path is checked.
 # A connected simple graph is a path iff max degree<=2 and |E|=|V|-1.
 induced_paths=0;triple_mask=sum(1<<u for u in twins)
 for bits in range(1,1<<N):
  V=[u for u in range(N) if bits>>u&1];subset_checks+=1
  deg=[sum(bits>>v&1 for v in a[u]) for u in V]
  if max(deg)>2 or sum(deg)!=2*(len(V)-1):continue
  seen={V[0]};q=deque([V[0]])
  while q:
   for v in a[q.popleft()]:
    if bits>>v&1 and v not in seen:seen.add(v);q.append(v)
  if len(seen)!=len(V):continue
  induced_paths+=1;assert bits&triple_mask!=triple_mask
 counts['false_twin_mp_at_least_three']+=1
 survivors.append(dict(positive_steps=positive,connection=sorted(conn),false_twin_triple=twins,induced_path_vertex_subsets=induced_paths,diameter=2))
assert sum(counts.values())==128
assert [x['positive_steps'] for x in survivors]==[[1,4,6],[2,3,7]]
# Deliberately wrong twin certificates fail in the path P3.
a=[{1},{0,2},{1}]
assert not(a[0]==a[1]==a[2]);negative_controls+=1
# Replacing the target by n=5 must not receive a nonexistence conclusion:
# C5 is a circulant of diameter2, and every triple lies in an induced P4.
a=[{(u-1)%5,(u+1)%5} for u in range(5)]
for tri in combinations(range(5),3):
 assert any(set(tri)<=({0,1,2,3,4}-{omit}) for omit in range(5))
# The induced graph after deleting each vertex is directly checked to be P4.
for omit in range(5):
 V=set(range(5))-{omit};degrees=sorted(len(a[u]&V) for u in V)
 assert degrees==[1,1,2,2]
negative_controls+=1
print(json.dumps(dict(status='PASS',python=platform.python_version(),order=15,all_circulant_connection_sets=128,classification=dict(counts),survivors=survivors,induced_vertex_subsets_checked=subset_checks,negative_controls=negative_controls,scope='no simple undirected circulant of order15 has both diameter2 and mp2; pending independent review'),sort_keys=True))
