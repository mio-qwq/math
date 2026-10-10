"""New route: independent I with maximum degree(G^2[V-I])<=4.
Numerical integer solver discovers witnesses/obstructions only, never certifies UNSAT.
"""
from itertools import combinations
from collections import deque,Counter
from pathlib import Path
import json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint

def matchings(n,E):
    adj=[set() for _ in range(n)]
    for u,v in E:adj[u].add(v);adj[v].add(u)
    def go(rem,chosen):
        if not rem:yield chosen;return
        u=min(rem)
        for v in sorted(adj[u]&rem):yield from go(rem-{u,v},chosen+[(u,v)])
    yield from go(set(range(n)),[])

def build(n,E,M):
    a=[set() for _ in range(n)];M={tuple(sorted(e)) for e in M}
    def edge(u,v):a[u].add(v);a[v].add(u)
    for u,v in E:
        if tuple(sorted((u,v))) in M:
            w=len(a);a.append(set());edge(u,w);edge(w,v)
        else:edge(u,v)
    assert all(len(s)<=3 and (len(s)!=3 or sum(len(a[v])==3 for v in s)<=2) for s in a)
    return a

def search(a):
    n=len(a);near=[]
    for u in range(n):near.append((a[u]|set().union(*(a[v] for v in a[u])))-{u})
    rows=[];lo=[];hi=[]
    for u in range(n):
        for v in a[u]:
            if u<v:
                r=np.zeros(n);r[u]=r[v]=1;rows.append(r);lo.append(-np.inf);hi.append(1)
    for u,ns in enumerate(near):
        need=max(0,len(ns)-4);r=np.zeros(n)
        for v in ns:r[v]=1
        r[u]=need;rows.append(r);lo.append(need);hi.append(np.inf)
    r=milp(-np.ones(n),integrality=np.ones(n),bounds=Bounds(0,1),constraints=LinearConstraint(np.array(rows),lo,hi),options={'time_limit':2})
    I=None if r.x is None else [u for u,x in enumerate(r.x) if x>.5]
    if I is not None:
        S=set(I);assert all(not(a[u]&S) for u in S)
        assert all(len(ns-S)<=4 for u,ns in enumerate(near) if u not in S)
    return int(r.status),I

def main():
    cube=[(u,v) for u in range(8) for v in range(u+1,8) if (u^v).bit_count()==1]
    wagner=[tuple(sorted((i,(i+1)%8))) for i in range(8)]+[(i,i+4) for i in range(4)]
    pet=[tuple(sorted((i,(i+1)%5))) for i in range(5)]+[(i,i+5) for i in range(5)]+[tuple(sorted((i+5,(i+2)%5+5))) for i in range(5)]
    cores=[('K4',4,list(combinations(range(4),2))),('K33',6,[(u,v) for u in range(3) for v in range(3,6)]),('cube',8,cube),('Wagner',8,wagner),('Petersen',10,pet)]
    stats=Counter()
    for name,n,E in cores:
        for M in matchings(n,E):
            a=build(n,E,M);status,I=search(a);stats[name+':'+str(status)]+=1
            if I is None:
                out=dict(core=name,vertices=len(a),edges=[(u,v) for u,ns in enumerate(a) for v in ns if u<v],matching=M,solver_status=status,scope='restricted max-degree-four route; original coloring not decided')
                print(json.dumps(out),flush=True)
                Path(__file__).with_name('brooks_route_probe.json').write_text(json.dumps(out,indent=2)+'\n')
                print(json.dumps(dict(stats)),flush=True);return
    print(json.dumps(dict(stats)),flush=True)
if __name__=='__main__':main()
