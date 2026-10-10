#!/usr/bin/env python3
"""Independent original-definition finite checks for odd CG(n) theorem.

Rebuild source edges without importing resolving-set discovery. Classify
six-cycle edges from simple actual paths, identify two ring cycles and leaf
matching, verify explicit dihedral/deck maps, strongly switching guides,
and finite metric landmark upper bounds. These are falsification checks,
not the proof for arbitrary odd n.
"""
from collections import deque, Counter
from hashlib import sha256
import json
import pathlib
import platform


def graph(n):
    assert n >= 3 and n % 2 == 1
    size = 10*n
    A = [set() for _ in range(size)]
    def edge(u,v):
        assert u != v
        A[u].add(v);A[v].add(u)
    for t in range(6*n):
        edge(t,(t+1)%(6*n))
    for p in range(3*n):
        leaf=7*n+3*(p%n)+p//n
        center=6*n+p%n
        edge(leaf,center)
        edge(leaf,p)
        edge(leaf,p+3*n)
    assert all(len(v)==3 for v in A)
    return A


def cover(A):
    C=[set() for _ in range(2*len(A))]
    for u in range(len(A)):
        for v in A[u]:
            C[2*u].add(2*v+1)
            C[2*u+1].add(2*v)
    assert all(len(row)==3 for row in C)
    return C


def edge_in_hexagon(A,u,v):
    # A simple alternative path with five edges after deleting uv.
    def dfs(last,used,depth):
        if depth==5:
            return last==u
        for w in A[last]:
            if last==v and w==u:continue
            if w==u:
                if depth==4:return True
                continue
            if w not in used and dfs(w,used|{w},depth+1):
                return True
        return False
    return dfs(v,{v,u},0)


def distances(A):
    all_dist=[]
    for root in range(len(A)):
        d=[-1]*len(A)
        d[root]=0
        queue=deque([root])
        while queue:
            u=queue.popleft()
            for v in A[u]:
                if d[v]<0:
                    d[v]=d[u]+1
                    queue.append(v)
        assert all(t>=0 for t in d)
        all_dist.append(d)
    return all_dist


def count_landmark_images(D,landmarks):
    n=len(D)
    count=0
    def rec(images):
        nonlocal count
        j=len(images)
        if j==len(landmarks):
            count+=1
            return
        for v in range(n):
            if v in images:continue
            if all(D[landmarks[j]][landmarks[i]]==D[v][images[i]]
                   for i in range(j)):
                rec(images+(v,))
    rec(())
    return count


def dihedral_and_deck(n,A):
    size=10*n
    perms={}
    def leaf_index(p):
        return 7*n+3*(p%n)+p//n
    for reflect in (False,True):
        for t in range(6*n):
            base=[0]*size
            for u in range(6*n):
                base[u]=((t-u) if reflect else (u+t))%(6*n)
            for i in range(n):
                base[6*n+i]=6*n+((t-i) if reflect else (i+t))%n
            for p in range(3*n):
                mapped=((t-p) if reflect else (p+t))%(3*n)
                base[leaf_index(p)]=leaf_index(mapped)
            assert sorted(base)==list(range(size))
            assert all((v in A[u])==(base[v] in A[base[u]])
                       for u in range(size) for v in range(size))
            for deck in (0,1):
                cover_perm=tuple(2*base[u]+(l^deck)
                                 for u in range(size) for l in (0,1))
                perms[(reflect,t,deck)]=cover_perm
    assert len(set(perms.values()))==24*n
    return perms


def negative_tests():
    n=3
    A=graph(n)
    H=cover(A)
    broken=[set(r) for r in A]
    broken[0].remove(1)
    broken[1].remove(0)
    assert not all(len(r)==3 for r in broken)
    fake=list(range(10*n))
    fake[0],fake[6*n]=fake[6*n],fake[0]
    assert not all((v in A[u])==(fake[v] in A[fake[u]])
                   for u in range(10*n) for v in range(10*n))
    bad=[set(r) for r in H]
    bad[0].add(0)
    assert any(i in bad[i] for i in range(20*n))
    return 3


def verify(n):
    A=graph(n)
    C=cover(A)
    N=len(C)
    six=set()
    for u in range(N):
        for v in C[u]:
            if u<v and edge_in_hexagon(C,u,v):
                six.add((u,v))
    incidence=[sum((min(u,v),max(u,v)) in six for v in C[u])
               for u in range(N)]
    assert Counter(incidence)==Counter({3:12*n,2:6*n,0:2*n})
    for u in range(N):
        source_type='R' if u//2<6*n else 'C' if u//2<7*n else 'L'
        assert incidence[u]=={'R':3,'C':0,'L':2}[source_type]
    # Ring subgraph: exactly two simple 6n-cycles.
    ring=set(range(12*n))
    components=[]
    ring_all=set(ring)
    while ring:
        start=min(ring)
        comp={start}
        queue=[start]
        ring.remove(start)
        for u in queue:
            for v in C[u]&ring_all:
                if v not in comp:
                    comp.add(v)
                    queue.append(v)
                    ring.remove(v)
        components.append(comp)
    assert len(components)==2 and all(len(c)==6*n for c in components)
    assert all(len(C[u]&ring_all)==2
               for component in components for u in component)
    # Every leaf bridges the distinct ring components.
    for leaf in range(14*n,20*n):
        pair=C[leaf]&ring_all
        assert len(pair)==2
        assert len(pair&components[0])==len(pair&components[1])==1
    for component in components:
        for u in component:
            assert len([v for v in C[u] if v>=14*n])==1
    perms=dihedral_and_deck(n,A)
    invol=[]
    strong=[]
    for label,perm in perms.items():
        if label[2]!=1:continue
        if not all(perm[perm[u]]==u for u in range(N)):continue
        invol.append(label)
        if all(perm[u] not in C[u] for u in range(N)):
            strong.append(label)
    assert len(invol)==6*n+2
    assert len(strong)==3*n+2
    assert set(strong)=={(False,0,1),(False,3*n,1)}|{
        (True,t,1) for t in range(0,6*n,2)}
    D=distances(C)
    if n==3:
        landmarks=(0,3,35,43,27,30)
        expected=1656
    else:
        landmarks=(0,3,12*n-1,14*n+1,10*n,8*n+3,2*n+1,1)
        expected=24*n
    signatures={tuple(D[s][u] for s in landmarks) for u in range(N)}
    assert len(signatures)==N
    actual=count_landmark_images(D,landmarks)
    assert actual==expected
    return {
        'n':n,'base_nodes':10*n,'base_edges':15*n,
        'cover_nodes':20*n,'cover_edges':30*n,
        'hexagonal_edges':len(six),
        'incident_hexagons':dict(Counter(incidence)),
        'ring_components':[6*n,6*n],
        'explicit_cover_automorphisms':len(perms),
        'layer_exchanging_involutions':len(invol),
        'strongly_switching_involutions':len(strong),
        'landmark_count':len(landmarks),
        'distance_compatible_landmark_maps':actual
    }


def main():
    result={
       'scope':'FINITE tests only, not universal proof',
       'source':'Mizzi arXiv:2603.27559v3 Definition 6.1',
       'python':platform.python_version(),
       'negative_tests_rejected':negative_tests(),
       'cases':[]
    }
    for n in (3,5,7,9,11,13,15):
        record=verify(n)
        result['cases'].append(record)
        print('PASS',record,flush=True)
    target=pathlib.Path(__file__).with_name('cg_all_odd_check_results.json')
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',
                      encoding='utf-8')
    print('SOURCE_SHA256',sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
    print('RESULT_SHA256',sha256(target.read_bytes()).hexdigest())


if __name__=='__main__':
    main()
