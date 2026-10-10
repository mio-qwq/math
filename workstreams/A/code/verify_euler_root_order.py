#!/usr/bin/env python3
"""End-to-end original-definition regression for the independent Euler-root engine.

Uses frozen verify_d5_exhaustive.matchings for INPUT generation only.
Actual accepting predicate (global sequences) comes from the separately
frozen verify_all_regular.validate. The new root-selection uses Eulerian
bipartite incidence balancing, not the old orientation implementation.
"""
from itertools import combinations
from verify_d5_exhaustive import matchings
from verify_all_regular import validate,make_order
from euler_root_edge_order import construct_euler_root_order


def test_factor(parts, d=5):
    n=sum(parts);base=[];bad=set();offset=0;V=set(range(n))
    for size in parts:
        cycle=tuple(range(offset,offset+size));offset+=size
        for j,a in enumerate(cycle):
            b=cycle[(j+1)%size];p=(min(a,b),max(a,b));base.append((*p,j%2));bad.add(p)
    counts=0
    for M2 in matchings(n,tuple(sorted(bad))):
        blocked2=bad|set(M2)
        for M3 in matchings(n,tuple(sorted(blocked2))):
            blocked3=blocked2|set(M3)
            for M4 in matchings(n,tuple(sorted(blocked3))):
                edges=base+[(a,b,2) for a,b in M2]+[(a,b,3) for a,b in M3]+[(a,b,4) for a,b in M4]
                order,certificate=construct_euler_root_order(V,edges,d)
                assert validate(V,edges,order,d)
                for C in certificate['leftover_components']:
                    assert len(set(C)-set(certificate['rootset']))>=len(C)//2
                # Original independent constructor serves only as a DIFFERENT
                # method of producing a positive order (not proof by agreement).
                legacy,_=make_order(V,edges,d)
                assert validate(V,edges,legacy,d)
                counts+=1
    return counts


def test_complete_even_graph(n):
    d=n-1;V=set(range(n));edges=[]
    for c in range(d):
        for a,b in [(n-1,c)]+[((c+i)%d,(c-i)%d) for i in range(1,n//2)]:
            edges.append((min(a,b),max(a,b),c))
    order,cert=construct_euler_root_order(V,edges,d)
    assert validate(V,edges,order,d)
    assert not validate(V,edges,order[:-1],d)
    assert len(cert['rootset'])==len(cert['cycles'])


def main():
    counts={str(p):test_factor(p) for p in ((8,),(4,4))}
    assert counts=={'(8,)':2502,'(4, 4)':3096},counts
    for n in (4,6,8,10,12):test_complete_even_graph(n)
    # Distinct invalid inputs must be rejected; no recalculating by small models.
    try:construct_euler_root_order(set(range(4)),[(0,1,0)],3)
    except AssertionError:pass
    else:raise AssertionError('invalid regularity was accepted')
    print('PASS Euler-root full-order graph certificates:',counts,
          'sum',sum(counts.values()),'complete K4,K6,K8,K10,K12 and negative control')


if __name__=='__main__':main()
