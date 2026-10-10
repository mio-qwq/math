#!/usr/bin/env python3
"""Small, bounded *discovery* probe for first Mizzi v3 TF-cousin clause.
Uses networkx ONLY for quick discovery and isomorphism screening; an independent
standard-library exact checker is required for any candidate counterexample.
DO NOT treat unsuccessful finite trials as proof of the public conjecture.
"""
from itertools import combinations
from collections import defaultdict
from random import Random
import networkx as nx
import argparse,json, time

def make_perm(parts):
    P=[]; at=0
    for length in parts:
        P += [at+(i+1)%length for i in range(length)]
        at+=length
    return P

def edge_orbits(T):
    n=len(T)
    inv=[0]*n
    for i,j in enumerate(T):inv[j]=i
    def norm(a,b):return (min(a,b),max(a,b))
    remaining=set(combinations(range(n),2)); out=[]; invalid=0
    while remaining:
        seed=min(remaining);todo=[seed];closed={seed};bad=False
        while todo:
            u,v=todo.pop()
            for x,y in [(T[u],inv[v]),(T[v],inv[u])]:
                if x==y:bad=True;continue
                z=norm(x,y)
                if z not in closed:closed.add(z);todo.append(z)
        assert closed<=remaining
        remaining-=closed
        if any(v==T[u] or u==T[v] for u,v in closed):bad=True
        if bad:invalid+=1
        else:out.append(tuple(sorted(closed)))
    return out,invalid

def graph_from_mask(n,T,orbits,mask):
    A=[[0]*n for _ in range(n)];B=[[0]*n for _ in range(n)]
    for idx,orb in enumerate(orbits):
        if (mask>>idx)&1:
            for u,v in orb:A[u][v]=A[v][u]=1
    for u in range(n):
        for v in range(n): B[u][v]=A[u][T[v]]
    assert all(A[i][i]==B[i][i]==0 for i in range(n))
    assert all(B[i][j]==B[j][i] for i in range(n) for j in range(n))
    return A,B

def nxg(A):
    G=nx.Graph();G.add_nodes_from(range(len(A)))
    G.add_edges_from((u,v) for u in range(len(A)) for v in range(u+1,len(A)) if A[u][v]);return G

def cycles_at_size(A,k):
    n=len(A); neigh=[[v for v in range(n) if A[u][v]] for u in range(n)]
    out=set()
    def rec(path,marked,origin):
        u=path[-1]
        if len(path)==k:
            if A[u][origin]:
                out.add(frozenset(path))
            return
        for v in neigh[u]:
            if v>origin and not (marked>>v)&1:
                rec(path+[v], marked|(1<<v), origin)
    for origin in range(n):
        for v in neigh[origin]:
            if v>origin:rec([origin,v],(1<<origin)|(1<<v),origin)
    return out

def property_holds(A,B):
    n=len(A)
    for k in range(3,n//2+1,2):
        ac=cycles_at_size(A,k); bc=cycles_at_size(B,k)
        if ac and cycles_at_size(B,2*k):
            if any(a.isdisjoint(b) for a,b in combinations(ac,2)):
                return True,k,'G'
        if bc and cycles_at_size(A,2*k):
            if any(a.isdisjoint(b) for a,b in combinations(bc,2)):
                return True,k,'H'
    return False,None,None

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--trials',type=int,default=1000)
    parser.add_argument('--seed',type=int,default=20261010)
    opts=parser.parse_args();rng=Random(opts.seed)
    classes=[(4,2,2,2),(4,4,2),(6,4),(6,2,2),(8,2),(4,4,4),(6,6),(4,4,2,2),(6,4,2),(4,2,2,2,2),(8,4),(10,2),(6,3,3),(3,3,2,2,2),(2,2,2,2,2,2)]
    print('seed',opts.seed,'trials_per_class',opts.trials,'library',nx.__version__,flush=True)
    for parts in classes:
        T=make_perm(parts);n=len(T);orbs,inv=edge_orbits(T)
        stats=defaultdict(int)
        num=len(orbs)
        if num==0:
            print(parts,'allowed edge orbits=0, skip');continue
        for count in range(opts.trials):
            # generate at 3 different orbit densities
            density=[0.20,0.35,0.52,0.72][count%4]
            mask=sum((1<<i) for i in range(num) if rng.random()<density)
            if mask==0:continue
            A,B=graph_from_mask(n,T,orbs,mask)
            G,H=nxg(A),nxg(B)
            if min(G.number_of_edges(),H.number_of_edges()) < n:continue
            if not nx.is_connected(G) or not nx.is_connected(H):continue
            stats['conn']+=1
            if nx.is_bipartite(G) or nx.is_bipartite(H):continue
            stats['nonbip']+=1
            if len({tuple(A[i]) for i in range(n)})<n or len({tuple(B[i]) for i in range(n)})<n:continue
            stats['twinsfree']+=1
            if nx.is_isomorphic(G,H):continue
            stats['cousins']+=1
            ok,k,which=property_holds(A,B)
            if not ok:
                output={'parts':parts,'T':T,'n':n,'orbits':num,'edge_count_G':G.number_of_edges(),'edge_count_H':H.number_of_edges(),
                'edges_G':list(map(list,G.edges())),'edges_H':list(map(list,H.edges())),'mask':mask,'seed':opts.seed,'trial':count}
                print('POTENTIAL COUNTEREXAMPLE: exact-cycle check required',json.dumps(output),flush=True)
                with open('/mnt/data/c_next_study/possible_tf_cousin.json','w') as file:json.dump(output,file,indent=2)
                return
            stats['ok']+=1
        print('class',parts,'edge_orbits',num,'invalid_edge_orbits',inv,'stats',dict(stats),flush=True)
    print('NO COUNTEREXAMPLE IN THIS BOUNDED MODEL (not universal)')
if __name__=='__main__':main()
