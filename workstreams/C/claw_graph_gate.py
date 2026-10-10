#!/usr/bin/env python3
"""Initial bounded feasibility gate for Mizzi 2026 v3 Section 7 CG(n) cousin counts.
Reconstructs Definition 6.1, then tries bounded enumeration of automorphisms
of the actual canonical double cover. A timer cutoff is NOT completeness.
"""
import networkx as nx
from time import perf_counter
import signal,sys

class Timeout(Exception):pass

def timeout(sig,frame):raise Timeout()

def claw(n,companion=False):
    assert n>=1
    G=nx.Graph(); G.add_nodes_from(range(10*n))
    # u = 0..6n-1, centres 6n..7n-1, leaves 7n..10n-1
    for i in range(6*n):
        if not companion:
            G.add_edge(i,(i+1)%(6*n))
        else:
            p=i//(3*n)
            G.add_edge(i,p*3*n+((i-p*3*n+1)%(3*n)))
    for i in range(n):
        c=6*n+i
        for j in range(3):
            v=7*n+3*i+j
            G.add_edges_from([(c,v),(v,i+j*n),(v,i+j*n+3*n)])
    assert G.number_of_nodes()==10*n and G.number_of_edges()==15*n
    assert all(d==3 for _,d in G.degree())
    assert nx.is_connected(G)
    return G

def cdc(G):
    H=nx.Graph()
    H.add_nodes_from(range(2*G.number_of_nodes()))
    for u,v in G.edges():
        H.add_edges_from([(2*u,2*v+1),(2*u+1,2*v)])
    return H

def try_automorphisms(K,deadline=10,max_yield=100000):
    t=perf_counter(); n=K.number_of_nodes()
    match=nx.algorithms.isomorphism.GraphMatcher(K,K)
    seen=0;switch=0;strong=0;classes=[]
    signal.signal(signal.SIGALRM,timeout);signal.alarm(deadline)
    try:
        for p in match.isomorphisms_iter():
            seen+=1
            if all(p[2*i]%2==1 and p[2*i+1]%2==0 for i in range(n//2)):
                switch+=1
                if all(p[p[i]]==i and not K.has_edge(i,p[i]) for i in range(n)):
                    strong+=1
            if seen>=max_yield:break
        complete=(seen<max_yield)
    except Timeout:
        complete=False
    finally:
        signal.alarm(0)
    return dict(enumerated=seen,switching=switch,strong=strong,seconds=round(perf_counter()-t,2),complete=complete)

def main():
    for n in (1,3):
        G=claw(n);Gp=claw(n,True);C=cdc(G);Cp=cdc(Gp)
        print(f'n={n}, vertices={len(G)}, degree={set(dict(G.degree()).values())}, edges={len(G.edges())}, connected=True')
        print('known explicit companion CDC iso=',nx.is_isomorphic(C,Cp),'original iso=',nx.is_isomorphic(G,Gp),flush=True)
        report=try_automorphisms(C,deadline=10)
        print('aut attempt',report,flush=True)
if __name__=='__main__':main()
