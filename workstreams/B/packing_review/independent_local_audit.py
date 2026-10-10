#!/usr/bin/env python3
"""Independent exact BFS audit of proposed tile/cap rules. Stdlib only.
Written from the mathematical sketch, without reading discovery code.
This is finite validation, not a replacement for the universal proof.
"""
from collections import deque, Counter
from itertools import product, combinations
import json

T = {4: (1,3,1,2,1), 5:(1,3,1,4,2,1),
     6:(1,3,1,4,1,2,1), 7:(1,3,1,2,1,4,2,1)}

def word(lengths):
    w = [1]; boundaries=[0]
    for k in lengths:
        w.extend(T[k][1:]); boundaries.append(len(w)-1)
    return w,boundaries

class Graph:
    def __init__(self): self.a={}; self.c={}
    def vertex(self,v,c): self.a[v]=set(); self.c[v]=c
    def edge(self,u,v):
        assert u != v
        self.a[u].add(v); self.a[v].add(u)
    def remove(self,v):
        for u in self.a[v]: self.a[u].remove(v)
        del self.a[v]; del self.c[v]
    def duplicate(self,v):
        d=('twin',v); self.vertex(d,self.c[v])
        for u in self.a[v].copy(): self.edge(u,d)
    def bad(self):
        for s in self.a:
            ds={s:0}; q=deque([s])
            while q:
                u=q.popleft()
                for v in self.a[u]:
                    if v not in ds: ds[v]=ds[u]+1; q.append(v)
            for v,d in ds.items():
                if s!=v and self.c[s]==self.c[v] and d<=self.c[s]:
                    return (s,v,self.c[s],d)
        return None

def build(lengths,marks,cyclic=False,caps=('square','square'),bad_right=False):
    w,bs=word(lengths); n=len(w)-1
    g=Graph()
    if cyclic:
        for i,c in enumerate(w[:-1]): g.vertex(i,c)
        for i in range(n): g.edge(i,(i+1)%n)
        for i in marks: g.duplicate(bs[i]%n)
    else:
        for i,c in enumerate(w): g.vertex(i,c)
        for i in range(n): g.edge(i,i+1)
        g.vertex(-1,2); g.edge(-1,0)
        g.vertex(n+1,3); g.edge(n,n+1)
        for i in marks: g.duplicate(bs[i])
        if caps[0]=='triangle':
            g.remove(-1); g.remove(('twin',0)); g.vertex('left',2)
            g.edge('left',0); g.edge('left',1)
        if caps[1]=='triangle':
            g.remove(n+1); g.remove(('twin',n))
            h=3 if bad_right else (4 if lengths[-1]==4 else 3)
            g.vertex('right',h); g.edge('right',n); g.edge('right',n-1)
    return g

def audit():
    stats=Counter(); failures=[]
    # Every one/two/three-tile sequence, with arbitrary actual-square selection.
    # An unselected tile boundary is only an auxiliary 1, not a graph square.
    for count in (1,2,3):
        for seq in product(T,repeat=count):
            for mask in range(1<<(count-1)):
                marks=[0,count]+[i+1 for i in range(count-1) if mask>>i&1]
                for caps in product(('square','triangle'),repeat=2):
                    g=build(seq,marks,caps=caps); bad=g.bad(); stats['capped_chains']+=1
                    if bad: failures.append((seq,marks,caps,bad))
            for mask in range(1<<(count-1)):
                marks=[0]+[i+1 for i in range(count-1) if mask>>i&1]
                g=build(seq,marks,cyclic=True); bad=g.bad(); stats['necklaces']+=1
                if bad: failures.append((seq,marks,'cycle',bad))
    # Universal join constraints only require two adjacent tiles: maximum radius4,
    # elementary tile length >=4; a radius4 pair cannot span a full intervening tile.
    for seq in product(T, repeat=2):
        w,_=word(seq); g=Graph()
        for i,c in enumerate(w): g.vertex(i,c)
        for i in range(len(w)-1): g.edge(i,i+1)
        assert g.bad() is None; stats['two_tile_linear_joins']+=1
    # Negative controls exercise the distance threshold and the special cap choice.
    g=build((4,),[0,1],caps=('triangle','triangle'),bad_right=True)
    assert g.bad() is not None; stats['negative_controls']+=1
    g=build((4,),[0],cyclic=True)
    g.c[('twin',0)]=3
    assert g.bad() is not None; stats['negative_controls']+=1
    # Known K2,3 coloring: degree2 class1; two degree3 vertices2,3.
    g=Graph()
    for v,c in enumerate((2,3,1,1,1)): g.vertex(v,c)
    for u in (0,1):
        for v in (2,3,4): g.edge(u,v)
    assert g.bad() is None; stats['K23']+=1
    print(json.dumps({'counts':dict(stats),'failures':failures},indent=2))
    assert not failures
if __name__=='__main__': audit()

# Independent overlap classification: glue every pair of distinct 3/4-cycles
# along every nonempty vertex intersection; keep precisely subcubic graphs whose
# degree3 vertices are independent. Extra graph edges could only increase degrees.
def overlap_audit():
    from itertools import permutations
    admitted=set(); tested=set(); retained=0
    for p,q in product((3,4),repeat=2):
        e1=frozenset(tuple(sorted((i,(i+1)%p))) for i in range(p))
        for new in range(q):
            n=p+new
            for cyc in permutations(range(n),q):
                if not set(range(p,n)).issubset(cyc): continue
                e2=frozenset(tuple(sorted((cyc[i],cyc[(i+1)%q]))) for i in range(q))
                if e1==e2: continue
                edges=e1|e2
                sig=(n,edges)
                if sig in tested: continue
                tested.add(sig)
                adj=[set() for _ in range(n)]
                for u,v in edges: adj[u].add(v); adj[v].add(u)
                if max(map(len,adj))>3: continue
                if any(len(adj[u])==len(adj[v])==3 for u,v in edges): continue
                retained+=1
                # Certify actual K2,3, not merely the degree sequence.
                a={u for u in range(n) if len(adj[u])==3}
                b=set(range(n))-a
                assert n==5 and len(a)==2 and len(b)==3
                assert all(adj[u]==b for u in a) and all(adj[v]==a for v in b)
                admitted.add((n,len(edges),tuple(sorted(map(len,adj)))))
    print(json.dumps({'overlap_union_graphs_checked':len(tested),
                      'admitted_labeled_unions':retained,
                      'admitted_signatures':list(admitted)},indent=2))
if __name__=='__main__': overlap_audit()
