#!/usr/bin/env python3
"""Test uniform younger omission for B=W+1 beyond width two.

This is counterexample search, not a proof. At a full ready window the
policy omits each non-oldest job with equal probability. It issues all
ready jobs in every other state. All arithmetic is exact.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import time

from sanity_check import solve_rob


def local_graph(n, mask, window):
    deps = [0] * n
    offset = 0
    for j in range(1, n):
        for i in range(max(0, j - window + 1), j):
            if mask >> offset & 1:
                deps[j] |= 1 << i
            offset += 1
    return tuple(deps)


def values(deps, width):
    n = len(deps)
    window = width + 1
    final = (1 << n) - 1
    unit = width ** n

    @lru_cache(None)
    def rec(done):
        if done == final:
            return 0, 0
        oldest = 0
        while done >> oldest & 1:
            oldest += 1
        ready = [j for j in range(oldest, min(n, oldest + window))
                 if not done >> j & 1 and not deps[j] & ~done]
        assert ready and ready[0] == oldest
        if len(ready) <= width:
            action = sum(1 << j for j in ready)
            optimum, expected = rec(done | action)
            return optimum + 1, expected + unit
        actions = [sum(1 << j for j in action)
                   for action in combinations(ready, width)]
        optimum = 1 + min(rec(done | action)[0] for action in actions)
        fair_actions = [action for action in actions if action >> oldest & 1]
        assert len(fair_actions) == width
        expected_sum = sum(rec(done | action)[1] for action in fair_actions)
        assert expected_sum % width == 0
        return optimum, unit + expected_sum // width

    optimum, numerator = rec(0)
    return optimum, Fraction(numerator, unit)


def run(width=3, max_n=8):
    start = time.perf_counter()
    candidate = Fraction(3 * width - 1, 2 * width)
    rows = []
    witness = None
    for n in range(1, max_n + 1):
        bits = sum(min(j, width) for j in range(n))
        count = 0
        worst = Fraction(1)
        worst_mask = 0
        for mask in range(1 << bits):
            deps = local_graph(n, mask, width + 1)
            optimum, expected = values(deps, width)
            ratio = expected / optimum
            count += 1
            if ratio > worst:
                worst, worst_mask = ratio, mask
            if ratio > candidate:
                checked, schedule = solve_rob(deps, width + 1, width)
                assert checked == optimum
                witness = {
                    "n": n, "local_edge_mask": mask,
                    "edges_one_based": [[i + 1, j + 1] for j in range(n)
                                         for i in range(j) if deps[j] >> i & 1],
                    "optimum": optimum, "expected": str(expected),
                    "ratio": str(ratio),
                    "optimal_schedule_one_based": [[i + 1 for i in a] for a in schedule],
                }
                break
        rows.append({"n": n, "graphs_examined": count,
                     "all_local_graphs_exhausted": count == 1 << bits,
                     "largest_ratio": str(worst), "worst_mask": worst_mask})
        if witness:
            break
    return {
        "status": "COUNTEREXAMPLE" if witness else "NO_COUNTEREXAMPLE_IN_FINITE_RANGE",
        "B": width + 1, "W": width, "candidate_ratio": str(candidate),
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python": platform.python_version(), "graphs_by_n": rows, "witness": witness,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "scope": "Tests this policy only; no global minimax upper bound is established."
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
