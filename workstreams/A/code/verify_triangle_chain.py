#!/usr/bin/env python3
"""End-to-end sequence verification of iterated triangle expansions from K4."""
from random import Random

def check(vertices,edges,order):
    assert len(order)==len(edges) and set(order)==set(edges)
    assert len({tuple(sorted((u,v))) for u,v,c in edges})==len(edges)
    seq={v:[] for v in vertices}
    for u,v,c in order:
        seq[u].append(c)
        seq[v].append(c)
    assert all(len(seq[v])==3 and len(set(seq[v]))==3 for v in vertices)
    assert all(seq[u]!=seq[v] for u,v,c in edges)

def expand(vertices,edges,order,root):
    ext=[e for e in order if root in e[:2]]
    assert len(ext)==3
    neighbors=[v if u==root else u for u,v,c in ext]
    colors=[e[2] for e in ext]
    a,b,c=max(vertices)+1,max(vertices)+2,max(vertices)+3
    newext=[(c,neighbors[0],colors[0]),(a,neighbors[1],colors[1]),(b,neighbors[2],colors[2])]
    internal=[(a,b,colors[0]),(b,c,colors[1]),(c,a,colors[2])]
    remap=dict(zip(ext,newext))
    old=[remap.get(e,e) for e in order]
    i0=old.index(newext[0])
    i2=old.index(newext[2])
    orders=[
        old[:i0]+[internal[0],internal[1],internal[2]]+old[i0:],
        old[:i0]+[internal[2],internal[0],internal[1]]+old[i0:],
        old[:i0]+[internal[2]]+old[i0:i2]+[internal[0],internal[1]]+old[i2:],
    ]
    G=[e for e in edges if root not in e[:2]]+newext+internal
    vs=(vertices-{root})|{a,b,c}
    for candidate in orders:
        try:
            check(vs,G,candidate)
            return vs,G,candidate
        except AssertionError:
            pass
    raise AssertionError('all explicit three templates failed')

def main():
    E=[(0,1,0),(2,3,0),(0,2,1),(1,3,1),(0,3,2),(1,2,2)]
    order=sorted(E,key=lambda e:(e[0]+e[1],e[0],e[1]))
    vertices=set(range(4))
    check(vertices,E,order)
    rng=Random(31337)
    for i in range(160):
        root=rng.choice(sorted(vertices))
        vertices,E,order=expand(vertices,E,order,root)
    check(vertices,E,order)
    assert len(vertices)==324 and len(E)==486
    try:
        check(vertices,E,order[:-1])
    except AssertionError:
        pass
    else:
        raise AssertionError('incomplete edge order accepted')
    print('PASS 160 successful triangle expansions, final simple cubic G has 324 vertices / 486 edges')
if __name__=='__main__':
    main()
