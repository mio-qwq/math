"""Independent exact three-column counterexample; generic GF(2) projection only."""
from fractions import Fraction
import json
from pathlib import Path
from independent_probe import sbox, ROTATIONS, rank, project_rows

def ddt(a,b): return sum(sbox(x)^sbox(x^a)==b for x in range(32))
def diffuse(columns):
    out=[]
    for j in range(64):
        value=0
        for lane,(a,b) in enumerate(ROTATIONS):
            z=0
            for off in (0,a,b): z^=(columns[(j+off)%64]>>(4-lane))&1
            value |= z<<(4-lane)
        out.append(value)
    return out

def record(frac):
    return {'numerator':frac.numerator,'denominator':frac.denominator,
            'power_of_two_exponent':-(frac.denominator.bit_length()-1) if frac.numerator==1 else None}

I=[0,1,6]
A=[2 if j in I else 0 for j in range(64)]
B=[25 if j in I else 0 for j in range(64)]
alpha=diffuse(B)
T=[j for j in range(64) if alpha[j]]
first_x=[x for x in range(32) if sbox(x)^sbox(x^2)==25]
first_y=[sbox(x) for x in first_x]
assert len(first_x)==4 and all(y&4 for y in first_y)
# Every free-source matrix has full row rank except lane 2, row j=0.
# That row is identically zero after deleting I={0,1,6}; all other rows are independent.
for lane in range(5):
    rows=project_rows(I,T,lane)
    if lane==2:
        assert rows[T.index(0)]==0
        assert rank(rows)==len(T)-1
        assert rank([r for j,r in zip(T,rows) if j!=0])==len(T)-1
    else: assert rank(rows)==len(T)
# With second constant e1, bit 0 is 1. Therefore Z_(2,0)=1^1^1^1=0.
assert (0xe1&1)==1
z20=1^1^1^(0xe1&1)
assert z20==0

results=[]
for c0 in (3,6):
    C=[sbox(0)^sbox(a) if a else 0 for a in alpha]
    C[0]=c0
    first_probability=Fraction(1)
    nominal_second=Fraction(1)
    actual_second=Fraction(1)
    details=[]
    for j in range(64):
        first_probability*=Fraction(ddt(A[j],B[j]),32)
        count=ddt(alpha[j],C[j])
        nominal_second*=Fraction(count,32)
        if j==0:
            allowed=[z for z in range(32) if (z>>2&1)==z20]
            good=[z for z in allowed if sbox(z)^sbox(z^alpha[j])==C[j]]
            actual_second*=Fraction(len(good),16)
        else: actual_second*=Fraction(count,32)
        if alpha[j]: details.append({'column':j,'alpha':alpha[j],'C':C[j],'DDT':count})
    nominal=first_probability*nominal_second
    actual=first_probability*actual_second
    assert nominal>0
    assert actual==(0 if c0==3 else 2*nominal)
    results.append({'special_C0':c0,'C':C,'second_transition_details':details,
                    'nominal_DDT_product':record(nominal),'actual_joint_path_probability':record(actual),
                    'actual_over_nominal':record(actual/nominal)})

out={'source':'NIST SP 800-232 Section 3',
     'bit_convention':'Column integer x = 16*x0+8*x1+4*x2+2*x3+x4; column j is word bit 2**j',
     'first_constant_lane2':'0xf0','second_constant_lane2':'0xe1',
     'first_active_columns':I,'A':A,'B':B,'alpha':alpha,'second_active_columns':T,
     'first_local_input_solutions':first_x,'first_local_output_values':first_y,
     'fixed_first_output_lane2_bit':1,
     'projection_ranks':[rank(project_rows(I,T,lane)) for lane in range(5)],
     'number_second_active_columns':len(T),'fixed_second_input_lane2_column0':z20,
     'proof_of_probability':'Conditionally on first path, all 105 active second-input bits except Z_(2,0) are jointly uniform and independent; Z_(2,0)=0. Generic free-column projection ranks and zero row establish this exactly.',
     'witnesses':results}
Path(__file__).with_name('independent_witness_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'first_local_solutions':first_x,'first_local_outputs':first_y,
                 'projection_ranks':out['projection_ranks'],
                 'witnesses':[{k:v for k,v in w.items() if k not in ('C','second_transition_details')} for w in results]},indent=2))
