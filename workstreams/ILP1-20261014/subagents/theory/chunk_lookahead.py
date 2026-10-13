#!/usr/bin/env python3
"""Causal prefix-lookahead chunk policy, specifically for B=4,W=3."""

import random

from forced_segment_dp import solve


def run_policy(n, extra_lookahead, read_parents, issue, *, initial_chunk_size=None):
    """Execute via observation/issue callbacks; do not accept the future DAG.

    read_parents(j) returns the original-index predecessor bit mask of j.
    issue(action) executes one cycle of the supplied original-index jobs.
    Both callbacks may reject a visibility or operational violation.
    The first chunk may have a supplied size in 1,...,4+L; later chunks
    have size 4+L. The default recovers the deterministic equal-block rule.
    Return counts and the chosen initial size, not unseen program data.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("N must be a nonnegative integer")
    if not isinstance(extra_lookahead, int) or extra_lookahead < 0:
        raise ValueError("extra lookahead must be a nonnegative integer")
    block_size = 4 + extra_lookahead
    if initial_chunk_size is None:
        initial_chunk_size = block_size
    if not isinstance(initial_chunk_size, int) or not 1 <= initial_chunk_size <= block_size:
        raise ValueError("initial chunk size must lie between one and 4+L")
    cycles = largest_block = 0
    start = 0
    next_size = initial_chunk_size
    while start < n:
        stop = min(n, start + next_size)
        local = []
        for j in range(start, stop):
            mask = read_parents(j)
            if not isinstance(mask, int) or mask < 0 or mask >> j:
                raise ValueError("observed predecessor mask is not forward")
            # Earlier-block parents are already complete. Renumbering
            # preserves all internal index gaps and therefore ROB edges.
            local.append(mask >> start)
        optimum = solve(tuple(local), 3)
        largest_block = max(largest_block, stop - start)
        for action in optimum["schedule"]:
            issue(tuple(start + j for j in action))
            cycles += 1
        start = stop
        next_size = block_size
    return {"cycles": cycles, "largest_block": largest_block,
            "initial_chunk_size": initial_chunk_size}


def run_random_policy(n, extra_lookahead, read_parents, issue, *, rng=None):
    """Draw one uniform offset before execution, independently of the input.

    Inject random.Random(seed) for reproducibility. The default uses
    SystemRandom. All later behavior is the same causal chunk policy.
    """
    if not isinstance(extra_lookahead, int) or extra_lookahead < 0:
        raise ValueError("extra lookahead must be a nonnegative integer")
    generator = random.SystemRandom() if rng is None else rng
    initial = generator.randrange(1, 5 + extra_lookahead)
    return run_policy(n, extra_lookahead, read_parents, issue,
                      initial_chunk_size=initial)
