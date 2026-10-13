#!/usr/bin/env python3
"""Check the chunk guarantee and enforce the actual observation frontier."""

import hashlib
import json
from pathlib import Path
import platform
import random
import time

from chunk_lookahead import run_policy
from lookahead_boundary_check import instance
from sanity_check import all_graphs, solve_rob


class Environment:
    def __init__(self, deps, lookahead):
        self.deps, self.lookahead = deps, lookahead
        self.done = 0
        self.actions, self.reads = [], []

    def retired(self):
        return next((j for j in range(len(self.deps)) if not (self.done >> j & 1)),
                    len(self.deps))

    def read(self, j):
        assert 0 <= j < min(len(self.deps), self.retired() + 4 + self.lookahead)
        self.reads.append(j)
        return self.deps[j]

    def issue(self, action):
        retired = self.retired()
        assert 1 <= len(action) <= 3 and len(action) == len(set(action))
        for j in action:
            assert retired <= j < min(len(self.deps), retired + 4)
            assert not (self.done >> j & 1) and self.deps[j] & ~self.done == 0
        self.done |= sum(1 << j for j in action)
        self.actions.append(action)


def check(deps, lookahead):
    env = Environment(deps, lookahead)
    result = run_policy(len(deps), lookahead, env.read, env.issue)
    optimum, optimal_schedule = solve_rob(deps, 4, 3)
    n, q = len(deps), 4 + lookahead
    cuts = list(range(q, n, q))
    assert env.done == (1 << n) - 1
    assert env.reads == list(range(n))
    assert result["cycles"] == len(env.actions)
    assert result["cycles"] <= optimum + 3 * len(cuts)
    assert q * result["cycles"] <= (q + 9) * optimum
    if n <= q:
        assert result["cycles"] == optimum
    touched_count = sum(len({j // q for j in action}) for action in optimal_schedule)
    crossings = [sum(min(action) < cut <= max(action) for action in optimal_schedule)
                 for cut in cuts]
    assert all(x <= 3 for x in crossings)
    assert touched_count == len(optimal_schedule) + sum(crossings)
    assert result["cycles"] <= touched_count


def run():
    started = time.perf_counter()
    complete = 0
    for n in range(6):
        for deps in all_graphs(n):
            for lookahead in (0, 1, 2, 5):
                check(deps, lookahead)
                complete += 1
    seed = 20261014
    rng = random.Random(seed)
    random_cases = 0
    for n in (6, 9, 12, 20, 30):
        for probability in (0.05, 0.2, 0.5, 0.9):
            deps = tuple(sum(1 << i for i in range(j) if rng.random() < probability)
                         for j in range(n))
            for lookahead in (0, 1, 2, 5, 10):
                check(deps, lookahead)
                random_cases += 1
    hidden_family_cases = 0
    for m in range(1, 6):
        for padding in (0, 1):
            for hidden in ("A", "B"):
                deps, _, _ = instance(m, padding, hidden)
                for lookahead in (0, 2 * m, len(deps)):
                    check(deps, lookahead)
                    hidden_family_cases += 1
    return {
        "status": "PASS", "python": platform.python_version(), "seed": seed,
        "complete_program_range": "all 1,100 forward DAGs on 0 through 5 jobs",
        "complete_lookahead_values": [0, 1, 2, 5],
        "complete_program_lookahead_cases": complete,
        "seeded_random_cases": random_cases,
        "random_N_values": [6, 9, 12, 20, 30],
        "hidden_family_cases": hidden_family_cases,
        "checks": ["causal operand access below actual r+4+L frontier",
                   "operational ROB issue replay", "independent full-state optimum",
                   "additive boundary and multiplicative guarantees",
                   "projected optimal schedules and per-cut crossing counts"],
        "implementation_sha256": hashlib.sha256(Path(__file__).with_name("chunk_lookahead.py").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope": "finite implementation evidence, not a universal proof or novelty claim"
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
