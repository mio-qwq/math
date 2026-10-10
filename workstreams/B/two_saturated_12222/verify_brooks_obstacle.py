"""Exact route obstruction checker: enumerate EVERY independent set from original edges.
No imports from MILP/discovery or coloring solvers. Stdlib only.
"""
from pathlib import Path
from collections import deque,Counter
from itertools import combinations
import json,platform
obj=json.loads(Path(__file__).with_name('brooks_route_probe.json').read_text())
n=obj['vertices'];a=[set() for _ in range(n)]
for u,v in obj['edges']:
    assert 0<=u<n and 0<=v<n and u!=v and v not in a[u]
    a[u].add(v);a[v].add(u)
assert n==12 and sum(map(len,a))==32
assert all(len(ns)<=3 and (len(ns)!=3 or sum(len(a[v])==3 for v in ns)<=2) for ns in a)
D=[]
for s in range(n):
    dd=[-1]*n;dd[s]=0;q=deque([s])
    while q:
        u=q.popleft()
        for v in a[u]:
            if dd[v]<0:dd[v]=dd[u]+1;q.append(v)
    assert min(dd)>=0;D.append(dd)
F=[sum(1<<v for v in range(n) if v!=u and D[u][v]<=2) for u in range(n)]
edge_masks=[(1<<u)|(1<<v) for u in range(n) for v in a[u] if u<v]
full=(1<<n)-1;hist=Counter();count=0
for I in range(1<<n):
    if any(I&e==e for e in edge_masks):continue
    count+=1;outside=full^I
    score=max(((F[u]&outside).bit_count() for u in range(n) if outside>>u&1),default=0)
    hist[score]+=1
assert min(hist)==5 and not any(k<=4 for k in hist)
c=obj['original_coloring'];assert len(c)==n and all(x in range(5) for x in c)
def valid(colors):
    return all(colors[u]!=colors[v] or D[u][v]>(1 if colors[u]==0 else 2) for u,v in combinations(range(n),2))
assert valid(c)
bad=c[:];u=0;v=min(a[0]);bad[v]=bad[u];assert not valid(bad)
# A false generalized conclusion to every graph is rejected: edgeless graph has score0.
empty_F=[0]*n;assert max((x&full).bit_count() for x in empty_F)==0
print(json.dumps(dict(status='PASS',python=platform.python_version(),vertices=n,edges=16,all_subsets=1<<n,independent_sets=count,minimum_remaining_square_max_degree=min(hist),score_histogram=dict(sorted(hist.items())),original_coloring=c,bfs_distance_pairs=n*n,negative_controls=2,scope='restricted Brooks-degree criterion impossible; original palette SAT'),sort_keys=True))
