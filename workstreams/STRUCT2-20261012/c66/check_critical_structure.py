#!/usr/bin/env python3
"""Definition-level regressions for the written critical-boundary proof.

Labelled breadth-first components use every original ordered equation. They
are compared with the preceding DSU program, but no graph/automorphism search
or prior probability-bound enumeration is repeated. Analytic limit claims
are proved in CRITICAL_BOUNDARY.md, not by these finite checks.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from itertools import permutations
from math import ceil, comb, factorial
from pathlib import Path
import hashlib
import json
import platform
import random
import time

import mpmath as mp

from check_quantitative import constraint_components, probability


def cycle_lengths(perm):
    lengths = [0] * len(perm)
    for start in range(len(perm)):
        if lengths[start]:
            continue
        cycle = [start]
        v = perm[start]
        while v != start:
            cycle.append(v)
            v = perm[v]
        for v in cycle:
            lengths[v] = len(cycle)
    return lengths


def labelled_components(alpha, beta):
    """Independent traversal rather than disjoint-set union."""
    n = len(alpha)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    index = {edge: v for v, edge in enumerate(edges)}
    ground = len(edges)
    adj = [set() for _ in range(ground + 1)]

    def variable(i, j):
        return ground if i == j else index[min(i, j), max(i, j)]

    for i in range(n):
        for j in range(n):
            u, v = variable(i, j), variable(alpha[i], beta[j])
            adj[u].add(v)
            adj[v].add(u)
    seen = set()
    free = []
    grounded = []
    for start in range(ground + 1):
        if start in seen:
            continue
        pending = [start]
        seen.add(start)
        component = []
        while pending:
            v = pending.pop()
            component.append(v)
            for w in adj[v]:
                if w not in seen:
                    seen.add(w)
                    pending.append(w)
        ordinary = [edges[v] for v in component if v != ground]
        if ground in component:
            grounded = ordinary
        else:
            free.append(ordinary)
    return free, grounded


def structural_check(alpha, beta):
    n = len(alpha)
    free, grounded = labelled_components(alpha, beta)
    signature = (tuple(sorted(len(c) for c in free)), len(grounded))
    assert signature == constraint_components(alpha, beta)
    la, lb = cycle_lengths(alpha), cycle_lengths(beta)
    endpoint_checks = 0
    for component in free:
        vertices = {v for edge in component for v in edge}
        assert {alpha[v] for v in vertices} == vertices
        assert {beta[v] for v in vertices} == vertices
        assert all(la[v] <= 2 * len(component) and lb[v] <= 2 * len(component)
                   for v in vertices)
        endpoint_checks += 1

    variables = len(grounded) + sum(len(c) for c in free if len(c) >= 2)
    excess = len(grounded) + sum(len(c) - 2 for c in free if len(c) >= 2)
    a = max(sum(alpha[i] != i for i in range(n)),
            sum(beta[i] != i for i in range(n)))
    assert 2 * variables >= a * (2 * n - a - 3)
    density_checks = 0
    for cutoff in (4, 5, 8):
        minimum_size = cutoff // 2 + 1
        theta = Fraction(minimum_size - 2, minimum_size)
        for lengths in (la, lb):
            long = sum(length > cutoff for length in lengths)
            incident = comb(n, 2) - comb(n - long, 2)
            assert excess >= theta * incident
            density_checks += 1
    return signature, variables, excess, endpoint_checks, density_checks


def structured_permutations(n):
    identity = tuple(range(n))
    rotation = tuple((i + 1) % n for i in range(n))
    reflection = tuple(n - 1 - i for i in range(n))
    matching = tuple(i ^ 1 if (i ^ 1) < n else i for i in range(n))
    four = list(range(n))
    for start in range(0, n - 3, 4):
        for j in range(4):
            four[start + j] = start + (j + 1) % 4
    return (identity, rotation, reflection, matching, tuple(four))


def cycle_vector_count_checks():
    """Exact cycle-index counts vs literal permutations, through n=7."""
    comparisons = 0
    for n in range(1, 8):
        hist = Counter()
        for perm in permutations(range(n)):
            lengths = cycle_lengths(perm)
            vector = tuple(lengths.count(j) // j for j in range(1, n + 1))
            hist[vector] += 1
        for vector, count in hist.items():
            denominator = 1
            for j, number in enumerate(vector, 1):
                denominator *= j ** number * factorial(number)
            assert count * denominator == factorial(n)
            comparisons += 1
        for cutoff in (4, 5):
            for epsilon in (Fraction(1, 2), Fraction(1, 4)):
                actual = sum(count for vector, count in hist.items()
                             if sum(j * number for j, number in enumerate(vector, 1)
                                    if j <= cutoff) >= epsilon * n)
                minimum = ceil(epsilon * n / cutoff)
                bound = Fraction((n + 1) ** cutoff * factorial(n) * cutoff ** n,
                                 factorial(minimum))
                assert actual <= bound
                comparisons += 1
    return comparisons


def empty_graph_expansion_checks():
    """High precision checks of coefficients; never a proof of the limit."""
    mp.mp.dps = 90
    results = []
    for c in (0, 7, 8, 9):
        last_error = None
        for exponent in (4, 6, 9, 12):
            n = mp.mpf(10) ** exponent
            logn = mp.log(n)
            p = (4 * logn - 4 - c * logn ** 2 / n) / n
            observed = 2 * mp.loggamma(n + 1) + n * (n - 1) / 2 * mp.log1p(-p)
            predicted = (mp.mpf(c) / 2 - 4) * logn ** 2 + 11 * logn + mp.log(2 * mp.pi) - 6
            error = observed - predicted
            assert abs(error) <= 10000 * logn ** 3 / n
            if last_error is not None:
                assert abs(error) < last_error
            last_error = abs(error)
            results.append({'c': c, 'n': str(int(n)),
                            'log_empty_contribution': mp.nstr(observed, 30),
                            'expansion_error': mp.nstr(error, 18)})
    return results


def convergence_parameter_checks():
    """Exact rational witnesses for the three support/cycle cases."""
    results = []
    for c in (Fraction(-1), Fraction(0), Fraction(4), Fraction(7),
              Fraction(79, 10), Fraction(799, 100)):
        nonnegative = max(c, Fraction(0))
        gap = 1 - nonnegative / 8
        cutoff = 2 * ceil(8 / gap)
        minimum_size = cutoff // 2 + 1
        theta = Fraction(minimum_size - 2, minimum_size)
        epsilon = gap / 2
        gamma = epsilon / cutoff
        delta = gamma / 4
        assert 0 < epsilon <= Fraction(1, 2)
        assert 0 < delta <= Fraction(1, 8)
        assert 2 * delta * delta < gamma
        assert 4 * theta * (1 - epsilon * epsilon) > nonnegative / 2
        results.append({'c': str(c), 'K': cutoff, 'epsilon': str(epsilon),
                        'delta': str(delta),
                        'log_square_margin': str(4 * theta * (1 - epsilon * epsilon)
                                                 - nonnegative / 2)})
    return results


def finer_empty_window_checks():
    results = []
    for h, s in ((21, 0), (22, 0), (22, 3), (23, 0)):
        n = mp.mpf(10) ** 12
        logn = mp.log(n)
        p = (4 * logn - 4 - 8 * logn ** 2 / n + (h * logn + s) / n) / n
        observed = 2 * mp.loggamma(n + 1) + n * (n - 1) / 2 * mp.log1p(-p)
        predicted = (11 - mp.mpf(h) / 2) * logn + mp.log(2 * mp.pi) - 6 - mp.mpf(s) / 2
        assert abs(observed - predicted) <= 10000 * logn ** 3 / n
        results.append({'h': h, 's': s, 'n': str(int(n)),
                        'log_empty_contribution': mp.nstr(observed, 30),
                        'expansion_error': mp.nstr(observed - predicted, 18)})
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    pairs = endpoint_checks = density_checks = rational_checks = 0
    orders = []
    for n in range(2, 6):
        ps = list(permutations(range(n)))
        count = 0
        for alpha in ps:
            for beta in ps:
                signature, variables, excess, endpoints, densities = structural_check(alpha, beta)
                endpoint_checks += endpoints
                density_checks += densities
                count += 1
        orders.append({'n': n, 'mode': 'all pairs; structural statements only', 'pairs': count})
        pairs += count

    rng = random.Random(20261013)
    for n in (6, 7, 8, 9, 10, 16, 32):
        structured = structured_permutations(n)
        samples = [(alpha, beta) for alpha in structured for beta in structured]
        for _ in range(128):
            alpha, beta = list(range(n)), list(range(n))
            rng.shuffle(alpha)
            rng.shuffle(beta)
            samples.append((tuple(alpha), tuple(beta)))
        for alpha, beta in samples:
            signature, variables, excess, endpoints, densities = structural_check(alpha, beta)
            endpoint_checks += endpoints
            density_checks += densities
            if n <= 10:
                a = max(sum(alpha[i] != i for i in range(n)),
                        sum(beta[i] != i for i in range(n)))
                for p in (Fraction(1, 10), Fraction(1, 2), Fraction(9, 10)):
                    q = p * p + (1 - p) ** 2
                    z = min(p * p, (1 - p) ** 2) / q
                    assert probability(signature, p) ** 4 <= (
                        q ** (a * (2 * n - a - 3)) * (1 - z) ** (2 * excess))
                    rational_checks += 1
        pairs += len(samples)
        orders.append({'n': n, 'mode': 'structured + seeded sample', 'pairs': len(samples)})

    # A four-cycle has an ungrounded two-edge component. The true 2k endpoint
    # bound passes, while replacing 2k by k must fail.
    rotation = (1, 2, 3, 0)
    free, _ = labelled_components(rotation, rotation)
    size_two = next(component for component in free if len(component) == 2)
    endpoints = {v for edge in size_two for v in edge}
    assert all(cycle_lengths(rotation)[v] <= 2 * len(size_two) for v in endpoints)
    assert any(cycle_lengths(rotation)[v] > len(size_two) for v in endpoints)

    count_comparisons = cycle_vector_count_checks()
    expansion = empty_graph_expansion_checks()
    parameters = convergence_parameter_checks()
    finer = finer_empty_window_checks()
    root = Path(__file__).resolve().parent
    report = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(), 'mpmath': mp.__version__,
        'seconds': round(time.perf_counter() - start, 6),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'proof_sha256': hashlib.sha256((root / 'CRITICAL_BOUNDARY.md').read_bytes()).hexdigest(),
        'dependency_sha256': hashlib.sha256((root / 'check_quantitative.py').read_bytes()).hexdigest(),
        'pairs_checked': pairs, 'orders': orders,
        'endpoint_component_checks': endpoint_checks,
        'cycle_density_checks': density_checks,
        'rational_probability_checks': rational_checks,
        'cycle_count_comparisons': count_comparisons,
        'empty_graph_expansion': expansion,
        'convergence_parameter_witnesses': parameters,
        'finer_empty_window': finer,
        'damage_controls_detected': 1,
        'success': True,
        'scope': ('Definition-level component/cycle/count regressions and high-precision '
                  'coefficient checks. The all-n limit is written, not inferred from '
                  'finite checks, not Lean-verified, and not independently accepted.')
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS:', pairs, 'permutation pairs;', density_checks, 'density bounds;',
          rational_checks, 'exact probabilities;', count_comparisons,
          'cycle counts; 1 damage control;', report['seconds'], 'seconds')


if __name__ == '__main__':
    main()
