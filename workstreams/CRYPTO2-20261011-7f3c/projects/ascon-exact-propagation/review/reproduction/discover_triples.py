#!/usr/bin/env python3
"""Finite discovery certificate for the complete three-column projection gate."""
from itertools import combinations
from fractions import Fraction
from pathlib import Path
import json
import random
from discover import ROT, MASK, linrow, rank, fiber, sbox, diffusion, analyze

def main():
    out=Path(__file__).resolve().parent
    T={0}|{(-x)%64 for ab in ROT for x in ab}
    cases=[]
    for i,j in combinations(range(1,64),2):
        I={0,i,j};J=sorted({(x+t)%64 for x in I for t in T})
        free=MASK^sum(1<<x for x in I)
        rr=[rank([(linrow(l,x)>>(64*l))&free for x in J]) for l in range(5)]
        cases.append({'I':sorted(I),'J':J,'ranks':rr})
    (out/'triple-rank-certificate.json').write_text(json.dumps(cases,separators=(',',':'))+'\n')
    rng=random.Random(20261012)
    fixtures=[]
    for l,(a,b) in enumerate(ROT):
        choices=[(u,v) for u in range(1,32) for v in range(1,32)
                 if (ff:=fiber(u,v)) and sum(1-2*((y>>l)&1) for y in ff)]
        for k in [1,2]:
            s=7*l
            I=sorted({s,(s+k*a)%64,(s+k*b)%64})
            K=[s] if k==1 else [s,(s+a)%64,(s+b)%64]
            selected=[]
            for trial in range(200):
                A=[0]*64;B=[0]*64
                for j in I:A[j],B[j]=rng.choice(choices)
                alpha=diffusion(B)
                C=[sbox(x)^sbox(0) for x in alpha]
                for j in K:
                    z=(trial%2)<<l
                    C[j]=sbox(z)^sbox(z^alpha[j])
                r=analyze(A,B,C)
                if k==1 and r['probability']==r['markov']:continue
                if k==2 and r['probability']!=r['markov']:
                    raise AssertionError('doubled support should have zero correction')
                selected.append({'lane':l,'scale':k,'shift':s,'c1':225,
                                 'A':A,'B':B,'C':C,
                                 'probability':str(r['probability']),
                                 'markov':str(r['markov'])})
                if len(selected)==2:break
            if len(selected)!=2:raise AssertionError(('no examples',l,k))
            fixtures.extend(selected)
    (out/'triple-formula-certificate.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    print(json.dumps({'cases':len(cases),'rank_blocks':5*len(cases),
                      'exceptional':sum(c['ranks']!=[len(c['J'])]*5 for c in cases),
                      'formula_fixtures':len(fixtures),
                      'ratios':sorted({str(Fraction(c['probability'])/Fraction(c['markov'])) for c in fixtures})}))

if __name__=='__main__':main()
