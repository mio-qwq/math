"""Branching triangle networks with admissible direct two-port interfaces."""
import importlib.util,itertools,json,random
from pathlib import Path
from collections import Counter
s=importlib.util.spec_from_file_location('frozen_csp',Path(__file__).resolve().parents[1]/'triangle_packing'/'explore.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def expand(n,es,specs):
 a=[set() for _ in range(3*n)];use=[0]*n
 def edge(u,v):assert u!=v and v not in a[u];a[u].add(v);a[v].add(u)
 def triangle():
  b=len(a);a.extend([set() for _ in range(3)])
  for x,y in [(0,1),(0,2),(1,2)]:edge(b+x,b+y)
  return b
 def path(u,v,L):
  for _ in range(L-1):w=len(a);a.append(set());edge(u,w);u=w
  edge(u,v)
 for i in range(n):
  for x,y in [(0,1),(0,2),(1,2)]:edge(3*i+x,3*i+y)
 for (u,v),(r,L) in zip(es,specs):
  x=3*u+use[u];use[u]+=1;y=3*v+use[v];use[v]+=1
  if r==0:path(x,y,L);continue
  for i in range(r):
   b=triangle();path(x,b,2 if i==0 else 1);x=b+1
  path(x,y,2)
 assert all(len(ns)<=3 and (len(ns)!=3 or (sum(len(a[v])==3 for v in ns)<=2 and any(a[v]&ns for v in ns))) for ns in a)
 return a
if __name__=='__main__':
 r=random.Random(222230825);stats=Counter();worst=0
 cores=[('dipole',2,[(0,1)]*3),('K4',4,list(itertools.combinations(range(4),2))),('K33',6,[(u,v) for u in range(3) for v in range(3,6)]),('prism',6,[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]),('Petersen',10,[(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)])]
 for name,n,es in cores:
  for rep in range(40):
   specs=[(r.choice([0,0,2,3,4]),r.choice([2,3,4])) for _ in es]
   a=expand(n,es,specs);state,c,nodes=m.solve(a,(2,2,2,2,3),limit=1);stats[state]+=1;worst=max(worst,nodes)
   if state=='UNSAT':
    data={'n':len(a),'edges':[(u,v) for u,ns in enumerate(a) for v in sorted(ns) if u<v],'core':name,'specs':specs,'nodes':nodes}
    Path(__file__).with_name('dense_candidate.json').write_text(json.dumps(data,indent=2)+'\n');print('CANDIDATE',json.dumps(data),flush=True);raise SystemExit
  print(json.dumps({'core':name,'stats':dict(stats),'worst_nodes':worst}),flush=True)
