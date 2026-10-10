#!/usr/bin/env python3
"""Exact, stdlib-only finite regression; proof is in ../braun-bruegge-f31/PROOF.md."""
from math import comb
from itertools import product
from collections import Counter

def C(n,k): return comb(n,k) if 0<=k<=n else 0

def F(a,b,c):
    if min(a,b,c)<1 or a<b or b<c or (a-b)%2 or (b-c)%2:
        raise ValueError('ordered positive same parity required')
    return sum(C(c,j)*C(b,(b-c)//2+j)*C(a,(a-c)//2+j) for j in range(c+1))

def B(m,t): return C(m,(m+t)//2) if abs(t)<=m and (m+t)%2==0 else 0

def T(a,b,c): return sum(B(a,t)*B(b,t)*B(c,t) for t in range(-min(a,b,c),min(a,b,c)+1))

def words(a,b,c):
    def counts(m):
        d=Counter()
        for x in product((0,1),repeat=m): d[2*sum(x)-m]+=1
        return d
    x,y,z=counts(a),counts(b),counts(c)
    return sum(v*y.get(t,0)*z.get(t,0) for t,v in x.items())

def run():
    orig=brute=trans=mx=vand=0
    for s in range(3,46):
        triples=[(a,b,c) for a in range(1,s) for b in range(1,a+1)
                 for c in range(1,b+1) if a+b+c==s and (a-b)%2==0 and (b-c)%2==0]
        for a,b,c in triples:
            z=F(a,b,c);assert z==T(a,b,c)
            orig+=1
            if s<=13:assert z==words(a,b,c);brute+=1
            if c>=3:assert z<=F(a+2,b,c-2);trans+=1
            if b>=c+2:assert z<=F(a+2,b-2,c);trans+=1
        n=s-1;target=(n-1,1,1) if n%2==0 else (n-3,2,2)
        if target[0]>=target[1]>=target[2]>=1 and sum(target)==s:
            best=F(*target)
            assert all(F(*x)<=best for x in triples)
            mx+=len(triples)
    for p in range(3,30):
        for q in range(2,p+1):
            if (p-q)%2:continue
            z=sum(B(p,t)*B(q,t) for t in range(-q,q+1))
            assert z==comb(p+q,(p+q)//2)
            if q>=3:assert z==sum(B(p+2,t)*B(q-2,t) for t in range(-q,q+1))
            vand+=1
    assert F(5,5,5)==2252 and F(7,5,3)==2310
    assert sum(C(3,j)*C(5,1+j)*C(7,j) for j in range(4))==1020
    for v in [(3,4,3),(0,0,0),(2,2,1)]:
        try:F(*v)
        except ValueError:pass
        else:raise AssertionError('invalid input accepted')
    assert not (2252<=1020)
    print(f'PASS original={orig} brute={brute} transfer={trans} maxima={mx} Vandermonde={vand} negative-tests=PASS')

if __name__=='__main__':run()
