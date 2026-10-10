"""Definition-first BFS checks for SUBDIVIDED_PROOF.md; Python stdlib only."""
from collections import deque
from itertools import combinations, product
import json, platform

def word(p,q,L):
    if L==2:
        assert p!=q
        return [p,0,q]
    base=3+(L-3)%3
    e=next(x for x in (1,2,3) if x!=q)
    w={3:[p,0,4,q],4:[p,0,4,0,q],5:[p,4,0,e,0,q]}[base]
    while len(w)-1<L:
        t=w[-2]
        r=next(x for x in (1,2,3,4) if x!=q and x!=t)
        w=w[:-2]+[t,q,r,t,q]
    assert len(w)==L+1 and w[1] in (0,4) and w[-2] in (0,4)
    return w

def adjacency(n,E):
    a=[set() for _ in range(n)]
    for u,v in E:
        assert u!=v and v not in a[u]
        a[u].add(v);a[v].add(u)
    return a

def check(c,a):
    pairs=0
    for s in range(len(a)):
        d={s:0}; todo=deque([s])
        while todo:
            u=todo.popleft()
            for v in a[u]:
                if v not in d:d[v]=d[u]+1;todo.append(v)
        for v in range(s+1,len(a)):
            pairs+=1
            if c[s]==c[v] and v in d and d[v]<=(1 if c[s]==0 else 2):return False,pairs
    return True,pairs

def triangle_colors(k,connectors):
    E=[e for j in range(k) for e in combinations(range(3*j,3*j+3),2)]
    es=set(E)
    for u,v,L in connectors:
        if L==2:es.add(tuple(sorted((u,v))))
    a=adjacency(3*k,sorted(es));c=[0]*(3*k)
    def visit():
        if all(c):return True
        u=max((v for v in range(3*k) if not c[v]),key=lambda v:len({c[w] for w in a[v]}))
        for x in (1,2,3):
            if all(c[v]!=x for v in a[u]):
                c[u]=x
                if visit():return True
        c[u]=0;return False
    assert visit()
    return c,E

def assemble(k,connectors):
    ports=[v for u,v,L in connectors for v in (u,v)]
    assert len(ports)==len(set(ports))
    c,E=triangle_colors(k,connectors)
    for u,v,L in connectors:
        w=word(c[u],c[v],L); ids=[u]+list(range(len(c),len(c)+L-1))+[v]
        c+=w[1:-1];E+=list(zip(ids,ids[1:]))
    a=adjacency(len(c),E)
    assert max(map(len,a),default=0)<=3
    for neighbors in a:
        for x,y,z in combinations(neighbors,3):
            assert y in a[x] or z in a[x] or z in a[y]
    return c,a

def main():
    words=pairs=graphs=0
    for L,p,q in product(range(2,51),(1,2,3),(1,2,3)):
        if L==2 and p==q:continue
        c=word(p,q,L);a=adjacency(len(c),list(zip(range(L),range(1,L+1))))
        ok,n=check(c,a);assert ok;pairs+=n;words+=1
    # Triple parallel pair, including every combination of short lengths.
    cases=[(2,[(0,3,x),(1,4,y),(2,5,z)]) for x,y,z in product(range(2,7),repeat=3)]
    # Two looped core vertices joined by a path, plus isolated triangle.
    cases += [(3,[(0,1,x),(3,4,y),(2,5,z)]) for x,y,z in product((2,3,4,5,8,17),repeat=3)]
    # Branching K4 core, distinct port at each incidence.
    edges=[(0,3),(1,6),(2,9),(4,7),(5,10),(8,11)]
    cases += [(4,[(u,v,2+(i+shift)%9) for i,(u,v) in enumerate(edges)]) for shift in range(9)]
    # Unused ports and a long connector; two connected triangles.
    cases += [(2,[(0,3,L)]) for L in range(2,51)]
    for k,E in cases:
        c,a=assemble(k,E);ok,n=check(c,a);assert ok;pairs+=n;graphs+=1
    c,a=assemble(2,[(0,3,3)]);c[1]=c[0]
    assert not check(c,a)[0]
    print(json.dumps(dict(status='PASS',python=platform.python_version(),path_words=words,original_graphs=graphs,distance_pairs=pairs,negative_controls=1,scope='finite construction checks; unbounded theorem uses written induction and Brooks'),sort_keys=True))
if __name__=='__main__':main()
