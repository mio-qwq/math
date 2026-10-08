"""Additional rectangular-sized integration replay; not a general proof."""
import random
from fractions import Fraction as Q

import compatible_pair_costs as solver
import check_compatible_pair_costs as checker

rng = random.Random(202610080923)
counts = {'E': 0, 'F': 0}
for t in range(80):
    psize, isize, ssize, jsize = 3, 4, 3, 4
    E = {(p, i) for p in range(psize) for i in range(isize)
         if rng.randrange(3) != 0}
    F = {(s, j) for s in (0, 1) for j in (0, 1, 2)} | {(2, 3)}
    R = {(p, j) for p in range(psize) for j in range(jsize)
         if rng.randrange(4) != 0}
    C = {(i, s) for i in range(isize) for s in range(ssize)
         if rng.randrange(4) != 0}
    x = [[Q(rng.randrange(9), rng.randrange(1, 6)) for j in range(jsize)]
         for p in range(psize)]
    y = [[Q(rng.randrange(9), rng.randrange(1, 6)) for s in range(ssize)]
         for i in range(isize)]
    z = [[Q(rng.randrange(1, 10), rng.randrange(1, 6)) for j in range(jsize)]
         for i in range(isize)]
    h = [[Q(0) for s in range(ssize)] for p in range(psize)]
    for p, j in R:
        for i, s in C:
            if (p, i) in E and (s, j) in F:
                h[p][s] = max(h[p][s], x[p][j]*y[i][s]/z[i][j])
    dims = dict(P=psize, I=isize, S=ssize, J=jsize)
    if t % 2:
        dims = dict(P=ssize, I=jsize, S=psize, J=isize)
        E, F = F, E
        R, C = {(s, i) for i, s in C}, {(j, p) for p, j in R}
        x, y = [list(v) for v in zip(*y)], [list(v) for v in zip(*x)]
        h, z = [list(v) for v in zip(*h)], [list(v) for v in zip(*z)]
    data = dict(format='compatible-pair-costs-v1', sizes=dims,
                E=[list(v) for v in sorted(E)], F=[list(v) for v in sorted(F)],
                R=[list(v) for v in sorted(R)], C=[list(v) for v in sorted(C)],
                costs={name:[[str(v) for v in row] for row in mat]
                       for name,mat in zip(('R','C','H','Z'), (x,y,h,z))})
    cert = solver.solve(data)
    actual = checker.check(cert)
    counts[cert['structured_relation']] += 1
    assert Q(actual['cover_cost']) <= Q(actual['H_mass'])+Q(actual['Z_mass'])
    assert Q(actual['deletion_cost']) <= Q(actual['H_mass'])+Q(actual['uncovered_mass'])
print({'PASS': 80, 'structured_orientation_counts': counts,
       'base_dimensions': [3,4,3,4], 'exact_arithmetic': True,
       'general_theorem_proof': False})
