#!/usr/bin/env python3
"""Exact finite and large-scale regression for globally tight partition balancing."""
from itertools import product
from random import Random
from global_balanced_partitions import global_balanced,validate_global


def partitions(n):
    blocks=[]
    def rec(x):
        if x==n:
            yield [tuple(z) for z in blocks];return
        for b in blocks:
            b.append(x);yield from rec(x+1);b.pop()
        blocks.append([x]);yield from rec(x+1);blocks.pop()
    yield from rec(0)


def brute(P,S,n):
    for bits in product((0,1),repeat=n):
        if sum(t==0 for t in bits)!=n//2:continue
        if all(abs(sum(bits[x]==0 for x in b)-sum(bits[x]==1 for x in b))<=1
               for b in P+S):return True
    return False


def main():
    hist={}
    for n in range(7):
        parts=list(partitions(n));count=0
        for P in parts:
            for S in parts:
                c=global_balanced(P,S)
                assert validate_global(P,S,c)
                assert sum(t==0 for t in c.values())==n//2
                if n<=4:assert brute(P,S,n)
                count+=1
        hist[n]=count
    assert hist=={0:1,1:1,2:4,3:25,4:225,5:2704,6:41209},hist
    rng=Random(20261010)
    extra=0
    for n in range(7,81):
        for _ in range(37):
            def rand_partition():
                a=list(range(n));rng.shuffle(a);out=[];i=0
                while i<n:
                    sz=rng.randint(1,min(9,n-i));out.append(a[i:i+sz]);i+=sz
                return out
            P=rand_partition();S=rand_partition()
            c=global_balanced(P,S)
            assert validate_global(P,S,c)
            extra+=1
    big=100000
    P=[list(range(big))];S=[[i] for i in range(big)]
    c=global_balanced(P,S)
    assert validate_global(P,S,c)
    assert sum(t==0 for t in c.values())==50000
    # Original incidence multigraph has parallel edges here; simulated
    # artificial pairing never drops a label and global count remains exact.
    P=[[0,1],[2,3]];S=[[0,1],[2,3]]
    c=global_balanced(P,S);assert validate_global(P,S,c)
    invalid=[([[0,0]],[[0]]),([[0,1],[1,2]],[[0,1,2]]),
             ([[0,1]],[[0,2]]),([[]],[[0]]),([[0]],[[0,1]])]
    for p,s in invalid:
        try:global_balanced(p,s)
        except ValueError:pass
        else:raise AssertionError('bad partition accepted')
    # This certificate satisfies every singleton-block discrepancy bound but
    # violates the new global half-size requirement.
    assert not validate_global([[i] for i in range(4)],[[i] for i in range(4)],
                               {i:0 for i in range(4)})
    # A legacy balanced but globally unbalanced colouring can be found for
    # n=4 and singleton blocks; the new property is genuinely stronger.
    print('PASS balanced every block AND exactly floor(n/2) red: small pairs',hist,
          'total',sum(hist.values()))
    print('PASS larger deterministic partition pairs:',extra,
          'and 100000-element test exactly 50000 red')
    print('PASS parallel incidences, invalid partitions and globally unbalanced controls')


if __name__=='__main__':main()
