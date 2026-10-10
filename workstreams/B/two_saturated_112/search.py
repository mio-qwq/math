"""Exact odd-cycle branching; discovery only, independent verification required."""
import json,random,time
from collections import deque
from pathlib import Path

def odd_cycle(adj,removed):
    color={}; parent={}
    for root in range(len(adj)):
        if removed>>root&1 or root in color: continue
        color[root]=0; parent[root]=None; q=deque([root])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if removed>>v&1: continue
                if v not in color:
                    color[v]=color[u]^1; parent[v]=u;q.append(v)
                elif color[v]==color[u]:
                    a=[];x=u
                    while x is not None:a.append(x);x=parent[x]
                    b=[];x=v
                    while x not in a:b.append(x);x=parent[x]
                    return a[:a.index(x)+1]+b[::-1]
    return None

def solve(adj,limit=1000000):
    balls=[]
    for u in range(len(adj)):
        s={u}|adj[u]
        for v in adj[u]:s|=adj[v]
        balls.append(sum(1<<v for v in s))
    nodes=0
    def rec(selected,blocked):
        nonlocal nodes
        nodes+=1
        if nodes>limit:raise TimeoutError
        cyc=odd_cycle(adj,selected)
        if cyc is None:return selected
        choices=[v for v in cyc if not blocked>>v&1]
        for v in choices:
            ans=rec(selected|1<<v,blocked|balls[v])
            if ans is not None:return ans
        return None
    try:return rec(0,0),nodes
    except TimeoutError:return 'UNKNOWN',nodes

def graph(n,edges,sub):
    adj=[set() for _ in range(n)]
    for i,(u,v) in enumerate(edges):
        last=u
        for _ in range(sub.get(i,0)):
            w=len(adj);adj.append({last});adj[last].add(w);last=w
        adj[last].add(v);adj[v].add(last)
    assert all(len(a)<=3 for a in adj)
    assert all(sum(len(adj[v])==3 for v in a)<=2 for a in adj if len(a)==3)
    return adj

def random_core(n,rng):
    # Cycle plus a disjoint perfect matching, hence simple cubic and connected.
    edges={(i,(i+1)%n) if i<(i+1)%n else ((i+1)%n,i) for i in range(n)}
    for _ in range(10000):
        vs=list(range(n));rng.shuffle(vs)
        matching=[tuple(sorted(vs[i:i+2])) for i in range(0,n,2)]
        if all(e not in edges for e in matching):return sorted(edges)+matching
    raise RuntimeError('matching rejection')

def run():
    rng=random.Random(1122026); totals={};worst=(0,None);start=time.time()
    for mode in ['matching','edgecover','parity']:
        count=0
        for n in [4,6,8,10,12,16,20,24,30,40]:
            for rep in range(100):
                edges=random_core(n,rng)
                if mode=='matching': sub={i:1 for i in range(n,len(edges))}
                else:
                    uncovered=set(range(n));sub={}
                    order=list(range(len(edges)));rng.shuffle(order)
                    for i in order:
                        u,v=edges[i]
                        if u in uncovered or v in uncovered:
                            sub[i]=rng.choice([1,2,3]) if mode=='parity' else 1
                            uncovered.discard(u);uncovered.discard(v)
                adj=graph(n,edges,sub);ans,nodes=solve(adj)
                count+=1
                if nodes>worst[0]:worst=(nodes,{'mode':mode,'core_order':n,'edges':edges,'sub':sub})
                if ans is None:
                    Path(__file__).with_name('candidate.json').write_text(json.dumps({'n':len(adj),'edges':[(u,v) for u,a in enumerate(adj) for v in a if u<v],'core':edges,'sub':sub},indent=2));print('UNSAT',mode,n,nodes,flush=True);return
                if ans=='UNKNOWN': print('UNKNOWN',mode,n,flush=True);continue
                chosen=[u for u in range(len(adj)) if ans>>u&1]
                assert odd_cycle(adj,ans) is None
                assert all(v not in adj[u] and not(adj[u]&adj[v]) for i,u in enumerate(chosen) for v in chosen[i+1:])
        totals[mode]=count;print(mode,count,'SAT/finished','worst',worst[0],flush=True)
    print(json.dumps({'tested':totals,'worst':worst,'seconds':time.time()-start}),flush=True)
if __name__=='__main__':run()
