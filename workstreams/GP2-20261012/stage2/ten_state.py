#!/usr/bin/env python3
"""All strict codes embed in the ten-profile target, including adjacency."""
from __future__ import annotations
from itertools import product
import model

P = tuple((a,b) for a in range(1,5) for b in range(a+1,6))
Q = tuple((a,b) for a in range(1,4) for b in range(a+1,5))
R = tuple((a,b) for a in range(1,3) for b in range(a+1,4))
PAIR_FROM_LEVEL = ((2,4),(1,4),(1,3))


def five_profile(x: int, y: int, tau: int):
    if tau == 1 and x < 2:
        return (3-x,5)
    if tau == 0 and y > 0:
        return (1,5-y)
    return (2,4)


def domain(q,qq):
    return tuple(p for p in P if qq[0]<=p[0]<=q[0]+1 and qq[1]<=p[1]<=q[1]+1)


def pair_domain(r,rr):
    return tuple(q for q in Q if rr[0]<=q[0]<=r[0]+1 and rr[1]<=q[1]<=r[1]+1)


def active(q,qq):
    D=domain(q,qq)
    if not D:
        raise ValueError('Empty ten-profile domain')
    out=set()
    if q[1] == 4:out.add((q[0]+1,5))
    if qq[0] == 1:out.add((1,qq[1]))
    if q[1] == 4 and qq[0] == 1:out.add((1,5))
    if not out:out.add(min(D))
    if not out<=set(D):raise AssertionError('Active profile outside domain')
    return tuple(sorted(out))


def validate(n,eta,kappa,gamma):
    if set(eta)!=set(range(n)) or any(r not in R for r in eta.values()):
        raise ValueError('Invalid ten-model letter assignment')
    if set(kappa)!=set(product(range(n),repeat=2)) or set(gamma)!=set(product(range(n),repeat=3)):
        raise ValueError('Incomplete ten-model domains')
    if any(kappa[a,b] not in pair_domain(eta[a],eta[b]) for a,b in product(range(n),repeat=2)):
        raise ValueError('Invalid ten-model ordered pair')
    if any(gamma[a,b,c] not in domain(kappa[a,b],kappa[b,c]) for a,b,c in product(range(n),repeat=3)):
        raise ValueError('Invalid ten-model triple')


def from_code(n,code):
    C=model.validate_code(n,code)
    canonical=model.profile_from_code(n,C)  # rejects non-strict inputs
    independent=all(u[1:]!=v[:3] for u in C for v in C)
    if independent:
        levels=[0]*(n*n)
        for _ in range(2):
            old=levels[:]
            for a,b,c,d in C:levels[c*n+d]=max(levels[c*n+d],old[a*n+b]+1)
        prefixes={w[:3] for w in C}
        gamma={(a,b,c):five_profile(levels[a*n+b],levels[b*n+c],int((a,b,c) in prefixes))
               for a,b,c in product(range(n),repeat=3)}
        eta={a:(1,3) for a in range(n)}
        kappa={(a,b):PAIR_FROM_LEVEL[levels[a*n+b]] for a,b in product(range(n),repeat=2)}
    else:
        gamma=canonical
        if any(p not in P for p in gamma.values()):
            raise AssertionError('An adjacent pair failed to force F_5=2')
        kappa={(b,c):(min(3,min(gamma[a,b,c][0] for a in range(n))),
                       min(4,min(gamma[a,b,c][1] for a in range(n))))
               for b,c in product(range(n),repeat=2)}
        eta={b:(min(2,min(kappa[a,b][0] for a in range(n))),
                min(3,min(kappa[a,b][1] for a in range(n)))) for b in range(n)}
    validate(n,eta,kappa,gamma)
    if not C<=model.marked_code(n,gamma):raise AssertionError('Ten-model code containment')
    return independent,eta,kappa,gamma


def reduce_active(n,eta,kappa,gamma):
    validate(n,eta,kappa,gamma)
    result={s:next(q for q in active(kappa[s[:2]],kappa[s[1:]])
                   if all((not model.marked(p,t) or model.marked(q,t)) and
                          (not model.marked(t,p) or model.marked(t,q)) for t in P))
            for s,p in gamma.items()}
    validate(n,eta,kappa,result)
    return result
