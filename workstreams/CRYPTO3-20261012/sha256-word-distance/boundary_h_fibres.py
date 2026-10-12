#!/usr/bin/env python3
"""Discovery: exact affine pieces of one fixed-mask h collision boundary."""
import json
from pathlib import Path

MASK = (1 << 32) - 1
ALPHA = 0xfbca7000


def rotr(x,k):
    return ((x >> k) | (x << (32-k))) & MASK


def g(x):
    return rotr(x,17) ^ rotr(x,19) ^ (x >> 10)


def f(x):
    return rotr(x,7) ^ rotr(x,18) ^ (x >> 3)


def add_equation(pivots, row, value):
    out = dict(pivots)
    while row:
        pivot = row.bit_length()-1
        if pivot not in out:
            out[pivot] = (row,value)
            return out
        other, bit = out[pivot]
        row ^= other
        value ^= bit
    return None if value else out


def representative(pivots):
    word = 0
    for pivot, (row,value) in sorted(pivots.items()):
        if ((row & word).bit_count() & 1) ^ value:
            word |= 1 << pivot
    return word


def analyse():
    beta = g(ALPHA)
    grows = [sum(((g(1 << j) >> i) & 1) << j for j in range(32)) for i in range(32)]
    nodes = 0
    leaves = []
    def visit(bit, carry, pivots):
        nonlocal nodes
        nodes += 1
        if nodes > 1000000:
            raise RuntimeError('one-million-node discovery limit')
        if bit == 32:
            x = representative(pivots)
            y = x ^ ALPHA
            if (x+g(x)-y-g(y)) & MASK:
                raise ValueError('bad representative')
            leaves.append({'rank':len(pivots),'x':x,'y':y,'delta':(y-x)&MASK,
                           'F':(f(y)-f(x))&MASK,
                           'equations':[[r,b] for _,(r,b) in sorted(pivots.items())]})
            return
        left = (0,1) if (ALPHA >> bit) & 1 else (None,)
        right = (0,1) if (beta >> bit) & 1 else (None,)
        for xb in left:
            for gb in right:
                total = carry + (1-2*xb if xb is not None else 0) + (1-2*gb if gb is not None else 0)
                if total % 2:
                    continue
                new = pivots
                if xb is not None:
                    new = add_equation(new,1 << bit,xb)
                if new is not None and gb is not None:
                    new = add_equation(new,grows[bit],gb)
                if new is not None:
                    visit(bit+1,total//2,new)
    visit(12,0,{})
    result={'schema':'crypto3-h-boundary-fibres-discovery-v1','alpha':ALPHA,'beta':beta,
            'nodes':nodes,'leaves':leaves,'deltas':sorted({r['delta'] for r in leaves}),
            'scope':'Fixed local h-collision XOR mask; not a complete message schedule.'}
    return result


if __name__ == '__main__':
    result=analyse()
    output=Path(__file__).with_name('H_BOUNDARY_FIBRES.json')
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'nodes':result['nodes'],'leaves':len(result['leaves']),
                      'deltas':[hex(x) for x in result['deltas']],
                      'ranks':sorted({r['rank'] for r in result['leaves']})}))
