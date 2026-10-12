#!/usr/bin/env python3
"""Exact integer check of even-row cross-parity theorem; stdlib only."""
from math import comb
from fractions import Fraction

def O(h,k):return 2*comb(2*k+2*h-1,k+h)
def E(h,k):return 2**(2*h-1)*comb(2*k,k)+2*comb(2*k,k+1)

def main():
    count=0
    for h in range(2,33):
        prev=None
        for k in range(1,60):
            ratio=Fraction(O(h,k),E(h,k))
            assert prev is None or ratio>prev,(h,k)
            prev=ratio
            count+=1
        assert (O(h,1)>E(h,1))==(h in (2,3))
        assert O(h,59)>E(h,59),('budget may be too small',h)
    assert O(4,1)==252 and E(4,1)==258
    assert O(4,2)==924 and E(4,2)==776
    assert not (O(4,1)>=E(4,1))
    print('PASS h=2..32 k=1..59 strict-ratio-comparisons='+str(count-31)+' crossed-t8-examples=PASS')
if __name__=='__main__':main()
