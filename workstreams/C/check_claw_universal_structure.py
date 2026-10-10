#!/usr/bin/env python3
"""Definition-first standard-library checker of CG(n) universal classification.

Rebuilds CG(n) from the original paper and its actual canonical double cover,
then independently builds the proposed 4-type model; checks vertex bijection,
all graph edges and nonedges, simple C8 counts, every proposed dihedral
automorphism, every candidate strong guide, and all guide conjugacy classes.
Only the written proof, not finite tests, establishes claims for all odd n.
"""
import hashlib
import pathlib


def graph(N): return [set() for _ in range(N)]


def edge(A, u, v):
    assert u != v
    A[u].add(v)
    A[v].add(u)


def source_cg(n):
    N = 10*n
    A = graph(N)
    for t in range(6*n):
        edge(A, t, (t+1)%(6*n))
    for i in range(n):
        c = 6*n+i
        for j in range(3):
            r = i+j*n
            leaf = 7*n+3*i+j
            edge(A, c, leaf)
            edge(A, leaf, r)
            edge(A, leaf, r+3*n)
    assert all(len(s)==3 for s in A)
    return A


def cover(A):
    N=len(A)
    B=graph(2*N)
    for u in range(N):
        for v in A[u]:
            if u<v:
                edge(B,2*u,2*v+1)
                edge(B,2*u+1,2*v)
    return B


def model(n):
    M=6*n
    A=graph(20*n)
    # U_t=t, V_t=M+t, L_t=2M+t, W_a=3M+a.
    for t in range(M):
        edge(A,t,(t+1)%M)
        edge(A,M+t,M+(t+1)%M)
        edge(A,2*M+t,t)
        edge(A,2*M+t,M+t)
        edge(A,2*M+t,3*M+t%(2*n))
    assert all(len(row)==3 for row in A)
    return A


def vertex_map(n):
    M=6*n
    P=[None]*(20*n)
    for t in range(M):
        P[t]=2*t+t%2
        P[M+t]=2*((t+3*n)%M)+t%2
        r=t%(3*n)
        i=r%n
        j=r//n
        P[2*M+t]=2*(7*n+3*i+j)+(1-t)%2
    for a in range(2*n):
        P[3*M+a]=2*(6*n+a%n)+a%2
    assert sorted(P)==list(range(20*n))
    return P


def direct_model_check(n):
    A=model(n)
    K=cover(source_cg(n))
    P=vertex_map(n)
    assert all({P[v] for v in A[u]}==K[P[u]] for u in range(len(A)))
    return A,P,K


def c8_incidence(A):
    N=len(A)
    visits=[0]*N
    total=0
    for root in range(N):
        def go(path,used):
            nonlocal total
            if len(path)==8:
                if root in A[path[-1]] and path[1]<path[-1]:
                    total+=1
                    for v in path:visits[v]+=1
                return
            for v in A[path[-1]]:
                if v>root and v not in used:
                    go(path+[v],used|{v})
        for v in A[root]:
            if v>root:go([root,v],{root,v})
    return total,visits


def transform(n,eps,b,sw):
    M=6*n
    P=[None]*(20*n)
    for t in range(M):
        s=(eps*t+b)%M
        P[t]=s+(M if sw else 0)
        P[M+t]=s+(0 if sw else M)
        P[2*M+t]=2*M+s
    for a in range(2*n):
        P[3*M+a]=3*M+(eps*a+b)%(2*n)
    assert sorted(P)==list(range(20*n))
    return tuple(P)


def is_automorphism(A,P):
    return all({P[v] for v in A[u]}==A[P[u]] for u in range(len(A)))


def check(n):
    assert n>=3 and n%2==1
    A,P,K=direct_model_check(n)
    M=6*n
    N=len(A)
    count,visits=c8_incidence(A)
    assert count==M
    assert set(visits[:2*M])=={3}
    assert set(visits[2*M:3*M])=={2}
    assert set(visits[3*M:])=={0}
    group={}
    guides={}
    for eps in (1,-1):
        for b in range(M):
            for sw in (0,1):
                p=transform(n,eps,b,sw)
                assert is_automorphism(A,p)
                group[p]=(eps,b,sw)
                if b%2 and all(p[p[u]]==u for u in range(N)):
                    if all(p[u] not in A[u] for u in range(N)):
                        guides[p]=(eps,b,sw)
    assert len(group)==24*n
    assert len(guides)==3*n+2
    assert {x for x in guides.values() if x[0]==1}=={(1,3*n,0),(1,3*n,1)}
    assert {x for x in guides.values() if x[0]==-1}=={(-1,b,1) for b in range(1,M,2)}
    seen=set()
    sizes=[]
    for p in guides:
        if p in seen:continue
        orbit=set()
        for a in group:
            inverse=[None]*N
            for u,v in enumerate(a):inverse[v]=u
            conjugate=tuple(a[p[inverse[u]]] for u in range(N))
            assert conjugate in guides
            orbit.add(conjugate)
        assert p in orbit
        seen.update(orbit)
        sizes.append(len(orbit))
    assert seen==set(guides)
    assert sorted(sizes)==[1,1,3*n]
    return {'n':n,'CG_nodes':10*n,'CDC_nodes':20*n,'C8':count,
            'C8_type_visits':[3,2,0],'automorphisms':len(group),
            'strong_guides':len(guides),'class_sizes':sorted(sizes),
            'nonisomorphic_cousins':len(sizes)-1}


def negative_tests():
    A,P,K=direct_model_check(3)
    B=[set(row) for row in A]
    B[0].remove(1);B[1].remove(0)
    assert not all({P[v] for v in B[u]}==K[P[u]] for u in range(len(A)))
    bad=P.copy()
    bad[0],bad[1]=bad[1],bad[0]
    assert not all({bad[v] for v in A[u]}==K[bad[u]] for u in range(len(A)))
    reflection=transform(3,-1,1,0)
    assert any(reflection[u] in A[u] for u in range(len(A)))
    return 3


if __name__=='__main__':
    for n in (3,5,7,9):
        print('PASS',check(n),flush=True)
    print('negative_tests_rejected',negative_tests())
    print('sha256',hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
