"""Independent small exact replay; imports no family constructor or checker."""
import json
from fractions import Fraction as F
from pathlib import Path

base = Path(__file__).resolve().parents[1]
suite = json.loads((base / 'examples/reflexive-cost-families.json').read_text(encoding='utf-8'))
records = []
enumerated = 0
for case in suite['cases']:
    n, m = case['sizes']
    grid = [(p, j) for p in range(n) for j in range(m)]
    E = {tuple(e) for e in case['E']}
    relF = {tuple(e) for e in case['F']}
    def table(name):
        return {(p,j): F(case[name][p][j]) for p,j in grid}
    h, z = table('h'), table('z')
    if case['family'] == 'proportional':
        x = table('w')
        k = F(case['kappa'])
        y = {t:k*x[t] for t in grid}
    else:
        a, b = F(case['a']), F(case['b'])
        x = {(p,j): a if p == j else b for p,j in grid}
        y = {(p,j): b if p == j else a for p,j in grid}
    conflicts = [(r,c) for r in grid for c in grid
                 if (r[0],c[0]) in E and (c[1],r[1]) in relF]
    if any(x[r]*y[c] > h[r[0],c[1]]*z[c[0],r[1]] for r,c in conflicts):
        raise ValueError('local failure: '+case['name'])
    vertices = [('R',t) for t in grid] + [('C',t) for t in grid]
    edges = [(('R',r),('C',c)) for r,c in conflicts]
    edges += [(('R',r),('ZR',t)) for r in grid for t in grid
              if r[1] == t[1] and (r[0],t[0]) in E]
    edges += [(('ZL',t),('C',c)) for t in grid for c in grid
              if t[0] == c[0] and (c[1],t[1]) in relF]
    costs = {('R',t):x[t] for t in grid} | {('C',t):y[t] for t in grid}
    costs |= {(s,t):z[t] for s in ('ZL','ZR') for t in grid}
    H, Z = sum(h.values(),F(0)), sum(z.values(),F(0))
    candidates = []
    for removed in ({('R',t) for t in grid}, {('C',t) for t in grid}, set(vertices)):
        kept_r = [t for t in grid if ('R',t) not in removed]
        kept_c = [t for t in grid if ('C',t) not in removed]
        U = [t for t in grid
             if not any(r[1] == t[1] and (r[0],t[0]) in E for r in kept_r)
             and not any(c[0] == t[0] and (c[1],t[1]) in relF for c in kept_c)]
        D = sum((costs[v] for v in removed),F(0))
        cover = set(removed)
        for t in grid:
            if any(r[1] == t[1] and (r[0],t[0]) in E for r in kept_r):
                cover.add(('ZR',t))
            if any(c[0] == t[0] and (c[1],t[1]) in relF for c in kept_c):
                cover.add(('ZL',t))
        if any(u not in cover and v not in cover for u,v in edges):
            raise ValueError('invalid complete cover')
        cost = sum((costs[v] for v in cover),F(0))
        candidates.append((D-sum((z[t] for t in U),F(0)),cost,D,U))
    if case['family'] == 'exchange':
        chosen = candidates[2]
    else:
        chosen = candidates[0] if sum(x.values(),F(0)) <= H else (
            candidates[1] if sum(y.values(),F(0)) <= H else candidates[2])
    if chosen[0] > H or chosen[1] > H+Z:
        raise ValueError('theorem bound failed')
    optimum = None
    if len(vertices) <= 8:
        for mask in range(1 << len(vertices)):
            enumerated += 1
            removed = {v for j,v in enumerate(vertices) if (mask >> j) & 1}
            if any(('R',r) not in removed and ('C',c) not in removed for r,c in conflicts):
                continue
            kept_r = [t for t in grid if ('R',t) not in removed]
            kept_c = [t for t in grid if ('C',t) not in removed]
            U = [t for t in grid
                 if not any(r[1] == t[1] and (r[0],t[0]) in E for r in kept_r)
                 and not any(c[0] == t[0] and (c[1],t[1]) in relF for c in kept_c)]
            adjusted = sum((costs[v] for v in removed),F(0))-sum((z[t] for t in U),F(0))
            optimum = adjusted if optimum is None else min(optimum,adjusted)
        if optimum is None or optimum > H:
            raise ValueError('independent optimum violates bound')
        if case.get('sharp') and optimum != H:
            raise ValueError('independent sharp pruning failure')
    if case.get('sharp'):
        packing = [(('R',t),('ZR',t),x[t]) for t in grid]
        packing += [(('ZL',t),('C',t),y[t]) for t in grid]
        loads = dict.fromkeys(costs,F(0))
        for u,v,c in packing:
            if (u,v) not in edges:
                raise ValueError('packing nonedge')
            loads[u] += c
            loads[v] += c
        if any(loads[v] > costs[v] for v in costs):
            raise ValueError('packing overload')
        if sum((c for _,_,c in packing),F(0)) != chosen[1] or chosen[1] != H+Z:
            raise ValueError('sharp packing identity failed')
    if case.get('sqrt_lower'):
        a,b = F(case['a']),F(case['b'])
        v = ([a*a,a*a+b*b-a*b,a*b,b*b] if b >= a
             else [b*b,a*b,b*b+a*a-a*b,a*a])
        ell = [F(t) for row in case['sqrt_lower'] for t in row]
        if any(t*t > w for t,w in zip(ell,v)) or 2*sum(ell,F(0)) < 4*(a+b):
            raise ValueError('all-angle certificate failed')
    records.append({'name':case['name'],'chosen_cover_cost':str(chosen[1]),
                    'minimum_augmented_cover':str(optimum+Z) if optimum is not None else None})
print(json.dumps({'status':'PASS','fixtures':len(records),'subsets_inspected':enumerated,
                  'independent_public_imports':0,'records':records},sort_keys=True))
