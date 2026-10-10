"""Independent certificate checker: rebuild old/new graphs and all BFS distances.
No imports from discovery, construction, or other B checkers.
"""
import json,platform
from pathlib import Path
from itertools import product,combinations,permutations
from collections import deque

def graph(L):
    edges=[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)]
    path=[0]+list(range(6,6+L-1))+[3]
    edges+=list(zip(path,path[1:]))
    a=[set() for _ in range(6+L-1)]
    for u,v in edges:a[u].add(v);a[v].add(u)
    d=[]
    for s in range(len(a)):
        dist={s:0};q=deque([s])
        while q:
            u=q.popleft()
            for v in a[u]:
                if v not in dist:dist[v]=dist[u]+1;q.append(v)
        d.append(dist)
    return d,path

def valid(c,d):
    return all(c[u]!=c[v] or d[u][v]>(1 if c[u]==0 else 2) for u,v in combinations(range(len(c)),2))

def norm(c):
    seen=[]
    for x in c:
        if x and x not in seen:seen.append(x)
    return tuple(0 if x==0 else seen.index(x)+1 for x in c)

def main():
    old,_=graph(1)
    allowed={c for c in product(range(5),repeat=6) if valid(c,old)}
    reps={norm(c) for c in allowed}
    data=json.loads(Path(__file__).with_name('subdivision_certificate.json').read_text())
    assert {tuple(r['boundary']) for r in data}==reps
    assert len(data)==len(reps)
    count=pairs=0
    for row in data:
        base=row['boundary']
        for L in (4,5,6):
            w=row['words'][str(L)]
            assert len(w)==L+1 and w[0]==base[0] and w[-1]==base[3]
            d,path=graph(L)
            c=base+w[1:-1]
            assert valid(c,d)
            pairs+=len(c)*(len(c)-1)//2;count+=1
    # Verify all generic suffix-extension choices on arbitrary two-letter prefixes.
    transitions=0
    for a,b,t,q,r in product(range(5),repeat=5):
        if r==0 or r==t or r==q:continue
        oldword=[a,b,t,q]
        def pathvalid(w):
            return all(w[i]!=w[j] or j-i>(1 if w[i]==0 else 2) for i,j in combinations(range(len(w)),2))
        if not pathvalid(oldword):continue
        assert pathvalid([a,b,t,q,r,t,q]);transitions+=1
    # All square-color permutations really produce the full boundary set.
    orbit=set()
    for row in data:
        for perm in permutations((1,2,3,4)):
            mapping=(0,)+perm
            orbit.add(tuple(mapping[x] for x in row['boundary']))
    assert orbit==allowed
    bad=list(data[0]['boundary'])+data[0]['words']['4'][1:-1]
    bad[1]=bad[0]
    assert not valid(bad,graph(4)[0])
    print(json.dumps(dict(status='PASS',python=platform.python_version(),valid_old_boundaries=len(allowed),canonical_boundaries=len(reps),base_words=count,distance_pairs=pairs,generic_suffix_transitions=transitions,negative_controls=1),sort_keys=True))
if __name__=='__main__':main()
