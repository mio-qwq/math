#!/usr/bin/env python3
"""Definition-based verifier for a SAT result; standard library only."""
import argparse,json
from pathlib import Path
MASK=(1<<32)-1
SUPPORT=(10,11,13,15,18,20,26,28,29,34,42,43,57)

def rows(kind,j):
    if kind=='f':
        r={(j+7)%32,(j+18)%32}
        if j+3<32:r.symmetric_difference_update({j+3})
    else:
        r={(j+17)%32,(j+19)%32}
        if j+10<32:r.symmetric_difference_update({j+10})
    return r

def sigma(x,kind):return sum((sum((x>>i)&1 for i in rows(kind,j))&1)<<j for j in range(32))
def sub(a,b):return (a-b)&MASK
def v2(x):return (x&-x).bit_length()-1

def main():
    p=argparse.ArgumentParser();p.add_argument('result',type=Path);a=p.parse_args()
    q=json.loads(a.result.read_text());assert q['result']=='sat' and set(map(int,q['model']))==set(SUPPORT)
    d=[0]*64;F=[0]*64;G=[0]*64
    for s,pair in q['model'].items():
        i=int(s);x=int(pair['x'],16);xp=int(pair['xp'],16)
        d[i]=sub(xp,x);F[i]=sub(sigma(xp,'f'),sigma(x,'f'));G[i]=sub(sigma(xp,'g'),sigma(x,'g'))
        assert d[i]!=0
    assert v2(d[18])==16
    for t in range(16,64):assert d[t]==(G[t-2]+d[t-7]+F[t-15]+d[t-16])&MASK,t
    print(json.dumps({'status':'PASS','actual_pairs':len(SUPPORT),'original_equations':48,
                      'valuation_d18':v2(d[18]),'base_schedule_completed':False},sort_keys=True))
if __name__=='__main__':main()
