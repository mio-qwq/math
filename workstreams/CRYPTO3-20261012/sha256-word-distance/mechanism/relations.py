#!/usr/bin/env python3
"""Derive two-term equality components; never divide by a nonunit.

This is discovery data, not a solver certificate or a distance proof.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path


def equations(support):
    support = set(support)
    return [(t, [(kind, i, sign) for kind, i, sign in
             [('d', t, 1), ('g', t-2, -1), ('d', t-7, -1),
              ('f', t-15, -1), ('d', t-16, -1)] if i in support])
            for t in range(16, 64)]


def component_relations(support):
    variables = [(kind, i) for i in support for kind in 'dfg']
    parent = {v: v for v in variables}
    sign = {v: 1 for v in variables}
    half = set()

    def find(v):
        if parent[v] != v:
            root, s = find(parent[v])
            sign[v] *= s
            parent[v] = root
        return parent[v], sign[v]

    def union(a, b, s):
        ra, sa = find(a)
        rb, sb = find(b)
        if ra == rb:
            if sa != s*sb:
                half.add(ra)
            return
        was_half = ra in half or rb in half
        parent[ra] = rb
        sign[ra] = s*sb*sa
        half.discard(ra)
        half.discard(rb)
        if was_half:
            half.add(rb)

    eqs = equations(support)
    for _, terms in eqs:
        if len(terms) == 2:
            (ka, ia, ca), (kb, ib, cb) = terms
            union((ka, ia), (kb, ib), -cb*ca)
    groups = defaultdict(list)
    for v in variables:
        r, s = find(v)
        groups[r].append((v, s))
    ordered = sorted(groups, key=lambda r: min(groups[r]))
    names = {r: 'c'+str(i) for i, r in enumerate(ordered)}
    out = {'groups': {}, 'half_forced': [], 'residual': []}
    for r in ordered:
        out['groups'][names[r]] = [f'{s:+d}*{k}{i}' for (k,i),s in sorted(groups[r])]
        if r in half:
            out['half_forced'].append(names[r])
    for t, terms in eqs:
        coeff = defaultdict(int)
        for k, i, c in terms:
            r, s = find((k, i))
            coeff[names[r]] += c*s
        coeff = {k: v for k, v in sorted(coeff.items()) if v}
        if coeff:
            out['residual'].append({'t': t, 'coefficients': coeff})
    out['triples'] = {str(i): [names[find((k,i))[0]] for k in 'dfg'] for i in support}
    return out


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('supports', type=Path)
    p.add_argument('--indices', default='5,6,7,10,11,12,13')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    supports = json.loads(a.supports.read_text())['supports']
    result = {str(i): component_relations(supports[i]) for i in map(int, a.indices.split(','))}
    data = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if a.output:
        a.output.write_text(data)
    else:
        print(data, end='')
