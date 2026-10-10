"""B's reserved Conjecture5 discovery: original graphs, exact CSP/timeout."""
from pathlib import Path
import sys,json,random,itertools,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'triangle_packing'))
import importlib.util
spec=importlib.util.spec_from_file_location('old_packing_solver',Path(__file__).resolve().parents[1]/'triangle_packing'/'explore.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
solve=mod.solve

def expand(n,edges,lengths):
    adj=[set() for _ in range(3*n)];ports=[0]*n
    def edge(u,v):adj[u].add(v);adj[v].add(u)
    for u in range(n):
        for a,b in [(0,1),(0,2),(1,2)]:edge(3*u+a,3*u+b)
    for (u,v),L in zip(edges,lengths):
        a=3*u+ports[u];ports[u]+=1;b=3*v+ports[v];ports[v]+=1
        assert ports[u]<=3 and ports[v]<=3 and L>=2
        for _ in range(L-1):w=len(adj);adj.append(set());edge(a,w);a=w
        edge(a,b)
    for u,ns in enumerate(adj):
        assert len(ns)<=3
        if len(ns)==3:
            assert sum(len(adj[v])==3 for v in ns)<=2
            assert any(adj[v]&ns for v in ns)
    return adj

def main():
 rng=random.Random(222232026);root=Path(__file__).parent;stats={};start=time.time()
 cores=[('dipole',2,[(0,1)]*3),('K4',4,list(itertools.combinations(range(4),2))),('K33',6,[(u,v) for u in range(3) for v in range(3,6)]),('prism',6,[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]),('Petersen',10,[(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(5+i,5+(i+2)%5) for i in range(5)])]
 for name,n,edges in cores:
  patterns=[[L]*len(edges) for L in range(2,7)]
  patterns += [[rng.choice([2,3,4,5,6]) for _ in edges] for _ in range(30)]
  for lengths in patterns:
   adj=expand(n,edges,lengths);state,colors,nodes=solve(adj,(2,2,2,2,3),limit=1)
   key=name+':'+state;stats[key]=stats.get(key,0)+1
   if state=='UNSAT':
    data={'n':len(adj),'edges':[(u,v) for u,a in enumerate(adj) for v in a if u<v],'core_name':name,'core_edges':edges,'lengths':lengths,'nodes':nodes}
    (root/'candidate.json').write_text(json.dumps(data,indent=2));print('CANDIDATE',json.dumps(data),flush=True);return
  print(name,json.dumps(stats),flush=True)
 print(json.dumps({'stats':stats,'seconds':time.time()-start}),flush=True)
if __name__=='__main__':main()
