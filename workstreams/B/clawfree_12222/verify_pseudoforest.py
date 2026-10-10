"""Original-distance checker for the pseudoforest construction; no imports from B discovery."""
from itertools import combinations,product
from collections import deque
import json,platform

def run(n,E,L):
    adj=[set() for _ in range(3*n)];ports=[0]*n;end=[];weak=set()
    def edge(u,v):adj[u].add(v);adj[v].add(u)
    for j in range(n):
        for u,v in combinations(range(3*j,3*j+3),2):edge(u,v)
    for (u,v),l in zip(E,L):
        a=3*u+ports[u];ports[u]+=1;b=3*v+ports[v];ports[v]+=1;end.append((a,b))
        if l==1:edge(a,b)
        else:
            w=len(adj);adj.append(set());edge(a,w);edge(w,b);weak.add(w)
    direct={i for i,l in enumerate(L) if l==1};inc=[set() for _ in range(n)]
    for i in direct:
        for v in E[i]:inc[v].add(i)
    # Check pseudoforest condition before orienting, retaining parallel edge IDs.
    seen=set()
    for s in range(n):
        if s in seen:continue
        vs={s};es=set();q=[s];seen.add(s)
        while q:
            u=q.pop()
            for i in inc[u]:
                es.add(i)
                for v in E[i]:
                    if v not in seen:seen.add(v);vs.add(v);q.append(v)
        if len(es)>len(vs):return None
    chosen={}
    leaves=deque(v for v in range(n) if len(inc[v])<=1)
    while leaves:
        u=leaves.popleft()
        if not inc[u]:continue
        i=next(iter(inc[u]));v=E[i][0] if E[i][1]==u else E[i][1]
        chosen[i]=u;inc[u].remove(i);inc[v].remove(i)
        if len(inc[v])<=1:leaves.append(v)
    while any(inc):
        u=next(v for v in range(n) if inc[v]);start=u
        while inc[u]:
            i=min(inc[u]);v=E[i][0] if E[i][1]==u else E[i][1]
            chosen[i]=u;inc[u].remove(i);inc[v].remove(i);u=v
    assert set(chosen)==direct
    assert len(set(chosen.values()))==len(chosen)
    for i,u in chosen.items():weak.add(end[i][0 if E[i][0]==u else 1])
    assert all(not(adj[u]&weak) for u in weak)
    D=[]
    for s in range(len(adj)):
        d={s:0};q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in d:d[v]=d[u]+1;q.append(v)
        D.append(d)
    positive=set(range(len(adj)))-weak
    F={u:{v for v in positive-{u} if D[u].get(v,10**6)<=2} for u in positive}
    assert max(map(len,F.values()),default=0)<=4
    seen=set()
    for s in positive:
        if s in seen:continue
        comp={s};q=[s];seen.add(s)
        while q:
            for v in F[q.pop()]:
                if v not in seen:seen.add(v);comp.add(v);q.append(v)
        assert any(len(F[v])<=3 for v in comp)
    color={u:0 for u in weak}
    def dfs():
        if len(color)==len(adj):return True
        u=max(positive-color.keys(),key=lambda v:(len({color[w] for w in F[v] if w in color}),len(F[v])))
        for c in (1,2,3,4):
            if all(color.get(v)!=c for v in F[u]):
                color[u]=c
                if dfs():return True
                del color[u]
        return False
    assert dfs()
    def valid():
        return all(color[u]!=color[v] or D[u].get(v,10**6)>(1 if color[u]==0 else 2) for u,v in combinations(range(len(adj)),2))
    assert valid()
    # Deliberate adjacent equal-color corruption on original triangle edge.
    color[1]=color[0];assert not valid()
    return len(adj)*(len(adj)-1)//2

def main():
    cores=[('dipole',2,[(0,1)]*3),('K4',4,list(combinations(range(4),2))),('K33',6,[(u,v) for u in range(3) for v in range(3,6)]),('binary_tree',7,[(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)])]
    stats={};pairs=total=skipped=0
    for name,n,E in cores:
        ok=skip=0
        for L in product((1,2),repeat=len(E)):
            result=run(n,E,L)
            if result is None:skip+=1;skipped+=1
            else:ok+=1;total+=1;pairs+=result
        stats[name]=dict(verified=ok,outside_hypothesis=skip)
    print(json.dumps(dict(status='PASS',python=platform.python_version(),families=stats,graphs=total,distance_pairs=pairs,negative_controls=total,outside_hypothesis=skipped,scope='finite 1/2 models; long extension is proved in writing'),sort_keys=True))
if __name__=='__main__':main()
