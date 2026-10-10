"""New admissible dense-interface mechanism: two-port triangles, direct joins."""
import importlib.util,itertools,json,time
from pathlib import Path
from collections import Counter
s=importlib.util.spec_from_file_location('frozen_csp',Path(__file__).resolve().parents[1]/'triangle_packing'/'explore.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def graph(lengths):
 k=len(lengths);a=[set() for _ in range(3*k)]
 def edge(u,v):assert u!=v and v not in a[u];a[u].add(v);a[v].add(u)
 for i in range(k):
  for x,y in [(0,1),(1,2),(0,2)]:edge(3*i+x,3*i+y)
 for i,L in enumerate(lengths):
  u=3*i+1;v=3*((i+1)%k)
  for _ in range(L-1):w=len(a);a.append(set());edge(u,w);u=w
  edge(u,v)
 assert all(len(ns)<=3 and (len(ns)!=3 or (sum(len(a[v])==3 for v in ns)<=2 and any(a[v]&ns for v in ns))) for ns in a)
 return a
if __name__=='__main__':
 stats=Counter()
 for k in range(3,13):
  words={(1,)*k,(2,)*k,(1,2)*(k//2)+(1,)*(k%2)}
  if k<=7:words.update(itertools.product([1,2],repeat=k))
  for lens in sorted(words):
   a=graph(lens);state,c,nodes=m.solve(a,(2,2,2,2,3),limit=1);stats[state]+=1
   if state=='UNSAT':
    data={'n':len(a),'edges':[(u,v) for u,ns in enumerate(a) for v in sorted(ns) if u<v],'connector_lengths':lens,'nodes':nodes}
    Path(__file__).with_name('direct_candidate.json').write_text(json.dumps(data,indent=2)+'\n');print('CANDIDATE',json.dumps(data),flush=True);raise SystemExit
  print(json.dumps({'k':k,'stats':dict(stats)}),flush=True)
