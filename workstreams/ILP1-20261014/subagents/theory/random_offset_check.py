#!/usr/bin/env python3
"""Exact finite-offset average with independently checked causal callbacks."""

from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import random
import time

from chunk_lookahead import run_policy, run_random_policy
from chunk_lookahead_check import Environment
from sanity_check import all_graphs, solve_rob


def check(deps, lookahead):
    n, q = len(deps), 4 + lookahead
    optimum, actions = solve_rob(deps, 4, 3)
    span_sum = sum(max(a) - min(a) for a in actions)
    costs = []
    for offset in range(1, q + 1):
        env = Environment(deps, lookahead)
        result = run_policy(n, lookahead, env.read, env.issue,
                            initial_chunk_size=offset)
        assert env.done == (1 << n) - 1 and env.reads == list(range(n))
        assert result["initial_chunk_size"] == offset
        costs.append(result["cycles"])
    mean = Fraction(sum(costs), q)
    assert mean <= optimum + Fraction(span_sum, q)
    assert mean <= Fraction(q + 3, q) * optimum
    # The wrapper performs a real draw, rather than reading an offset
    # from an input-dependent table. Its seeded result must agree with
    # the corresponding exact member of the finite partition average.
    env = Environment(deps, lookahead)
    sampled = run_random_policy(n, lookahead, env.read, env.issue,
                                rng=random.Random(20261014))
    assert sampled["cycles"] == costs[sampled["initial_chunk_size"] - 1]
    assert env.done == (1 << n) - 1 and env.reads == list(range(n))
    return q


def run():
    started = time.perf_counter()
    cases = offsets = 0
    for n in range(6):
        for deps in all_graphs(n):
            for lookahead in (0, 1, 2, 5):
                offsets += check(deps, lookahead)
                cases += 1
    rng = random.Random(20261014)
    random_cases = random_offsets = 0
    for n in (8, 13, 21):
        for probability in (0.05, 0.3, 0.8):
            deps = tuple(sum(1 << i for i in range(j) if rng.random() < probability)
                         for j in range(n))
            for lookahead in (0, 3, 9):
                random_offsets += check(deps, lookahead)
                random_cases += 1
    return {
        "status": "PASS", "python": platform.python_version(), "seed": 20261014,
        "complete_graph_range": "all 1,100 forward DAGs on 0 through 5 jobs",
        "complete_lookahead_values": [0, 1, 2, 5],
        "complete_program_lookahead_cases": cases,
        "complete_exact_offset_replays": offsets,
        "random_program_lookahead_cases": random_cases,
        "random_exact_offset_replays": random_offsets,
        "seeded_wrapper_calls": cases + random_cases,
        "expectation": "exact Fraction sum over every U in 1,...,4+L",
        "bound_checked": "E[T] <= T* + sum_optimal_action_spans/(4+L) <= (1+3/(4+L))*T*",
        "causality": "all callbacks enforce actual r+4+L visibility and B4W3 legality",
        "implementation_sha256": hashlib.sha256(Path(__file__).with_name("chunk_lookahead.py").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope": "finite exact checks; general theorem is the independent written offset proof"
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
