#!/usr/bin/env python3
"""Build32-bit valuation signatures with witness or explicit XOR receipt."""
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
MASK=(1<<32)-1

def sigma(x,k):
    a,b,s=((7,18,3),(17,19,10))[k]
    return (((x>>a)|(x<<(32-a)))^((x>>b)|(x<<(32-b)))^(x>>s))&MASK

ROWS=[[sum(((sigma(1<<i,k)>>j)&1)<<i for i in range(32))
       for j in range(32)] for k in (0,1)]

def solve(equations):
    basis={}
    for ordinal,(r,b) in enumerate(equations):
        selected=1<<ordinal
        while r:
            p=r.bit_length()-1
            if p in basis:
                rr,bb,old=basis[p];r^=rr;b^=bb;selected^=old
            else:basis[p]=(r,b,selected);break
        if not r and b:
            return None,[i for i in range(len(equations)) if selected>>i&1]
    witness=0
    for p,(r,b,_) in sorted(basis.items()):
        if (r&witness).bit_count()%2!=b:witness|=1<<p
    return witness,None

def case(a,b):
    eq=[(1<<j,0) for j in range(a)]+[(1<<a,1)]+[(ROWS[0][j],0) for j in range(b)]+[(ROWS[0][b],1)]
    w,c=solve(eq)
    return {'a':a,'b':b,'witness':None if w is None else f'{w:08x}','contradiction_rows':c}

if __name__=='__main__':
    cases=[case(a,b) for a in range(32) for b in range(32)]
    possible={(c['a'],c['b']) for c in cases if c['witness'] is not None}
    allowed=sorted((a,b) for a,b in possible if (b,a) in possible)
    inverse={}
    for k in (0,1):
        cols=[]
        for bit in range(32):
            v,c=solve([(ROWS[k][j],int(j==bit)) for j in range(32)])
            assert c is None and sigma(v,k)==1<<bit
            cols.append(f'{v:08x}')
        inverse[str(k)]=cols
    certificate={'schema':'CRYPTO3-support12-analytic-structure-v7',
                 'definition':{'bits':32,'f_rotations':[7,18],'f_shift':3,'g_rotations':[17,19],'g_shift':10},
                 'inverse_basis_columns':inverse,'valuation_cases':cases,
                 'necessary_transposed_signatures':[list(x) for x in allowed],
                 'half_constants':{'H':'80000000','f_H':'11002000','f_inv_H':'94857ee6',
                                   'v_f_H':13,'v_f_inv_H':1},
                 'consequences':{'maximum_sum':max(a+b for a,b in allowed),
                                 'maximum_individual':max(a for a,b in allowed),
                                 'allowed_count':len(allowed)},
                 'scope':'exact single-pair valuation signatures; transposed table is necessary, not sufficient for numerical two-pair coupling'}
    (HERE/'CERTIFICATE.json').write_text(json.dumps(certificate,indent=2,sort_keys=True)+'\n')
    print(json.dumps(certificate['consequences'],sort_keys=True))
