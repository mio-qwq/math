#!/usr/bin/env python3
"""Definition-level certificates for full TF expectation coefficients and bounds.

The DSU enforces every ordered adjacency equation, including the diagonal.
A separate graph enumerator uses row bitmasks and no DSU. All probabilities
tested here are exact rational numbers. These finite checks do not prove the
universal asymptotic or sparse threshold theorem by extrapolation.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from itertools import permutations
import hashlib
import json
from math import comb, factorial
from pathlib import Path
import platform
import time


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        x, y = self.find(x), self.find(y)
        if x != y:
            self.parent[x] = y


def constraint_components(alpha, beta):
    n = len(alpha)
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    index = {edge: i for i, edge in enumerate(edges)}
    ground = len(edges)
    dsu = DSU(ground + 1)

    def variable(i, j):
        return ground if i == j else index[min(i, j), max(i, j)]

    for i in range(n):
        for j in range(n):
            dsu.union(variable(i, j), variable(alpha[i], beta[j]))
    sizes = Counter(dsu.find(i) for i in range(ground))
    grounded = sizes.pop(dsu.find(ground), 0)
    return tuple(sorted(sizes.values())), grounded


def probability(components, p):
    sizes, grounded = components
    result = (1 - p) ** grounded
    for size in sizes:
        result *= p ** size + (1 - p) ** size
    return result


def support_signature(alpha, beta):
    s = len(alpha)
    dsu = DSU(s)
    for i in range(s):
        dsu.union(i, alpha[i])
        dsu.union(i, beta[i])
    d = s - len({dsu.find(i) for i in range(s)})
    components, _ = constraint_components(alpha, beta)
    rank = comb(s, 2) - len(components)
    return d, rank


def support_histogram(s):
    ps = list(permutations(range(s)))
    histogram = Counter()
    for alpha in ps:
        for beta in ps:
            if all(alpha[i] != i or beta[i] != i for i in range(s)):
                histogram[support_signature(alpha, beta)] += 1
    return histogram


def expectation_from_support(n, histograms):
    result = Fraction(1)
    for s in range(2, n + 1):
        for (d, rank), count in histograms[s].items():
            result += Fraction(comb(n, s) * count, 2 ** (d * (n - s) + rank))
    return result


def direct_graph_enumerator(n):
    """Read adjacency rows directly; independently count all alpha/beta pairs."""
    ps = list(permutations(range(n)))
    edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    total = 0
    projected = 0
    for mask in range(1 << len(edges)):
        rows = [0] * n
        for bit, (i, j) in enumerate(edges):
            if mask >> bit & 1:
                rows[i] |= 1 << j
                rows[j] |= 1 << i
        # For each beta, build the transformed adjacency rows. The TF equation
        # asks for the transformed row at alpha(i) to equal the original row i.
        beta_rows = [tuple(sum(((row >> beta[j]) & 1) << j for j in range(n))
                           for row in rows) for beta in ps]
        present = set()
        for alpha in ps:
            for transformed in beta_rows:
                if all(rows[i] == transformed[alpha[i]] for i in range(n)):
                    total += 1
                    present.add(alpha)
        projected += len(present)
    denominator = 1 << len(edges)
    return Fraction(total, denominator), Fraction(projected, denominator)


def selected_constraint_check(alpha, beta):
    """Check the sparse-proof selection and each component's edge/vertex bound."""
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
    assert len({x for x, _ in selected}) == len(selected)
    assert 2 * len(selected) >= a * (2 * n - a - 3)
    vertices = Counter(dsu.find(i) for i in range(ground))
    arcs = Counter(dsu.find(x) for x, _ in selected)
    for component, count in arcs.items():
        assert count <= vertices[component]
        if component != dsu.find(ground):
            assert vertices[component] >= 2


def effective_remainder_checks():
    n0 = 1024
    # These endpoint inequalities, paired with the stated monotone ratios in
    # SECOND_ORDER.md, prove the four whole half-lines; no numerical fit.
    checks = {}
    for s in range(7, 11):
        d = (s + 1) // 2
        numerator = factorial(s) * 2 ** (d * s) * n0 ** (s - 6)
        denominator = 2 ** ((d - 3) * n0)
        assert numerator <= denominator
        # Ratio of n^j*2^(-k*n) is <=1 for every n>=n0 because
        # (1+1/n)^j <= (1+1/n0)^j < 2^k.
        j, k = s - 6, d - 3
        assert Fraction(n0 + 1, n0) ** j <= 2 ** k
        checks[str(s)] = True
    assert 2 * n0.bit_length() <= Fraction(n0 - 3, 32) - 4
    assert 2 * n0.bit_length() <= Fraction(n0, 16)
    assert 1376 + 3932160 + 188743680 + 7 < 200000000
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    histograms = {s: support_histogram(s) for s in range(2, 6)}
    expected = {
        2: {(1, 0): 1, (1, 1): 2},
        3: {(2, 2): 2, (2, 3): 24},
        4: {(2, 2): 3, (2, 4): 18, (2, 5): 6,
            (3, 4): 12, (3, 5): 54, (3, 6): 360},
    }
    assert all(dict(histograms[s]) == expected[s] for s in expected)
    coefficients = {}
    for s, histogram in histograms.items():
        coefficients[s] = {d: str(sum(Fraction(count) * Fraction(2) ** (d * s - r)
                                    for (dd, r), count in histogram.items() if dd == d))
                           for d in sorted({d for d, _ in histogram})}
    assert coefficients[2][1] == '8'
    assert coefficients[3][2] == '224'
    assert coefficients[4][2] == '528'
    assert coefficients[4][3] == '33024'
    direct = {}
    for n in range(2, 6):
        full, projection = direct_graph_enumerator(n)
        assert full == expectation_from_support(n, histograms)
        direct[n] = {'full': str(full), 'projection': str(projection)}
        print('direct', n, direct[n], flush=True)
    sparse_count = 0
    for n in (4, 5):
        ps = list(permutations(range(n)))
        for alpha in ps:
            for beta in ps:
                a = max(sum(alpha[i] != i for i in range(n)),
                        sum(beta[i] != i for i in range(n)))
                if a == 0:
                    continue
                selected_constraint_check(alpha, beta)
                components = constraint_components(alpha, beta)
                for p in (Fraction(1, 10), Fraction(1, 2), Fraction(9, 10)):
                    q = p * p + (1 - p) ** 2
                    assert probability(components, p) ** 4 <= q ** (a * (2 * n - a - 3))
                    sparse_count += 1
    # A damaged ground constraint changes the known support-two probability.
    assert probability(constraint_components((1, 0), (0, 1)), Fraction(1, 2)) == Fraction(1, 2)
    # Verify the isolated-k-set edge count by constructing its incident edges.
    for n in range(2, 10):
        for k in range(1, n + 1):
            incident = [(i, j) for i in range(n) for j in range(i + 1, n) if i < k or j < k]
            assert 2 * len(incident) == 2 * k * n - k * (k + 1)
    report = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(), 'seconds': round(time.perf_counter() - start, 6),
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'histograms': {s: [{'external_deficit': d, 'internal_rank': r, 'pairs': count}
                           for (d, r), count in sorted(h.items())] for s, h in histograms.items()},
        'coefficients': coefficients, 'direct_graph_expectations': direct,
        'sparse_exact_probability_checks': sparse_count,
        'effective_remainder_endpoint_checks': effective_remainder_checks(),
        'success': True,
        'scope': 'Finite original-adjacency certificates; not universal Lean or independent written review.'
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS', report['seconds'], 'seconds;', sparse_count, 'rational sparse checks')


if __name__ == '__main__':
    main()
