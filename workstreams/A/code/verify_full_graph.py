#!/usr/bin/env python3
"""Independent graph/colouring regression for construct_full_graph.py."""
from collections import defaultdict
from itertools import combinations
from random import Random
from construct_full_graph import construct,parse_graph,independent_validate,components


def greedy(E,unique=False):
    used=defaultdict(set);result=[]
    for i,(u,v) in enumerate(E):
        c=i if unique else next(x for x in range(len(E)+1)
                                if x not in used[u] and x not in used[v])
        used[u].add(c);used[v].add(c);result.append([u,v,c])
    return result


def obstruction(V,edges):
    for S in components(V,[tuple(e) for e in edges]):
        inside=[e for e in edges if e[0] in S and e[1] in S]
        if len(S)==2 and len(inside)==1:return True
        if len(S)>=4 and len(inside)==len(S):
            degree={v:0 for v in S}
            for u,v,c in inside:degree[u]+=1;degree[v]+=1
            if all(x==2 for x in degree.values()) and len({c for u,v,c in inside})==2:
                return True
    return False


def run():
    counts=defaultdict(int);total=0;rng=Random(71397)
    for n in range(7):
        possible=list(combinations(range(n),2))
        if n<=5:masks=range(1<<len(possible))
        else:masks=[0,(1<<len(possible))-1]+[rng.getrandbits(len(possible)) for _ in range(10000)]
        for mask in masks:
            edges=[p for i,p in enumerate(possible) if mask&(1<<i)]
            for unique in (False,True):
                data={'n':n,'edges':greedy(edges,unique)}
                bad=obstruction(set(range(n)),data['edges'])
                try:certificate=construct(data)
                except ValueError as e:
                    if not bad:raise AssertionError(('false obstruction',data,e))
                    counts['correct_obstruction']+=1
                else:
                    if bad:raise AssertionError(('accepted obstruction',data))
                    _,original=parse_graph(data)
                    assert independent_validate(set(range(n)),original,
                                                [tuple(e) for e in certificate['order']])
                    assert len(certificate['order'])==len(original)
                    counts['valid_order']+=1
                total+=1
    for n in (7,8,9,10,12):
        possible=list(combinations(range(n),2))
        for _ in range(600):
            probability=rng.random()
            edges=[p for p in possible if rng.random()<probability]
            rng.shuffle(edges)
            data={'n':n,'edges':greedy(edges)}
            bad=obstruction(set(range(n)),data['edges'])
            try:certificate=construct(data)
            except ValueError as e:
                if not bad:raise AssertionError(('false obstruction large',data,e))
                counts['correct_obstruction']+=1
            else:
                assert not bad
                _,original=parse_graph(data)
                assert independent_validate(set(range(n)),original,
                                            [tuple(e) for e in certificate['order']])
                counts['valid_order']+=1
            total+=1
    invalid=[
        {'n':3,'edges':[[0,1,0],[0,2,0]]},
        {'n':2,'edges':[[0,1,0],[0,1,1]]},
        {'n':2,'edges':[[0,0,0]]},
        {'n':4,'edges':[[0,4,0]]},
        {'n':3,'edges':[[0,1,True]]},
    ]
    for data in invalid:
        try:construct(data)
        except ValueError:pass
        else:raise AssertionError('invalid input accepted')
    assert total==25204
    assert counts['valid_order']==24070 and counts['correct_obstruction']==1134
    print('PASS 25204 tested graph/colouring inputs:',
          dict(counts),'negative input controls:',len(invalid))


if __name__=='__main__':run()
