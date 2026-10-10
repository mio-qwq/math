#!/usr/bin/env python3
"""Witness-producing CLI for the fixed-d-colour d-regular subcase.
Usage: python3 workstreams/A/code/construct_order_cli.py graph.json
Input: {"n": 6, "d": 5, "edges": [[0,1,0], ...]}.
Output: {"order": [[u,v,colour], ...], "verified": true, "cycle_count": k}.
Do not use for graphs outside the listed hypotheses. Standard library only.
"""
import argparse
import json
import sys
from verify_all_regular import make_order, validate


def get_input(data):
    n, d = data['n'], data['d']
    if type(n) is not int or type(d) is not int or not (3 <= d < n):
        raise ValueError('require integer n>d>=3')
    if n*d % 2 != 0: raise ValueError('bad degree parity')
    V = set(range(n)); E = []; pairs = set()
    for v in data['edges']:
        if len(v) != 3 or any(type(x) is not int for x in v):
            raise ValueError('edge must be a triple of integers')
        a,b,c = v
        if not (a in V and b in V and a != b and 0 <= c < d):
            raise ValueError('bad endpoint or colour')
        a,b = sorted((a,b))
        if (a,b) in pairs: raise ValueError('duplicate edge')
        pairs.add((a,b)); E.append((a,b,c))
    if len(E) != n*d//2:raise ValueError('missing or extra edges')
    palettes = {v:set() for v in V};degrees = {v:0 for v in V}
    for a,b,c in E:
        for v in (a,b):
            if c in palettes[v]:raise ValueError('improper fixed colouring')
            palettes[v].add(c);degrees[v]+=1
    if any(degrees[v]!=d or palettes[v]!=set(range(d)) for v in V):
        raise ValueError('not uniformly d-regular/d-edge-coloured')
    return V,E,d


def certify(data):
    V,E,d = get_input(data)
    result,cycles = make_order(V,E,d)
    # Independent original-definition verifier from frozen source module:
    if not validate(V,E,result,d):raise AssertionError('bad witness')
    return {'order':[list(t) for t in result], 'verified':True, 'cycle_count':cycles}


def selftest():
    for n in (4,6,8,10,12):
        d=n-1;E=[]
        for c in range(d):
            pairs=[(n-1,c)]+[((c+i)%d,(c-i)%d) for i in range(1,n//2)]
            for a,b in pairs:E.append([a,b,c])
        data={'n':n,'d':d,'edges':E}
        q=certify(data);V,En,deg=get_input(data)
        assert validate(V,En,[tuple(e) for e in q['order']],deg)
        assert not validate(V,En,[tuple(e) for e in q['order'][:-1]],deg)
        for bad in (E[:-1], E+[E[0]], [[a,b,0] for a,b,c in E]):
            try:certify({**data,'edges':bad})
            except (ValueError,AssertionError):pass
            else:raise AssertionError('invalid input accepted')
    print('PASS five complete graphs K4..K12, exact order replay, omitted-edge and 15 invalid-input tests')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file',nargs='?',help='JSON input (default stdin)')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    if args.self_test:return selftest()
    with (open(args.file,encoding='utf8') if args.file else sys.stdin) as f:
        data=json.load(f)
    print(json.dumps(certify(data),separators=(',',':')))


if __name__=='__main__':main()
