#!/usr/bin/env python3
"""Exact semantic checks for the universal written reciprocal-trace proof.

Finite samples validate formulas, not a universal extremum. The rational
coefficient chain and the tangent-polynomial certificate are checked exactly.
Accept/reject logic uses explicit exceptions, including under python -O.
"""
from __future__ import annotations
import argparse
import copy
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import random

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def multiply(a, b):
    n = len(a)
    return [[sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def transpose(a):
    return [list(row) for row in zip(*a)]


def add(a, b):
    return [[x + y for x, y in zip(r, s)] for r, s in zip(a, b)]


def trace_product(*matrices):
    value = matrices[0]
    for b in matrices[1:]:
        value = multiply(value, b)
    return sum(value[i][i] for i in range(len(value)))


def quantities(m, mt):
    return {
        'T': trace_product(m, mt, m, mt),
        'L': trace_product(m, m, m, m),
        'Y': trace_product(m, m, mt, mt),
        'X': trace_product(m, m, m, mt),
        'R4': trace_product(*([add(m, mt)] * 4)),
    }


def check_quantities(q, coefficient):
    t, l, y, x, r4 = (q[k] for k in ('T', 'L', 'Y', 'X', 'R4'))
    need(min(t, l, y, x) >= 0, 'negative trace quantity')
    need(y <= t, 'first Frobenius inequality')
    need(4*x*x <= (y+l)*(t+y), 'second Frobenius inequality')
    need(2*x*x <= (t+l)**2, 'square majorization')
    need(x <= F(177,250)*(t+l), 'rational square-root majorant')
    need(r4 == 2*l+8*x+4*y+2*t, 'sixteen-term trace expansion')
    need(coefficient*r4 <= 2*(t+l), 'symmetrized trace bound')


def constant_certificate():
    return {
        'schema': 'GP2-reciprocal-trace-rational-v1',
        'trace_coefficients_T_L_Y_X': [2,2,4,8],
        'sqrt_half_majorant': '177/250',
        'symmetrized_trace_multiplier': '1458/125',
        'off_diagonal_coefficient': '125/729',
        'mass_coefficients': ['1']*3+['125/729']*3,
        'tangent_masses': ['5/42']*3+['3/14']*3,
        'tangent_remainder_coefficients': [1,2,3],
        'empty_orbit_lower': '125/74088',
        'strict_density_upper': '73963/296352',
        'direction_patterns_row_major': [[0,0,0,0],[1,1,1,1],[0,1,1,0],[1,0,0,1]],
        'scope': 'All finite alphabets, all probability weights, arbitrary three-valued ordered-pair relation; semantic samples are not a universal proof',
    }


def validate_certificate(c):
    need(c['schema'] == 'GP2-reciprocal-trace-rational-v1', 'schema binding')
    need(c['trace_coefficients_T_L_Y_X'] == [2,2,4,8], 'trace coefficient binding')
    z = F(c['sqrt_half_majorant'])
    need(z >= 0 and z*z >= F(1,2), 'square-root majorant invalid')
    multiplier = 6+8*z
    need(F(c['symmetrized_trace_multiplier']) == multiplier, 'matrix multiplier identity')
    coefficient = F(c['off_diagonal_coefficient'])
    need(coefficient == 2/multiplier, 'matrix coefficient identity')
    cs = list(map(F,c['mass_coefficients']))
    ts = list(map(F,c['tangent_masses']))
    need(len(cs) == len(ts) == 6 and cs == [F(1)]*3+[coefficient]*3, 'six-class coefficient binding')
    need(min(ts) >= 0 and sum(ts) == 1, 'tangent probability binding')
    lower = F(c['empty_orbit_lower'])
    need(all(c0*t0**3 == lower for c0,t0 in zip(cs,ts)), 'constant tangent slope')
    need(sum(c0*t0**4 for c0,t0 in zip(cs,ts)) == lower, 'tangent objective')
    need(c['tangent_remainder_coefficients'] == [1,2,3], 'quartic remainder identity')
    # Exact polynomial coefficients of both sides in x, for a symbolic t.
    # x^4 - 4t^3*x + 3t^4 = (x-t)^2(x^2+2tx+3t^2).
    left = {4:F(1), 3:F(0), 2:F(0), 1:F(-4), 0:F(3)}
    right = {k:F(0) for k in range(5)}
    for i,a in [(2,1),(1,-2),(0,1)]:
        for j,b in [(2,1),(1,2),(0,3)]:
            right[i+j] += a*b
    need(left == right, 'symbolic quartic polynomial identity')
    need(F(c['strict_density_upper']) == (1-lower)/4, 'rotation-density coefficient')
    need(lower == F(125,74088) and lower > F(1,729), 'theorem lower binding')
    need(c['direction_patterns_row_major'] == [[0,0,0,0],[1,1,1,1],[0,1,1,0],[1,0,0,1]], 'four-pattern binding')
    return coefficient, lower


def check_relation(levels, mu, coefficient, lower):
    n = len(mu)
    need(n>0 and len(levels)==n and all(len(r)==n for r in levels), 'alphabet/matrix dimensions')
    need(all(type(v) is int and 0<=v<3 for r in levels for v in r), 'level range/type')
    need(all(v>=0 for v in mu) and sum(mu)==1, 'letter probability distribution')
    kernels = {(i,j):[[int(levels[a][b]==i and levels[b][a]==j) for b in range(n)] for a in range(n)] for i,j in product(range(3),repeat=2)}
    classes = [(0,0),(1,1),(2,2),(0,1),(0,2),(1,2)]
    masses = []
    contribution = F(0)
    for i,j in classes:
        k = kernels[i,j]; kt = kernels[j,i]
        r = [[k[a][b]+kt[a][b] if i!=j else k[a][b] for b in range(n)] for a in range(n)]
        mass = sum(mu[a]*mu[b]*r[a][b] for a,b in product(range(n),repeat=2))
        masses.append(mass)
        m = [[mu[a]*k[a][b] for b in range(n)] for a in range(n)]
        mt = [[mu[a]*kt[a][b] for b in range(n)] for a in range(n)]
        q = quantities(m,mt)
        check_quantities(q,coefficient)
        rmatrix = [[mu[a]*r[a][b] for b in range(n)] for a in range(n)]
        r4 = trace_product(*([rmatrix]*4))
        need(r4 >= mass**4, 'symmetric C4 density inequality')
        if i==j:
            contribution += q['T']
        else:
            need(q['R4']==r4, 'weighted symmetric-union binding')
            contribution += 2*(q['T']+q['L'])
    need(sum(masses)==1, 'six reciprocal classes partition pairs')
    e = F(0); directed = F(0)
    for a,b,c,d in product(range(n),repeat=4):
        w = mu[a]*mu[b]*mu[c]*mu[d]
        event = levels[a][b]==levels[c][d] and levels[b][c]==levels[d][a]
        if event:e+=w
        # Each counted event has one common unordered reciprocal class
        # on all cross pairs; literal orientation tests count all four types.
        hit=0
        for i,j in classes:
            k=kernels[i,j]; kt=kernels[j,i]
            if i==j:
                hit += k[a][b]*k[a][d]*k[c][b]*k[c][d]
            else:
                hit += (k[a][b]*k[a][d]*k[c][b]*k[c][d]
                        +kt[a][b]*kt[a][d]*kt[c][b]*kt[c][d]
                        +k[a][b]*kt[a][d]*kt[c][b]*k[c][d]
                        +kt[a][b]*k[a][d]*k[c][b]*kt[c][d])
        need(hit in (0,1) and (not hit or event), 'pattern disjointness/defect inclusion')
        directed += w*hit
    need(directed==contribution, 'literal pattern / matrix trace agreement')
    weighted = sum((F(1) if i<3 else coefficient)*r**4 for i,r in enumerate(masses))
    need(e>=contribution>=weighted>=lower, 'complete rational defect chain')
    return e


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'trace_certificate.json')
    args=ap.parse_args();c=json.loads(args.certificate.read_text());coefficient,lower=validate_certificate(c)
    rows=0; smallest=F(1)
    for entries in product(range(3),repeat=4):
        levels=[list(entries[:2]),list(entries[2:])]
        for mu in ([F(1,2)]*2,[F(1,3),F(2,3)],[F(1),F(0)]):
            smallest=min(smallest,check_relation(levels,mu,coefficient,lower));rows+=1
    rng=random.Random(2026101303)
    for n in (1,3,4):
        for trial in range(18):
            levels=[[rng.randrange(3) for _ in range(n)] for _ in range(n)]
            weights=[rng.randrange(1,8) for _ in range(n)];mu=[F(w,sum(weights)) for w in weights]
            smallest=min(smallest,check_relation(levels,mu,coefficient,lower));rows+=1
    matrices=0
    for n in (1,2,3,4):
        for trial in range(20):
            m=[[F(rng.randrange(4),7) for _ in range(n)] for _ in range(n)]
            check_quantities(quantities(m,transpose(m)),coefficient);matrices+=1
    negative=[]
    changes={'sqrt_half_majorant':'1/2','symmetrized_trace_multiplier':'12',
             'off_diagonal_coefficient':'126/729','empty_orbit_lower':'1/500',
             'strict_density_upper':'1/4','trace_coefficients_T_L_Y_X':[2,2,4,7],
             'tangent_masses':['1/6']*6,'tangent_remainder_coefficients':[1,2,2],
             'direction_patterns_row_major':[[0,0,0,0]]}
    for field,value in changes.items():
        bad=copy.deepcopy(c);bad[field]=value
        try:validate_certificate(bad)
        except ValueError as error:negative.append({'field':field,'rejected':str(error)})
        else:raise RuntimeError('Damaged certificate accepted: '+field)
    for field,levels,mu in [('bad-level',[[0,3],[1,2]],[F(1,2)]*2),('negative-weight',[[0,1],[2,0]],[F(2),F(-1)]),('boolean-level',[[True,1],[2,0]],[F(1,2)]*2)]:
        try:check_relation(levels,mu,coefficient,lower)
        except ValueError as error:negative.append({'field':field,'rejected':str(error)})
        else:raise RuntimeError('Damaged relation accepted: '+field)
    print(json.dumps({'status':'PASS','relation_cases':rows,'rational_matrix_cases':matrices,
                     'smallest_sample_E':str(smallest),'universal_rational_E_lower':str(lower),
                     'universal_rational_density_upper':c['strict_density_upper'],
                     'negative_controls':negative,
                     'scope':'Samples check semantics; the written trace/Cauchy/polynomial argument proves universality'},indent=2))


if __name__=='__main__':main()
