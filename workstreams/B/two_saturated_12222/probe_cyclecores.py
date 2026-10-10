"""Distinct forced-clique mechanism: C5 squares force original vertices into I."""
import importlib.util,json,random
from pathlib import Path
from collections import Counter
s=importlib.util.spec_from_file_location('new',Path(__file__).with_name('explore.py'));m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rng=random.Random(512222);stats=Counter();hardest=0
for size in [4,5,7]:
 for count in [2,4,6,10,16]:
  n=size*count
  cycle_edges=[]
  for j in range(count):
   for i in range(size):cycle_edges.append(tuple(sorted((size*j+i,size*j+(i+1)%size))))
  for rep in range(20):
   for attempt in range(10000):
    vs=list(range(n));rng.shuffle(vs);mat=[tuple(sorted(vs[i:i+2])) for i in range(0,n,2)]
    if all(e not in cycle_edges for e in mat):break
   else:raise RuntimeError
   es=cycle_edges+mat;sub={i:1 for i in range(len(cycle_edges),len(es))}
   a=m.old.graph(n,es,sub);state,c,nodes=m.solver.solve(a,(1,2,2,2,2),limit=1)
   stats[str(size)+':'+state]+=1;hardest=max(hardest,nodes)
   if state=='UNSAT':
    Path(__file__).with_name('candidate.json').write_text(json.dumps({'n':len(a),'edges':[(u,v) for u,ns in enumerate(a) for v in ns if u<v]},indent=2));print('CANDIDATE',size,count,flush=True);raise SystemExit
 print(size,json.dumps(dict(stats)),flush=True)
print('max_search_nodes',hardest)
