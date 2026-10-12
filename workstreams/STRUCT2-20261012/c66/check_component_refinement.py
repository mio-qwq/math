#!/usr/bin/env python3
"""Exact finite checks for the sparse constraint-component refinement.

The universal inequality is proved in COMPONENT_REFINEMENT.md.  This program
checks its transcription on full and selected constraint systems for every
nonidentity permutation pair at n=4,5 and three exact rational probabilities.
It is a regression certificate, not an extrapolation to arbitrary n.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from itertools import permutations
import hashlib
import json
from pathlib import Path
import platform
import time

from check_quantitative import DSU, constraint_components, probability


def selected_components(alpha, beta):
    n = len(alpha)
    a = sum(alpha[i] != i for i in range(n))
    b = sum(beta[i] != i for i in range(n))
    if b > a:
        alpha, beta, a = beta, alpha, b
    moved = [i for i in range(n) if alpha[i] != i]
    order = moved + [i for i in range(n) if alpha[i] == i]
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    index = {edge: i for i, edge in enumerate(edges)}
    ground = len(edges)

    def variable(i, j):
        return ground if i == j else index[min(i, j), max(i, j)]

    selected = []
    dsu = DSU(ground + 1)
    for position, u in enumerate(order):
        if alpha[u] == u:
            continue
        for v in order[position + 1:]:
            source, target = variable(u, v), variable(alpha[u], beta[v])
            if source != target:
                selected.append((source, target))
                dsu.union(source, target)
    assert len({source for source, _ in selected}) == len(selected)
    assert 2 * len(selected) >= a * (2 * n - a - 3)

    involved = {v for edge in selected for v in edge if v != ground}
    sizes = Counter(dsu.find(v) for v in involved)
    grounded = sizes.pop(dsu.find(ground), 0)
    ordinary = tuple(sorted(k for k in sizes.values() if k >= 2))
    assert sum(ordinary) + grounded == len(involved)
    return ordinary, grounded


def refined_parameters(components):
    sizes, grounded = components
    sizes = tuple(k for k in sizes if k >= 2)
    constrained_variables = grounded + sum(sizes)
    excess = grounded + sum(k - 2 for k in sizes)
    return constrained_variables, excess


def exact_refined_check(components, p):
    q = p * p + (1 - p) ** 2
    z = min(p * p, (1 - p) ** 2) / q
    variables, excess = refined_parameters(components)
    # This is the square of P <= q^(variables/2)*(1-z)^(excess/2),
    # so every quantity remains an exact Fraction even for odd exponents.
    return probability(components, p) ** 2 <= q ** variables * (1 - z) ** excess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    probabilities = (Fraction(1, 10), Fraction(1, 2), Fraction(9, 10))
    checks = 0
    maxima = {}
    for n in (4, 5):
        ps = list(permutations(range(n)))
        max_selected_excess = 0
        max_full_excess = 0
        for alpha in ps:
            for beta in ps:
                if all(alpha[i] == i and beta[i] == i for i in range(n)):
                    continue
                selected = selected_components(alpha, beta)
                full = constraint_components(alpha, beta)
                max_selected_excess = max(max_selected_excess,
                                          refined_parameters(selected)[1])
                max_full_excess = max(max_full_excess,
                                      refined_parameters(full)[1])
                for p in probabilities:
                    assert exact_refined_check(selected, p)
                    assert exact_refined_check(full, p)
                    checks += 2
        maxima[str(n)] = {'selected_excess': max_selected_excess,
                          'full_excess': max_full_excess}

    # A two-variable ungrounded component attains the old q bound exactly at
    # p=1/2.  Falsely charging one unit of excess therefore fails.
    p = Fraction(1, 2)
    pair_component = ((2,), 0)
    q = p * p + (1 - p) ** 2
    assert probability(pair_component, p) ** 2 == q ** 2
    assert not probability(pair_component, p) ** 2 <= q ** 2 * Fraction(1, 2)

    report = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'seconds': round(time.perf_counter() - start, 6),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dependency_sha256': hashlib.sha256(
            (Path(__file__).parent / 'check_quantitative.py').read_bytes()).hexdigest(),
        'orders': [4, 5],
        'probabilities': ['1/10', '1/2', '9/10'],
        'exact_checks': checks,
        'maxima_observed': maxima,
        'damage_controls_detected': 1,
        'success': True,
        'scope': ('Exact finite transcription checks for the component refinement; '
                  'the all-n inequality is written, and the K=4 structural excess '
                  'bound remains open.')
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS:', checks, 'exact refined bounds; 1 damage control;',
          report['seconds'], 'seconds')


if __name__ == '__main__':
    main()
