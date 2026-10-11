"""Independent post-disclosure audit of all triple certificate entries."""
import json
from pathlib import Path
from fractions import Fraction
from collections import Counter
from independent_probe import sbox,check,ROTATIONS
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
rev=lambda x:int(f'{x:05b}'[::-1],2)

def diffuse(cols):
    out=[]
    for j in range(64):
        z=0
        for lane,(a,b) in enumerate(ROTATIONS):
            bit=0
            for off in (0,a,b):bit^=(cols[(j+off)%64]>>(4-lane))&1
            z|=bit<<(4-lane)
        out.append(z)
    return out

ranks=json.loads((ROOT/'triple-rank-certificate.json').read_text())
for case in ranks:
    own=check(case['I'])
    assert own['T']==case['J'] and own['ranks']==case['ranks']
fixtures=json.loads((ROOT/'triple-formula-certificate.json').read_text())
records=[]
for c in fixtures:
    l,k,s=c['lane'],c['scale'],c['shift'];a,b=ROTATIONS[l]
    I={s,(s+k*a)%64,(s+k*b)%64}
    K={s} if k==1 else {s,(s+a)%64,(s+b)%64}
    A,B,C=([rev(x) for x in c[key]] for key in ('A','B','C'))
    assert {j for j,x in enumerate(A) if x}==I
    alpha=diffuse(B)
    betaF=Fraction(1);betaG=Fraction(1);nominal=Fraction(1)
    for j in range(64):
        F=[sbox(x) for x in range(32) if sbox(x)^sbox(x^A[j])==B[j]]
        G=[z for z in range(32) if sbox(z)^sbox(z^alpha[j])==C[j]]
        assert F and G
        nominal*=Fraction(len(F)*len(G),1024)
        if j in I:betaF*=Fraction(sum(1-2*(y>>(4-l)&1) for y in F),len(F))
        if j in K:betaG*=Fraction(sum(1-2*(z>>(4-l)&1) for z in G),len(G))
    eta=(-1)**(sum(c['c1']>>j&1 for j in K) if l==2 else 0)
    exact=nominal*(1+eta*betaF*betaG)
    assert str(exact)==c['probability'] and str(nominal)==c['markov']
    assert (exact!=nominal) if k==1 else (exact==nominal)
    records.append({'lane':l,'k':k,'betaF':str(betaF),'betaG':str(betaG),
                    'eta':eta,'ratio':str(exact/nominal),'nominal':str(nominal),'exact':str(exact)})
counts=Counter((r['lane'],r['k']) for r in records)
assert counts=={(l,k):2 for l in range(5) for k in (1,2)}
result={'all_9765_rank_claims_independently_recomputed':True,
        'all_20_formula_claims_independently_recomputed_from_NIST_polynomials':True,
        'exactly_two_fixtures_per_lane_and_scale':True,'formula_records':records}
(HERE/'extension_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='formula_records'},indent=2))
