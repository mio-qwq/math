#!/usr/bin/env python3
"""Falsify the fair younger-choice policy at B=3,W=2 using exact arithmetic.

Searches only gap-one/gap-two true edges because every longer edge is already
an artificial ROB edge. Stops at the first ratio greater than 5/4, or at the
declared search limit. It independently compares the scalar optimal recurrence
with the general completed-set solver on every examined graph through N=6.
"""

from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import time

from sanity_check import solve_rob


def local_graph(n, bits):
    deps = [0] * n
    offset = 0
    for j in range(1, n):
        if bits >> offset & 1:
            deps[j] |= 1 << (j - 1)
        offset += 1
        if j >= 2:
            if bits >> offset & 1:
                deps[j] |= 1 << (j - 2)
            offset += 1
    return tuple(deps)


def scalar_recurrence(deps):
    n = len(deps)
    unit = 1 << n
    optimum = [0] * (n + 4)
    expected = [0] * (n + 4)
    for i in range(n - 1, -1, -1):
        b_ready = i + 1 < n and not (deps[i + 1] >> i & 1)
        c_ready = i + 2 < n and not (deps[i + 2] & ((1 << i) | (1 << (i + 1))))
        if c_ready:
            d_ready = i + 3 < n and not (deps[i + 3] >> (i + 1) & 1)
            target = i + 4 if d_ready else i + 3
            c_cost = 2 + optimum[target]
            c_expected = 2 * unit + expected[target]
        if b_ready and c_ready:
            optimum[i] = min(1 + optimum[i + 2], c_cost)
            total = unit + expected[i + 2] + c_expected
            assert total % 2 == 0
            expected[i] = total // 2
        elif b_ready:
            optimum[i] = 1 + optimum[i + 2]
            expected[i] = unit + expected[i + 2]
        elif c_ready:
            optimum[i] = c_cost
            expected[i] = c_expected
        else:
            optimum[i] = 1 + optimum[i + 1]
            expected[i] = unit + expected[i + 1]
    return optimum[0], expected[0], unit


def exact_policy(deps):
    """Independent state recursion for this randomized policy, using Fractions."""
    from fractions import Fraction
    n = len(deps)
    full = (1 << n) - 1

    @lru_cache(None)
    def rec(done):
        if done == full:
            return Fraction(0)
        r = 0
        while done >> r & 1:
            r += 1
        ready = [j for j in range(r, min(n, r + 3))
                 if not (done >> j & 1) and not (deps[j] & ~done)]
        assert r in ready
        actions = [tuple(ready)] if len(ready) <= 2 else [(r, ready[1]), (r, ready[2])]
        return 1 + sum((rec(done | sum(1 << j for j in action)) for action in actions),
                       Fraction(0)) / len(actions)

    return rec(0)


def run(max_n=12):
    from fractions import Fraction
    start = time.perf_counter()
    counts, witness = [], None
    checked_optimum = 0
    checked_expectation = 0
    for n in range(1, max_n + 1):
        examined = 0
        worst = Fraction(1)
        for bits in range(1 << (max(0, n - 1) + max(0, n - 2))):
            deps = local_graph(n, bits)
            optimum, numerator, denominator = scalar_recurrence(deps)
            expected = Fraction(numerator, denominator)
            if n <= 6:
                assert optimum == solve_rob(deps, 3, 2)[0]
                assert expected == exact_policy(deps)
                checked_optimum += 1
                checked_expectation += 1
            ratio = expected / optimum
            worst = max(worst, ratio)
            examined += 1
            if ratio > Fraction(5, 4):
                actual_optimum, schedule = solve_rob(deps, 3, 2)
                assert actual_optimum == optimum
                assert exact_policy(deps) == expected
                witness = {
                    "n": n, "local_edge_mask": bits,
                    "edges_one_based": [[i + 1, j + 1] for j in range(n)
                                         for i in range(j) if deps[j] >> i & 1],
                    "optimal_makespan": optimum,
                    "optimal_schedule_one_based": [[j + 1 for j in action] for action in schedule],
                    "policy_expected_makespan": str(expected), "expected_ratio": str(ratio),
                    "meaning": "Refutes this fair-choice policy, not all randomized policies."
                }
                break
        counts.append({"n": n, "graphs_examined": examined,
                       "all_local_graphs_exhausted": examined == 1 << (max(0, n - 1) + max(0, n - 2)),
                       "largest_ratio_examined": str(worst)})
        if witness:
            break
    report = {
        "status": "COUNTEREXAMPLE" if witness else "NO_COUNTEREXAMPLE_IN_FINITE_RANGE",
        "model": {"B": 3, "W": 2}, "max_n_requested": max_n,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(), "graphs_by_n": counts,
        "independent_optimum_crosschecks": checked_optimum,
        "independent_expectation_crosschecks": checked_expectation,
        "witness": witness, "elapsed_seconds": round(time.perf_counter() - start, 6)
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    run()
