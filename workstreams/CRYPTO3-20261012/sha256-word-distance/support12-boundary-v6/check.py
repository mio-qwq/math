#!/usr/bin/env python3
"""Exact mod-2^32 finite proof cases at valuation 17, using frozen v4 rows.

Candidate proof replay; no solver result is a premise. This extension
does not constitute independent-agent acceptance. Certificates are xz
compressed JSON and reconstruct from the complete high input quotients.
"""
import argparse
from functools import cache
import hashlib
import importlib.util
import itertools
import json
import lzma
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'support12-v4'
KERNEL_SHA256='b159cb1a0190bc9d85062b30415ef55461b098ee2c6bf9ce522e7e5b34a55fff'
MANIFEST_SHA256='3f8fab844410d88aebc26afed62a186553e9127b4196424d334be6831698acdc'

def load_kernel():
    for name,wanted in (('check.py',KERNEL_SHA256),('manifest.json',MANIFEST_SHA256)):
        if hashlib.sha256((OLD/name).read_bytes()).hexdigest()!=wanted:
            raise ValueError('modified frozen v4 dependency '+name)
    spec=importlib.util.spec_from_file_location('frozen_support12_v4',OLD/'check.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    module.image=cache(module.image)
    return module

K=load_kernel()

def width_check():
    for j in range(22,30):
        K.require(K.SIGMA_ROWS[1][j]>>17==0,'unchanged sigma1 bit'+str(j))
    K.require(K.SIGMA_ROWS[1][30]==(1<<15)^(1<<17),'quarter output dependencies')
    K.require(3*(1<<23)<1<<31,'integer carry representative uniqueness')
    representatives=[(q,h,(q<<17)+(h<<31)) for q in range(1,32,2) for h in (0,1)]
    K.require(len(representatives)==len({D for q,h,D in representatives})==32,
              '32 distinct representative residues')
    K.require(all((D&-D)==1<<17 for q,h,D in representatives),'valuation17')
    # Positive and negative lists are disjoint and cover all signed q/H
    # orientations from the written reduction modulo 2^31.
    wanted={(sign*(q<<17)+(h<<31))&K.MASK
            for sign in (-1,1) for q in range(1,32,2) for h in (0,1)}
    actual={D for _,_,D in representatives}|{(-D)&K.MASK for _,_,D in representatives}
    K.require(actual==wanted and len(wanted)==64,'signed residue coverage')
    return {'status':'PASS','screening_modulus':1<<31,'final_model_modulus':1<<32,
            'representatives':representatives,'scope':'finite row checks supporting candidate written width17 lemma'}

def recover(basis):
    word=0
    for p,(eq,_) in sorted(basis.items(),reverse=True):
        rhs=eq>>K.WIDTH
        coeff=eq&K.COEFFICIENT
        if (word&coeff).bit_count()%2!=rhs: word|=1<<p
    return word

def core_witness(basis,ax,ay,ar,D):
    w=recover(basis)
    words={'x':w&K.MASK,'y':(w>>32)&K.MASK,'r':(w>>64)&K.MASK}
    for name,a in (('x',ax),('y',ay),('r',ar)): words[name+'p']=words[name]^a
    d=lambda n:(words[n+'p']-words[n])&K.MASK
    f=lambda n:(K.image(words[n+'p'],0)-K.image(words[n],0))&K.MASK
    g=lambda n:(K.image(words[n+'p'],1)-K.image(words[n],1))&K.MASK
    K.require(d('x')==d('y')==D and d('r')==(-D)&K.MASK,'actual witness d')
    K.require(f('x')==f('y')==f('r'),'actual witness F')
    K.require((g('y')-g('x'))&K.MASK==(2*D)&K.MASK,'actual witness G gap1')
    K.require((g('y')-g('r'))&K.MASK==D,'actual witness G gap2')
    return words

def reconstruct(q,h):
    K.require(q in range(1,32,2) and h in (0,1),'exact case parameters')
    D=(q<<17)+(h<<31)
    R=K.Rebuild();cases=[];positive=K.input_classes(D);negative=K.input_classes((-D)&K.MASK)
    witnesses=[]
    for (ax,ex),(ay,ey) in itertools.product(positive,repeat=2):
        basis,receipt=K.insert({},ex+[(r<<32,v) for r,v in ey])
        K.require(receipt is None,'consistent actual input cubes')
        f,fc=R.carry([basis],0,ax,ay,0,32,0)
        g,gc=R.carry(f,1,ax,ay,0,32,(2*D)&K.MASK)
        thirds=[]
        for ordinal,b in enumerate(g):
            for ar,er in negative:
                rb,rc=K.insert(b,[(r<<64,v) for r,v in er])
                if rb is None:
                    thirds.append({'branch':ordinal,'alpha_r':f'{ar:08x}',
                                   'input_conflict':R.bank_id(rc)})
                    continue
                rf,rfc=R.carry([rb],0,ay,ar,32,64,0)
                rg,rgc=R.carry(rf,1,ar,ay,64,32,D)
                for b2 in rg: witnesses.append(core_witness(b2,ax,ay,ar,D))
                thirds.append({'branch':ordinal,'alpha_r':f'{ar:08x}',
                               'f_leaves':len(rf),'g_leaves':len(rg),
                               'f_conflicts':rfc,'g_conflicts':rgc})
        cases.append({'alpha_x':f'{ax:08x}','alpha_y':f'{ay:08x}',
                      'f_leaves':len(f),'g_leaves':len(g),
                      'f_conflicts':fc,'g_conflicts':gc,'third_pair':thirds})
    cs={orientation:[{'alpha':f'{a:08x}','input_rows':[[f'{r:08x}',v] for r,v in eqs]}
                     for a,eqs in arr]
        for orientation,arr in (('positive',positive),('negative',negative))}
    return {'schema':'CRYPTO3-support12-valuation17-onecase-v6',
            'definition':{'bits':32,'q':q,'h':h,'D':f'{D:08x}',
                          'f_rotations':[7,18],'f_shift':3,'g_rotations':[17,19],'g_shift':10,
                          'final_carry':'discarded modulo2^32, not mod2^31'},
            'input_classes':cs,'cases':cases,'witnesses':witnesses,
            'conflict_row_bank':[[[f'{c:024x}',rhs] for c,rhs in proof] for proof in R.bank],
            'stats':dict(R.stats),'kernel_sha256':KERNEL_SHA256,'v4_manifest_sha256':MANIFEST_SHA256,
            'scope':'one fixed-D triple core modulo2^32, not an actual message pair'}

def encoded(data):
    return json.dumps(data,sort_keys=True,separators=(',',':')).encode()+b'\n'

def case_path(q,h): return HERE/f'CASE-{q}-{h}.json.xz'

def summary(data):
    return {'q':data['definition']['q'],'h':data['definition']['h'],'D':data['definition']['D'],
            'positive_masks':len(data['input_classes']['positive']),
            'negative_masks':len(data['input_classes']['negative']),
            'mask_pairs':len(data['cases']),
            'twin_branches':sum(c['g_leaves'] for c in data['cases']),
            'third_masks_checked':sum(len(c['third_pair']) for c in data['cases']),
            'final_branches':sum(r.get('g_leaves',0) for c in data['cases'] for r in c['third_pair']),
            'actual_witnesses':len(data['witnesses']),
            'xor_conflict_proofs':len(data['conflict_row_bank']),'stats':data['stats']}

def build(q,h):
    start=time.monotonic();data=reconstruct(q,h);raw=encoded(data)
    target=case_path(q,h);target.write_bytes(lzma.compress(raw,preset=6))
    return {'status':'BUILT','path':target.name,'raw_json_sha256':hashlib.sha256(raw).hexdigest(),
            'xz_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
            'raw_bytes':len(raw),'xz_bytes':target.stat().st_size,
            'seconds':time.monotonic()-start,'summary':summary(data)}

def check_case(q,h):
    start=time.monotonic();path=case_path(q,h);raw=lzma.decompress(path.read_bytes());stored=json.loads(raw)
    K.require(stored==reconstruct(q,h),'complete case reconstruction mismatch')
    for proof in stored['conflict_row_bank']:
        coeff=rhs=0
        for c,b in proof: coeff^=int(c,16);rhs^=b
        K.require(coeff==0 and rhs==1,'explicit XOR-of-original-rows contradiction')
    return {'status':'PASS','path':path.name,'raw_json_sha256':hashlib.sha256(raw).hexdigest(),
            'xz_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'seconds':time.monotonic()-start,'summary':summary(stored)}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--q',type=int)
    p.add_argument('--h',type=int,choices=(0,1))
    p.add_argument('--build',action='store_true')
    p.add_argument('--output',type=Path)
    a=p.parse_args();width=width_check()
    if a.q is None:
        K.require(not a.build,'build requires exact q and h')
        receipts=[check_case(q,h) for q in range(1,32,2) for h in (0,1)]
        K.require(all(r['summary']['final_branches']==r['summary']['actual_witnesses']==0 for r in receipts),
                  'nonempty fullmod triple case')
        result={'status':'PASS','width':width,'cases':receipts,
                'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'scope':'author full 32-case finite proof replay; independent-agent review separate'}
    else:
        K.require(a.h is not None,'case h is required')
        result=build(a.q,a.h) if a.build else check_case(a.q,a.h)
    if a.output: a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
