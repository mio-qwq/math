#!/usr/bin/env python3
"""Independent literal-block verification of Euler balanced partition colouring."""
from itertools import product
from random import Random
from balanced_partitions import (balanced_colouring, verify_balance,
                                 component_avoiding_transversal)


def all_partitions(n):
    if n == 0:
        yield []
        return
    blocks = []
    def rec(x):
        if x == n:
            yield [tuple(b) for b in blocks]
            return
        for b in blocks:
            b.append(x)
            yield from rec(x+1)
            b.pop()
        blocks.append([x])
        yield from rec(x+1)
        blocks.pop()
    yield from rec(0)


def brute_exists(P, S, n):
    for bits in product((0,1), repeat=n):
        if all(abs(sum(bits[x] == 0 for x in b)-sum(bits[x] == 1 for x in b)) <= 1
               for b in P+S):
            return True
    return False


def check_original(P, S, colouring):
    n=sum(map(len,P))
    assert len(colouring)==n and set(colouring)==set(range(n))
    for block in P+S:
        seen=[colouring[x] for x in block]
        assert all(v in (0,1) for v in seen)
        assert abs(seen.count(0)-seen.count(1))<=1,(P,S,block,seen)
        if len(block)>1:assert 0 in seen and 1 in seen
    return True


def run():
    counts={}
    for n in range(7):
        P=list(all_partitions(n))
        count=0
        for a in P:
            for b in P:
                result=balanced_colouring(a,b)
                assert verify_balance(a,b,result)
                if n>0:check_original(a,b,result)
                if n<=4:assert brute_exists(a,b,n)
                if a and b and all(len(block)>=2 for block in a+b):
                    R=component_avoiding_transversal(a,b)
                    assert all(len(set(block)&R)==1 for block in a)
                    assert all(not set(block)<=R for block in b)
                count+=1
        counts[n]=count
    assert counts=={0:1,1:1,2:4,3:25,4:225,5:2704,6:41209},counts
    rng=Random(20261010)
    extra=0
    for n in range(7,81):
        for _ in range(37):
            def arbitrary_partition():
                perm=list(range(n));rng.shuffle(perm)
                out=[];i=0
                while i<n:
                    size=rng.randint(1,min(9,n-i))
                    out.append(perm[i:i+size]);i+=size
                return out
            a=arbitrary_partition();b=arbitrary_partition()
            c=balanced_colouring(a,b)
            assert check_original(a,b,c)
            extra+=1
    P=[list(range(100000))]
    S=[[i] for i in range(100000)]
    c=balanced_colouring(P,S)
    assert verify_balance(P,S,c)
    assert check_original([[0,1]],[[0,1]],balanced_colouring([[0,1]],[[0,1]]))
    bad=[([[0,0]],[[0]]), ([[0,1],[1,2]],[[0,1,2]]),
         ([[0,1]],[[0,2]]), ([[]], [[0]]),
         ([[0]],[[0,1]])]
    for a,b in bad:
        try:balanced_colouring(a,b)
        except ValueError:pass
        else:raise AssertionError('invalid partition accepted')
    assert not verify_balance([[0,1]],[[0,1]],{0:0,1:0})
    try:component_avoiding_transversal([[0]],[[0]])
    except ValueError:pass
    else:raise AssertionError('singleton restriction not enforced')
    print('PASS exhaustive two-partition pairs:',counts,'total',sum(counts.values()))
    print('PASS extra seeded n=7..80:',extra,'100000-singleton stress PASS')
    print('PASS parallel-incidence, wrong-certificate, six malformed/singleton negative controls')


if __name__=='__main__':run()
