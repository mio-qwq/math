#!/usr/bin/env python3
"""New exact-window regression; finite checks do not certify the limit.

Dependencies: Python 3 and mpmath==1.3.0. This reuses the full-component
traversal without repeating the old graph/automorphism enumerations.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from itertools import permutations
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import platform
import random
import time

import mpmath as mp

from check_critical_structure import labelled_components, cycle_lengths
from check_quantitative import probability


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def statistics(alpha, beta):
    n = len(alpha)
    fixed = [i for i in range(n) if alpha[i] == beta[i] == i]
    shared = [(i, j) for i in range(n) for j in range(i + 1, n)
              if alpha[i] == beta[i] == j and alpha[j] == beta[j] == i]
    predicted = {(i, j) for i in fixed for j in fixed if i < j} | set(shared)
    free, grounded = labelled_components(alpha, beta)
    actual = {c[0] for c in free if len(c) == 1}
    assert actual == predicted
    f, u, m = len(fixed), len(shared), n - len(fixed)
    assert len(actual) == comb(f, 2) + u
    assert 2 * u <= m
    constrained = comb(n, 2) - len(actual)
    assert 2 * constrained >= m * (2 * n - m - 2)
    short = {i for i, k in enumerate(cycle_lengths(alpha)) if k <= 4}
    small_edges = {e for c in free if len(c) <= 2 for e in c}
    assert all(i in short and j in short for i, j in small_edges)
    counts = Counter(map(len, free))
    assert counts[1] <= comb(len(short), 2)
    assert 2 * counts[2] <= comb(len(short), 2)
    return (tuple(sorted(map(len, free))), len(grounded)), m, counts


def rational_checks(signature, n, m, counts):
    checks = 0
    for p in (Fraction(1, 10), Fraction(1, 2)):
        exact = probability(signature, p)
        t = p / (1 - p)
        baseline = (1 - p) ** comb(n, 2)
        product = baseline
        for k, c in counts.items():
            product *= (1 + t ** k) ** c
        assert product == exact
        q = p * p + (1 - p) ** 2
        assert exact ** 4 <= q ** (m * (2 * n - m - 2))
        checks += 2
    return checks


def literal_graph_oracle(n):
    """Independently scan original adjacency matrices only at n=3,4."""
    ps = list(permutations(range(n)))
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    M = len(edges)
    histogram = {pair: Counter() for pair in ((a, b) for a in ps for b in ps)}
    for mask in range(1 << M):
        matrix = [[0] * n for _ in range(n)]
        for bit, (i, j) in enumerate(edges):
            matrix[i][j] = matrix[j][i] = (mask >> bit) & 1
        weight = mask.bit_count()
        for (alpha, beta), hist in histogram.items():
            if all(matrix[i][j] == matrix[alpha[i]][beta[j]]
                   for i in range(n) for j in range(n)):
                hist[weight] += 1
    checks = 0
    expectations = []
    for p in (Fraction(1, 10), Fraction(1, 2)):
        expectation = Fraction(0)
        for (alpha, beta), hist in histogram.items():
            observed = sum(count * p ** k * (1-p) ** (M-k)
                           for k, count in hist.items())
            free, grounded = labelled_components(alpha, beta)
            signature = (tuple(sorted(map(len, free))), len(grounded))
            assert observed == probability(signature, p)
            expectation += observed
            checks += 1
        expectations.append({'n': n, 'p': str(p), 'expectation': str(expectation)})
        for R in range(n):
            pp = mp.mpf(p.numerator) / p.denominator
            t, q = pp / (1-pp), pp**2+(1-pp)**2
            r = (R + 4) // 4
            eps = (mp.mpf(25)/12)**r / factorial(r)
            eta = t*comb(R,2) + t*t*comb(R,2)/2 + M*t**3/3
            xi = t*(comb(R,2)+mp.mpf(n)/2) + M*t*t/2 + M*t**3/3
            B = factorial(n)**2*(1-pp)**M
            rem = sum(comb(n,m)*factorial(m)**2*q**(mp.mpf(m*(2*n-m-2))/4)
                      for m in range(2,n-R))
            value = mp.mpf(expectation.numerator)/expectation.denominator
            assert 1+B-(1-pp)**M <= value + mp.mpf('1e-70')
            assert value <= 1+B*(mp.exp(eta)+eps*mp.exp(xi))+rem
            checks += 1
    return checks, expectations


def short_cycle_moments():
    checks = 0
    H = Fraction(25,12)
    for n in range(1,9):
        hist = Counter()
        for a in permutations(range(n)):
            lengths = cycle_lengths(a)
            Z = sum(lengths.count(j)//j for j in range(1,5))
            short = sum(k <= 4 for k in lengths)
            hist[Z, short] += 1
        for r in range(1,n+1):
            lhs = Fraction(sum(count*comb(Z,r) for (Z,_), count in hist.items()),factorial(n))
            exact = Fraction(0)
            for d1 in range(r+1):
                for d2 in range(r-d1+1):
                    for d3 in range(r-d1-d2+1):
                        d4 = r-d1-d2-d3
                        if d1+2*d2+3*d3+4*d4 <= n:
                            exact += Fraction(1, factorial(d1)*2**d2*factorial(d2)
                                              *3**d3*factorial(d3)*4**d4*factorial(d4))
            assert lhs == exact <= H**r/factorial(r)
            checks += 1
        for R in range(n+1):
            r = (R+4)//4
            tail = Fraction(sum(count for (_,s),count in hist.items() if s>R),factorial(n))
            assert tail <= H**r/factorial(r)
            checks += 1
    return checks


def asymptotic_transcription():
    results = []
    for exponent in (6,9,12,18):
        n = mp.mpf(10)**exponent
        L, M = mp.log(n), n*(n-1)/2
        center = -mp.expm1(-2*mp.loggamma(n+1)/M)
        expansion = (4*L-4)/n+(-8*L**2+22*L+2*mp.log(2*mp.pi)-12)/n**2
        error = (center-expansion)*n**3/L**3
        assert abs(error) < 100
        for x in (-2,0,2):
            p = center+2*x/n**2
            logB = 2*mp.loggamma(n+1)+M*mp.log1p(-p)
            assert abs(logB+x) < 100*L/n
            results.append({'n': str(int(n)), 'x': x,
                            'log_B_plus_x': mp.nstr(logB+x,24),
                            'center_scaled_error': mp.nstr(error,24)})
        for h in (21,22,23):
            s = mp.mpf(3)
            p = (4*L-4-8*L**2/n+(h*L+s)/n)/n
            logB = 2*mp.loggamma(n+1)+M*mp.log1p(-p)
            predicted = (11-mp.mpf(h)/2)*L+mp.log(2*mp.pi)-6-s/2
            assert abs(logB-predicted) < 100*L**3/n
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    mp.mp.dps = 90
    pairs = rational = support_counts = 0
    orders = []
    for n in range(2,6):
        ps = list(permutations(range(n)))
        unions = Counter()
        for alpha in ps:
            for beta in ps:
                signature, m, counts = statistics(alpha,beta)
                unions[m] += 1
                if n <= 4:
                    rational += rational_checks(signature,n,m,counts)
                pairs += 1
        for m in range(n+1):
            assert unions[m] <= comb(n,m)*factorial(m)**2
            support_counts += 1
        assert unions[0] == 1 and unions[1] == 0
        orders.append({'n':n, 'mode':'all pairs; new structural lemmas', 'pairs':len(ps)**2})
    rng = random.Random(2026101302)
    for n in (6,8,12,24,48):
        samples = []
        identity = tuple(range(n))
        for m in (2,3,n//2,n):
            alpha = list(identity)
            beta = list(identity)
            alpha[:m] = alpha[1:m]+alpha[:1]
            beta[:m] = reversed(beta[:m])
            samples.extend([(tuple(alpha),tuple(beta)),(tuple(alpha),tuple(alpha)),
                            (identity,tuple(alpha))])
        for _ in range(64):
            alpha, beta = list(identity),list(identity)
            rng.shuffle(alpha)
            rng.shuffle(beta)
            samples.append((tuple(alpha),tuple(beta)))
        for alpha,beta in samples:
            signature,m,counts = statistics(alpha,beta)
            rational += rational_checks(signature,n,m,counts)
            pairs += 1
        orders.append({'n':n, 'mode':'structured and seeded pairs', 'pairs':len(samples)})
    # Damage controls for two tempting but false singleton classifications.
    a = (1,0,2)
    signature,_,counts = statistics(a,a)
    assert counts[1] == 1 != comb(1,2)  # shared transposition cannot be omitted
    _,_,counts2 = statistics(a,(0,1,2))
    assert counts2[1] == 0              # an alpha 2-cycle alone is insufficient
    oracle_checks = 0
    expectations = []
    for n in (3,4):
        number,values = literal_graph_oracle(n)
        oracle_checks += number
        expectations.extend(values)
    report = {
        'utc':datetime.now(timezone.utc).isoformat(), 'python':platform.python_version(),
        'mpmath':mp.__version__, 'success':True,
        'pairs':pairs,'orders':orders,'rational_probability_assertions':rational,
        'union_support_count_assertions':support_counts,
        'short_cycle_assertions':short_cycle_moments(),
        'literal_oracle_and_finite_bound_assertions':oracle_checks,
        'literal_expectations':expectations,'damage_controls':2,
        'high_precision_center_checks':asymptotic_transcription(),
        'source_sha256':digest(__file__),
        'dependencies_sha256':{f:digest(Path(__file__).with_name(f)) for f in
                              ('check_critical_structure.py','check_quantitative.py')},
        'proof_sha256':digest(Path(__file__).with_name('EXACT_WINDOW.md')),
        'scope':'Finite original-definition regression and coefficient checks; not an all-n proof or independent acceptance.',
        'seconds':round(time.perf_counter()-started,6)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS:',pairs,'pairs;',rational,'rational assertions;',oracle_checks,
          'literal-oracle/bound assertions;',report['seconds'],'seconds')


if __name__ == '__main__':
    main()
