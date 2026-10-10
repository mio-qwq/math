"""Independent generic core/connector probes for the original August Problem1."""
from pathlib import Path
import importlib.util,random,json,itertools,time
from collections import deque,Counter
root=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('frozen_csp',root/'triangle_packing'/'explore.py');mod=importlib.util.module_from_spec(s);s.loader.exec_module(mod)
def core(n,rng):
 for _ in range(10000):
  stubs=[u for u in range(n) for _ in range(3)];rng.shuffle(stubs);es=[tuple(sorted(stubs[i:i+2])) for i in range(0,len(stubs),2)]
  if any(u==v for u,v in es):continue
  reached={0}
  while True:
   new=reached|{v for u,v in es if u in reached}|{u for u,v in es if v in reached}
   if new==reached:break
   reached=new
  if len(reached)==n:return sorted(es)
 raise RuntimeError('rejection exhausted')
def expand(n,es,lens):
 a=[set() for _ in range(3*n)];used=[0]*n
 def edge(u,v):assert u!=v and v not in a[u];a[u].add(v);a[v].add(u)
 for i in range(n):
  for u,v in [(0,1),(0,2),(1,2)]:edge(3*i+u,3*i+v)
 for (u,v),L in zip(es,lens):
  x=3*u+used[u];used[u]+=1;y=3*v+used[v];used[v]+=1
  for _ in range(L-1):w=len(a);a.append(set());edge(x,w);x=w
  edge(x,y)
 assert all(len(ns)<=3 and (len(ns)!=3 or any(a[v]&ns for v in ns)) for ns in a)
 return a
rng=random.Random(113342026);stats=Counter();start=time.time();worst=(0,None)
for mode in ['direct','subdivision','edge_sum']:
 for n in ([2,4,6,8,10,12] if mode!='edge_sum' else [8]):
  for rep in range(20):
   if mode=='edge_sum':
    es=[e for e in itertools.combinations(range(4),2) if e!=(0,1)]+[e for e in itertools.combinations(range(4,8),2) if e!=(4,5)]+[(0,4),(1,5)]
   else:es=core(n,rng)
   lens=[1]*len(es)
   if mode=='subdivision' or (mode=='edge_sum' and rep>0):
    lens=[rng.choice([1,1,1,2,3]) for e in es]
   if n==4 and len(set(es))==6 and all(L==1 for L in lens):stats['excluded_H']+=1;continue
   a=expand(n,es,lens);state,c,nodes=mod.solve(a,(1,1,3,3,4),limit=0.5);stats[mode+':'+state]+=1
   if nodes>worst[0]:worst=(nodes,{'mode':mode,'n':len(a),'core_order':n,'edges':es,'lengths':lens,'state':state})
   if state=='UNSAT':
    data={'n':len(a),'edges':[(u,v) for u,ns in enumerate(a) for v in ns if u<v],'core_order':n,'core_edges':es,'lengths':lens,'nodes':nodes}
    Path(__file__).with_name('candidate.json').write_text(json.dumps(data,indent=2));print('CANDIDATE',json.dumps(data),flush=True);raise SystemExit
  print(mode,n,json.dumps(dict(stats)),flush=True)
print(json.dumps({'stats':dict(stats),'worst':worst,'seconds':time.time()-start}),flush=True)
