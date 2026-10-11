#!/usr/bin/env python3
"""Exact two-round Ascon trail conditioning; lane 0 is bit 0 in columns.
Integer word bits use least-significant-bit positions, right rotations.
No imported cryptanalytic code. Not an AEAD/key-recovery model.
"""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import random

W = 64
ROT = ((19,28),(61,39),(1,6),(10,17),(7,41))
MASK = (1<<64)-1

def sbox(x):
    a=[(x>>i)&1 for i in range(5)]
    a[0]^=a[4]; a[4]^=a[3]; a[2]^=a[1]
    b=[a[i]^((1^a[(i+1)%5])&a[(i+2)%5]) for i in range(5)]
    b[1]^=b[0]; b[0]^=b[4]; b[3]^=b[2]; b[2]^=1
    return sum(v<<i for i,v in enumerate(b))

def rank(rows):
    piv={}
    for x in rows:
        while x:
            i=x.bit_length()-1
            if i not in piv:
                piv[i]=x
                break
            x^=piv[i]
    return len(piv)

def linrow(l,j):
    a,b=ROT[l]
    return (1<<(64*l+j))^(1<<(64*l+(j+a)%64))^(1<<(64*l+(j+b)%64))

def diffusion(cols):
    words=[sum(((x>>l)&1)<<j for j,x in enumerate(cols)) for l in range(5)]
    out=[]
    for x,(a,b) in zip(words,ROT):
        rr=lambda n:((x>>n)|(x<<(64-n)))&MASK
        out.append(x^rr(a)^rr(b))
    return [sum(((x>>j)&1)<<l for l,x in enumerate(out)) for j in range(64)]

def hrows(alpha):
    rows=[]
    for j,a in enumerate(alpha):
        d=sbox(a)^sbox(0)
        col=[sbox(a^(1<<i))^sbox(1<<i)^d for i in range(5)]
        for l in range(5):
            row=0
            for i in range(5):
                if (col[i]>>l)&1: row^=linrow(i,j)
            rows.append(row)
    return rows

def fiber(a,b):
    return [sbox(x) for x in range(32) if sbox(x)^sbox(x^a)==b]

def analyze(A,B,C,c1=0xe1):
    """Return exact probability by eliminating all unconditioned variables.
    Cost exponential in first active-column count; bounded scout only.
    """
    I=[i for i,a in enumerate(A) if a]
    if any((not A[j]) and B[j] for j in range(64)):
        return {'probability':Fraction(0),'reason':'invalid first local transition'}
    fibers=[fiber(A[j],B[j]) for j in I]
    if any(not xs for xs in fibers):
        return {'probability':Fraction(0),'reason':'empty first fiber'}
    alpha=diffusion(B)
    H=hrows(alpha)
    # Equation D_alpha S(LY + c1)=C, with c1 only in lane 2.
    ccols=[4*((c1>>j)&1) for j in range(64)]
    rhs=[((C[j]^sbox(alpha[j]^ccols[j])^sbox(ccols[j]))>>l)&1
         for j in range(64) for l in range(5)]
    active=sum(1<<(64*l+j) for j in I for l in range(5))
    free=((1<<320)-1)^active
    piv={};constraints=[]
    for row,z in zip(H,rhs):
        while row&free:
            k=(row&free).bit_length()-1
            if k not in piv:
                piv[k]=(row,z)
                break
            r,t=piv[k];row^=r;z^=t
        else:
            if row or z:constraints.append((row,z))
    accepted=0
    for ys in product(*fibers):
        v=sum(((y>>l)&1)<<(64*l+j) for j,y in zip(I,ys) for l in range(5))
        accepted+=all(((row&v).bit_count()&1)==z for row,z in constraints)
    exact=Fraction(accepted,1<<(5*len(I)+len(piv)))
    local=Fraction(1)
    for a,b in zip(A,B):local*=Fraction(len(fiber(a,b)),32)
    for a,b in zip(alpha,C):local*=Fraction(len(fiber(a,b)),32)
    return {'probability':exact,'markov':local,'free_rank':len(piv),
            'total_rank':rank(H),'accepted_fiber_tuples':accepted,
            'fiber_sizes':[len(x) for x in fibers],
            'residual_constraints':[(hex(row),z) for row,z in constraints],
            'active_columns':I}

def support_check():
    shifts={0}|{(-x)%64 for ab in ROT for x in ab}
    results=[]
    for d in range(64):
        I={0,d};J=sorted({(j+s)%64 for j in I for s in shifts})
        free=MASK^sum(1<<i for i in I)
        rr=[]
        for l in range(5):
            rows=[(linrow(l,j)>>(64*l))&free for j in J]
            rr.append(rank(rows))
        if any(r!=len(J) for r in rr):raise AssertionError((I,J,rr))
        results.append({'I':sorted(I),'J':J,'ranks':rr})
    return results

def scout():
    rng=random.Random(20261012)
    I=[0,1,6]
    choices={b:[(a,fiber(a,b)) for a in range(1,32)
                 if fiber(a,b) and len({(y>>2)&1 for y in fiber(a,b)})==1]
             for b in range(1,32) if not b&4}
    choices={b:xs for b,xs in choices.items() if xs}
    for trial in range(1,1001):
        B=[0]*64;A=[0]*64
        for j in I:
            B[j]=rng.choice(list(choices));A[j]=rng.choice(choices[B[j]])[0]
        alpha=diffusion(B)
        C=[sbox(a)^sbox(0) for a in alpha]
        result=analyze(A,B,C)
        if result['probability']!=result['markov']:
            return {'round_constants':[0xf0,0xe1], 'A':A,'B':B,'C':C,
                    'trial':trial,'result':{k:str(v) if isinstance(v,Fraction) else v for k,v in result.items()}}
    raise AssertionError('no mismatch in bounded scout')

if __name__=='__main__':
    out=Path(__file__).resolve().parent
    ranks=support_check()
    (out/'rank-certificate.json').write_text(json.dumps(ranks,indent=2)+'\n')
    case=scout()
    (out/'mismatch-certificate.json').write_text(json.dumps(case,indent=2)+'\n')
    impossible=json.loads(json.dumps(case))
    alpha=diffusion(impossible['B'])
    impossible['C'][0]=sbox(4)^sbox(4^alpha[0])
    result=analyze(impossible['A'],impossible['B'],impossible['C'])
    impossible['result']={k:str(v) if isinstance(v,Fraction) else v for k,v in result.items()}
    impossible['construction']='Same prefix; set C[0] = D_alpha[0] S(4) to require the opposite forced value bit.'
    (out/'impossible-certificate.json').write_text(json.dumps(impossible,indent=2)+'\n')
    print(json.dumps({'support_cases':len(ranks),'mismatch':case['result'],'trial':case['trial']}))
