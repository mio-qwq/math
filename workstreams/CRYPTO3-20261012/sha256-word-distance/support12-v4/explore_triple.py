#!/usr/bin/env python3
"""Retain the third actual pair in the high-divisibility support-12 core."""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time
import explore as twin

MASK=twin.MASK
HERE=Path(__file__).resolve().parent

def walk(kind,alpha_left,alpha_right,left,right,constant,basis,stats):
    betas=(twin.sigma(alpha_left,kind),twin.sigma(alpha_right,kind))
    def dfs(j,carry,b):
        stats['nodes']+=1
        if j==32:
            stats['leaves']+=1
            yield b
            return
        for nxt in range(-3,3):
            if j<31:
                parity=((betas[0]>>(j+1))^(betas[1]>>(j+1))^(constant>>(j+1)))&1
                if nxt%2!=parity: continue
            eqs=twin.allowed_equations(betas,j,carry,nxt,constant,kind)
            if eqs is None: continue
            eqs=[(((r&MASK)<<left)^((r>>32)<<right),v) for r,v in eqs]
            stats['edges']+=1
            nb=twin.extend(b,eqs)
            if nb is None: stats['conflicts']+=1
            else: yield from dfs(j+1,nxt,nb)
    yield from dfs(0,0,basis)

def run(delta):
    start=time.monotonic()
    positive=twin.classes(delta)
    negative=twin.classes((-delta)&MASK)
    stats=Counter();cases=[];solutions=[]
    for (ax,ex),(ay,ey) in itertools.product(positive,repeat=2):
        b=twin.extend({},ex+[(r<<32,v) for r,v in ey])
        partial=[]
        before=dict(stats)
        for b0 in walk(0,ax,ay,0,32,0,b,stats):
            partial.extend(walk(1,ax,ay,0,32,(2*delta)&MASK,b0,stats))
        third=[]
        for br0 in partial:
            for ar,er in negative:
                br=twin.extend(br0,[(r<<64,v) for r,v in er])
                third_start=dict(stats);sat=[]
                for br1 in walk(0,ay,ar,32,64,0,br,stats):
                    for br2 in walk(1,ar,ay,64,32,delta,br1,stats):
                        w=twin.recover(br2)
                        x=w&MASK;y=(w>>32)&MASK;r=(w>>64)&MASK
                        ws=dict(x=x,xp=x^ax,y=y,yp=y^ay,r=r,rp=r^ar)
                        d=lambda a:(ws[a+'p']-ws[a])&MASK
                        f=lambda a:(twin.sigma(ws[a+'p'],0)-twin.sigma(ws[a],0))&MASK
                        g=lambda a:(twin.sigma(ws[a+'p'],1)-twin.sigma(ws[a],1))&MASK
                        assert d('x')==d('y')==delta and d('r')==(-delta)&MASK
                        assert f('x')==f('y')==f('r')
                        assert (g('y')-g('x'))&MASK==(2*delta)&MASK
                        assert (g('y')-g('r'))&MASK==delta
                        sat.append(ws);solutions.append(ws)
                third.append({'alpha_r':f'{ar:08x}','sat_count':len(sat),
                              'stats':{k:stats[k]-third_start.get(k,0) for k in stats
                                       if stats[k]!=third_start.get(k,0)}})
        cases.append({'alpha_x':f'{ax:08x}','alpha_y':f'{ay:08x}',
                      'twin_leaves':len(partial),'r_cases':third,
                      'stats':{k:stats[k]-before.get(k,0) for k in stats
                               if stats[k]!=before.get(k,0)}})
    return {'delta':delta,'input_classes_positive':len(positive),
            'input_classes_negative':len(negative),'twin_mask_pairs':len(cases),
            'sat_count':len(solutions),'solutions':solutions,'stats':dict(stats),
            'seconds':time.monotonic()-start,'cases':cases,
            'scope':'six actual words in necessary triple core; not a complete support witness',
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (HERE/'explore.py',Path(__file__))}}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--delta',default=5<<19,type=lambda s:int(s,0))
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();r=run(a.delta)
    a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='cases'},sort_keys=True))
