"""Definition-first exact obstruction to independent deletion / 3-degeneracy.
Enumerate all subsets. Witness every obstruction by an actual minimum-degree-four
induced subgraph of the original graph square. No discovery or solver imports.
"""
from pathlib import Path
from collections import deque,Counter
from itertools import combinations
import json,platform
obj=json.loads(Path(__file__).with_name('degeneracy_route_probe.json').read_text())
n=obj['vertices'];assert n==15
a=[set() for _ in range(n)]
for u,v in obj['edges']:
 assert 0<=u<n and 0<=v<n and u!=v and v not in a[u]
 a[u].add(v);a[v].add(u)
assert sum(map(len,a))==40
assert all(len(ns)<=3 and (len(ns)!=3 or sum(len(a[v])==3 for v in ns)<=2) for ns in a)
D=[]
for s in range(n):
 d=[-1]*n;d[s]=0;q=deque([s])
 while q:
  u=q.popleft()
  for v in a[u]:
   if d[v]<0:d[v]=d[u]+1;q.append(v)
 assert min(d)>=0;D.append(d)
f=[{v for v in range(n) if v!=u and D[u][v]<=2} for u in range(n)]
edges=[(u,v) for u in range(n) for v in a[u] if u<v]
counts=Counter();independent=0;core_degree_counts=Counter();brooks_candidates=[]
for bits in range(1<<n):
 if any(bits>>u&1 and bits>>v&1 for u,v in edges):continue
 independent+=1;R={u for u in range(n) if not bits>>u&1}
 while True:
  small={u for u in R if len(f[u]&R)<=3}
  if not small:break
  R-=small
 assert R and all(len(f[u]&R)>=4 for u in R)
 counts[len(R)]+=1
 mx=max(len(f[u]&R) for u in R);core_degree_counts[mx]+=1
 if mx==4:brooks_candidates.append((bits,sorted(R)))
c=obj['original_coloring'];assert len(c)==n and all(x in range(5) for x in c)
def valid(c):
 return all(c[u]!=c[v] or D[u][v]>(1 if c[u]==0 else 2) for u,v in combinations(range(n),2))
assert valid(c)
bad=c[:];u,v=edges[0];bad[v]=bad[u];assert not valid(bad)
# Deleting everything is not an independent-set certificate on this graph.
assert any((1<<n)-1>>u&1 and (1<<n)-1>>v&1 for u,v in edges)
print(json.dumps(dict(status='PASS',python=platform.python_version(),vertices=n,edges=len(edges),all_subsets=1<<n,independent_sets=independent,four_core_size_histogram=dict(sorted(counts.items())),four_core_maxdegree_histogram=dict(sorted(core_degree_counts.items())),degree_four_core_candidates=len(brooks_candidates),first_degree_four_core=brooks_candidates[:1],bfs_distance_pairs=n*n,original_palette='SAT',negative_controls=2,scope='all independent deletions leave nonempty 4-core; original conjecture not refuted'),sort_keys=True))
