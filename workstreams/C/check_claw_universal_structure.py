#!/usr/bin/env python3
"""Definition-first, standard-library exact checker of the structural theorem.

Reconstructs BOTH the source's CG(n) canonical double cover and an entirely
separately defined 4-type synchronized-cylinder model, checks an explicit
2-layer vertex isomorphism, builds every claimed D_(6n) x C2 automorphism,
checks 8-cycle incidence and computes all guide conjugacy classes using the
claimed transformations. Universal completeness is proven in the MANUSCRIPT,
not by the finite runs below. No networkx and no discovery imports.
"""
import hashlib, pathlib, itertools, collections

def graph(N):return [set() for _ in range(N)]
def link(a,u,v):
    assert u!=v
    a[u].add(v);a[v].add(u)
def source_cg(n):
    N=10*n; a=graph(N)
    for t in range(6*n):link(a,t,(t+1)%(6*n))
    for i in range(n):
        c=6*n+i
        for j in range(3):
            t=i+j*n; leaf=7*n+3*i+j
            link(a,c,leaf);link(a,leaf,t);link(a,leaf,t+3*n)
    assert all(len(v)==3 for v in a)
    return a

def canonical_double_cover(A):
    n=len(A);B=graph(2*n)
    for u in range(n):
        for v in A[u]:
            if u<v:link(B,2*u,2*v+1);link(B,2*u+1,2*v)
    return B

def model(n):
    M=6*n; a=graph(20*n)
    # U_t = t; V_t = M+t; L_t=2M+t; W_a=3M+a.
    for t in range(M):
        link(a,t,(t+1)%M)
        link(a,M+t,M+(t+1)%M)
        link(a,2*M+t,t);link(a,2*M+t,M+t)
        link(a,2*M+t,3*M+t%(2*n))
    assert len(a)==20*n and all(len(s)==3 for s in a)
    return a

def structural_permutation_to_source(n):
    M=6*n;P=[None]*(20*n)
    # U_t=(u_t,layer=t mod2) ; V_t=(u_(t+3n),layer=t mod2).
    # L_t=(leaf of antipodal pair containing t, layer=(1-t) mod2).
    # W_a=(claw centre i=a mod n, layer=a mod2).
    for t in range(M):
        P[t]=2*t+t%2
        P[M+t]=2*((t+3*n)%M)+t%2
        r=t%(3*n); i=r%n; j=r//n
        P[2*M+t]=2*(7*n+3*i+j)+(1-t)%2
    for a in range(2*n):P[3*M+a]=2*(6*n+a%n)+a%2
    assert sorted(P)==list(range(20*n))
    return P

def assert_model(n):
    A=model(n);K=canonical_double_cover(source_cg(n))
    P=structural_permutation_to_source(n)
    assert all({P[v] for v in A[u]}==K[P[u]] for u in range(len(A)))
    return A,P

def simple_cycle_8_per_vertex(a):
    n=len(a);count=[0]*n;total=0
    for root in range(n):
        def dfs(path,visited):
            nonlocal total
            if len(path)==8:
                if root in a[path[-1]] and path[1]<path[-1]:
                    total+=1
                    for v in path:count[v]+=1
                return
            for v in a[path[-1]]:
                if v>root and v not in visited:
                    dfs(path+[v],visited|{v})
        for v in a[root]:
            if v>root:dfs([root,v],{root,v})
    return total,count

def perm(n,eps,b,swap):
    M=6*n;N=20*n;p=[None]*N
    for t in range(M):
        s=(eps*t+b)%M
        p[t]=s+(M if swap else 0)
        p[M+t]=s+(0 if swap else M)
        p[2*M+t]=2*M+s
    for r in range(2*n):p[3*M+r]=3*M+(eps*r+b)%(2*n)
    assert sorted(p)==list(range(N))
    return tuple(p)

def isauto(A,p):
    return all({p[v] for v in A[u]}==A[p[u]] for u in range(len(A)))

def test(n):
    assert n>=3 and n%2==1
    A,P=assert_model(n);N=len(A);M=6*n
    ncycles,cyc=simple_cycle_8_per_vertex(A)
    assert ncycles==M and set(cyc[:2*M])=={3} and set(cyc[2*M:3*M])=={2} and set(cyc[3*M:])=={0}
    elems=[(eps,b,swap,perm(n,eps,b,swap)) for eps in [1,-1] for b in range(M) for swap in [0,1]]
    assert len(set(t[3] for t in elems))==24*n
    assert all(isauto(A,t[3]) for t in elems)
    guides=[]
    for eps,b,swap,p in elems:
        switching=b%2==1
        involutive=all(p[p[u]]==u for u in range(N))
        strong=(switching and involutive and all(p[u] not in A[u] for u in range(N)))
        if strong:guides.append((eps,b,swap,p))
    assert len(guides)==3*n+2
    group={t[3] for t in elems}
    # Construct classes from exact conjugates within the EXPLICIT proven group.
    seen=set();class_sizes=[]
    for eps,b,sw,p in guides:
        if p in seen:continue
        orbit=set()
        for a in group:
            inv=[None]*N
            for i,j in enumerate(a):inv[j]=i
            conj=tuple(a[p[inv[i]]] for i in range(N))
            assert conj in group
            orbit.add(conj)
        seen|=orbit;class_sizes.append(len(orbit))
    assert seen=={g[3] for g in guides}
    assert sorted(class_sizes)==[1,1,3*n]
    return {'n':n,'cg_vertices':10*n,'cg_edges':15*n,'cdc_vertices':N,
       'cdc_edges':30*n,'model_isomorphism':'PASS','8_cycles':ncycles,
       '8_cycle_participation':{'U,V':3,'L':2,'W':0},
       'explicit_aut_group_size':len(group),'strong_guides':len(guides),
       'guide_class_sizes':sorted(class_sizes),'base_graph_classes':len(class_sizes),
       'nonisomorphic_cousins':len(class_sizes)-1}

def negatives():
    A,P=assert_model(3)
    damaged=[set(row) for row in A]
    u,v=0,1
    damaged[u].remove(v);damaged[v].remove(u)
    assert not all({P[y] for y in damaged[x]}==canonical_double_cover(source_cg(3))[P[x]] for x in range(len(A)))
    badP=P.copy();badP[0],badP[1]=badP[1],badP[0]
    B=canonical_double_cover(source_cg(3))
    assert not all({badP[y] for y in A[x]}==B[badP[x]] for x in range(len(A)))
    bad=perm(3,-1,1,0)
    assert any(bad[u] in A[u] for u in range(len(A)))
    return 3

if __name__=='__main__':
    for n in [3,5,7,9]:print('PASS',test(n),flush=True)
    print('negative_cases_rejected',negatives(),flush=True)
    print('SHA256',hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest())
