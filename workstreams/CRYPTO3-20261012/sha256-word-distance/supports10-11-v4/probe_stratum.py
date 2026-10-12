#!/usr/bin/env python3
"""Complete independent signed-mask feasibility for a finite k stratum."""
import argparse
import hashlib
import json
import platform
import time
from collections import Counter
from pathlib import Path
from probe_masks import MASK, f, g, output_row, kernel, span

HERE=Path(__file__).resolve().parent


def independent_zero(masks):
    carry={0}
    for i in range(32):
        count=sum((mask >> i)&1 for mask in masks)
        carry={(c+t)//2 for c in carry for t in range(-count,count+1,2) if (c+t)%2==0}
        if not carry:return False,i
    return True,None


def quick_two(a,b):
    # The zero-output Lipmaa--Moriai mask condition; discovery acceleration.
    return ((a ^ b) & ~((a | b) << 1) & MASK)==0


def run(k):
    start=time.monotonic()
    bx,rx=kernel([1<<i for i in range(k)]+[output_row(g,i) for i in range(k)])
    by,ry=kernel([output_row(f,i) for i in range(k)])
    X=span(bx)[1:]
    Y=span(by)
    first=[]
    counts=Counter()
    for alpha in X:
        gamma=f(alpha)
        for beta in Y:
            if quick_two(beta,gamma):
                assert independent_zero([beta,gamma])[0]
                first.append((alpha,beta))
    survivors={}
    hist={}
    for m in (1,2):
        hits=[]
        h=Counter()
        for alpha,beta in first:
            ok,bit=independent_zero([f(beta),(m*alpha)&MASK,g(alpha)])
            if ok:hits.append([alpha,beta])
            else:h[bit]+=1
        survivors[str(m)]=hits
        hist[str(m)]=dict(h)
    data={'scope':'complete necessary independent-sign mask relaxation; no actual pair or schedule',
          'k':k,'m_values':[1,2], 'python':platform.python_version(),
          'probe_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'support_sha256':hashlib.sha256((HERE.parent/'supports-v2.json').read_bytes()).hexdigest(),
          'kernel_X_rank':rx,'kernel_X_basis':bx,
          'kernel_Y_rank':ry,'kernel_Y_basis':by,
          'tested_mask_pairs':len(X)*len(Y),
          'first_carry_survivors':first,
          'second_carry_survivors':survivors,
          'second_first_empty_bit_histogram':hist,
          'elapsed_s':time.monotonic()-start}
    (HERE/f'STRATUM_K{k}.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in ('first_carry_survivors','second_carry_survivors')}
          | {'first_survivor_count':len(first),'second_survivor_counts':{m:len(h) for m,h in survivors.items()}},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--k',type=int,required=True)
    run(p.parse_args().k)
