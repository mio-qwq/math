#!/usr/bin/env python3
"""Finite proof replay of the new odd valuation-18 representatives.

Reuse of the hash-pinned v4 definition-based kernel is explicit. This
author extension is not an independent-agent acceptance. No SMT import.
"""
import argparse
from functools import cache
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'support12-v4'
KERNEL_SHA256='b159cb1a0190bc9d85062b30415ef55461b098ee2c6bf9ce522e7e5b34a55fff'
MANIFEST_SHA256='3f8fab844410d88aebc26afed62a186553e9127b4196424d334be6831698acdc'

def load_kernel():
    for name,wanted in (('check.py',KERNEL_SHA256),('manifest.json',MANIFEST_SHA256)):
        got=hashlib.sha256((OLD/name).read_bytes()).hexdigest()
        if got!=wanted: raise ValueError('modified frozen v4 dependency '+name)
    spec=importlib.util.spec_from_file_location('frozen_support12_v4',OLD/'check.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    # Memoize only the pure output-row evaluation. Its values and exact
    # Boolean truth-table transition semantics are unchanged.
    module.image=cache(module.image)
    return module

K=load_kernel()

def reconstruct():
    R=K.Rebuild();groups=[];class_records={}
    for q in range(1,16,2):
        D=q<<18
        positive=K.input_classes(D)
        negative=K.input_classes((-D)&K.MASK)
        class_records[str(q)]={orientation:[{'alpha':f'{a:08x}',
                                             'input_rows':[[f'{r:08x}',v] for r,v in eqs]}
                                            for a,eqs in cs]
                              for orientation,cs in (('positive',positive),('negative',negative))}
        cases=[]
        for (ax,ex),(ay,ey) in itertools.product(positive,repeat=2):
            basis,conflict=K.insert({},ex+[(r<<32,v) for r,v in ey])
            K.require(conflict is None,'input cube consistency')
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
                    K.require(not rg,'valuation18 triple core has an actual survivor')
                    thirds.append({'branch':ordinal,'alpha_r':f'{ar:08x}',
                                   'f_leaves':len(rf),'g_leaves':len(rg),
                                   'f_conflicts':rfc,'g_conflicts':rgc})
            cases.append({'alpha_x':f'{ax:08x}','alpha_y':f'{ay:08x}',
                          'f_leaves':len(f),'g_leaves':len(g),
                          'f_conflicts':fc,'g_conflicts':gc,'third_pair':thirds})
        groups.append({'q':q,'delta':f'{D:08x}','positive_masks':len(positive),
                       'negative_masks':len(negative),'mask_pairs':len(cases),'cases':cases})
    return {'schema':'CRYPTO3-support12-valuation18-finite-carry-certificate-v5',
            'definition':{'bits':32,'lowest_divisibility_bit':18,
                          'new_odd_representatives':list(range(1,16,2)),
                          'f_rotations':[7,18],'f_shift':3,'g_rotations':[17,19],'g_shift':10,
                          'final_carry':'discarded modulo 2^32'},
            'kernel_sha256':KERNEL_SHA256,'v4_manifest_sha256':MANIFEST_SHA256,
            'input_classes':class_records,'cases':groups,
            'conflict_row_bank':[[[f'{c:024x}',rhs] for c,rhs in proof] for proof in R.bank],
            'stats':dict(R.stats),
            'scope':'eight new odd valuation18 triple exclusions; with width-v5 and v4 implies v2(D)<=17'}

def check(certificate):
    start=time.monotonic();stored=json.loads(certificate.read_text())
    rebuilt=reconstruct()
    K.require(stored==rebuilt,'complete finite rebuild does not match certificate')
    for proof in stored['conflict_row_bank']:
        coeff=rhs=0
        for c,b in proof: coeff^=int(c,16);rhs^=b
        K.require(coeff==0 and rhs==1,'explicit original-row XOR contradiction')
    summary=[]
    for group in stored['cases']:
        summary.append({'q':group['q'],'positive_masks':group['positive_masks'],
                        'negative_masks':group['negative_masks'],'mask_pairs':group['mask_pairs'],
                        'twin_branches':sum(c['g_leaves'] for c in group['cases']),
                        'third_masks_checked':sum(len(c['third_pair']) for c in group['cases']),
                        'final_branches':sum(r.get('g_leaves',0) for c in group['cases']
                                             for r in c['third_pair'])})
    return {'status':'PASS','certificate_sha256':hashlib.sha256(certificate.read_bytes()).hexdigest(),
            'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'kernel_sha256':KERNEL_SHA256,'v4_manifest_sha256':MANIFEST_SHA256,
            'summary':summary,'xor_conflict_proofs':len(stored['conflict_row_bank']),
            'stats':stored['stats'],'seconds':time.monotonic()-start,
            'scope':'author finite proof of new odd cases only; independent-agent review separate'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--certificate',type=Path,default=HERE/'CERTIFICATE.json')
    p.add_argument('--output',type=Path)
    p.add_argument('--build',action='store_true')
    a=p.parse_args()
    if a.build:
        data=reconstruct();a.certificate.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
        result={'status':'BUILT','bytes':a.certificate.stat().st_size,
                'xor_conflict_proofs':len(data['conflict_row_bank']),'stats':data['stats']}
    else: result=check(a.certificate)
    if a.output: a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
