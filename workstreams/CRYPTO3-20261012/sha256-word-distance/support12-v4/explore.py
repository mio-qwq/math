#!/usr/bin/env python3
"""Fixed additive twin-core test by exact affine carry traversal.

Research data only; the separate checker and written proof control scope.
No solver import, no linearized replacement for modular arithmetic.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

N=1<<32
MASK=N-1

def sigma(x,kind):
    a,b,c=((7,18,3),(17,19,10))[kind]
    return (((x>>a)|(x<<(32-a)))^((x>>b)|(x<<(32-b)))^(x>>c))&MASK

ROWS=[[sum(((sigma(1<<i,k)>>j)&1)<<i for i in range(32))
       for j in range(32)] for k in (0,1)]

def classes(delta):
    k=(delta&-delta).bit_length()-1
    highbits=32-k
    grouped={}
    for q in range(1<<highbits):
        alpha=(q^((q+(delta>>k))%(1<<highbits)))<<k
        grouped.setdefault(alpha,[]).append(q)
    result=[]
    for alpha,qs in sorted(grouped.items()):
        c=((alpha-delta)&MASK)//2
        assert ((alpha-delta)&MASK)%2==0
        assert c&~(alpha&0x7fffffff)==0
        eqs=[(1<<j,c>>j&1) for j in range(31) if alpha>>j&1]
        rebuilt=[q for q in range(1<<highbits)
                 if all(((q<<k)&row).bit_count()%2==rhs for row,rhs in eqs)]
        assert rebuilt==qs
        result.append((alpha,eqs))
    return result

def extend(basis,eqs):
    basis=dict(basis)
    for row,value in eqs:
        while row:
            pivot=row.bit_length()-1
            if pivot in basis:
                r,v=basis[pivot]
                row^=r;value^=v
            else:
                basis[pivot]=row,value
                break
        if not row and value:
            return None
    return basis

def recover(basis):
    word=0
    for pivot,(row,rhs) in sorted(basis.items()):
        if (word&row).bit_count()%2 != rhs:
            word|=1<<pivot
    return word

def allowed_equations(betas,j,carry,nxt,constant,kind):
    bx,by=(b>>j&1 for b in betas)
    needed=2*nxt-carry-(by-bx-(constant>>j&1))
    if needed%2: return None
    needed//=2
    a=ROWS[kind][j];b=a<<32
    if bx and by:
        if needed==0: return [(a^b,0)]
        if needed==1: return [(a,1),(b,0)]
        if needed==-1: return [(a,0),(b,1)]
        return None
    if bx: return [(a,needed)] if needed in (0,1) else None
    if by: return [(b,-needed)] if needed in (0,-1) else None
    return [] if needed==0 else None

def solve_pair(delta,cx,cy,order):
    ax,ex=cx;ay,ey=cy
    basis=extend({},ex+[(r<<32,v) for r,v in ey])
    stats=Counter();witness=[]
    betas=[(sigma(ax,k),sigma(ay,k)) for k in (0,1)]
    constants=(0,(2*delta)&MASK)

    def dfs(stage,j,carry,b):
        stats['nodes']+=1
        if j==32:
            if stage+1<len(order):
                return dfs(stage+1,0,0,b)
            stats['sat_leaves']+=1
            if not witness:
                w=recover(b)
                x=w&MASK;y=w>>32
                xp=x^ax;yp=y^ay
                assert (xp-x)&MASK==delta and (yp-y)&MASK==delta
                assert (sigma(yp,0)-sigma(y,0)-sigma(xp,0)+sigma(x,0))&MASK==0
                assert (sigma(yp,1)-sigma(y,1)-sigma(xp,1)+sigma(x,1))&MASK==(2*delta)&MASK
                witness.append(dict(x=x,xp=xp,y=y,yp=yp))
            return
        k=order[stage]
        for nxt in range(-3,3):
            if j<31:
                bx,by=betas[k]
                parity=((bx>>(j+1))^(by>>(j+1))^(constants[k]>>(j+1)))&1
                if nxt%2!=parity: continue
            eqs=allowed_equations(betas[k],j,carry,nxt,constants[k],k)
            if eqs is None: continue
            stats['edges']+=1
            out=extend(b,eqs)
            if out is None: stats['conflicts']+=1
            else: dfs(stage,j+1,nxt,out)

    dfs(0,0,0,basis)
    return {'alpha_x':f'{ax:08x}','alpha_y':f'{ay:08x}',
            'stats':dict(stats),'witness':witness[0] if witness else None}

def run(delta,order=(0,1)):
    start=time.monotonic();cs=classes(delta)
    cases=[solve_pair(delta,cx,cy,order) for cx,cy in itertools.product(cs,repeat=2)]
    stats=Counter()
    for case in cases: stats.update(case['stats'])
    return {'bits':32,'delta':delta,'order':list(order),
            'input_classes':len(cs),'case_count':len(cases),
            'sat_cases':sum(c['witness'] is not None for c in cases),
            'stats':dict(stats),'seconds':time.monotonic()-start,'cases':cases,
            'scope':'fixed-difference twin core; not a full support or schedule witness',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--delta',required=True,type=lambda s:int(s,0))
    p.add_argument('--output',required=True,type=Path)
    p.add_argument('--g-first',action='store_true')
    a=p.parse_args()
    r=run(a.delta,(1,0) if a.g_first else (0,1))
    a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='cases'},sort_keys=True))
