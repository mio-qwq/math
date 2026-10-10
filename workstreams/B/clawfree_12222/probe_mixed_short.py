"""Test an explicitly restricted weak-color placement in mixed 1/2 connectors.
All forced weak colors are propagated initially. Timeouts are UNKNOWN.
"""
from itertools import combinations,product
from collections import deque,Counter
from pathlib import Path
import json,time

def build(n,E,L):
    a=[set() for _ in range(3*n)];used=[0]*n;forced=[]
    def edge(u,v):a[u].add(v);a[v].add(u)
    for i in range(n):
        for u,v in combinations(range(3*i,3*i+3),2):edge(u,v)
    for (u,v),l in zip(E,L):
        x=3*u+used[u];used[u]+=1;y=3*v+used[v];used[v]+=1
        if l==2:
            z=len(a);a.append(set());edge(x,z);edge(z,y);forced.append(z)
        else:assert l==1;edge(x,y)
    return a,forced

def solve(a,forced,limit=1):
    n=len(a);radii=(1,2,2,2,2);D=[]
    for s in range(n):
        d=[n+1]*n;d[s]=0;q=deque([s])
        while q:
            u=q.popleft()
            for v in a[u]:
                if d[v]==n+1:d[v]=d[u]+1;q.append(v)
        D.append(d)
    F=[[[v for v in range(n) if 0<D[u][v]<=r] for r in radii] for u in range(n)]
    deadline=time.monotonic()+limit;nodes=0
    def propagate(ds,q):
        while q:
            u=q.pop();b=ds[u];c=b.bit_length()-1
            for v in F[u][c]:
                if ds[v]&b:
                    ds[v]^=b
                    if not ds[v]:return False
                    if ds[v].bit_count()==1:q.append(v)
        return True
    def rec(ds):
        nonlocal nodes
        nodes+=1
        if nodes%256==0 and time.monotonic()>deadline:raise TimeoutError
        free=[v for v in range(n) if ds[v].bit_count()>1]
        if not free:return [x.bit_length()-1 for x in ds]
        u=min(free,key=lambda v:(ds[v].bit_count(),-len(F[v][1])))
        for c in range(5):
            if not ds[u]>>c&1:continue
            nd=ds[:];nd[u]=1<<c
            if propagate(nd,[u]):
                ans=rec(nd)
                if ans is not None:return ans
        return None
    ds=[1 if v in forced else 31 for v in range(n)]
    try:ans=rec(ds) if propagate(ds,list(forced)) else None
    except TimeoutError:return 'UNKNOWN',None,nodes
    if ans is not None:
        assert all(ans[u]!=ans[v] or D[u][v]>radii[ans[u]] for u in range(n) for v in range(u))
    return ('SAT' if ans is not None else 'UNSAT'),ans,nodes

def main():
    cores=[('dipole',2,[(0,1)]*3),('K4',4,list(combinations(range(4),2))),('K33',6,[(u,v) for u in range(3) for v in range(3,6)])]
    allstats={}
    for name,n,E in cores:
        stats=Counter()
        for L in product((1,2),repeat=len(E)):
            if min(L)==max(L):continue
            a,f=build(n,E,L);st,c,nodes=solve(a,f);stats[st]+=1
            if st=='UNSAT':
                orig,col,onodes=solve(a,[],3)
                out=dict(core_name=name,core_vertices=n,core_edges=E,lengths=L,restricted=st,restricted_nodes=nodes,original=orig,original_nodes=onodes,original_coloring=col,forced_weak_vertices=f)
                Path(__file__).with_name('mixed_short_obstacle.json').write_text(json.dumps(out,indent=2)+'\n')
                print(json.dumps(out),flush=True);allstats[name]=dict(stats)
                print(json.dumps(dict(stats=allstats,scope='restricted all-length2-interiors-weak rule only')),flush=True);return
        allstats[name]=dict(stats)
        print(json.dumps(dict(core=name,stats=dict(stats))),flush=True)
    print(json.dumps(dict(stats=allstats,scope='restricted all-length2-interiors-weak rule only')),flush=True)
if __name__=='__main__':main()
