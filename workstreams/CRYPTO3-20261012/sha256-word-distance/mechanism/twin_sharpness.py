#!/usr/bin/env python3
"""Exact linear construction attempt at valuation 21; stdlib only."""
import json
from pathlib import Path


def sigma(w, kind):
    a,b,s=((7,18,3),(17,19,10))[kind]
    def rotr(x,r):
        return ((x>>r)|(x<<(32-r)))&0xffffffff
    return rotr(w,a)^rotr(w,b)^(w>>s)


def solve(rows):
    basis={}
    for row,rhs in rows:
        while row:
            pivot=row.bit_length()-1
            if pivot in basis:
                br,bc=basis[pivot]
                row^=br
                rhs^=bc
            else:
                basis[pivot]=(row,rhs)
                break
        if not row and rhs:
            return None,len(basis)
    word=0
    for pivot,(row,rhs) in sorted(basis.items()):
        if ((row&word).bit_count()&1)^rhs:
            word|=1<<pivot
    return word,len(basis)


def construct():
    delta=1<<21
    alpha=0xffe00000
    beta=[sigma(alpha,k) for k in (0,1)]
    rows=[]
    for kind in (0,1):
        cols=[sigma(1<<i,kind) for i in range(21)]
        for bit in range(32):
            if beta[kind]>>bit&1:
                row=sum(((col>>bit)&1)<<i for i,col in enumerate(cols))
                rows.append((row,int(kind==1 and bit==21)))
    z,rank=solve(rows)
    result={'scope':'valuation-bound sharpness for independent four-word core only',
            'delta':delta,'alpha':alpha,'sigma_alpha':beta,
            'equations':len(rows),'rank':rank,'translation':z}
    if z is not None:
        high=0x7fe00000
        words={'x':high^z,'xp':((high^z)+delta)&0xffffffff,
               'y':high,'yp':(high+delta)&0xffffffff}
        result['words']=words
        dx=words['xp']-words['x']
        dy=words['yp']-words['y']
        fx=sigma(words['xp'],0)-sigma(words['x'],0)
        fy=sigma(words['yp'],0)-sigma(words['y'],0)
        gx=sigma(words['xp'],1)-sigma(words['x'],1)
        gy=sigma(words['yp'],1)-sigma(words['y'],1)
        result['raw_differences']={'dx':dx,'dy':dy,'fx':fx,'fy':fy,'gx':gx,'gy':gy}
        result['construction_checks']=(dx==dy==delta and fx==fy and gy-gx==2*delta)
    return result


if __name__=='__main__':
    result=construct()
    Path(__file__).with_name('TWIN-SHARPNESS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
