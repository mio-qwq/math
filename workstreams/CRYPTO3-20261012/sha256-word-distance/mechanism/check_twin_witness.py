#!/usr/bin/env python3
"""Direct-bit validation of relaxation witnesses, with damaged controls."""
import argparse
import copy
import json
from pathlib import Path

N=1<<32


def sigma_bits(x,kind):
    a,b,s=((7,18,3),(17,19,10))[kind]
    out=0
    for j in range(32):
        bit=((x>>((j+a)%32))^(x>>((j+b)%32)))&1
        if j+s<32:
            bit^=(x>>(j+s))&1
        out|=bit<<j
    return out


def check_words(words,expected_delta=None):
    if set(words)!=set(('x','xp','y','yp')):
        raise ValueError('word names')
    if not all(type(w) is int and 0<=w<N for w in words.values()):
        raise ValueError('word range')
    x,xp,y,yp=(words[k] for k in ('x','xp','y','yp'))
    dx=(xp-x)%N;dy=(yp-y)%N
    if dx==0 or dx!=dy:
        raise ValueError('equal nonzero input differences')
    if expected_delta is not None and dx!=expected_delta:
        raise ValueError('expected input difference')
    fx=(sigma_bits(xp,0)-sigma_bits(x,0))%N
    fy=(sigma_bits(yp,0)-sigma_bits(y,0))%N
    gx=(sigma_bits(xp,1)-sigma_bits(x,1))%N
    gy=(sigma_bits(yp,1)-sigma_bits(y,1))%N
    if fx!=fy:
        raise ValueError('matching sigma0 derivative')
    if (gy-gx)%N != (2*dx)%N:
        raise ValueError('sigma1 second difference')
    return {'delta':dx,'F':fx,'Gx':gx,'Gy':gy,
            'scope':'independent pairs only; no base-schedule equations'}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--directory',type=Path,default=Path(__file__).parent)
    a=p.parse_args()
    run=json.loads((a.directory/'TWIN-RUN.json').read_text())
    results={'generic':check_words(run['words'],run['delta'])}
    carry=json.loads((a.directory/'TWIN-V21-HALF-CARRY.json').read_text())
    accepted=[]
    for case in carry['cases']:
        if case['witness'] is not None:
            accepted.append(check_words(case['witness'],carry['delta']))
    results['high_valuation_witnesses']=len(accepted)
    results['high_valuation_first']=accepted[0]
    controls=[]
    bad=copy.deepcopy(run['words']);bad['x']^=1;controls.append((bad,run['delta']))
    bad=copy.deepcopy(run['words']);bad['xp']=N;controls.append((bad,run['delta']))
    controls.append((run['words'],run['delta']^1))
    bad=copy.deepcopy(run['words']);bad['yp']^=1;controls.append((bad,run['delta']))
    reasons=[]
    for words,delta in controls:
        try:
            check_words(words,delta)
        except ValueError as e:
            reasons.append(str(e))
        else:
            raise ValueError('damaged control accepted')
    results['rejected_controls']=reasons
    print(json.dumps(results,sort_keys=True))
