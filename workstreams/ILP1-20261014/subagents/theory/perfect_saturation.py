#!/usr/bin/env python3
"""Linear perfect-width saturation certificates for B=W+1 and W dividing N.

Each input mask contains the zero-based true predecessors of one job.
This solves T*=N/W, not attainability of ceil(N/W) when W does not divide N.
"""


def analyse(deps, width):
    """Convenience wrapper for predecessor bit masks; see analyse_edges."""
    deps = tuple(deps)
    n = len(deps)
    for j, mask in enumerate(deps):
        if not isinstance(mask, int) or mask < 0 or mask >> j:
            raise ValueError("dependencies must be forward predecessor bit masks")

    def edges():
        for v, mask in enumerate(deps):
            remaining = mask
            while remaining:
                bit = remaining & -remaining
                yield bit.bit_length() - 1, v
                remaining ^= bit

    return analyse_edges(n, edges(), width)


def analyse_edges(n, edges, width):
    """Core O(N+|E|) algorithm on a zero-based forward edge iterable."""
    if not isinstance(width, int) or width < 1:
        raise ValueError("width must be a positive integer")
    if not isinstance(n, int) or n < 0 or n % width:
        raise ValueError("N must be nonnegative and divisible by width")
    blocks = n // width
    single = [True] * blocks
    double = [True] * max(0, blocks - 1)
    single_witness = [None] * blocks
    double_witness = [None] * max(0, blocks - 1)

    def batch(x, start):
        boundary = (start + 1) * width - 1
        return 0 if x < boundary or x == boundary + 1 else 1

    for u, v in edges:
        if not isinstance(u, int) or not isinstance(v, int) or not 0 <= u < v < n:
            raise ValueError("edges must be forward, zero-based, and inside the program")
        block_u, block_v = u // width, v // width
        if block_u == block_v:
            single[block_u] = False
            single_witness[block_u] = (u, v)
        # A true edge can occur inside at most two adjacent-block candidates.
        for start in (block_u - 1, block_u):
            if 0 <= start < blocks - 1 and v < (start + 2) * width:
                if batch(u, start) >= batch(v, start):
                    double[start] = False
                    double_witness[start] = (u, v)

    tiles = []
    obstruction = None
    if width == 1:
        # The special case is always saturated; keep its certificate in order.
        tiles = [(j, 1) for j in range(blocks)]
    else:
        start = 0
        while start < blocks:
            end = start + 1
            while end < blocks and double[end - 1]:
                end += 1
            if (end - start) % 2 == 0:
                tiles.extend((j, 2) for j in range(start, end, 2))
            else:
                pivot = next((j for j in range(start, end, 2) if single[j]), None)
                if pivot is None:
                    obstruction = (start, end)  # half-open block component
                    tiles = []
                    break
                tiles.extend((j, 2) for j in range(start, pivot, 2))
                tiles.append((pivot, 1))
                tiles.extend((j, 2) for j in range(pivot + 1, end, 2))
            start = end

    schedule = []
    for start, length in tiles:
        lo = start * width
        if length == 1:
            schedule.append(tuple(range(lo, lo + width)))
        else:
            boundary = lo + width - 1
            schedule.append(tuple(range(lo, boundary)) + (boundary + 1,))
            schedule.append((boundary,) + tuple(range(boundary + 2, lo + 2 * width)))
    negative_certificate = None
    if obstruction is not None:
        lo, hi = obstruction
        negative_certificate = {
            "first_block": lo, "past_last_block": hi,
            "forbidden_singletons": tuple((j, *single_witness[j]) for j in range(lo, hi, 2)),
            "left_boundary": None if lo == 0 else (lo - 1, *double_witness[lo - 1]),
            "right_boundary": None if hi == blocks else (hi - 1, *double_witness[hi - 1]),
        }
    return {
        "feasible": obstruction is None,
        "N": n, "W": width, "B": width + 1,
        "target_cycles": blocks,
        "single_legal": tuple(single), "double_legal": tuple(double),
        "tiles": tuple(tiles), "schedule": tuple(schedule),
        "obstruction_component": obstruction,
        "negative_certificate": negative_certificate,
    }
