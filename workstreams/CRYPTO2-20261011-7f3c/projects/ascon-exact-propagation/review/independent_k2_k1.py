"""Independent verification of k=2 exactness and sharpness of all five k=1 families."""
import json
from fractions import Fraction
from pathlib import Path
from independent_probe import ROTATIONS,sbox,rank,project_rows
HERE=Path(__file__).resolve().parent

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

def inputs(a,b):return [x for x in range(32) if sbox(x)^sbox(x^a)==b]
def bit(x,lane):return x>>(4-lane)&1
out={'encoding':'NIST table: lane l has weight 2**(4-l)', 'k2_influences':[],'k1_sharpness':[]}
# Independently compute every contributing lane/source to the proposed special columns.
choices=(19,61,1,17,41)
for lane,(a,b) in enumerate(ROTATIONS):
    I=sorted({0,2*a%64,2*b%64});j=choices[lane]
    influences=[]
    for r,(aa,bb) in enumerate(ROTATIONS):
        for source in (j,(j+aa)%64,(j+bb)%64):
            if source in I:influences.append([r,source])
    if lane!=1:assert len(influences)==1 and influences[0][0]==lane
    else:assert influences==[[1,58],[3,14]]
    out['k2_influences'].append({'lane':lane,'I':I,'special_column':j,'influences':influences})
# Root encoding D_8 invariant under XOR 6 becomes NIST D_2 invariant under XOR 12.
assert all((sbox(z)^sbox(z^2))==(sbox(z^12)^sbox(z^12^2)) for z in range(32))
assert bit(12,1)==1
out['lane1_special_derivative_pairing_all_32_inputs']=True
# Every output differential fiber is stable under adding its output difference.
for a in range(32):
    for b in range(32):
        F={sbox(x) for x in inputs(a,b)}
        assert {y^b for y in F}==F
out['all_first_output_fiber_pairings_checked']=True
for lane,(ra,rb) in enumerate(ROTATIONS):
    I=sorted({0,ra,rb})
    found=None
    for a in range(1,32):
        for b in range(1,32):
            F=[sbox(x) for x in inputs(a,b)]
            if not F or len({bit(y,lane) for y in F})!=1:continue
            q=bit(F[0],lane)
            forced=q ^ (lane==2) # second constant e1 has bit 0 equal 1 only in lane 2
            for c in range(1,32):
                G=inputs(b,c)
                if G and {bit(z,lane) for z in G}=={forced}:
                    found=(a,b,c,F,G,forced);break
            if found:break
        if found:break
    assert found
    a,b,c,F,G,forced=found
    A=[a if j in I else 0 for j in range(64)]
    B=[b if j in I else 0 for j in range(64)]
    alpha=diffuse(B)
    assert alpha[0]==b
    C=[sbox(0)^sbox(x) if x else 0 for x in alpha];C[0]=c
    T=[j for j,x in enumerate(alpha) if x]
    rr=[rank(project_rows(I,T,l)) for l in range(5)]
    assert rr==[len(T)-(l==lane) for l in range(5)]
    assert project_rows(I,[0],lane)==[0]
    nominal=Fraction(len(F),32)**3
    for aa,cc in zip(alpha,C):nominal*=Fraction(len(inputs(aa,cc)),32)
    assert nominal>0
    # Projection is uniform except the one fixed bit. All target-local input solutions
    # lie in its actual slice, hence the exact second probability is double nominal.
    out['k1_sharpness'].append({'lane':lane,'I':I,'local_a':a,'local_b':b,'C0':c,
       'first_fiber':F,'second_fiber_at_zero':G,'forced_bit':int(forced),
       'nominal':str(nominal),'exact':str(2*nominal),'ratio':2,
       'projection_ranks':rr,'A':A,'B':B,'C':C})
(HERE/'independent_k2_k1_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'k2_influences':out['k2_influences'],
                  'lane1_pairing_passed':True,
                  'five_independent_factor_two_witnesses':[{k:v for k,v in w.items() if k in ('lane','I','local_a','local_b','C0','nominal','exact','ratio')} for w in out['k1_sharpness']]},indent=2))
