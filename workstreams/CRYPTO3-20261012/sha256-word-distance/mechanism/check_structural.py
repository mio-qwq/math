#!/usr/bin/env python3
"""Check the small finite dependencies of the written divisibility proof.

This is not a complete proof assistant or an independent-agent review.
No discovery search, solver, or rotation implementation is imported.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path


def require(ok,reason):
    if not ok:
        raise ValueError(reason)


def row(kind,j):
    a,b,s=((7,18,3),(17,19,10))[kind]
    mask=(1<<((j+a)%32))^(1<<((j+b)%32))
    if j+s<32:
        mask ^= 1<<(j+s)
    return mask


def sigma(mask,kind):
    return sum(((mask&row(kind,j)).bit_count()%2)<<j for j in range(32))


def check(cert,supports):
    require(cert['schema']=='sha256-twin-divisibility-obstruction-v1','schema')
    require(cert['bits']==32 and cert['forbidden_divisibility_exponent']==21,'word/stratum')
    masks=[int(v,16) for v in cert['sigma1_masks_hex']]
    require(len(masks)==11 and len(cert['gap_bits'])==10,'complete carry/gap lists')
    for end,mask in zip(range(21,32),masks):
        alpha=sum(1<<j for j in range(21,end+1))
        require(sigma(alpha,1)==mask,'sigma1 carry mask')
    require(max(masks[:-1])*2<1<<22,'non-top-carry magnitude bound')
    top=masks[-1]
    for mask,h in zip(masks[:-1],cert['gap_bits']):
        require(type(h) is int and 1<=h<22,'gap position')
        require((mask>>(h-1)&1)==(top>>(h-1)&1)==0,'preceding gap zeros')
        require((mask^top)>>h&1==1,'exactly one active gap bit')
    alpha=int(cert['alpha_hex'],16)
    fm=int(cert['sigma0_alpha_hex'],16);gm=int(cert['sigma1_alpha_hex'],16)
    require(alpha==0xffe00000,'top carry alpha')
    require(sigma(alpha,0)==fm and sigma(alpha,1)==gm==top,'top sigma masks')
    require(2*fm<1<<32 and gm.bit_length()==22,'integer signed-sum bounds')
    require(cert['identity_target_sigma1_bit']==21,'identity target')
    target=row(1,21)
    require(all(21<=j<=30 for j in cert['identity_raw_bits']),'raw zero coordinates')
    for j in cert['identity_raw_bits']:
        target ^= 1<<j
    for j in cert['identity_sigma0_bits']:
        require(0<=j<32 and fm>>j&1,'sigma0 zero coordinates')
        target ^= row(0,j)
    for j in cert['identity_sigma1_bits']:
        require(0<=j<32 and j!=21 and gm>>j&1,'sigma1 zero coordinates')
        target ^= row(1,j)
    require(target==0,'universal XOR row identity')
    for j in range(22,32):
        require(row(1,j)>>21==0,'sigma1 locality')
    base=[
        (19,[('d',19,1),('d',12,-1)]),
        (28,[('d',21,-1),('d',12,-1)]),
        (35,[('d',35,1),('d',19,-1)]),
        (21,[('d',21,1),('g',19,-1),('d',14,-1)]),
        (30,[('d',30,1),('d',14,-1)]),
        (37,[('g',35,-1),('d',30,-1),('d',21,-1)]),
        (46,[('g',44,-1),('d',30,-1)]),
        (51,[('d',44,-1),('d',35,-1)]),
        (34,[('d',27,-1),('f',19,-1)]),
        (43,[('d',43,1),('d',27,-1)]),
        (50,[('d',43,-1),('f',35,-1)])]
    expected=[(6,0,19,35,44),(7,2,21,37,46),(12,-1,18,34,43),(13,1,20,36,45)]
    actual=[tuple(c[k] for k in ('index','shift','x','y','r')) for c in cert['support_cases']]
    require(actual==expected,'support case coordinates')
    substitutions=0
    for case in cert['support_cases']:
        shift=case['shift'];S=set(supports[case['index']])
        require({case[k] for k in ('x','y','r')}<=S,'active core differences')
        for t0,wanted in base:
            t=t0+shift
            require(16<=t<64,'recurrence boundary')
            terms=[(kind,i,s) for kind,i,s in
                   [('d',t,1),('g',t-2,-1),('d',t-7,-1),('f',t-15,-1),('d',t-16,-1)] if i in S]
            shifted=[(kind,i+shift,s) for kind,i,s in wanted]
            require(sorted(terms)==sorted(shifted),'recurrence reduction')
            substitutions+=1
    return {'sigma1_masks':11,'gap_obstructions':10,'xor_identities':1,
            'recurrence_substitutions':substitutions,'support_indices':[6,7,12,13],
            'conclusion':'central nonzero difference is not divisible by 2^21',
            'scope':'finite dependencies of full written proof; distance bound remains 13'}


def negatives(cert,supports):
    bad=[]
    c=copy.deepcopy(cert);c['sigma1_masks_hex'][0]='00000815';bad.append((c,supports))
    c=copy.deepcopy(cert);c['gap_bits'][0]=14;bad.append((c,supports))
    c=copy.deepcopy(cert);c['identity_raw_bits'].pop();bad.append((c,supports))
    c=copy.deepcopy(cert);c['support_cases'][0]['r']+=1;bad.append((c,supports))
    c=copy.deepcopy(cert);c['sigma1_masks_hex'].pop();bad.append((c,supports))
    s=copy.deepcopy(supports);s[6]=[i for i in s[6] if i!=27];bad.append((cert,s))
    rejected=[]
    for c,s in bad:
        try:
            check(c,s)
        except ValueError as e:
            rejected.append(str(e))
        else:
            raise ValueError('corrupted finite dependency accepted')
    return rejected


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('supports',type=Path)
    p.add_argument('--certificate',type=Path,default=Path(__file__).with_name('STRUCTURAL-CERTIFICATE.json'))
    p.add_argument('--negative',action='store_true')
    a=p.parse_args()
    cert=json.loads(a.certificate.read_text())
    supports=json.loads(a.supports.read_text())['supports']
    result=check(cert,supports)
    result['support_source_sha256']=hashlib.sha256(a.supports.read_bytes()).hexdigest()
    if a.negative:
        result['rejected_controls']=negatives(cert,supports)
    print(json.dumps(result,sort_keys=True))
