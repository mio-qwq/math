"""Definition-first exact verifier. No discovery/checker imports; Python stdlib.

Every hypothetical five-coloring selects a high-colored vertex per triangle.
Adjacent triangles have all cross-distances <=3, so the selected labels give
one of the enumerated proper core colorings. The radius-four representatives
are then enumerated using ORIGINAL BFS distances, without private-neighbor
or diamond-forcing predicates. Zero representatives for every labeling is
an exhaustive obstruction covering any number of high vertices per triangle.
"""
from collections import deque
from itertools import combinations,product
from pathlib import Path
import json,hashlib,platform

def graph(k):
 assert k>=3
 core=[set() for _ in range(4*k)]
 def link(u,v):assert u!=v and v not in core[u];core[u].add(v);core[v].add(u)
 for i in range(k):
  a,b,p,q=range(4*i,4*i+4)
  for u,v in [(a,b),(a,p),(a,q),(b,p),(b,q),(q,4*((i+1)%k)+2)]:link(u,v)
 labels=[(v,w) for v,ns in enumerate(core) for w in sorted(ns)]
 index={pair:i for i,pair in enumerate(labels)}
 adj=[set() for _ in labels]
 for x,(v,w) in enumerate(labels):
  adj[x].add(index[w,v])
  adj[x].update(index[v,z] for z in core[v] if z!=w)
 blocks=[[index[v,w] for w in sorted(ns)] for v,ns in enumerate(core)]
 return core,labels,adj,blocks

def bfs(adj):
 D=[]
 for r in range(len(adj)):
  d=[None]*len(adj);d[r]=0;q=deque([r])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if d[v] is None:d[v]=d[u]+1;q.append(v)
  D.append(d)
 return D

def valid_color(D,c,radii):
 return len(c)==len(D) and all(0<=x<len(radii) for x in c) and all(
  c[u]!=c[v] or D[u][v]>radii[c[u]] for u,v in combinations(range(len(c)),2))

def transversal(D,blocks,ids,radius,all_choices=False):
 total=0;good=[]
 for choice in product(*(blocks[v] for v in ids)):
  total+=1
  if all(D[u][v]>radius for u,v in combinations(choice,2)):
   good.append(choice)
   if not all_choices:return total,good
 return total,good

def complete(adj,D,blocks,lab,radii):
 c=[-1]*len(adj)
 for col,r in enumerate(radii[2:]):
  _,choices=transversal(D,blocks,[v for v,x in enumerate(lab) if x==col],r)
  if not choices:return None
  for v in choices[0]:c[v]=col+2
 for s in range(len(adj)):
  if c[s]>=0:continue
  c[s]=0;q=[s]
  for u in q:
   for v in adj[u]:
    if c[v]>=2:continue
    if c[v]<0:c[v]=1-c[u];q.append(v)
    elif c[v]==c[u]:return None
 assert valid_color(D,c,radii)
 return c

def verify_certificate(data):
 core,labels,adj,blocks=graph(3)
 edges=[[u,v] for u in range(len(adj)) for v in sorted(adj[u]) if u<v]
 assert data['n']==36 and data['edges']==edges
 assert data['labels']==[list(x) for x in labels]
 assert data['palette']==[1,1,3,3,4]
 assert data['core_edges']==[[u,v] for u in range(12) for v in sorted(core[u]) if u<v]
 return core,adj,blocks

def run():
 p=Path(__file__).with_name('counterexample.json');data=json.loads(p.read_text())
 core,adj,blocks=verify_certificate(data);D=bfs(adj)
 assert len(adj)==36 and sum(map(len,adj))//2==54
 assert all(len(ns)==3 for ns in adj) and all(x is not None for row in D for x in row)
 assert all(u in adj[v] for u,ns in enumerate(adj) for v in ns)
 assert all(any(v in adj[u] for u,v in combinations(ns,2)) for ns in adj)
 assert len(adj)!=12 # source H has twelve vertices
 assert all(v in adj[u] for block in blocks for u,v in combinations(block,2))
 core_edges=[(u,v) for u,ns in enumerate(core) for v in ns if u<v]
 cross_pairs=0
 for u,v in core_edges:
  for x in blocks[u]:
   for y in blocks[v]:assert D[x][y]<=3;cross_pairs+=1
 proper=choices=valid=0;weak_witness=None
 for lab in product(range(3),repeat=12):
  if any(lab[u]==lab[v] for u,v in core_edges):continue
  proper+=1
  n,ok=transversal(D,blocks,[v for v in range(12) if lab[v]==2],4,True)
  choices+=n;valid+=len(ok)
  if weak_witness is None:weak_witness=complete(adj,D,blocks,lab,[1,1,3,3,3])
 assert proper==48 and choices==3888 and valid==0
 assert weak_witness is not None and valid_color(D,weak_witness,[1,1,3,3,3])
 # False UNSAT conclusion under weaker original-distance condition is rejected.
 assert not valid_color(D,weak_witness,[1,1,3,3,4])
 # Damaged certificate is rejected, not silently accepted as the fixed graph.
 bad=json.loads(json.dumps(data));bad['edges'].pop()
 try:verify_certificate(bad)
 except AssertionError:pass
 else:raise AssertionError('damaged edge certificate accepted')
 # A corrupted coloring must fail the original full-graph distance checker.
 damaged=weak_witness.copy();damaged[blocks[0][0]]=damaged[blocks[0][1]]=0
 assert not valid_color(D,damaged,[1,1,3,3,3])
 # Even ring is a genuine SAT control for the exact queried palette.
 ec,_,ea,eb=graph(4);ed=bfs(ea);lab=[]
 for i in range(4):
  t=i%2;lab.extend([1-t,2,t,t])
 assert all(lab[u]!=lab[v] for u,ns in enumerate(ec) for v in ns)
 even=complete(ea,ed,eb,lab,[1,1,3,3,4]);assert even is not None
 assert valid_color(ed,even,[1,1,3,3,4])
 result={'status':'PASS','python':platform.python_version(),'n':36,'m':54,
 'connected_cubic_clawfree':True,'excluded_H_order':12,'bfs_rows':36,
 'adjacent_block_cross_pairs':cross_pairs,'core_labelings_considered':3**12,
 'proper_core_labelings':proper,'radius4_transversals_checked':choices,
 'valid_radius4_transversals':valid,'negative_controls':3,'even_ring_sat_control':True,
 'weaker_11333_coloring':weak_witness,'even_ring_11334_coloring':even,
 'certificate_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 print(json.dumps(result,sort_keys=True))
if __name__=='__main__':run()
