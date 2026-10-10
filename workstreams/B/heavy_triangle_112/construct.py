"""Construct a (1,1,2)-coloring from an original admissible graph.
No discovery-solver imports, external packages, or bounded search.
"""
from collections import deque

def construct(adj):
 n=len(adj);assert all(u not in ns and all(u in adj[v] for v in ns) for u,ns in enumerate(adj))
 assert all(len(ns)<=3 for ns in adj)
 heavy={u for u,ns in enumerate(adj) if len(ns)==3 and all(len(adj[v])==3 for v in ns)}
 assert all(not(adj[u]&heavy) for u in heavy)
 assert all(len(ns)!=3 or any(adj[v]&ns for v in ns) for u,ns in enumerate(adj))
 live=set(range(n));deg=[len(ns) for ns in adj];q=deque(u for u in live if deg[u]<=1);peeled=[]
 while q:
  u=q.popleft()
  if u not in live:continue
  live.remove(u);peeled.append(u)
  for v in adj[u]&live:
   deg[v]-=1
   if deg[v]<=1:q.append(v)
 tris=[]
 for u in sorted(live):
  for v in sorted(adj[u]&live):
   if v<=u:continue
   for w in sorted(adj[u]&adj[v]&live):
    if w>v:tris.append({u,v,w})
 blocks=[]
 for t in tris:
  hits=[i for i,b in enumerate(blocks) if b&t]
  union=t.copy()
  for i in hits:union|=blocks[i]
  blocks=[b for i,b in enumerate(blocks) if i not in hits]+[union]
 which={u:i for i,b in enumerate(blocks) for u in b};ports=[]
 for b in blocks:
  assert len(b) in (3,4)
  ps={u for u in b if adj[u]&live-b};ports.append(ps)
  if len(b)==4:assert len(ps)<=1
 edges=[];used=set()
 for i,b in enumerate(blocks):
  for u in sorted(ports[i]):
   v=next(iter((adj[u]&live)-b));key=tuple(sorted((u,v)))
   if key in used:continue
   path=[u,v];used.add(key)
   while path[-1] not in which:
    curr=path[-1];ns=(adj[curr]&live)-{path[-2]};assert len(ns)==1
    w=next(iter(ns));used.add(tuple(sorted((curr,w))));path.append(w)
   edges.append({'u':i,'v':which[path[-1]],'path':path,'L':len(path)-1})
 inc=[[] for _ in blocks]
 for e,dat in enumerate(edges):inc[dat['u']].append(e);inc[dat['v']].append(e)
 D={e for e,d in enumerate(edges) if d['L']==1}
 assert all(len(es)<=3 for es in inc)
 assert all(sum(e in D for e in es)<=1 for es in inc if len(es)==3)
 # Hall matching: assign distinct available edges to the degree-three nodes.
 owner={};out={}
 def augment(u,seen):
  for e in sorted(set(inc[u])-D):
   if e in seen:continue
   seen.add(e)
   if e not in owner or augment(owner[e],seen):owner[e]=u;out[u]=e;return True
  return False
 for u,es in enumerate(inc):
  if len(es)==3:assert augment(u,set())
 assert len(set(out.values()))==len(out)
 exchanges=0
 while True:
  selected=set(out.values());remaining=set(range(len(edges)))-selected
  unseen=set(range(len(blocks)));cycle=None
  while unseen:
   root=next(iter(unseen));nodes={root};ee=set();stack=[root];unseen.remove(root)
   while stack:
    u=stack.pop()
    for e in inc[u]:
     if e not in remaining:continue
     ee.add(e);d=edges[e];v=d['v'] if d['u']==u else d['u']
     if v not in nodes:nodes.add(v);unseen.discard(v);stack.append(v)
   if ee and all(sum(e in remaining for e in inc[u])==2 for u in nodes) and ee-D:
    cycle=(nodes,ee);break
  if cycle is None:break
  nodes,ee=cycle;e=min(ee-D);u=edges[e]['u'];old=out.get(u)
  if old is not None:
   d=edges[old];v=d['v'] if d['u']==u else d['u'];assert v not in nodes
  else:assert len(inc[u])==2 and len(blocks[u])==3
  out[u]=e;exchanges+=1
  assert exchanges<=len(edges) and len(set(out.values()))==len(out)
 C=set()
 for u,b in enumerate(blocks):
  if len(b)==4:
   assert u not in out
   C.add(min(v for v in b if len(adj[v]&b)==3))
  elif u in out:
   d=edges[out[u]];C.add(d['path'][0] if d['u']==u else d['path'][-1])
  else:C.add(min(b-ports[u]))
 # Degree-two components with no block are independent plain cycles.
 unseen=live-set(which)
 while unseen:
  root=next(iter(unseen));component={root};stack=[root];touch=False;unseen.remove(root)
  while stack:
   u=stack.pop()
   for v in adj[u]&live:
    if v in which:touch=True;continue
    if v not in component:component.add(v);unseen.discard(v);stack.append(v)
  if not touch and len(component)%2:C.add(min(component))
 colors={u:2 for u in C}
 for root in sorted(live-C):
  if root in colors:continue
  colors[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v in (adj[u]&live)-C:
    if v not in colors:colors[v]=1-colors[u];q.append(v)
    else:assert colors[v]!=colors[u],('odd residual cycle',u,v)
 for u in reversed(peeled):
  forbidden={colors[v] for v in adj[u] if v in colors}
  colors[u]=next(c for c in (0,1) if c not in forbidden)
 return [colors[u] for u in range(n)],{'blocks':len(blocks),'core_edges':len(edges),'cycle_exchanges':exchanges,'peeled':len(peeled)}
