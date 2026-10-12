#!/usr/bin/env python3
"""Exact finite primitives for the GP2 stage-two structural results.

Standard library only. These algorithms do not prove the optimum over all
alphabets; the accompanying mathematical statements specify that boundary.
"""
from __future__ import annotations
from collections import defaultdict, deque
from fractions import Fraction
from itertools import product
from math import prod
from typing import Iterable

Word = tuple[int, ...]
Profile = tuple[int, int]
P: tuple[Profile, ...] = tuple((a,b) for a in range(1,5) for b in range(a+1,7))
Q: tuple[Profile, ...] = tuple((a,b) for a in range(1,4) for b in range(a+1,6))
R: tuple[Profile, ...] = tuple((a,b) for a in range(1,3) for b in range(a+1,5))
GAPS = tuple((a,b) for a in range(1,4) for b in range(1,5-a))


def allowed(p: Profile, q: Profile) -> bool:
    a,b = p; c,d = q
    return c <= a+1 and (b >= 5 or d <= b+1)


def marked(p: Profile, q: Profile) -> bool:
    a,b = p; c,d = q
    return allowed(p,q) and c == 1 and b >= 5 and d <= a+1


def threshold_arc(p: Profile, q: Profile) -> bool:
    return q[0] <= p[0]+1 and q[1] <= p[1]+1


def profile_domain(q: Profile, qq: Profile) -> tuple[Profile, ...]:
    return tuple(p for p in P if p[0] <= q[0]+1 and p[1] <= q[1]+1
                 and p[0] >= qq[0] and p[1] >= qq[1])


def pair_domain(r: Profile, rr: Profile) -> tuple[Profile, ...]:
    return tuple(q for q in Q if q[0] <= r[0]+1 and q[1] <= r[1]+1
                 and q[0] >= rr[0] and q[1] >= rr[1])


def active_domain(q: Profile, qq: Profile) -> tuple[Profile, ...]:
    dom = profile_domain(q,qq)
    if not dom:
        raise ValueError('Empty profile domain')
    a,b = q; c,d = qq
    out: set[Profile] = set()
    if b >= 4:
        out.add((a+1,b+1))               # source extreme
    if c == 1 and d <= 4:
        out.add((1,d))                   # terminal extreme
    if c == 1 and b >= 4:
        out.add((1,5))                   # the two-sided bridge
    if not out:
        out.add(min(dom))               # all profiles are unmarked/inert
    if not out <= set(dom):
        raise AssertionError('Active-domain formula left its original domain')
    return tuple(sorted(out))


def dominates(q: Profile, p: Profile) -> bool:
    """All marked arcs into/out of p remain after replacing p by q."""
    return all((not marked(p,t) or marked(q,t)) and
               (not marked(t,p) or marked(t,q)) for t in P)


def validate_code(n: int, code: Iterable[Word]) -> set[Word]:
    if type(n) is not int or n < 1:
        raise ValueError('The alphabet size must be a positive integer')
    C = set(tuple(w) for w in code)
    if any(len(w) != 4 or any(type(a) is not int or not 0 <= a < n for a in w) for w in C):
        raise ValueError('A word is outside the specified four-letter alphabet')
    return C


def profile_from_code(n: int, code: Iterable[Word]) -> dict[Word,Profile]:
    C = validate_code(n,code)
    triples = tuple(product(range(n),repeat=3))
    if not C:
        return {s:(4,6) for s in triples}
    F = {s:[0] for s in triples}
    for t in range(1,6):
        for s in triples:
            F[s].append(max(F[(a,)+s[:2]][t-1]+int((a,)+s in C) for a in range(n)))
    if any(F[s][5] > 2 for s in triples):
        raise ValueError('Input is not a strict five-window code')
    return {s:(next(t for t in range(1,5) if F[s][t] >= 1),
               next((t for t in range(2,6) if F[s][t] >= 2),6)) for s in triples}


def canonical_hierarchy(n: int, gamma: dict[Word,Profile]):
    if set(gamma) != set(product(range(n),repeat=3)) or any(p not in P for p in gamma.values()):
        raise ValueError('Wrong profile domain or missing triple')
    if any(not allowed(gamma[w[:3]],gamma[w[1:]]) for w in product(range(n),repeat=4)):
        raise ValueError('Profile assignment is not admissible')
    kappa = {(b,c):(min(3,min(gamma[a,b,c][0] for a in range(n))),
                         min(5,min(gamma[a,b,c][1] for a in range(n))))
             for b,c in product(range(n),repeat=2)}
    eta = {b:(min(2,min(kappa[a,b][0] for a in range(n))),
              min(4,min(kappa[a,b][1] for a in range(n)))) for b in range(n)}
    validate_hierarchy(n,eta,kappa,gamma)
    return eta,kappa


def validate_hierarchy(n: int, eta, kappa, gamma) -> None:
    if set(eta) != set(range(n)) or any(p not in R for p in eta.values()):
        raise ValueError('Invalid letter types')
    if set(kappa) != set(product(range(n),repeat=2)):
        raise ValueError('Missing ordered pair')
    if set(gamma) != set(product(range(n),repeat=3)):
        raise ValueError('Missing triple')
    for a,b in product(range(n),repeat=2):
        if kappa[a,b] not in pair_domain(eta[a],eta[b]):
            raise ValueError('Invalid pair type')
    for a,b,c in product(range(n),repeat=3):
        if gamma[a,b,c] not in profile_domain(kappa[a,b],kappa[b,c]):
            raise ValueError('Invalid triple profile')


def reduce_active(n: int, eta, kappa, gamma):
    validate_hierarchy(n,eta,kappa,gamma)
    result = {}
    for s,p in gamma.items():
        options = active_domain(kappa[s[:2]],kappa[s[1:]])
        result[s] = next(q for q in options if dominates(q,p))
    validate_hierarchy(n,eta,kappa,result)
    return result


def marked_code(n: int, gamma):
    return {w for w in product(range(n),repeat=4) if marked(gamma[w[:3]],gamma[w[1:]])}


def rotations(w: Word) -> tuple[Word, ...]:
    return tuple(sorted({w[i:]+w[:i] for i in range(4)}))


def validate_levels(n, levels, weights=None):
    if type(n) is not int or n < 1 or len(levels) != n*n:
        raise ValueError('Invalid alphabet/level-array binding')
    if any(type(x) is not int or not 0 <= x <= 2 for x in levels):
        raise ValueError('Levels must be integers 0,1,2')
    if weights is not None:
        if len(weights) != n or any(type(x) is not int or x < 0 for x in weights) or sum(weights) <= 0:
            raise ValueError('Weights must be nonnegative integers of positive total')


def candidate_orbits(n: int, levels: list[int]):
    validate_levels(n,levels)
    reps = sorted({min(rotations(w)) for w in product(range(n),repeat=4)})
    out = []
    for r in reps:
        candidates = tuple(w for w in rotations(r) if levels[n*w[0]+w[1]] < levels[n*w[2]+w[3]])
        if candidates:
            if len(candidates) > 2 or len(rotations(r)) != 4:
                raise AssertionError('Rotation candidate count failed')
            out.append(candidates)
    return out


def rotation_moments(n: int, levels: list[int], weights: list[int]):
    validate_levels(n,levels,weights)
    W = sum(weights)
    orbits = candidate_orbits(n,levels)
    forced = tuple(o[0] for o in orbits if len(o) == 1)
    T = Fraction(sum(prod(weights[x] for x in o[0]) for o in orbits),W**4)
    E = 1-4*T
    ins = {h:defaultdict(int) for h in range(1,4)}
    outs = {h:defaultdict(int) for h in range(1,4)}
    for u in forced:
        for h in range(1,4):
            ins[h][u[h:]] += prod(weights[x] for x in u[:h])
            outs[h][u[:4-h]] += prod(weights[x] for x in u[4-h:])
    moments = {}
    for a,b in GAPS:
        num = sum(prod(weights[x] for x in v)*ins[a][v[:4-a]]*outs[b][v[b:]] for v in forced)
        moments[a,b] = Fraction(num,W**(4+a+b))
    return E,T,moments,forced


def solve_completion(n: int, levels: list[int]):
    """Exact independent-subclass rotation saturation via 2-SAT.

    Literal 2*v+i denotes selecting candidate i in viable rotation orbit v.
    A singleton has candidate 0 only; literal 2*v+1 is its negation.
    UNSAT returns checkable implication paths, not a solver status alone.
    """
    orbits = candidate_orbits(n,levels)
    selected = {w:2*v+i for v,o in enumerate(orbits) for i,w in enumerate(o)}
    N = 2*len(orbits); g = [[] for _ in range(N)]; gr = [[] for _ in range(N)]; reason = {}
    def add(a,b,r):
        g[a].append(b); gr[b].append(a); reason[a,b] = r
    for v,o in enumerate(orbits):
        if len(o) == 1:
            add(2*v+1,2*v,{'unit':list(o[0])})
    prefixes = defaultdict(list)
    for w,l in selected.items():
        prefixes[w[:3]].append((w,l))
    conflicts = 0
    for w,l in selected.items():
        for u,k in prefixes[w[1:]]:
            why = {'conflict':[list(w),list(u)]}
            add(l,k^1,why); add(k,l^1,why); conflicts += 1
    seen = set(); order = []
    for v in range(N):
        if v in seen:
            continue
        stack = [(v,0)]; seen.add(v)
        while stack:
            a,j = stack[-1]
            if j == len(g[a]):
                stack.pop(); order.append(a); continue
            b = g[a][j]; stack[-1] = (a,j+1)
            if b not in seen:
                seen.add(b); stack.append((b,0))
    comp = [-1]*N; cc = 0
    for v in reversed(order):
        if comp[v] >= 0:
            continue
        comp[v] = cc; todo = [v]
        while todo:
            a = todo.pop()
            for b in gr[a]:
                if comp[b] < 0:
                    comp[b] = cc; todo.append(b)
        cc += 1
    out = {'n':n,'orbits':len(orbits),'singletons':sum(len(o)==1 for o in orbits),'conflicts':conflicts}
    bad = next((v for v in range(len(orbits)) if comp[2*v] == comp[2*v+1]),None)
    if bad is None:
        code = [orbits[v][int(comp[2*v+1] > comp[2*v])] for v in range(len(orbits))]
        out.update(status='SAT',code=[list(w) for w in code]); return out
    def path(a,b):
        prev = {a:None}; todo = deque([a])
        while todo:
            u = todo.popleft()
            if u == b:
                break
            for v in g[u]:
                if v not in prev:
                    prev[v] = u; todo.append(v)
        ret = []; cur = b
        while cur != a:
            p = prev[cur]; ret.append({'from':p,'to':cur,'reason':reason[p,cur]}); cur = p
        return list(reversed(ret))
    out.update(status='UNSAT',variable=bad,paths=[path(2*bad,2*bad+1),path(2*bad+1,2*bad)])
    return out
