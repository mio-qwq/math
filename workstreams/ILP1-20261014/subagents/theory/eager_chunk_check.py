#!/usr/bin/env python3
"""Actual callback and pathwise-dominance checks for the causal eager lift."""

import hashlib
import json
from pathlib import Path
import platform
import random
import time

from chunk_lookahead import run_policy
from chunk_lookahead_check import Environment
from eager_chunk_lookahead import run_eager_policy, run_random_eager_policy
from sanity_check import all_graphs


class NonDelayEnvironment(Environment):
    def issue(self, action):
        r = self.retired()
        ready = [j for j in range(r, min(len(self.deps), r + 4))
                 if not (self.done >> j & 1)
                 and self.deps[j] & ~self.done == 0]
        assert len(action) == min(3, len(ready))
        super().issue(action)


def check(deps, lookahead, counts, *, expected=None):
    n, q = len(deps), 4 + lookahead
    costs = []
    for offset in range(1, q + 1):
        original = Environment(deps, lookahead)
        baseline = run_policy(n, lookahead, original.read, original.issue,
                              initial_chunk_size=offset)
        env = NonDelayEnvironment(deps, lookahead)
        result = run_eager_policy(n, lookahead, env.read, env.issue,
                                  initial_chunk_size=offset)
        assert env.done == (1 << n) - 1
        assert len(env.reads) == len(set(env.reads)) == n
        assert result["cycles"] == len(env.actions)
        assert result["cycles"] <= baseline["cycles"]
        assert result["virtual_cycles"] <= baseline["cycles"]
        assert result["virtual_cycles"] == result["cycles"] + result["skipped_virtual_cycles"]
        assert result["observed_jobs"] == n
        if expected is not None:
            assert result["cycles"] == expected
        counts["offsets"] += 1
        counts["reads"] += len(env.reads)
        counts["cycles"] += len(env.actions)
        counts["strict_improvements"] += result["cycles"] < baseline["cycles"]
        counts["skipped_virtual_cycles"] += result["skipped_virtual_cycles"]
        counts["filler_jobs"] += result["filler_jobs"]
        costs.append(result["cycles"])
    env = NonDelayEnvironment(deps, lookahead)
    result = run_random_eager_policy(n, lookahead, env.read, env.issue,
                                     rng=random.Random(20261014))
    assert result["cycles"] == costs[result["initial_chunk_size"] - 1]
    assert env.done == (1 << n) - 1
    counts["wrappers"] += 1


def chain_family(blocks):
    k = 3
    deps = [0] * (2 * k * blocks)
    for block in range(blocks):
        start = block * 2 * k
        barrier = 0 if block == 0 else (1 << (start - 1)) | (1 << (start - k - 1))
        for side in (0, k):
            deps[start + side] = barrier
            for j in range(1, k):
                deps[start + side + j] = 1 << (start + side + j - 1)
    return tuple(deps)


def run():
    started = time.perf_counter()
    counts = dict(offsets=0, wrappers=0, reads=0, cycles=0,
                  strict_improvements=0, skipped_virtual_cycles=0, filler_jobs=0)
    exhaustive = random_cases = family_cases = 0
    for n in range(6):
        for deps in all_graphs(n):
            for lookahead in (0, 1, 5):
                check(deps, lookahead, counts)
                exhaustive += 1
    rng = random.Random(20261014)
    for n in (7, 11, 19):
        for _ in range(6):
            deps = tuple(sum(1 << i for i in rng.sample(range(j), rng.randrange(min(j, 2) + 1)))
                         for j in range(n))
            for lookahead in (0, 2, 6):
                check(deps, lookahead, counts)
                random_cases += 1
    for blocks in (1, 2, 5):
        for lookahead in (0, 1, 2, 7):
            check(chain_family(blocks), lookahead, counts, expected=3 * blocks)
            family_cases += 1
    assert counts["strict_improvements"] > 0
    assert counts["skipped_virtual_cycles"] > 0
    assert counts["filler_jobs"] > 0
    return {
        "status": "PASS", "python": platform.python_version(), "seed": 20261014,
        "exhaustive_range": "all 1,100 forward DAGs on 0 through 5 jobs, L=0,1,5",
        "exhaustive_program_lookahead_cases": exhaustive,
        "random_binary_input_cases": random_cases,
        "random_N_values": [7, 11, 19],
        "sharpness_family_cases": family_cases,
        "counts": counts,
        "checked": ["actual operand visibility and ROB issue callbacks",
                    "non-delay real action on every cycle",
                    "pathwise dominance for each common fixed offset",
                    "unique metadata reads, virtual inclusion assertions, skipped virtual cycles",
                    "exact optimality on the two-chain family",
                    "actual seeded uniform-wrapper calls"],
        "implementation_sha256": hashlib.sha256(Path(__file__).with_name("eager_chunk_lookahead.py").read_bytes()).hexdigest(),
        "unchanged_controller_sha256": hashlib.sha256(Path(__file__).with_name("chunk_lookahead.py").read_bytes()).hexdigest(),
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope": "finite implementation checks, not proof of a better universal competitive constant"
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
