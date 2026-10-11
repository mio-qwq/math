#!/usr/bin/env python3
"""Exact ALL-minor checker using division-free Laplace recurrence.
Does not import Gaussian elimination or the C++ field tables.
"""
from itertools import combinations
import json
from pathlib import Path
import sys
import time
from check import product, irreducible, raw_matrix, require, check


def verify(a, p):
    require(irreducible(p), 'reducible modulus')
    n = len(a)
    require(all(type(x) is int and 0 <= x < 1 << (p.bit_length()-1) for x in a), 'bad encoding')
    M = raw_matrix(a)
    previous = {0: 1}
    counts = []
    for k in range(1, n+1):
        subsets = [(sum(1<<i for i in s), s) for s in combinations(range(n), k)]
        current = {}
        for rm, rs in subsets:
            row = rs[0]
            base = (rm ^ (1<<row)) << n
            for cm, cs in subsets:
                det = 0
                for j in cs:
                    det ^= product(M[row][j], previous[base | (cm ^ (1<<j))], p)
                require(det != 0, 'singular minor rows=%r cols=%r' % (rs, cs))
                current[(rm << n) | cm] = det
        counts.append(len(current))
        previous = current
    return counts


if __name__ == '__main__':
    start = time.monotonic()
    cert = json.loads(Path(sys.argv[1]).read_text())
    check(cert)
    counts = verify(cert['column'], cert['modulus'])
    damaged = cert['column'][:]
    damaged[0] = 0
    try:
        verify(damaged, cert['modulus'])
    except ValueError:
        pass
    else:
        raise AssertionError('zero-entry non-MDS negative control accepted')
    print(json.dumps({'status':'PASS','n':len(cert['column']), 'modulus':cert['modulus'],
                      'minors_by_order':counts, 'total_minors':sum(counts),
                      'negative_controls':1, 'seconds':time.monotonic()-start}))
