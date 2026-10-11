"""Post-disclosure review audit; root artifacts are read-only."""
import sys
sys.dont_write_bytecode=True
import importlib.util
import json
from pathlib import Path
from fractions import Fraction
from itertools import product
from independent_probe import sbox, rank, project_rows, ROTATIONS

def diffuse(columns):
    out=[]
    for j in range(64):
        value=0
        for lane,(a,b) in enumerate(ROTATIONS):
            z=0
            for off in (0,a,b):
                z^=(columns[(j+off)%64]>>(4-lane))&1
            value |= z<<(4-lane)
        out.append(value)
    return out

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
check=module('opened_check',ROOT/'check.py')
discover=module('opened_discover',ROOT/'discover.py')
rev=lambda x:int(f'{x:05b}'[::-1],2)
assert all(sbox(rev(x))==rev(check.TABLE[x])==rev(discover.sbox(x)) for x in range(32))
# Independently verify every affine derivative identity used by the optional analyzer.
for a in range(32):
    d=discover.sbox(a)^discover.sbox(0)
    columns=[discover.sbox(a^(1<<i))^discover.sbox(1<<i)^d for i in range(5)]
    for x in range(32):
        val=d
        for i in range(5):
            if (x>>i)&1:val ^= columns[i]
        assert val==discover.sbox(x)^discover.sbox(x^a)

prior=json.loads((HERE/'independent_projection_results.json').read_text())
opened_ranks=json.loads((ROOT/'rank-certificate.json').read_text())
independent=[prior['singleton']]+prior['pairs']
for own,theirs in zip(independent,opened_ranks):
    assert own['I']==theirs['I'] and own['T']==theirs['J'] and own['ranks']==theirs['ranks']
assert len(independent)==len(opened_ranks)==64

out={'sboxes_crosschecked_all_32_values':True,'affine_derivatives_crosschecked_all_1024_pairs':True,
     'all_320_certificate_ranks_match_predisclosure_results':True,'fixtures':{}}
fixtures={name:json.loads((ROOT/name).read_text()) for name in ('mismatch-certificate.json','impossible-certificate.json')}
for name,cert in fixtures.items():
    A,B,C=([rev(x) for x in cert[k]] for k in ('A','B','C'))
    I=[j for j,a in enumerate(A) if a]
    Y=[[sbox(x) for x in range(32) if sbox(x)^sbox(x^A[j])==B[j]] for j in I]
    alpha=diffuse(B);T=[j for j,a in enumerate(alpha) if a]
    ownranks=[rank(project_rows(I,T,lane)) for lane in range(5)]
    assert ownranks==[17,17,16,17,17]
    assert project_rows(I,[0],2)==[0]
    nominal=Fraction(1)
    for ys in Y:nominal*=Fraction(len(ys),32)
    second={j:[z for z in range(32) if sbox(z)^sbox(z^alpha[j])==C[j]] for j in T}
    for zs in second.values():nominal*=Fraction(len(zs),32)
    exact_by_constant={}
    for c1 in (0xe1,0xe0):
        conditional_sum=Fraction(0)
        for ys in product(*Y):
            forced=(ys[0]^ys[1]^ys[2])>>2&1
            forced^=c1&1
            p=Fraction(sum((z>>2&1)==forced for z in second[0]),16)
            for j in T:
                if j:p*=Fraction(len(second[j]),32)
            conditional_sum+=p
        exact=conditional_sum/(1<<15)
        exact_by_constant[hex(c1)]=str(exact)
        analyzed=discover.analyze(cert['A'],cert['B'],cert['C'],c1=c1)
        assert analyzed['probability']==exact and analyzed['markov']==nominal
        if c1==0xe1:
            assert str(exact)==cert['result']['probability'] and str(nominal)==cert['result']['markov']
            # Audit discovery metadata beyond the frozen checker acceptance contract.
            for key,value in analyzed.items():
                if isinstance(value,Fraction):value=str(value)
                if key=='residual_constraints':value=[list(item) for item in value]
                assert cert['result'][key]==value,(key,cert['result'][key],value)
    out['fixtures'][name]={'independent_exact_by_second_constant':exact_by_constant,
                          'independent_DDT_product':str(nominal),'all_analyzer_metadata_matches':True,
                          'checker':check.check_case(cert)}
out['original_negative_controls_passed']=check.negative_tests(opened_ranks,fixtures['mismatch-certificate.json'],fixtures['impossible-certificate.json'])
(HERE/'opened_audit_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
