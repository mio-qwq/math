#!/usr/bin/env python3
"""Independent finite checks for incidence-multigraph red/blue splitting."""
from itertools import product
from random import Random
from linear_split import split_partitions, transversal
from verify_hall_transversal import all_set_partitions_min2


def run():
    cases=0;allsplit=0
    for n in range(2,9):
        parts=list(all_set_partitions_min2(n))
        for P in parts:
            for S in parts:
                colours=split_partitions(P,S)
                assert set(colours)==set(range(n))
                assert all({colours[x] for x in block}=={0,1} for block in P+S)
                if n<=6:
                    assert any(all({a[x] for x in block}=={0,1} for block in P+S)
                               for a in ({i:b for i,b in enumerate(bits)}
                                         for bits in product((0,1),repeat=n)))
                roots={next(x for x in block if colours[x]==0) for block in P}
                assert all(len(set(block)&roots)==1 for block in P)
                assert all(not set(block)<=roots for block in S)
                cases+=1;allsplit+=1
    rng=Random(4658)
    for n in range(10,80,2):
        for i in range(60):
            a=list(range(n));rng.shuffle(a)
            b=list(range(n));rng.shuffle(b)
            pa=[a[k:k+2] for k in range(0,n,2)]
            sb=[b[k:k+2] for k in range(0,n,2)]
            colours=split_partitions(pa,sb)
            assert all({colours[x] for x in c}=={0,1} for c in pa+sb)
            cases+=1
    P=[[0,2],[1,3]];S=[[0,1],[2,3]]
    assert all({split_partitions(P,S)[x] for x in B}=={0,1} for B in P+S)
    P=[[0,1],[2,3]];S=[[0,1],[2,3]]
    assert all({split_partitions(P,S)[x] for x in B}=={0,1} for B in P+S)
    for P,S in [([[0,1]],[[0],[1]]), ([[0],[1]],[[0,1]]),
                ([[0,1],[2,3]],[[0,1],[2,2]]),
                ([[0,1],[1,2]],[[0,1,2]])]:
        try:split_partitions(P,S)
        except ValueError:pass
        else:raise AssertionError('invalid partition accepted')
    print(f'PASS {cases} bipartite-multigraph partition pairs, both colours in EVERY block;'
          ' safe transversal verified; parallel/loop-equivalent/negative cases PASS')
if __name__=='__main__':run()
