#!/usr/bin/env python3
"""A causal non-delay lift of the fixed B=4,W=3 chunk controller.

The original chunk implementation is deliberately left unchanged. Its
callbacks run in a separate virtual execution; real execution may finish
virtual jobs early. No full-program dependency argument is accepted.
"""

import random

from chunk_lookahead import run_policy


class _RealExecutionComplete(Exception):
    pass


def run_eager_policy(n, extra_lookahead, read_parents, issue, *,
                     initial_chunk_size=None):
    """Keep pending virtual jobs, then fill real slots with oldest ready jobs.

    A virtual action already completed in real execution costs no real
    cycle. All readiness tests use the real completion set *before* the
    current real action, so the lift provides no same-cycle bypass.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("N must be a nonnegative integer")
    if not isinstance(extra_lookahead, int) or extra_lookahead < 0:
        raise ValueError("extra lookahead must be a nonnegative integer")
    q = 4 + extra_lookahead
    initial = q if initial_chunk_size is None else initial_chunk_size
    if not isinstance(initial, int) or not 1 <= initial <= q:
        raise ValueError("initial chunk size must lie between one and 4+L")

    full = (1 << n) - 1
    real_done = virtual_done = 0
    real_prefix = virtual_prefix = 0
    parents = {}
    real_cycles = virtual_cycles = skipped_cycles = filler_jobs = 0

    def observe(j):
        assert 0 <= j < min(n, real_prefix + q)
        if j not in parents:
            mask = read_parents(j)
            if not isinstance(mask, int) or mask < 0 or mask >> j:
                raise ValueError("observed predecessor mask is not forward")
            parents[j] = mask
        return parents[j]

    def virtual_read(j):
        # The controller cannot exploit data cached by the real filler
        # before that job becomes visible in its own virtual history.
        assert 0 <= j < min(n, virtual_prefix + q)
        return observe(j)

    def virtual_issue(action):
        nonlocal real_done, virtual_done, real_prefix, virtual_prefix
        nonlocal real_cycles, virtual_cycles, skipped_cycles, filler_jobs
        assert len(action) == len(set(action)) and len(action) <= 3
        for j in action:
            assert virtual_prefix <= j < min(n, virtual_prefix + 4)
            assert not (virtual_done >> j & 1)
            assert observe(j) & ~virtual_done == 0

        virtual_cycles += 1
        retained = tuple(j for j in action if not (real_done >> j & 1))
        if retained:
            ready = [j for j in range(real_prefix, min(n, real_prefix + 4))
                     if not (real_done >> j & 1)
                     and observe(j) & ~real_done == 0]
            assert set(retained) <= set(ready)
            selected = list(retained)
            for j in ready:
                if len(selected) == 3:
                    break
                if j not in retained:
                    selected.append(j)
            assert len(selected) == min(3, len(ready))
            issue(tuple(selected))
            real_done |= sum(1 << j for j in selected)
            real_cycles += 1
            filler_jobs += len(selected) - len(retained)
            while real_prefix < n and real_done >> real_prefix & 1:
                real_prefix += 1
        else:
            skipped_cycles += 1

        virtual_done |= sum(1 << j for j in action)
        while virtual_prefix < n and virtual_done >> virtual_prefix & 1:
            virtual_prefix += 1
        assert virtual_done & ~real_done == 0
        assert virtual_prefix <= real_prefix
        if real_done == full:
            # Remaining virtual planning is unnecessary once all actual
            # instructions have completed; no future callbacks are made.
            raise _RealExecutionComplete

    try:
        run_policy(n, extra_lookahead, virtual_read, virtual_issue,
                   initial_chunk_size=initial)
    except _RealExecutionComplete:
        pass
    assert real_done == full
    return {"cycles": real_cycles, "virtual_cycles": virtual_cycles,
            "skipped_virtual_cycles": skipped_cycles,
            "filler_jobs": filler_jobs, "observed_jobs": len(parents),
            "initial_chunk_size": initial}


def run_random_eager_policy(n, extra_lookahead, read_parents, issue, *, rng=None):
    """Draw the same input-independent uniform offset as the original policy."""
    if not isinstance(extra_lookahead, int) or extra_lookahead < 0:
        raise ValueError("extra lookahead must be a nonnegative integer")
    generator = random.SystemRandom() if rng is None else rng
    initial = generator.randrange(1, 5 + extra_lookahead)
    return run_eager_policy(n, extra_lookahead, read_parents, issue,
                            initial_chunk_size=initial)
