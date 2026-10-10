#!/usr/bin/env python3
"""Independent exact Burnside edge-orbit audit of unlabelled simple graphs.

Exhaust all vertex permutations (n<=7), count orbits on unordered pairs,
verify Burnside against known small counts and weighted symmetry identities.
Analytic all-n estimates are in the accompanying manuscript, NOT inferred
from the enumerated small cases.
"""
from itertools import combinations, permutations
from math import comb, factorial
from collections import Counter
from hashlib import sha256
from pathlib import Path

KNOWN={1:1,2:2,3:4,4:11,5:34,6:156,7:1044}


def edge_orbits(n,p):
    E=list(combinations(range(n),2));index={e:i for i,e in enumerate(E)}
    seen=set();orbits=[]
    for u,v in E:
        e=index[u,v]
        if e in seen:continue
        cyc=[];a,b=u,v
        while True:
            e=index[tuple(sorted((a,b)))]
            if e in seen:break
            seen.add(e);cyc.append(e)
            a,b=p[a],p[b]
        orbits.append(cyc)
    assert sum(map(len,orbits))==comb(n,2)
    return len(orbits)


def main():
    lines=[]
    for n,want in KNOWN.items():
        E=comb(n,2);ident=(1<<E);sumfixed=0;hist=Counter()
        for p in permutations(range(n)):
            c=edge_orbits(n,p)
            hist[c]+=1
            sumfixed+=1<<c
        assert sumfixed % factorial(n)==0
        unlabelled=sumfixed//factorial(n)
        assert unlabelled==want,(n,unlabelled,want)
        other=sumfixed-ident
        if n>=3:assert other>0
        lines.append((n,unlabelled,other,hist[E],sum(hist.values())))
    print('PASS complete vertex-permutation Burnside g_n n=1..7')
    for line in lines:print('n,unlabelled,nonidentity_fixed_pairs,identity_edge-orbit_count,n!:',line)
    print('SHA256',sha256(Path(__file__).read_bytes()).hexdigest())
if __name__=='__main__':main()
