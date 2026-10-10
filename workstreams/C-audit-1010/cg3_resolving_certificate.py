#!/usr/bin/env python3
"""Standalone, no external dependencies: exact Aut(CDC(CG(3))) via a resolving set.

The 6 distinguished vertices give pairwise-distinct distance fingerprints to
ALL vertices. Therefore any graph automorphism is uniquely determined by
its image on those six vertices. Enumerate every image-tuple preserving their
mutual graph distances, reconstruct the only possible full permutation, and
verify all actual edges AND nonedges. Conjugation classes of strongly
switching involutions classify TF-cousin bases (Mizzi v3 Theorem 4.6).
"""
from collections import deque, Counter
from itertools import combinations
from hashlib import sha256
from pathlib import Path
import json

N=3
LANDMARKS=(0,3,35,43,27,30)


def build_claw(n):
    size=10*n
    g=[set() for _ in range(size)]
    def edge(u,v):
        assert u != v and 0 <= u < size and 0 <= v < size
        g[u].add(v);g[v].add(u)
    for x in range(6*n):edge(x,(x+1)%(6*n))
    for i in range(n):
        center=6*n+i
        for j in range(3):
            leaf=7*n+3*i+j
            t=i+j*n
            edge(center,leaf);edge(leaf,t);edge(leaf,t+3*n)
    assert all(len(neighbors)==3 for neighbors in g)
    return g


def cover(g):
    n=len(g)
    h=[set() for _ in range(2*n)]
    for u in range(n):
        for v in g[u]:
            h[2*u].add(2*v+1)
            h[2*u+1].add(2*v)
    assert all(len(neighbors)==3 for neighbors in h)
    return h


def full_distances(g):
    n=len(g);dist=[]
    for r in range(n):
        d=[-1]*n;d[r]=0;queue=deque([r])
        while queue:
            u=queue.popleft()
            for v in g[u]:
                if d[v] < 0:d[v]=d[u]+1;queue.append(v)
        assert all(x>=0 for x in d)
        dist.append(d)
    return dist


def all_automorphisms(g,dist,landmarks):
    n=len(g)
    signatures={tuple(dist[s][u] for s in landmarks):u for u in range(n)}
    assert len(signatures)==n, 'given landmark set is not resolving'
    complete=[];landmark_candidates=0;unique_extensions=0
    def recurse(images):
        nonlocal landmark_candidates,unique_extensions
        j=len(images)
        if j==len(landmarks):
            landmark_candidates+=1
            # Candidate image landmarks must also distinguish all vertices.
            reverse={tuple(dist[b][v] for b in images):v for v in range(n)}
            if len(reverse)!=n:return
            phi=[reverse.get(tuple(dist[s][u] for s in landmarks),-1)
                 for u in range(n)]
            if sorted(phi)!=list(range(n)):return
            unique_extensions+=1
            if all((v in g[u]) == (phi[v] in g[phi[u]])
                   for u in range(n) for v in range(n)):
                complete.append(tuple(phi))
            return
        s=landmarks[j]
        for v in range(n):
            if v in images:continue
            if all(dist[s][landmarks[i]]==dist[v][images[i]] for i in range(j)):
                recurse(images+(v,))
    recurse(())
    assert len(complete)==len(set(complete))
    return complete,landmark_candidates,unique_extensions


def compose(f,g):
    return tuple(f[g[i]] for i in range(len(f)))


def inverse(f):
    g=[0]*len(f)
    for i,j in enumerate(f):g[j]=i
    return tuple(g)


def switching(g,autos):
    n=len(g)
    chosen=[]
    for f in autos:
        if (all(f[2*u]%2==1 and f[2*u+1]%2==0 for u in range(n//2))
                and all(f[f[u]]==u for u in range(n))
                and all(f[u] not in g[u] for u in range(n))):
            chosen.append(f)
    return chosen


def conjugacy_orbits(autos,chosen):
    permitted=set(chosen)
    assert permitted
    classes=[]
    while permitted:
        representative=min(permitted)
        conj={compose(compose(a,representative),inverse(a)) for a in autos}
        assert conj <= set(chosen)
        classes.append(sorted(conj))
        permitted-=conj
    return classes


def fold(g,f):
    n=len(g)//2
    rows=[0]*n
    for i in range(n):
        for j in range(n):
            if f[2*j] in g[2*i]:rows[i]|=1<<j
    assert all(not ((rows[i]>>i)&1) for i in range(n))
    assert all(((rows[i]>>j)&1)==((rows[j]>>i)&1) for i in range(n) for j in range(n))
    assert all(row.bit_count()==3 for row in rows)
    return rows


def graph_invariants(rows):
    n=len(rows)
    tris=sum(sum((rows[i]&rows[j]).bit_count() for j in range(n)
                 if (rows[i]>>j)&1) for i in range(n))//6
    return {'degree':[r.bit_count() for r in rows][:4], 'triangle_count':tris,
            'edge_count':sum(r.bit_count() for r in rows)//2}


def count_simple_cycles(rows,k):
    n=len(rows); total=0
    for root in range(n):
        def explore(last,used,second,length):
            if length==k:
                return int(bool((rows[last]>>root)&1) and second<last)
            count=0
            rest=rows[last]
            while rest:
                bit=rest & -rest;rest-=bit;v=bit.bit_length()-1
                if v>root and not (used&bit):
                    count+=explore(v,used|bit,second if second>=0 else v,length+1)
            return count
        total+=explore(root,1<<root,-1,1)
    return total


def validate_fold_cover(g,f,rows):
    n=len(rows)
    dest=[2*u if layer==0 else f[2*u]
          for u in range(n) for layer in (0,1)]
    assert sorted(dest)==list(range(2*n))
    for i in range(2*n):
        for j in range(2*n):
            u,li=divmod(i,2);v,lj=divmod(j,2)
            source=li!=lj and bool((rows[u]>>v)&1)
            assert source==(dest[j] in g[dest[i]])


def main():
    g=cover(build_claw(N))
    distances=full_distances(g)
    signatures=[tuple(distances[s][u] for s in LANDMARKS) for u in range(len(g))]
    assert len(set(signatures))==len(g)
    assert len({tuple(distances[s][u] for s in LANDMARKS[:-1]) for u in range(len(g))})<len(g), \
        'negative control: removing final landmark must lose resolving power'
    autos,landmark_tuples,unique_extensions=all_automorphisms(g,distances,LANDMARKS)
    assert len(autos)==72, f'unexpected automorphism count: {len(autos)}'
    identity=tuple(range(len(g)))
    assert identity in autos
    chosen=switching(g,autos)
    classes=conjugacy_orbits(autos,chosen)
    assert len(chosen)==11 and len(classes)==3
    originals=fold(g,tuple(i^1 for i in range(len(g))))
    assert originals==[sum(1<<v for v in build_claw(N)[u]) for u in range(10*N)]
    details=[]
    for cls in classes:
        rep=cls[0]
        rows=fold(g,rep)
        validate_fold_cover(g,rep,rows)
        three=count_simple_cycles(rows,3)
        nine=count_simple_cycles(rows,9)
        details.append({'conjugacy_class_size':len(cls),
                        'simple_C3_count':three,'simple_C9_count':nine,
                        'is_original_exact_labelling':rows==originals,
                        'representative':list(rep),
                        'base_invariants':graph_invariants(rows),
                        'base_edge_list':[[i,j] for i in range(len(rows))
                                          for j in range(i+1,len(rows)) if (rows[i]>>j)&1]})
    assert sorted((d['simple_C3_count'],d['simple_C9_count']) for d in details)==[(0,36),(0,38),(2,22)]
    assert sum(d['is_original_exact_labelling'] for d in details)==1
    total=len(g)
    report={'original_source':'Mizzi arXiv:2603.27559v3, Definition 6.1 and Theorem 4.6',
      'parameter_n':N,'cover_vertices':total,'cover_edges':sum(map(len,g))//2,
      'resolving_landmarks':list(LANDMARKS),
      'unique_distance_signatures':len(set(signatures)),
      'mutual_distance_matrix':[[distances[x][y] for y in LANDMARKS] for x in LANDMARKS],
      'candidate_landmark_image_tuples':landmark_tuples,
      'unique_extensions_tested':unique_extensions,
      'complete_cover_automorphism_count':len(autos),
      'strong_switching_involutions':len(chosen),
      'strong_switching_conjugacy_classes':len(classes),
      'TF_cousin_classes_excluding_original':len(classes)-1,
      'conjugacy_representatives':details,
      'all_automorphisms':[list(a) for a in sorted(autos)]}
    file=Path(__file__).with_name('cg3_resolving_certificate.json')
    file.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print('RESOLVING CERTIFICATE PASS',len(set(signatures)),'of',total)
    print('landmark tuples:',landmark_tuples,'unique possible maps:',unique_extensions)
    print('complete automorphism group:',len(autos),
          'strongly switching:',len(chosen),'conjugacy classes:',len(classes))
    print('class sizes:',[len(x) for x in classes],
          'base invariants:',[d['base_invariants'] for d in details])
    print('source_sha256',sha256(Path(__file__).read_bytes()).hexdigest())
    print('certificate_sha256',sha256(file.read_bytes()).hexdigest())


if __name__=='__main__': main()
