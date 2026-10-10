"""Distinct boundary mechanism: diamond caps and triangle networks with leaves."""
import importlib.util,json,random
from pathlib import Path
spec=importlib.util.spec_from_file_location('new_exp',Path(__file__).with_name('explore.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from collections import Counter
rng=random.Random(523);stats=Counter()
def valid(a):
 return all(len(ns)<=3 and (len(ns)!=3 or (sum(len(a[v])==3 for v in ns)<=2 and any(a[v]&ns for v in ns))) for ns in a)
for cap in ['diamond','leaf']:
 for L in range(1,10):
  for chain in range(1,7):
   a=[set() for _ in range(3*chain)]
   def edge(u,v):a[u].add(v);a[v].add(u)
   def path(u,v,L):
    for _ in range(L-1):w=len(a);a.append(set());edge(u,w);u=w
    edge(u,v)
   for i in range(chain):
    for x,y in [(0,1),(1,2),(0,2)]:edge(3*i+x,3*i+y)
   for i in range(chain-1):path(3*i+2,3*(i+1),rng.randrange(2,6))
   used={3*i+2 for i in range(chain-1)}|{3*i for i in range(1,chain)}
   for u in range(3*chain):
    if u in used:continue
    if cap=='leaf':v=len(a);a.append(set());path(u,v,L)
    else:
     v=len(a);a.extend([set() for _ in range(4)])
     for x,y in [(0,1),(0,2),(1,2),(1,3),(2,3)]:edge(v+x,v+y)
     path(u,v,max(2,L))
   assert valid(a)
   state,c,n=m.solve(a,(2,2,2,2,3),limit=1);stats[cap+':'+state]+=1
   if state=='UNSAT':
    Path(__file__).with_name('candidate.json').write_text(json.dumps({'n':len(a),'edges':[(u,v) for u,ns in enumerate(a) for v in ns if u<v]},indent=2));print('CANDIDATE',cap,L,chain,flush=True);raise SystemExit
print(json.dumps(dict(stats)))
