#!/usr/bin/env python3
"""Independent sigma0 anti-cycle high-signed-power exclusion.

Reviewer notation: a=d26=d42, b=d18=d34, pairs P at18 and Q at26.
Their input/sigma0 derivatives are (b,-a),(a,-b). No author imports.
"""
import datetime
import hashlib
import json
import pathlib

HERE=pathlib.Path(__file__).resolve().parent
N=1<<32
M=N-1

def rot(x,r):return ((x>>r)|(x<<(32-r)))&M

def f(x):return rot(x,7)^rot(x,18)^(x>>3)

def inverse_rows():
    original=[sum(1<<i for i in range(32) if f(1<<i)>>j&1) for j in range(32)]
    rows=[r|(1<<(32+j)) for j,r in enumerate(original)]
    for column in range(32):
        candidates=[j for j in range(column,32) if rows[j]>>column&1]
        assert candidates,'sigma0 matrix not invertible'
        pivot=candidates[0];rows[column],rows[pivot]=rows[pivot],rows[column]
        for j in range(32):
            if j!=column and rows[j]>>column&1:rows[j]^=rows[column]
    assert all(r&M==1<<j for j,r in enumerate(rows))
    return original,[r>>32 for r in rows]

def finv(x,rows):
    return sum(((r&x).bit_count()%2)<<j for j,r in enumerate(rows))

def interval(k,e):return ((1<<(e-k+1))-1)<<k

def bridge():
    source=HERE.parent/'supports-v2.json'
    S=set(json.loads(source.read_text())['supports'][12])
    templates={18:{'d18':1,'d11':-1},34:{'d34':1,'d18':-1},
               42:{'d42':1,'d26':-1},33:{'d26':-1,'F18':-1},
               41:{'d34':-1,'F26':-1},49:{'d42':-1,'F34':-1}}
    checked=[]
    for t,wanted in templates.items():
        row={kind+str(i):c for kind,i,c in [('d',t,1),('G',t-2,-1),
              ('d',t-7,-1),('F',t-15,-1),('d',t-16,-1)] if i in S}
        assert row==wanted,(t,row,wanted)
        checked.append({'t':t,'row':row})
    assert {18,26,34,42}<=S
    return {'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'reviewer_symbols':{'a':'d26=d42','b':'d18=d34=d11'},
            'actual_pairs':{'P':18,'Q':26},'rows':checked}

def run():
    original,inv=inverse_rows()
    for j in range(32):
        assert f(finv(1<<j,inv))==1<<j
        assert finv(f(1<<j),inv)==1<<j
    table=[]
    for k in range(22,32):
        possible={q^((q+1)&((1<<(32-k))-1)) for q in range(1<<(32-k))}
        expected={interval(k,e)>>k for e in range(k,32)}
        assert possible==expected
        inverse_cases=[]
        for e in range(k,32):
            alpha=interval(k,e)
            beta=f(alpha)
            # f is XOR-linear, so any derivative on that mask is divisible
            # by 2^(k-18): its low k-18 output bits cannot change.
            assert beta&((1<<(k-18))-1)==0
            inverse_alpha=finv(alpha,inv)
            assert inverse_alpha&((1<<(k-18))-1)!=0
            lowest=(inverse_alpha&-inverse_alpha).bit_length()-1
            inverse_cases.append({'end':e,'output_mask':f'{alpha:08x}',
                                  'inverse_input_mask':f'{inverse_alpha:08x}',
                                  'contradicting_low_bit':lowest,
                                  'required_equal_low_bits':k-18})
        # The e=31 case explicitly includes modular wraparound and either top base bit.
        wrapped=N-(1<<k)
        assert wrapped^((wrapped+(1<<k))&M)==interval(k,31)
        table.append({'k':k,'complete_masks':len(possible),'inverse_cases':inverse_cases})
    # Corrupt an inverse row and reject its composition on an original basis vector.
    wrong=list(inv);wrong[0]^=1
    assert f(finv(1,wrong))!=1
    # A true inverse image exists; the engine is not rejecting every nonzero word.
    assert finv(f(0x12345678),inv)==0x12345678
    assert f(0)!=((f(M)+f(1))&M)
    return {'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'scope':'two actual sigma0 derivative pairs (b,-a),(a,-b) forbid any a or b equal +/-2^k,22<=k<=31',
            'bridge':bridge(),'sigma0_rows':[f'{r:08x}' for r in original],
            'inverse_rows':[f'{r:08x}' for r in inv],
            'both_inverse_compositions_basis_vectors':64,
            'high_power_exponents':list(range(22,32)),
            'complete_inverse_masks':sum(len(x['inverse_cases']) for x in table),
            'table':table,'controls':['wrong inverse row rejected',
                 'actual word inverse accepted','ordinary sigma0 addition linearity rejected',
                 'positive addition wrap atbit31 included'],
            'negative_orientation':'simultaneously swap both actual pairs; both a,b negate',
            'member_exchange':'anti-cycle invariant under exchanging P and Q (and a,b)'}

if __name__=='__main__':
    data=run()
    (HERE/'INDEPENDENT_RUN.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':data['status'],'inverse_mask_cases':data['complete_inverse_masks'],
                      'scope':data['scope']}))
