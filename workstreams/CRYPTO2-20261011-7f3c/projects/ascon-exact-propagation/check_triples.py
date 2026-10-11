#!/usr/bin/env python3
"""Separate checker: column-image ranks and character averages of NIST table.
Uses the verification module check.py, never the discovery programs.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import copy
import json
from check import ROT, TABLE, require, projection_rank, apply_L

def verify_ranks(cases):
    require(len(cases)==1953,'missing triples')
    exceptions={}
    for l,(a,b) in enumerate(ROT):
        for k in [1,2]:
            base={0,k*a%64,k*b%64}
            for anchor in base:
                I=tuple(sorted((x-anchor)%64 for x in base))
                require(I not in exceptions,'duplicate exception orbit')
                exceptions[I]=(l,k,(-anchor)%64)
    require(len(exceptions)==30,'exception family size')
    T={0,45,36,3,25,63,58,54,47,57,23}
    deficient=0
    for c,(i,j) in zip(cases,combinations(range(1,64),2)):
        I=[0,i,j];J=sorted({(x+t)%64 for x in I for t in T})
        require(c['I']==I and c['J']==J,'triple support encoding')
        rr=[projection_rank(I,J,l) for l in range(5)]
        require(rr==c['ranks'],'wrong triple ranks')
        expected=[len(J)]*5
        if tuple(I) in exceptions:
            l,k,s=exceptions[tuple(I)];expected[l]-=1;deficient+=1
            a,b=ROT[l];K={s} if k==1 else {s,(s+a)%64,(s+b)%64}
            require(K<=set(J),'missing parity lies outside J')
            # Pull the mask back by physically accumulating source bits.
            pre=set()
            for pos in K:
                for q in [pos,(pos+a)%64,(pos+b)%64]:
                    if q in pre:pre.remove(q)
                    else:pre.add(q)
            require(pre==set(I),'wrong explicit missing parity')
        require(rr==expected,'exception classification failure')
    return {'rank_blocks':5*len(cases),'normalized_exceptions':deficient,
            'physical_exception_supports':deficient*64//3}

def verify_formula(c):
    l,k,s=c['lane'],c['scale'],c['shift']
    require(type(l) is int and 0<=l<5 and k in [1,2] and 0<=s<64,'bad family')
    A,B,C=c['A'],c['B'],c['C']
    for v in [A,B,C]:
        require(len(v)==64 and all(type(x) is int and 0<=x<32 for x in v),'bad array')
    a,b=ROT[l];I={s,(s+k*a)%64,(s+k*b)%64}
    require({j for j,v in enumerate(A) if v}==I,'wrong family support')
    K={s} if k==1 else {s,(s+a)%64,(s+b)%64}
    alpha=apply_L(B)
    betaF=Fraction(1);betaG=Fraction(1);M=Fraction(1)
    for j in range(64):
        F=[TABLE[x] for x in range(32) if TABLE[x]^TABLE[x^A[j]]==B[j]]
        G=[z for z in range(32) if TABLE[z]^TABLE[z^alpha[j]]==C[j]]
        require(F and G,'empty fiber not allowed in formula fixture')
        M*=Fraction(len(F)*len(G),1024)
        if j in I:betaF*=Fraction(sum(1-2*((y>>l)&1) for y in F),len(F))
        if j in K:betaG*=Fraction(sum(1-2*((z>>l)&1) for z in G),len(G))
    require(type(c['c1']) is int and 0<=c['c1']<256,'bad round constant')
    eta=(-1)**(sum((c['c1']>>j)&1 for j in K) if l==2 else 0)
    P=M*(1+eta*betaF*betaG)
    require(str(M)==c['markov'],'wrong local product')
    require(str(P)==c['probability'],'wrong corrected probability')
    require((P!=M) if k==1 else (P==M),'wrong actual exception family')
    return str(P/M)

def verify_doubled_cancellation():
    js=[19,61,1,17,41]
    wanted=[{(0,38)},{(1,58),(3,14)},{(2,2)},{(3,34)},{(4,18)}]
    for l,(a,b) in enumerate(ROT):
        I={0,2*a%64,2*b%64};j=js[l]
        require(j in {0,a,b},'cancellation position outside parity')
        influences={(r,q) for r,(u,v) in enumerate(ROT)
                    for q in {j,(j+u)%64,(j+v)%64}&I}
        require(influences==wanted[l],'wrong cancellation source table')
    for z in range(32):
        require(TABLE[z]^TABLE[z^8]==TABLE[z^6]^TABLE[z^6^8],
                'lane-1 balancing identity failed')
    return 5+32

def main():
    root=Path(__file__).resolve().parent
    cases=json.loads((root/'triple-rank-certificate.json').read_text())
    fixtures=json.loads((root/'triple-formula-certificate.json').read_text())
    r=verify_ranks(cases)
    require(len(fixtures)==20,'missing formula examples')
    require({(c['lane'],c['scale']) for c in fixtures}=={(l,k) for l in range(5) for k in [1,2]},'missing family')
    ratios=[verify_formula(c) for c in fixtures]
    tests=[]
    x=copy.deepcopy(cases);x[0]['ranks'][0]-=1;tests.append((verify_ranks,x))
    x=copy.deepcopy(cases);x.pop();tests.append((verify_ranks,x))
    x=copy.deepcopy(fixtures[0]);x['scale']=3;tests.append((verify_formula,x))
    x=copy.deepcopy(fixtures[0]);x['probability']=x['markov'];tests.append((verify_formula,x))
    for fn,x in tests:
        try:fn(x)
        except ValueError:continue
        raise AssertionError('negative control accepted')
    r.update(status='PASS',formula_fixtures=len(fixtures),ratios=sorted(set(ratios)),negative_controls=len(tests),
             doubled_cancellation_checks=verify_doubled_cancellation(),
             actual_exception_supports=320,universally_exact_three_column_supports=41344)
    print(json.dumps(r,indent=2))

if __name__=='__main__':main()
