#!/usr/bin/env python3
"""Exact carry-mask reduction for a fixed twin-core difference.

Discovery verifier: no SMT, no full message schedule claim. Output rows
use rotation-column construction; a separate checker should use direct
bit equations and audit traversal completeness before accepting an
exclusion claim.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

MASK=(1<<32)-1


def sigma(x,kind):
    a,b,s=((7,18,3),(17,19,10))[kind]
    return (((x>>a)|(x<<(32-a))) ^ ((x>>b)|(x<<(32-b))) ^ (x>>s))&MASK


ROWS=[[sum(((sigma(1<<i,kind)>>j)&1)<<i for i in range(32))
       for j in range(32)] for kind in range(2)]


def add_equations(basis,equations):
    basis=basis.copy()
    for row,value in equations:
        while row:
            pivot=row.bit_length()-1
            if pivot in basis:
                old,rhs=basis[pivot]
                row^=old
                value^=rhs
            else:
                basis[pivot]=(row,value)
                break
        if not row and value:
            return None
    return basis


def recover(basis):
    word=0
    for pivot,(row,rhs) in sorted(basis.items()):
        if ((row&word).bit_count()&1)^rhs:
            word |= 1<<pivot
    return word


def mask_case(k,end,half,offset):
    # At end=31 both carry stopping at bit31 and wrapping through bit31
    # have the same XOR mask, hence bit31 is deliberately unrestricted.
    alpha=(((1<<(end-k+1))-1)<<k) ^ (int(half)<<31)
    equations=[(1<<(i+offset),1) for i in range(k,end)]
    if end<31:
        equations.append((1<<(end+offset),0))
    return alpha,equations


def transition_equations(beta_x,beta_y,constant,j,carry,next_carry,kind):
    # gy-gx-C=0 (or fy-fx=0). At an active output bit, derivative
    # contribution is 1-2*bit. Thus local signed coefficient is
    # by-bx + 2*bx*u - 2*by*v - constant_bit.
    bx=(beta_x>>j)&1
    by=(beta_y>>j)&1
    cj=(constant>>j)&1
    needed=2*next_carry-carry-(by-bx-cj)
    if needed%2:
        return None
    needed//=2
    u=ROWS[kind][j]
    v=u<<32
    if bx and by:
        if needed==0:
            return [(u^v,0)]
        if needed==1:
            return [(u,1),(v,0)]
        if needed==-1:
            return [(u,0),(v,1)]
        return None
    if bx:
        return [(u,needed)] if needed in (0,1) else None
    if by:
        return [(v,-needed)] if needed in (0,-1) else None
    return [] if needed==0 else None


def solve_case(k,half,end_x,end_y):
    ax,ex=mask_case(k,end_x,half,0)
    ay,ey=mask_case(k,end_y,half,32)
    basis=add_equations({},ex+ey)
    delta=((1<<k)+(int(half)<<31))&MASK
    constants=(0,(2*delta)&MASK)
    betas=[(sigma(ax,kind),sigma(ay,kind)) for kind in range(2)]
    stats=Counter()
    solutions=[]

    def dfs(kind,j,carry,basis):
        stats['visited']+=1
        if j==32:
            # The terminal carry is discarded modulo 2^32.
            if kind==0:
                dfs(1,0,0,basis)
            else:
                stats['sat_leaves']+=1
                if not solutions:
                    xy=recover(basis)
                    x=xy&MASK; y=xy>>32
                    solutions.append({'x':x,'xp':(x+delta)&MASK,
                                      'y':y,'yp':(y+delta)&MASK})
            return
        bx,by=betas[kind]
        constant=constants[kind]
        # Every local coefficient is between -3 and 2, so starting
        # at 0 the carry always remains in [-3,2]. This deliberately
        # loose range contains every attainable carry.
        for nxt in range(-3,3):
            if j<31:
                parity=((bx>>(j+1))^(by>>(j+1))^(constant>>(j+1)))&1
                if nxt%2 != parity:
                    continue
            eqs=transition_equations(bx,by,constant,j,carry,nxt,kind)
            if eqs is None:
                continue
            stats['carry_edges']+=1
            newbasis=add_equations(basis,eqs)
            if newbasis is None:
                stats['linear_conflicts']+=1
            else:
                dfs(kind,j+1,nxt,newbasis)

    dfs(0,0,0,basis)
    return {'end_x':end_x,'end_y':end_y,'alpha_x':ax,'alpha_y':ay,
            'stats':dict(stats),'witness':solutions[0] if solutions else None}


def run(k,half):
    results=[]
    for ex in range(k,32):
        for ey in range(k,32):
            results.append(solve_case(k,half,ex,ey))
    return {'scope':'fixed-difference four-word twin core; no schedule equations',
            'bits':32,'k':k,'half':half,'delta':(1<<k)+(int(half)<<31),
            'case_count':len(results),'sat_cases':sum(r['witness'] is not None for r in results),
            'cases':results}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--k',type=int,default=21)
    p.add_argument('--half',action='store_true')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    result=run(a.k,a.half)
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},sort_keys=True))
