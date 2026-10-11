#!/usr/bin/env python3
"""Bounded exact regressions. All random choices are seeded test selection,
not probabilistic acceptance. Saved witnesses are checked directly.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path
import random
import sys
import time
import construct
import check

start = time.monotonic()
routes, windows = Counter(), []
saved = []
total = 0

for modulus, sizes in [(3, range(3, 11)), (7, range(3, 7))]:
    f = construct.Field(modulus)
    for n in sizes:
        invertible = 0
        for a in product(range(f.size), repeat=n):
            a = list(a)
            if construct.kernel(construct.matrix(a), f) is not None:
                continue
            cert = construct.witness(a, modulus)
            check.check(cert)
            routes[cert['route']] += 1
            invertible += 1
            total += 1
        windows.append({'modulus': modulus, 'n': n, 'all_columns': f.size**n,
                        'invertible_checked': invertible})

rng = random.Random(202610117)
for modulus in (0xb, 0x13, 0x11b):
    f = construct.Field(modulus)
    for n in (3, 4, 5, 6, 10, 14, 22, 26):
        accepted, trials = 0, 0
        while accepted < 8:
            trials += 1
            a = [rng.randrange(f.size) for _ in range(n)]
            if construct.kernel(construct.matrix(a), f) is not None:
                continue
            cert = construct.witness(a, modulus)
            check.check(cert)
            routes[cert['route']] += 1
            total += 1
            accepted += 1
            if n in (10, 14, 22, 26) and accepted == 1:
                saved.append(cert)
        windows.append({'modulus': modulus, 'n': n, 'seeded_trials': trials,
                        'invertible_checked': accepted})

# Direct n=2 F4 boundary: enumerate every pair, with no theorem constructor.
A = [[1, 2], [2, 1]]
assert check.nonsingular(A, 7)
assert all(all(row) for row in A)
vectors = [list(v) for v in product(range(4), repeat=2) if any(v)]
boundary_pairs, boundary_rd = 0, 0
for u in vectors:
    for v in vectors:
        if u == v:
            continue
        boundary_pairs += 1
        boundary_rd += int(check.related(u, v, 7) and
                           check.related(check.raw_apply(A, u, 7), check.raw_apply(A, v, 7), 7))
assert boundary_rd == 0
negative = check.negative_controls(saved[0])

# Reject singular inputs, which are outside the theorem's scope.
# MDS inheritance for actual MDS inputs is proved in PROOF-v2.md, Section 5a.
for a in ([0, 0, 0], [1, 1, 1, 1]):
    try:
        construct.witness(a, 7)
    except ValueError:
        negative += 1
    else:
        raise AssertionError('constructor accepted singular input')

root = Path(__file__).resolve().parent
(root/'certificates').mkdir(exist_ok=True)
(root/'certificates'/'regression-witnesses.json').write_text(json.dumps(saved, indent=2)+'\n')
result = {'status': 'PASS', 'python': sys.version, 'checked': total,
          'routes': dict(routes), 'windows': windows,
          'boundary_n2_F4': {'ordered_nontrivial_pairs': boundary_pairs, 'RD_pairs': boundary_rd},
          'negative_controls': negative, 'seconds': time.monotonic()-start}
(root/'REGRESSION.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
