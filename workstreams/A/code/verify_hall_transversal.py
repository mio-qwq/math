#!/usr/bin/env python3
"""Full small-partition check + independent brute existence + negative controls."""
from itertools import combinations, product
from random import Random
from hall_transversal import hall_transversal,verify_independently


def partitions_min2(values):
    values=tuple(values)
    if not values:
        yield ()
        return
    head=values[0]
    for tail in partitions_min2(values[1:]):
        for j in range(len(tail)):
            block=tail[j]
            new=tail[:j]+(tuple(sorted(block+(head,))),)+tail[j+1:]
            yield tuple(sorted(new))
        yield ((head,),)+tail


def all_set_partitions_min2(n):
    seen=set()
    for partition in partitions_min2(tuple(range(n))):
        blocks=tuple(sorted(tuple(sorted(b)) for b in partition))
        if all(len(b)>=2 for b in blocks) and blocks not in seen:
            seen.add(blocks)
            yield blocks


def brute_exists(P,S):
    for choice in product(*P):
        if all(not set(B)<=set(choice) for B in S):return True
    return False


def run():
    total=0; with_danger=0; with_parallel=0
    for n in range(2,9):
        partitions=list(all_set_partitions_min2(n))
        for P in partitions:
            for S in partitions:
                R,match,candidates=hall_transversal(P,S)
                assert verify_independently(P,S,R)
                if n<=6:
                    assert brute_exists(P,S), (P,S)
                total+=1
                if match:with_danger+=1
                if len(match)>=2 and len(P)>=2:
                    with_parallel+=1
    rng=Random(121882)
    for n in range(10,80,2):
        for trial in range(60):
            arr=list(range(n));rng.shuffle(arr)
            part=[arr[i:i+2] for i in range(0,n,2)]
            arr2=list(range(n));rng.shuffle(arr2)
            other=[arr2[i:i+2] for i in range(0,n,2)]
            R,match,candidates=hall_transversal(part,other)
            assert verify_independently(part,other,R)
            total+=1
    # True adversarial parallel 2-cycle: P parts and S blocks cross.
    P=[[0,2],[1,3]];S=[[0,1],[2,3]]
    R,match,_=hall_transversal(P,S)
    assert len(match)==2 and verify_independently(P,S,R)
    # Safe-component loops: candidate pair entirely within a Q block.
    P=[[0,1],[2,3]];S=[[0,1],[2,3]]
    R,match,_=hall_transversal(P,S)
    assert match=={} and verify_independently(P,S,R)
    invalid=[([[0,1]],[[0],[1]]),([[0],[1]],[[0,1]]),
             ([[0,1],[1,2]],[[0,2],[1]]), ([[0,1]],[[0,1],[2,3]])]
    for P,S in invalid:
        try:hall_transversal(P,S)
        except ValueError:pass
        else:raise AssertionError('invalid weak hypotheses accepted')
    print(f'PASS all two-partition pairs n=2..8 and larger deterministic checks: {total} pairs;'
          f' dangerous cases {with_danger}, multicomponent cases {with_parallel};'
          f' parallel/safe/invalid controls PASS')

if __name__=='__main__':run()
