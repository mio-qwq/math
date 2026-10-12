#!/usr/bin/env python3
"""One bounded exact-carry exploration for D=2^16."""
from functools import cache
import hashlib
import importlib.util
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'support12-v4'/'check.py'
EXPECTED='b159cb1a0190bc9d85062b30415ef55461b098ee2c6bf9ce522e7e5b34a55fff'
if hashlib.sha256(OLD.read_bytes()).hexdigest()!=EXPECTED:
    raise ValueError('frozen kernel hash mismatch')
spec=importlib.util.spec_from_file_location('support12_v4_kernel',OLD)
K=importlib.util.module_from_spec(spec);spec.loader.exec_module(K)
K.image=cache(K.image)

def recover(basis,width):
    word=0
    for p,(eq,_) in sorted(basis.items(),reverse=True):
        if p>=width: continue
        rhs=eq>>K.WIDTH
        coeff=eq&K.COEFFICIENT
        if (word&coeff).bit_count()%2!=rhs: word|=1<<p
    return word

def pair_values(w,delta):
    wp=(w+delta)&K.MASK
    return {'w':w,'wp':wp,'d':delta,
            'f':(K.image(wp,0)-K.image(w,0))&K.MASK,
            'g':(K.image(wp,1)-K.image(w,1))&K.MASK}

def reciprocal(A,D):
    R=K.Rebuild()
    for alpha,eqs in K.input_classes(A):
        basis,conf=K.insert({},eqs)
        if basis is None: continue
        leaves,_=R.carry([basis],0,0,alpha,0,0,D)
        if leaves:
            q=recover(leaves[0],32)&K.MASK
            rec=pair_values(q,A)
            if rec['f']!=D: raise ValueError('bad reciprocal recovery')
            return rec,alpha
    return None,None

def main():
    start=time.monotonic(); D=1<<16; R=K.Rebuild()
    positive=K.input_classes(D); negative=K.input_classes((-D)&K.MASK)
    triples=0
    for ax,ex in positive:
      for ay,ey in positive:
        basis,conf=K.insert({},ex+[(r<<32,v) for r,v in ey])
        if basis is None: continue
        f,_=R.carry([basis],0,ax,ay,0,32,0)
        g,_=R.carry(f,1,ax,ay,0,32,(2*D)&K.MASK)
        for b in g:
          for ar,er in negative:
            rb,conf=K.insert(b,[(r<<64,v) for r,v in er])
            if rb is None: continue
            rf,_=R.carry([rb],0,ay,ar,32,64,0)
            rg,_=R.carry(rf,1,ar,ay,64,32,D)
            for leaf in rg:
                triples+=1
                packed=recover(leaf,96)
                x=packed&K.MASK;y=(packed>>32)&K.MASK;r=(packed>>64)&K.MASK
                X=pair_values(x,D);Y=pair_values(y,D);Rpair=pair_values(r,(-D)&K.MASK)
                A=X['f']
                rec,aq=reciprocal(A,D)
                if rec is not None:
                    out={'status':'SAT_LOCAL','D':D,'A':A,
                         'v2_A':(A&-A).bit_length()-1,
                         'pairs':{'X':X,'Y':Y,'R':Rpair,'Q':rec},
                         'xor_masks':{'X':ax,'Y':ay,'R':ar,'Q':aq},
                         'checked_triple_survivors':triples,
                         'elapsed_seconds':time.monotonic()-start,
                         'kernel_sha256':EXPECTED,
                         'scope':'selected four-pair local system only; not a message pair'}
                    print(json.dumps(out,sort_keys=True));return
                if time.monotonic()-start>300:
                    print(json.dumps({'status':'TIMEOUT','checked_triple_survivors':triples,
                                      'elapsed_seconds':time.monotonic()-start},sort_keys=True));return
    print(json.dumps({'status':'NO_RECIPROCAL_SURVIVOR_FOR_FIXED_D',
                      'checked_triple_survivors':triples,
                      'elapsed_seconds':time.monotonic()-start,
                      'scope':'fixed D only'},sort_keys=True))

if __name__=='__main__': main()
