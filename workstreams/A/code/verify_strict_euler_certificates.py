#!/usr/bin/env python3
"""Audits the exact Euler-root construction, not just its final edge order.

Source discovery code is used for witness generation only. The separately
implemented check_strict() rederives the entire witness from the input graph,
checks canonical components/roots and literal adjacency sequences, then
compares every edge in the proposed order. All negative controls must fail.
"""
import copy
from random import Random
from verify_d5_exhaustive import matchings
from euler_root_edge_order import construct_euler_root_order
from check_euler_order_certificate import check_certificate as old_checker
from check_euler_order_certificate_strict import check_strict


def factor_cases(parts):
    n=sum(parts);base=[];blocked=set();offset=0
    for m in parts:
        C=list(range(offset,offset+m));offset+=m
        for i,u in enumerate(C):
            v=C[(i+1)%m];p=(min(u,v),max(u,v))
            base.append((*p,i%2));blocked.add(p)
    for m2 in matchings(n,tuple(sorted(blocked))):
        bad2=blocked|set(m2)
        for m3 in matchings(n,tuple(sorted(bad2))):
            bad3=bad2|set(m3)
            for m4 in matchings(n,tuple(sorted(bad3))):
                yield base+[(u,v,2) for u,v in m2]+[(u,v,3) for u,v in m3]+[(u,v,4) for u,v in m4]


def factorisation(n):
    assert n%2==0
    d=n-1;C=[]
    for colour in range(d):
        C.append([(n-1,colour)]+[((colour+j)%d,(colour-j)%d) for j in range(1,n//2)])
    return C


def random_regular_cases():
    rng=Random(26091010)
    for n in (4,6,8,10,12,14,16):
        factors=factorisation(n)
        for d in range(3,n):
            for _ in range(12):
                perm=list(range(n));rng.shuffle(perm)
                fs=list(factors);rng.shuffle(fs)
                colour_perm=list(range(d));rng.shuffle(colour_perm)
                edges=[]
                for col,matching in enumerate(fs[:d]):
                    for a,b in matching:
                        a,b=perm[a],perm[b]
                        edges.append((min(a,b),max(a,b),colour_perm[col]))
                rng.shuffle(edges)
                yield set(range(n)),edges,d


def invalid_mutations():
    n=6;d=n-1
    V=set(range(n));E=[]
    for colour,matching in enumerate(factorisation(n)):
        for a,b in matching:
            E.append((min(a,b),max(a,b),colour))
    O,C=construct_euler_root_order(V,E,d)
    assert check_strict(V,E,d,O,C)[0]
    bad=[]
    bad.append(('missing edge', E, O[:-1], C))
    bad.append(('duplicate order edge', E, O+[O[0]], C))
    X=copy.deepcopy(C);X['rootset']=[];bad.append(('bad roots',E,O,X))
    X=copy.deepcopy(C);X['cycles'][0]=X['cycles'][0][1:]+X['cycles'][0][:1]
    bad.append(('rotated cycle still a set',E,O,X))
    X=copy.deepcopy(C);X['blue_component_margins']=[0]
    bad.append(('false margin',E,O,X))
    X=copy.deepcopy(C);X['two_colour_map']={x:0 for x in V}
    bad.append(('false split',E,O,X))
    X=copy.deepcopy(C);X['ordered_roots']=list(reversed(X['ordered_roots']))
    if X['ordered_roots']!=C['ordered_roots']:
        bad.append(('root order changed',E,O,X))
    X=copy.deepcopy(C);X['leftover_components']=[[v] for v in V]
    bad.append(('fake Q components',E,O,X))
    bad.append(('recolouring an old edge',[(a,b,(c+1)%d if i==0 else c) for i,(a,b,c) in enumerate(E)],O,C))
    # A semantic valid-order swap of adjacent DISJOINT edges. The old checker
    # accepts this because it only verifies endpoint sequences. The STRICT
    # checker must reject it as NOT the algorithm specified by the certificate.
    found=False
    for j in range(len(O)-1):
        if set(O[j][:2]).isdisjoint(O[j+1][:2]):
            Z=O.copy();Z[j],Z[j+1]=Z[j+1],Z[j]
            if old_checker(V,E,d,Z,C):
                bad.append(('valid but non-certified order',E,Z,C))
                found=True
                break
    assert found, 'must exhibit valid-order mutation missed by weak verifier'
    for label,es,order,cert in bad:
        valid,reason=check_strict(V,es,d,order,cert)
        if valid:raise AssertionError((label,'strict checker accepted invalid claim'))
    return len(bad)


def main():
    counts={}
    for parts in ((8,),(4,4)):
        c=0;V=set(range(sum(parts)))
        for E in factor_cases(parts):
            out,C=construct_euler_root_order(V,E,5)
            ok,why=check_strict(V,E,5,out,C)
            assert ok,(parts,c,why)
            c+=1
        counts[str(parts)]=c
    assert counts=={'(8,)':2502,'(4, 4)':3096},counts
    sampled=0
    for V,E,d in random_regular_cases():
        out,C=construct_euler_root_order(V,E,d)
        ok,why=check_strict(V,E,d,out,C)
        assert ok,(d,len(V),why)
        sampled+=1
    nfail=invalid_mutations()
    print('PASS strict algorithm-reconstruction certificate checking:',counts,
          'total',sum(counts.values()))
    print('PASS independent random regular graph/colouring samples:',sampled)
    print('PASS rejected malicious or non-certified proofs:',nfail,
          '(including a valid order accepted by the weaker verifier)')

if __name__=='__main__':main()
