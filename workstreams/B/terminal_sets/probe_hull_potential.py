"""Third mechanism: test whether inclusion-minimal geodesic convex hulls force
maximal GP sets to be terminal. This is a PROOF-ROUTE conjecture, not the original.
"""
from probe_cubic import distances
from itertools import combinations
from pathlib import Path
import json,time
P=Path(__file__).parent;start=time.monotonic();tested=0
for graph in json.loads((P/'cubic_probe.json').read_text()):
 n=graph['order']
 if n>16:break
 a,D=distances(n,graph['edges']);full=(1<<n)-1
 lines=[[0]*n for _ in range(n)];intervals=[[0]*n for _ in range(n)];endcovers=[[0]*n for _ in range(n)]
 for u,v in combinations(range(n),2):
  for w in range(n):
   if D[u][w]+D[w][v]==D[u][v]:intervals[u][v]|=1<<w
   if abs(D[w][u]-D[w][v])==D[u][v]:endcovers[u][v]|=1<<w
  lines[u][v]=intervals[u][v]|endcovers[u][v]
  for t in (lines,intervals,endcovers):t[v][u]=t[u][v]
 maximal=[]
 def dfs(S,candidates,blocked,covered):
  mask=sum(1<<u for u in S)
  if (blocked|mask)==full:
   hull=mask
   while True:
    old=hull;V=[u for u in range(n) if hull>>u&1]
    for u,v in combinations(V,2):hull|=intervals[u][v]
    if old==hull:break
   maximal.append(dict(selected=S,mask=mask,hull=hull,terminal=(covered|mask)==full));return
  while candidates:
   bit=candidates&-candidates;candidates-=bit;v=bit.bit_length()-1
   if blocked&bit:continue
   b=blocked;c=covered
   for u in S:b|=lines[u][v];c|=endcovers[u][v]
   dfs(S+[v],candidates&~b,b,c)
 dfs([],full,0,0);tested+=1
 minimal=[r for r in maximal if not any(q['hull']!=r['hull'] and q['hull']&r['hull']==q['hull'] for q in maximal)]
 bad=next((r for r in minimal if not r['terminal']),None)
 if bad:
  data=dict(order=n,edges=graph['edges'],selected=bad['selected'],hull=[v for v in range(n) if bad['hull']>>v&1],maximal_gp_sets=len(maximal),minimal_hull_sets=len(minimal),terminal_witness=graph['selected'])
  (P/'hull_route_obstruction.json').write_text(json.dumps(data,indent=2)+'\n')
  print(json.dumps(dict(status='STRONG_ROUTE_FALSE',graphs=tested,**data,seconds=time.monotonic()-start)));break
else:print(json.dumps(dict(status='NO_OBSTRUCTION_IN_WINDOW',graphs=tested,seconds=time.monotonic()-start)))
