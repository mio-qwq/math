"""Original Conjecture6 search with genuinely heavy but independent vertices."""
from pathlib import Path
import importlib.util,random,json
from collections import Counter
root=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('oct_solver',root/'two_saturated_112'/'search.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
def expand(n,edges,special,lengths,diamond=False):
 a=[set() for _ in range(3*n)];ports=[0]*n
 def edge(u,v):a[u].add(v);a[v].add(u)
 def path(u,v,L):
  for _ in range(L-1):w=len(a);a.append(set());edge(u,w);u=w
  edge(u,v)
 for i in range(n):
  for x,y in [(0,1),(0,2),(1,2)]:edge(3*i+x,3*i+y)
 for i,(u,v) in enumerate(edges):
  x=3*u+ports[u];ports[u]+=1;y=3*v+ports[v];ports[v]+=1
  if i in special:
   p=len(a);a.extend([set() for _ in range(3)])
   for s,t in [(0,1),(0,2),(1,2)]:edge(p+s,p+t)
   edge(x,p);edge(p+1,y)
  else:path(x,y,lengths[i])
 heavy={u for u,ns in enumerate(a) if len(ns)==3 and all(len(a[v])==3 for v in ns)}
 assert heavy
 assert all(not(a[u]&heavy) for u in heavy)
 assert all(len(ns)<=3 and (len(ns)!=3 or any(a[v]&ns for v in ns)) for ns in a)
 return a
rng=random.Random(301122026);stats=Counter()
for mode in ['short','parity','sparseheavy']:
 for n in [4,6,8,10,12,16,20,30]:
  for rep in range(30):
   es=old.random_core(n,rng);special=set(range(n,len(es)))
   if mode=='sparseheavy':special={i for i in special if rng.random()<0.5} or {n}
   lengths=[rng.choice([2,3]) if mode=='short' else rng.randrange(2,8) for _ in es]
   a=expand(n,es,special,lengths);ans,nodes=old.solve(a,limit=100000)
   state='UNKNOWN' if ans=='UNKNOWN' else 'UNSAT' if ans is None else 'SAT';stats[mode+':'+state]+=1
   if state=='UNSAT':
    Path(__file__).with_name('candidate.json').write_text(json.dumps({'n':len(a),'edges':[(u,v) for u,ns in enumerate(a) for v in ns if u<v],'core':es,'special':sorted(special),'lengths':lengths,'nodes':nodes},indent=2));print('CANDIDATE',mode,n,len(a),nodes,flush=True);raise SystemExit
  print(mode,n,json.dumps(dict(stats)),flush=True)
print('FINAL',json.dumps(dict(stats)),flush=True)
