#!/usr/bin/env python3
"""Exact endpoint polynomials, sampling identities and five-index witness.

Standard library only; explicit exceptions remain active under python -O.
Finite tests do not replace the all-parameter written proofs.
"""
from collections import Counter, defaultdict, deque
from copy import deepcopy
from fractions import Fraction as Q
from itertools import permutations, product
from math import prod
from pathlib import Path
import argparse
import json

HERE = Path(__file__).resolve().parent
FIVE = '''0123 0124 0132 0134 0213 0214 0231 0234 0241 0243
0312 0314 0321 0324 0412 0413 0431 0432 1034 1042
1234 1324 1423 1432 2014 2034 2134 3014 3042 3124'''.split()
DELTA = Q(125, 74088)  # accepted rational weakening, not a fitted decimal


def need(ok, why):
    if not ok:
        raise ValueError(why)


def parse_words(raw, n, injective=False):
    words = [tuple(int(x) for x in w) for w in raw]
    need(len(set(words)) == len(words), 'duplicate word')
    need(all(len(w) == 4 and all(0 <= x < n for x in w) for w in words),
         'word domain')
    if injective:
        need(all(len(set(w)) == 4 for w in words), 'noninjective index word')
    return set(words)


def distribution(raw):
    need(raw and all(type(x) is int and x >= 0 for x in raw) and sum(raw) > 0,
         'invalid weights')
    return tuple(Q(x, sum(raw)) for x in raw)


def strict(n, code, literal=False):
    values = {s: 0 for s in product(range(n), repeat=3)}
    for _ in range(5):
        following = dict.fromkeys(values, 0)
        for s, val in values.items():
            for a in range(n):
                w = s+(a,)
                following[w[1:]] = max(following[w[1:]], val+int(w in code))
        values = following
    maximum = max(values.values())
    need(maximum <= 2, 'not a strict code')
    if literal:
        direct = max(sum(w[j:j+4] in code for j in range(5))
                     for w in product(range(n), repeat=8))
        need(direct == maximum, 'DP/literal strictness disagreement')
    return maximum


def rotations(w):
    return [w[j:]+w[:j] for j in range(4)]


def forbidden_endpoint(types):
    # Types 0=L, 1=R, 2=H, 3=N. First letter of edge in Q,
    # second in P: Q={1,2}, P={0,2}.
    return not any(types[j] in (1,2) and types[(j+1) % 4] in (0,2)
                   for j in range(4))


def endpoint_formula(l, r, h, n):
    need(l+r+h+n == 1, 'endpoint mass normalization')
    u, v = l+h, r+h
    return 1-4*u*v+4*u*v*h+2*u*u*v*v-4*u*v*h*h+h**4


def positive_formula(l, r, h, n):
    return (l**4+r**4+4*n*(l**3+r**3+l*l*r+l*r*r+h*(l*l+r*r+l*r))
            +n*n*(6*(l*l+r*r)+8*l*r+8*h*(l+r)+2*h*h)
            +4*n**3*(l+r+h)+n**4)


def type_polynomial():
    coeff = Counter()
    for w in product(range(4), repeat=4):
        if forbidden_endpoint(w):
            coeff[tuple(w.count(t) for t in range(4))] += 1
    # Independently encode every monomial in the written positive formula.
    declared = {(4,0,0,0):1, (0,4,0,0):1,
                (3,0,0,1):4, (0,3,0,1):4, (2,1,0,1):4, (1,2,0,1):4,
                (2,0,1,1):4, (0,2,1,1):4, (1,1,1,1):4,
                (2,0,0,2):6, (0,2,0,2):6, (1,1,0,2):8,
                (1,0,1,2):8, (0,1,1,2):8, (0,0,2,2):2,
                (1,0,0,3):4, (0,1,0,3):4, (0,0,1,3):4, (0,0,0,4):1}
    need(dict(coeff) == declared, 'type polynomial coefficient disagreement')
    checked = 0
    for raw in product(range(4), repeat=4):
        if not sum(raw):
            continue
        mu = distribution(raw)
        direct = sum((Q(c)*prod(mu[i]**e[i] for i in range(4))
                      for e,c in coeff.items()), Q())
        need(direct == endpoint_formula(*mu) == positive_formula(*mu),
             'endpoint formula disagreement')
        need(direct >= mu[0]**4+mu[1]**4, 'endpoint lower bound')
        checked += 1
    return {'type_words': 256, 'avoiding_words': sum(coeff.values()),
            'weight_cases': checked,
            'coefficients_L_R_H_N': {''.join(map(str,e)):c for e,c in sorted(coeff.items())}}


def endpoint_case(code, raw):
    mu = distribution(raw)
    nletters = len(mu)
    strict(nletters, code)
    P, RQ = {w[0] for w in code}, {w[-1] for w in code}
    sets = (P-RQ, RQ-P, P & RQ, set(range(nletters))-(P | RQ))
    l,r,h,n = [sum((mu[x] for x in s), Q()) for s in sets]
    p = sum((prod(mu[x] for x in w) for w in code), Q())
    incoming, outgoing = defaultdict(set), defaultdict(set)
    for w in code:
        incoming[w[1:]].add(w[0]); outgoing[w[:3]].add(w[3])
    active = set(incoming) & set(outgoing)
    b, a, d = Q(), Q(), Q()
    for s in active:
        need(incoming[s] <= sets[0] and outgoing[s] <= sets[1],
             'bridge endpoint support')
        mass = prod(mu[x] for x in s)
        i = sum((mu[x] for x in incoming[s]), Q())
        o = sum((mu[x] for x in outgoing[s]), Q())
        need(i <= l and o <= r, 'bridge pointwise mass')
        b += mass; a += mass*i*o; d += mass*min(i,o)
    literal_adj = sum((prod(mu[x] for x in w)
                       for w in product(range(nletters), repeat=5)
                       if w[:4] in code and w[1:] in code), Q())
    need(a == literal_adj, 'literal five-word adjacency')
    F = endpoint_formula(l,r,h,n)
    empty = Q()
    for w in product(range(nletters), repeat=4):
        hits = sum(v in code for v in rotations(w))
        need(hits <= 1, 'multiple selected rotations')
        if hits == 0:
            empty += prod(mu[x] for x in w)
    need(empty == 1-4*p, 'empty-orbit identity')
    need(empty >= F+DELTA*h**4, 'localized rational trace bound')
    need(a <= l*r*b <= l*r*(l+h)*(r+h) <= Q(1,16), 'adjacency chain')
    need(d <= b*min(l,r) and d*d <= b*a, 'deletion inequalities')
    # Exact steps underlying the inverse-square-root penalty; no floats.
    need((l+r)**2 >= 4*l*r and l*r <= Q(1,4), 'AM-GM domain')
    need(a <= l*r*(1-l)*(1-r), 'intrinsic bridge bound')
    need(empty >= F >= l**4+r**4 >= 2*(l*r)**2, 'rotation penalty chain')
    return {k:str(v) for k,v in
            dict(p=p, l=l, r=r, h=h, n=n, F=F, empty=empty,
                 adjacency=a, bridge_mass=b, deletion=d,
                 localized_slack=empty-F-DELTA*h**4).items()}


def graph_check(code):
    vertices = [w for w in product(range(5), repeat=4)
                if all(w[i] != w[i+1] for i in range(3))]
    edges = {w: [w[1:]+(a,) for a in range(5) if a != w[-1]] for w in vertices}
    need(code <= set(vertices), 'code invalid in original Kautz graph')
    distances = {}
    for source in code:
        dist = {source:0}; queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in edges[u]:
                if v not in dist:
                    dist[v] = dist[u]+1; queue.append(v)
        need(len(dist) == len(vertices), 'original directed reachability')
        distances[source] = dist
    triples = 0
    for u,v,w in permutations(code, 3):
        need(distances[u][w] != distances[u][v]+distances[v][w],
             'three vertices on a shortest directed path')
        triples += 1
    return {'vertices':len(vertices), 'arcs':sum(map(len, edges.values())),
            'BFS_sources':len(code), 'ordered_GP_triples':triples}


def sample_identity(code, raw, n):
    mu = distribution(raw)
    p = sum((prod(mu[x] for x in w) for w in code), Q())
    a = sum((prod(mu[x] for x in w) for w in product(range(len(mu)), repeat=5)
             if w[:4] in code and w[1:] in code), Q())
    indices4 = list(permutations(range(n), 4))
    indices5 = list(permutations(range(n), 5))
    expected_words, expected_adj, expected_empty = Q(), Q(), Q()
    maps = 0
    for f in product(range(len(mu)), repeat=n):
        mass = prod(mu[x] for x in f)
        D = {w for w in indices4 if tuple(f[x] for x in w) in code}
        adj = sum(w[:4] in D and w[1:] in D for w in indices5)
        empty = sum(not any(v in D for v in rotations(w)) for w in indices4)
        expected_words += mass*len(D)
        expected_adj += mass*adj
        expected_empty += mass*empty
        # This independently verifies preservation for every sampled map.
        strict(n, D)
        maps += 1
    need(expected_words == len(indices4)*p, 'sampling falling-four normalization')
    need(expected_adj == len(indices5)*a, 'sampling adjacent motif')
    need(expected_empty == len(indices4)*(1-4*p), 'sampling Boolean/rotation motif')
    return {'n':n, 'weights':raw, 'maps_checked':maps,
            'falling_four':len(indices4), 'falling_five':len(indices5),
            'p':str(p), 'a':str(a), 'expected_words':str(expected_words),
            'expected_adjacent':str(expected_adj), 'expected_empty':str(expected_empty)}


def evaluate(raw_words, expensive=True):
    code = parse_words(raw_words, 5, injective=True)
    maximum = strict(5, code, literal=expensive)
    orbits = {min(rotations(w)) for w in permutations(range(5),4)}
    occupied = Counter(min(rotations(w)) for w in code)
    need(len(code) == 30 and set(occupied) == orbits and set(occupied.values()) == {1},
         'thirty occupied rotation orbits')
    adjacent = [w for w in permutations(range(5),5) if w[:4] in code and w[1:] in code]
    need((0,1,2,3,4) in adjacent, 'specified nonindependent witness')
    restrictions = [sum(all(x != a for x in w) for w in code) for a in range(5)]
    need(restrictions == [6]*5, 'four-letter restrictions')
    result = {'schema':'GP2-sampling-endpoint-v1', 'five_words':raw_words,
              'five': {'size':len(code), 'strict_maximum':maximum,
                       'literal_eight_words':5**8, 'rotation_orbits':len(orbits),
                       'injective_adjacent_words':[''.join(map(str,w)) for w in adjacent],
                       'four_letter_sizes':restrictions},
              'type_polynomial':type_polynomial()}
    binary = {(0,0,0,1),(0,0,1,1)}
    fixtures = [('binary_equal', binary, [1,1]),
                ('binary_unequal', binary, [2,3]),
                ('binary_zero', binary, [0,1]),
                ('unused_letter', binary, [2,3,5]),
                ('five_uniform', code, [1]*5),
                ('five_unequal', code, [1,2,3,4,5]),
                ('empty', set(), [1])]
    result['endpoint_cases'] = {name:endpoint_case(C, raw) for name,C,raw in fixtures}
    if expensive:
        result['original_Kautz'] = graph_check(code)
        result['sampling'] = [sample_identity(binary, raw, n)
                              for raw,n in (([1,1],5),([2,3],5),([0,1],5),([1,2],6))]
    return result


def compare(claim, actual):
    need(claim == actual, 'certificate fields differ from exact reconstruction')


def negative_controls(actual):
    tests = [lambda:parse_words(FIVE+[FIVE[0]],5,True),
             lambda:parse_words(FIVE+['0001'],5,True),
             lambda:strict(2,{(0,0,0,0)}),
             lambda:distribution([1,-1,2])]
    for path, value in [(('five','size'),29),
                        (('type_polynomial','avoiding_words'),80),
                        (('original_Kautz','vertices'),321)]:
        damaged = deepcopy(actual); damaged[path[0]][path[1]] = value
        tests.append(lambda damaged=damaged:compare(damaged,actual))
    wrong = deepcopy(actual)
    wrong['sampling'][0]['falling_four'] = 5**4
    tests.append(lambda:compare(wrong,actual))
    for i,test in enumerate(tests):
        try:
            test()
        except ValueError:
            continue
        raise ValueError('negative control accepted: '+str(i))
    return len(tests)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-certificate', action='store_true')
    args = parser.parse_args()
    target = HERE/'sampling_endpoint_certificate.json'
    raw_words = FIVE if args.emit_certificate else json.loads(target.read_text())['five_words']
    actual = evaluate(raw_words)
    actual['negative_controls_rejected'] = negative_controls(actual)
    if args.emit_certificate:
        target.write_text(json.dumps(actual,indent=2,sort_keys=True)+'\n')
    else:
        compare(json.loads(target.read_text()),actual)
    print(json.dumps(actual,indent=2,sort_keys=True))
    print('PASS exact type polynomial, strict witness, raw BFS, sampling and 8 negative controls')


if __name__ == '__main__':
    main()
