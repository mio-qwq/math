#!/usr/bin/env python3
"""Small direct checker: actual positive masks and XOR contradictions.

No solver, no Gaussian elimination, no import of certificate builder.
Author validation is not an independent-agent receipt.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
MASK=(1<<32)-1

def need(b,message):
    if not b:raise ValueError(message)

def row(k,j):
    a,b,s=((7,18,3),(17,19,10))[k]
    r=(1<<((j+a)%32))^(1<<((j+b)%32))
    if j+s<32:r^=1<<(j+s)
    return r

def image(x,k):return sum(((row(k,j)&x).bit_count()%2)<<j for j in range(32))
def valuation(x):return (x&-x).bit_length()-1 if x else 32

def recurrences(supports):
    checks=[]
    for index,shift in ((12,0),(6,1),(7,3),(13,2)):
        S=set(supports[index]);eqs={}
        for t in range(16,64):
            eqs[t]={(k,i):c for k,i,c in [('d',t,1),('g',t-2,-1),('d',t-7,-1),
                         ('f',t-15,-1),('d',t-16,-1)] if i in S}
        first={v:-c for v,c in eqs[33+shift].items()}
        need(first=={('d',26+shift):1,('f',18+shift):1},'d26+F18 original row')
        sums={}
        for t in (34+shift,41+shift):
            for v,c in eqs[t].items():sums[v]=sums.get(v,0)-c
        sums={v:c for v,c in sums.items() if c}
        need(sums=={('d',18+shift):1,('f',26+shift):1},'F26+d18 original rows')
        checks.append({'support':index,'shift':shift,'original_t':[33+shift,34+shift,41+shift]})
    return checks

def verify(cert,supports):
    need(cert['definition']=={'bits':32,'f_rotations':[7,18],'f_shift':3,
                             'g_rotations':[17,19],'g_shift':10},'word definition')
    for k in (0,1):
        cols=cert['inverse_basis_columns'][str(k)]
        need(len(cols)==32,'inverse basis column coverage')
        for j,col in enumerate(cols):need(image(int(col,16),k)==1<<j,'inverse basis identity')
    indexed={(c['a'],c['b']):c for c in cert['valuation_cases']}
    need(len(indexed)==len(cert['valuation_cases'])==1024,'all1024 valuation cases')
    need(set(indexed)==set((a,b) for a in range(32) for b in range(32)),'valuation grid coverage')
    possible=set();negative=0
    for (a,b),case in indexed.items():
        eqs=[(1<<j,0) for j in range(a)]+[(1<<a,1)]+[(row(0,j),0) for j in range(b)]+[(row(0,b),1)]
        if case['witness'] is not None:
            x=int(case['witness'],16)
            need(case['contradiction_rows'] is None and 0<x<=MASK,'actual nonzero mask witness')
            need(valuation(x)==a and valuation(image(x,0))==b,'actual valuation witness')
            possible.add((a,b))
        else:
            selection=case['contradiction_rows']
            need(selection and len(selection)==len(set(selection)),'nonempty distinct contradiction rows')
            coeff=rhs=0
            for j in selection:
                need(0<=j<len(eqs),'original row index')
                r,v=eqs[j];coeff^=r;rhs^=v
            need(coeff==0 and rhs==1,'direct original-row XOR contradiction')
            negative+=1
    allowed=sorted((a,b) for a,b in possible if (b,a) in possible)
    need(cert['necessary_transposed_signatures']==[list(x) for x in allowed],'exact necessary transposed table')
    consequences={'maximum_sum':max(a+b for a,b in allowed),
                  'maximum_individual':max(a for a,b in allowed),'allowed_count':len(allowed)}
    need(cert['consequences']==consequences and consequences=={'maximum_sum':30,'maximum_individual':23,'allowed_count':309},
         'stated valuation consequences')
    need(all(a==b-18 and b<=23 for a,b in allowed if b>=18),'high A classification')
    H=1<<31;constants=cert['half_constants']
    need(constants=={'H':'80000000','f_H':'11002000','f_inv_H':'94857ee6','v_f_H':13,'v_f_inv_H':1},'half constants')
    need(image(H,0)==0x11002000 and image(0x94857ee6,0)==H,'direct half image identities')
    need(valuation(image(H,0))==13 and valuation(0x94857ee6)==1,'half valuation mismatch')
    bridges=recurrences(supports)
    return {'status':'PASS','single_pair_signatures':len(possible),'excluded_single_pair_signatures':negative,
            'necessary_transposed_signatures':len(allowed),'consequences':consequences,
            'half_strata':'D=H and A=H impossible in transposed two-pair coupling',
            'recurrence_bridges':bridges,'scope':'author small dependency check; written proof gives arbitrary-word quantifiers'}

def negatives(cert,supports):
    bad=[]
    c=copy.deepcopy(cert);c['valuation_cases'].pop();bad.append((c,supports))
    c=copy.deepcopy(cert);c['half_constants']['v_f_inv_H']=13;bad.append((c,supports))
    c=copy.deepcopy(cert);c['inverse_basis_columns']['0'][31]='94857ee7';bad.append((c,supports))
    c=copy.deepcopy(cert);next(x for x in c['valuation_cases'] if x['witness'] is None)['contradiction_rows']=[];bad.append((c,supports))
    c=copy.deepcopy(cert);c['necessary_transposed_signatures'].append([31,1]);bad.append((c,supports))
    s=copy.deepcopy(supports);s[12].remove(26);bad.append((cert,s))
    rejected=[]
    for c,s in bad:
        try:verify(c,s)
        except ValueError as e:rejected.append(str(e))
        else:raise ValueError('damaged proof dependency accepted')
    return rejected

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json')
    p.add_argument('--supports',type=Path,default=HERE.parent/'supports-v2.json')
    p.add_argument('--negative',action='store_true')
    p.add_argument('--output',type=Path)
    a=p.parse_args();c=json.loads(a.certificate.read_text());s=json.loads(a.supports.read_text())['supports']
    r=verify(c,s)
    if a.negative:r['rejected_controls']=negatives(c,s)
    r['certificate_sha256']=hashlib.sha256(a.certificate.read_bytes()).hexdigest()
    r['checker_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if a.output:a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps(r,sort_keys=True))
