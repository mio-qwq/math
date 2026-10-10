"""Separate exact check: one exceptional vertex is insufficient on one graph."""
from collections import deque
import json
# Two triangles, corresponding vertices joined by length-three paths.
E=[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)]
for i in range(3):E += [(i,6+2*i),(6+2*i,7+2*i),(7+2*i,3+i)]
a=[set() for _ in range(12)]
for u,v in E:a[u].add(v);a[v].add(u)
for u,ns in enumerate(a):
 assert len(ns)<=3
 if len(ns)==3:
  assert sum(len(a[v])==3 for v in ns)<=2
  assert any(a[v]&ns for v in ns)
D=[]
for r in range(12):
 d=[99]*12;d[r]=0;q=deque([r])
 while q:
  u=q.popleft()
  for v in a[u]:
   if d[v]==99:d[v]=d[u]+1;q.append(v)
 D.append(d)
def four_color(removed):
 V=[v for v in range(12) if v not in removed];color={};nodes=0
 def rec():
  nonlocal nodes
  nodes+=1
  if len(color)==len(V):return dict(color)
  u=max((u for u in V if u not in color),key=lambda u:(len({color[v] for v in color if D[u][v]<=2}),sum(D[u][v]<=2 for v in V)))
  forbidden={color[v] for v in color if D[u][v]<=2}
  for c in range(4):
   if c in forbidden:continue
   color[u]=c
   out=rec()
   if out is not None:return out
   del color[u]
  return None
 ans=rec();return ans,nodes
runs=[]
for v in range(12):
 ans,nodes=four_color({v});assert ans is None
 runs.append(nodes)
witness=None
for u in range(12):
 for v in range(u+1,12):
  if D[u][v]<=3:continue
  ans,nodes=four_color({u,v})
  if ans is not None:
   ans[u]=ans[v]=4
   assert all(ans[x]!=ans[y] or D[x][y]>(2,2,2,2,3)[ans[x]] for x in range(12) for y in range(x))
   witness=[ans[x] for x in range(12)];break
 if witness:break
assert witness is not None
print(json.dumps({'result':'one-exception route impossible; original conjecture satisfied','one_exception_unsat_nodes':runs,'two_exception_coloring':witness,'minimum_special_vertices':2}))
# Negative control: full deletion permits an empty four-coloring.
assert four_color(set(range(12)))[0]=={}
print('PASS positive and negative route controls')
