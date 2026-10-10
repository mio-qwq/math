"""Reserved original Conjecture4 bounded discovery with exact CSP."""
from pathlib import Path
import importlib.util,random,json,time
from collections import Counter
root=Path(__file__).resolve().parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
solver=load('frozen_solver',root/'triangle_packing'/'explore.py')
old=load('old_112',root/'two_saturated_112'/'search.py')
def cubic(n,rng):
 for _ in range(10000):
  stubs=[u for u in range(n) for _ in range(3)];rng.shuffle(stubs)
  es=[tuple(sorted(stubs[i:i+2])) for i in range(0,len(stubs),2)]
  if any(u==v for u,v in es) or len(set(es))!=len(es):continue
  return sorted(es)
 raise RuntimeError('configuration retry limit')
def main():
 rng=random.Random(122222026);stats=Counter();start=time.time();hardest=(0,None)
 for mode in ['matching','starcover','parity','generalcore']:
  for n in [4,6,8,10,12,16,20,24,30,40]:
   for rep in range(30):
    edges=cubic(n,rng) if mode=='generalcore' else old.random_core(n,rng)
    if mode=='matching':sub={i:1 for i in range(n,len(edges))}
    else:
     sub={};uncovered=set(range(n));order=list(range(len(edges)));rng.shuffle(order)
     for i in order:
      u,v=edges[i]
      if u in uncovered or v in uncovered:
       sub[i]=rng.choice([1,2,3]) if mode=='parity' else 1
       uncovered.discard(u);uncovered.discard(v)
    a=old.graph(n,edges,sub);state,c,nodes=solver.solve(a,(1,2,2,2,2),limit=0.5)
    stats[mode+':'+state]+=1
    if nodes>hardest[0]:hardest=(nodes,{'mode':mode,'core_order':n,'edges':edges,'sub':sub,'state':state})
    if state=='UNSAT':
     Path(__file__).with_name('candidate.json').write_text(json.dumps({'n':len(a),'edges':[(u,v) for u,ns in enumerate(a) for v in ns if u<v],'source':hardest},indent=2));print('CANDIDATE',mode,n,nodes,flush=True);return
  print(mode,json.dumps(dict(stats)),flush=True)
 print(json.dumps({'stats':dict(stats),'hardest':hardest,'seconds':time.time()-start}),flush=True)
if __name__=='__main__':main()
