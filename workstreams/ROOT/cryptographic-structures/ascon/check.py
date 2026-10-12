#!/usr/bin/env python3
"""Exact checker copied from the frozen source: NIST lookup table and
free-column physical bit images. The computation is unchanged.
It imports no discovery program; this copy is not a new independent implementation."""
from fractions import Fraction
import copy
import json
from pathlib import Path

NIST_TABLE=[4,11,31,20,26,21,9,2,27,5,8,18,29,3,6,28,
            30,19,7,14,0,13,17,24,16,12,1,25,22,10,15,23]
ROT=((19,28),(61,39),(1,6),(10,17),(7,41))

def rev5(x):
    return int(format(x,'05b')[::-1],2)

TABLE=[rev5(NIST_TABLE[rev5(x)]) for x in range(32)]

def require(b,msg):
    if not b:raise ValueError(msg)

def column_rank(images):
    basis={}
    for v in images:
        while v:
            p=(v&-v).bit_length()-1
            if p in basis:v^=basis[p]
            else:
                basis[p]=v
                break
    return len(basis)

def projection_rank(I,J,l):
    a,b=ROT[l]
    images=[]
    for k in range(64):
        if k in I:continue
        # Follow a single physical input bit through right rotations.
        places={k,(k-a)%64,(k-b)%64}
        images.append(sum((j in places)<<t for t,j in enumerate(J)))
    return column_rank(images)

def check_rank_cases(cases):
    require(len(cases)==64,'missing support case')
    offsets={0,45,36,3,25,63,58,54,47,57,23}
    for d,c in enumerate(cases):
        I=sorted({0,d})
        J=sorted({(i+s)%64 for i in I for s in offsets})
        require(c['I']==I and c['J']==J,'bad support encoding')
        ranks=[projection_rank(I,J,l) for l in range(5)]
        require(c['ranks']==ranks,'rank claim mismatch')
        require(ranks==[len(J)]*5,'projection is not onto')
    return 64*5

def apply_L(B):
    C=[0]*64
    for k,bits in enumerate(B):
        for l,(a,b) in enumerate(ROT):
            if bits&(1<<l):
                for j in [k,(k-a)%64,(k-b)%64]:C[j]^=1<<l
    return C

def check_case(c):
    A,B,C=c['A'],c['B'],c['C']
    for v in [A,B,C]:
        require(len(v)==64 and all(type(x) is int and 0<=x<32 for x in v),'bad columns')
    require(c['round_constants']==[240,225],'not the pinned two constants')
    I=[j for j in range(64) if A[j]]
    require(I==[0,1,6],'fixture scope')
    require(not any(B[j] for j in range(64) if j not in I),'unexpected active B')
    Y=[]
    for j in I:
        xs=[x for x in range(32) if TABLE[x]^TABLE[x^A[j]]==B[j]]
        require(xs,'empty first fiber')
        Y.append([TABLE[x] for x in xs])
    alpha=apply_L(B);J=[j for j,a in enumerate(alpha) if a]
    require(J==[0,1,3,6,24,25,36,37,42,45,46,47,48,51,54,55,58],'fixture J')
    require(not any(C[j] for j in range(64) if j not in J),'invalid inactive output')
    ranks=[projection_rank(I,J,l) for l in range(5)]
    require(ranks==[17,17,16,17,17],'unexpected projection dimensions')
    # Lane 2 at position 0 has source positions {0,1,6}, all fixed.
    # The other 84 projected coordinates are jointly uniform: rank 84,
    # and this particular coordinate has zero image from every free bit.
    require({0,ROT[2][0],ROT[2][1]}==set(I),'bad fixed-coordinate support')
    second={j:[z for z in range(32) if TABLE[z]^TABLE[z^alpha[j]]==C[j]] for j in J}
    markov=Fraction(1)
    for ys in Y:markov*=Fraction(len(ys),32)
    for j in J:markov*=Fraction(len(second[j]),32)
    # Direct enumeration of all 16 first-fiber assignments, followed by
    # exact 32-entry second-box counts. No affine-derivative assumption.
    conditional_sum=Fraction(0)
    tuples=0
    for y0 in Y[0]:
        for y1 in Y[1]:
            for y6 in Y[2]:
                tuples+=1
                forced=((y0^y1^y6)>>2)&1
                forced^=c['round_constants'][1]&1
                prob=Fraction(sum(((z>>2)&1)==forced for z in second[0]),16)
                for j in J:
                    if j:prob*=Fraction(len(second[j]),32)
                conditional_sum+=prob
    exact=conditional_sum/(1<<15)
    require(str(exact)==c['result']['probability'],'exact probability claim wrong')
    require(str(markov)==c['result']['markov'],'DDT product claim wrong')
    return {'exact':str(exact),'DDT_product':str(markov),
            'first_fiber_tuples':tuples,'projection_ranks':ranks,
            'ratio':str(exact/markov)}

def negative_tests(ranks,good,bad):
    trials=[]
    x=copy.deepcopy(ranks);x[0]['ranks'][0]-=1
    trials.append((check_rank_cases,x))
    x=copy.deepcopy(ranks);x.pop()
    trials.append((check_rank_cases,x))
    for source,change in [(good,lambda x:x['result'].update(probability=x['result']['markov'])),
                          (bad,lambda x:x['result'].update(probability=x['result']['markov'])),
                          (good,lambda x:x['round_constants'].__setitem__(1,224)),
                          (good,lambda x:x['A'].__setitem__(0,32)),
                          (good,lambda x:x['C'].__setitem__(2,1))]:
        x=copy.deepcopy(source);change(x);trials.append((check_case,x))
    for fn,x in trials:
        try:fn(x)
        except ValueError:continue
        raise AssertionError('negative control accepted')
    return len(trials)

if __name__=='__main__':
    p=Path(__file__).resolve().parent
    read=lambda name:json.loads((p/name).read_text())
    ranks=read('rank-certificate.json')
    good=read('mismatch-certificate.json');bad=read('impossible-certificate.json')
    checks=check_rank_cases(ranks)
    print(json.dumps({'status':'PASS','rank_blocks':checks,
                      'positive':check_case(good),'impossible':check_case(bad),
                      'negative_controls':negative_tests(ranks,good,bad)},indent=2))
