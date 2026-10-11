"""Independent reconstruction from NIST SP 800-232 Section 3, no discovery imports."""
import json
from itertools import combinations
from pathlib import Path
ROTATIONS=((19,28),(61,39),(1,6),(10,17),(7,41))
TABLE=(0x04,0x0b,0x1f,0x14,0x1a,0x15,0x09,0x02,
       0x1b,0x05,0x08,0x12,0x1d,0x03,0x06,0x1c,
       0x1e,0x13,0x07,0x0e,0x00,0x0d,0x11,0x18,
       0x10,0x0c,0x01,0x19,0x16,0x0a,0x0f,0x17)
def sbox(v):
    x0,x1,x2,x3,x4=[(v>>(4-i))&1 for i in range(5)]
    y0=x4*x1 ^ x3 ^ x2*x1 ^ x2 ^ x1*x0 ^ x1 ^ x0
    y1=x4 ^ x3*x2 ^ x3*x1 ^ x3 ^ x2*x1 ^ x2 ^ x1 ^ x0
    y2=x4*x3 ^ x4 ^ x2 ^ x1 ^ 1
    y3=x4*x0 ^ x4 ^ x3*x0 ^ x3 ^ x2 ^ x1 ^ x0
    y4=x4*x1 ^ x4 ^ x3 ^ x1*x0 ^ x1
    return sum(y<<(4-i) for i,y in enumerate((y0,y1,y2,y3,y4)))
assert tuple(map(sbox,range(32)))==TABLE
assert len(set(TABLE))==32

def rank(rows):
    piv={}
    for row in rows:
        while row:
            j=row.bit_length()-1
            if j in piv: row ^= piv[j]
            else: piv[j]=row; break
    return len(piv)

def envelope(I):
    return sorted({(i-r)%64 for i in I for pair in ROTATIONS for r in (0,*pair)})
def project_rows(I,T,lane):
    a,b=ROTATIONS[lane]
    mask=((1<<64)-1)^sum(1<<i for i in I)
    return [((1<<j)^(1<<((j+a)%64))^(1<<((j+b)%64))) & mask for j in T]
def check(I):
    T=envelope(I)
    ranks=[rank(project_rows(I,T,lane)) for lane in range(5)]
    return {'I':I,'T':T,'rows_per_lane':len(T),'ranks':ranks,'deficiency':sum(len(T)-r for r in ranks)}

if __name__=='__main__':
    singleton=check([0])
    pairs=[check([0,j]) for j in range(1,64)]
    triples=[check([0,*ab]) for ab in combinations(range(1,64),2)]
    bad=[c for c in triples if c['deficiency']]
    out={'source':'NIST SP 800-232, Section 3, equations (7)-(12), Table 6',
         'sbox_equations_match_all_32_table_values':True,
         'rotations':ROTATIONS,'singleton':singleton,
         'pairs':pairs,
         'normalized_triples_checked':len(triples),
         'normalized_triples_with_deficiency':len(bad),
         'triple_deficiency_histogram':{str(d):sum(c['deficiency']==d for c in triples) for d in sorted({c['deficiency'] for c in triples})},
         'deficient_triples':bad}
    path=Path(__file__).with_name('independent_projection_results.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'singleton':singleton,'pair_failures':[c for c in pairs if c['deficiency']],
                      'pair_count':len(pairs),'triple_deficiency_histogram':out['triple_deficiency_histogram'],
                      'first_deficient_triples':bad[:5]},indent=2))
