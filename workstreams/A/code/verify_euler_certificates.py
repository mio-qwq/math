#!/usr/bin/env python3
"""Adversarial unit plus full d=5 exhaustive certificate replay."""
from verify_d5_exhaustive import matchings
from euler_root_edge_order import construct_euler_root_order
from check_euler_order_certificate import check_certificate


def check_factors(parts):
    n=sum(parts);B=[];forbidden=set();offset=0;V=set(range(n));count=0
    for length in parts:
        C=list(range(offset,offset+length));offset+=length
        for i,u in enumerate(C):
            v=C[(i+1)%length];p=(min(u,v),max(u,v))
            B.append((*p,i%2));forbidden.add(p)
    for M2 in matchings(n,tuple(sorted(forbidden))):
        F2=forbidden|set(M2)
        for M3 in matchings(n,tuple(sorted(F2))):
            F3=F2|set(M3)
            for M4 in matchings(n,tuple(sorted(F3))):
                E=B+[(u,v,2) for u,v in M2]+[(u,v,3) for u,v in M3]+[(u,v,4) for u,v in M4]
                out,cert=construct_euler_root_order(V,E,5)
                assert check_certificate(V,E,5,out,cert)
                count+=1
    return count


def adversarial():
    V=set(range(4));E=[(0,1,0),(2,3,0),(0,2,1),(1,3,1),(0,3,2),(1,2,2)]
    O,C=construct_euler_root_order(V,E,3)
    assert check_certificate(V,E,3,O,C)
    assert not check_certificate(V,E,3,O[:-1],C)
    assert not check_certificate(V,E,3,O+[O[0]],C)
    from copy import deepcopy
    B=deepcopy(C);B['rootset']=[]
    assert not check_certificate(V,E,3,O,B)
    B=deepcopy(C);B['leftover_components']=[[0],[1],[2],[3]]
    assert not check_certificate(V,E,3,O,B)
    B=deepcopy(C);B['blue_component_margins']=[0]
    assert not check_certificate(V,E,3,O,B)
    B=deepcopy(C);B['two_colour_map']={x:0 for x in V}
    assert not check_certificate(V,E,3,O,B)
    print('PASS six deliberately damaged original-definition witness variants')


def main():
    counts={str(parts):check_factors(parts) for parts in ((8,),(4,4))}
    assert counts=={'(8,)':2502,'(4, 4)':3096}
    adversarial()
    print('PASS independent certificate checker:',counts,'total',sum(counts.values()))

if __name__=='__main__':main()
