#!/usr/bin/env python3
"""Independent exact checker of the Q5.8 demonstrator certificate.

Reads two *separate explicit graph edge lists*.  Rebuilds adjacencies, checks
an explicit CDC isomorphism using raw 2n x 2n edge tests, checks structural
non-isomorphism via local triangle counts, and checks the proposed main
minimal polynomial by integer Krylov multiplication.  No discovery-script
imports and no floating point arithmetic or external dependencies.

This checks the FINITE DEMONSTRATOR only.  The universal theorem is proved in
proof-q58.md and cannot be established by finite tests alone.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import pathlib
import platform
import sys


def adjacency(n, raw):
    assert isinstance(n, int) and n >= 1
    M = [[0 for _ in range(n)] for _ in range(n)]
    seen = set()
    for row in raw:
        assert isinstance(row, list) and len(row) == 2
        u, v = row
        assert isinstance(u, int) and isinstance(v, int)
        assert 0 <= u < v < n, (u,v)
        assert (u, v) not in seen, "duplicate input edge"
        seen.add((u,v))
        M[u][v] = M[v][u] = 1
    return M


def cdc_edge(M, a, b):
    """Encoded vertex = 2*v+layer, using original graph definition."""
    u, layer_u = divmod(a, 2)
    v, layer_v = divmod(b, 2)
    return bool(layer_u != layer_v and M[u][v] == 1)


def check_cdc_bijection(G, H, p):
    n = len(G)
    assert sorted(p) == list(range(n)), "row permutation is not bijective"
    # Map (u,0)->(p[u],0), (u,1)->(u,1).  Exhaustively verify the 2n-vertex
    # adjacency matrix under this explicit bijection, not just an edge count.
    phi = [0]*(2*n)
    for u in range(n):
        phi[2*u] = 2*p[u]
        phi[2*u+1] = 2*u+1
    assert sorted(phi) == list(range(2*n))
    for i in range(2*n):
        for j in range(i+1,2*n):
            assert cdc_edge(G, i, j) == cdc_edge(H, phi[i],phi[j]), (i,j)


def mul(M,v):
    return [sum(M[i][j]*v[j] for j in range(len(v))) for i in range(len(v))]


def tri_per_vertex(M):
    n=len(M)
    return [sum(M[u][v] * M[u][w] * M[v][w]
                for v in range(n) for w in range(v+1,n)) for u in range(n)]


def connected(M):
    seen={0}
    todo=[0]
    for u in todo:
        for v,e in enumerate(M[u]):
            if e and v not in seen:
                seen.add(v)
                todo.append(v)
    return len(seen)==len(M)


def check_document(doc):
    n=doc['n']; G=adjacency(n, doc['G_edges']);H=adjacency(n,doc['H_edges'])
    p=doc['permutation_row']
    assert connected(G) and connected(H), "demo graphs must be connected"
    assert len(doc['G_edges']) == len(doc['H_edges']) == doc['expected_edge_count']
    assert sorted(map(sum,G)) == sorted(map(sum,H)) == doc['expected_degree_multiset']
    check_cdc_bijection(G,H,p)
    # Invariant under graph isomorphism: multiset of numbers of triangles
    # incident with degree-four vertices.  This distinguishes G from H.
    triangles={}
    for name,M in [('G',G),('H',H)]:
        degrees=list(map(sum,M));local_tris=tri_per_vertex(M)
        triangles[name]=sorted(local_tris[u] for u in range(n) if degrees[u]==4)
        assert triangles[name] == doc['expected_degree4_triangle_multisets'][name]
    assert triangles['G'] != triangles['H'], "nonisomorphism certificate invalid"

    walks=[]
    vectors=[]
    for name,M in [('G',G),('H',H)]:
        v0=[1]*n
        v1=mul(M,v0)
        assert v1!=[v1[0]]*n, "degree must be nonconstant: cyclic dimension >=2"
        v2=mul(M,v1)
        coefs=doc['main_minimal_polynomial']
        assert len(coefs)==3 and coefs[0]==1
        # 1*x^2 - 3*x - 8; use supplied values rather than hardcoded
        # constants so a corrupted claimed polynomial is rejected.
        assert all(coefs[0]*v2[i]+coefs[1]*v1[i]+coefs[2]*v0[i]==0
                   for i in range(n)), "claimed main minimal polynomial false"
        v=v0
        seq=[]
        vec=[]
        for k in range(7):
            seq.append(sum(v))
            vec.append(tuple(v))
            v=mul(M,v)
        assert seq==doc['expected_all_ones_walks_0_to_6']
        walks.append(seq)
        vectors.append(vec)
    assert walks[0]==walks[1]
    assert vectors[0]==vectors[1]
    return n,doc['expected_edge_count'],triangles,walks[0]


def run_negative_tests(doc):
    ntests=0
    for corrupt in ('H_edge','row_permutation','polynomial'):
        bad=copy.deepcopy(doc)
        if corrupt=='H_edge':
            bad['H_edges'].pop()
        elif corrupt=='row_permutation':
            p=bad['permutation_row']
            p[0],p[1]=p[1],p[0]
        else:
            bad['main_minimal_polynomial'][-1]-=1
        try:
            check_document(bad)
        except AssertionError:
            ntests+=1
        else:
            raise AssertionError(f'FAIL: corrupt input {corrupt} accepted')
    return ntests


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate',type=pathlib.Path,
                        default=pathlib.Path(__file__).with_name('certificate-q58.json'))
    parser.add_argument('--skip-negative',action='store_true')
    args=parser.parse_args()
    doc=json.loads(args.certificate.read_text(encoding='utf-8'))
    n,m,triangles,walks=check_document(doc)
    nneg=run_negative_tests(doc) if not args.skip_negative else 0
    print('PASS; exact integer computation; no third-party dependencies')
    print('Python:',platform.python_version())
    print(f'graphs: n={n}, m={m}, connected=True')
    print('CDC(G) ≅ CDC(H) with explicitly tested 24-vertex map')
    print('nonisomorphism: triangles at degree-4 vertices:',triangles)
    print('minimal polynomial: x^2-3x-8; roots (3±sqrt(41))/2')
    print('same walk totals for k=0..6:',walks)
    print('negative tests rejected:',nneg)
    for path in [pathlib.Path(__file__),args.certificate]:
        print('SHA256:',path.name,hashlib.sha256(path.read_bytes()).hexdigest())

if __name__=='__main__':
    main()
