#!/usr/bin/env python3
"""Exact polynomial optimizer for eager ROB capacity B = W + 1.

The proof is FORCED_SEGMENT_DP.md. This implementation uses predecessor
counters and clear-prefix macro states, not completed-set enumeration.
The edge-list API has O(N min(B,N) (N+E)) time and O(N+E) working space.
The optional bit-mask adapter's bit-extraction cost is separate.
"""


def solve_edges(n, edges, width):
    """Return exact cycles, an optimal schedule and macro-DP evidence.

    Indices are zero based. Repeated forward edges are harmless: the
    predecessor and successor lists retain the same multiplicities.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("N must be a nonnegative integer")
    if not isinstance(width, int) or width < 1:
        raise ValueError("issue width must be a positive integer")
    parents = [[] for _ in range(n)]
    successors = [[] for _ in range(n)]
    edge_count = 0
    for u, v in edges:
        if not isinstance(u, int) or not isinstance(v, int) or not (0 <= u < v < n):
            raise ValueError("true edges must satisfy 0 <= u < v < N")
        parents[v].append(u)
        successors[u].append(v)
        edge_count += 1
    capacity = width + 1

    def initial_ready(prefix):
        return tuple(j for j in range(prefix, min(n, prefix + capacity))
                     if all(u < prefix for u in parents[j]))

    def macro(prefix, omit, retain_trace=False):
        # Initialization scans jobs/edges once. Counts concern only
        # predecessors not already in the completed initial prefix.
        completed = [j < prefix for j in range(n)]
        remaining = [sum(u >= prefix for u in ps) for ps in parents]
        retired = prefix
        admitted = min(n, retired + capacity)
        ready = [j for j in range(retired, admitted) if remaining[j] == 0]
        first = tuple(j for j in ready if j != omit)
        assert first and len(first) == min(width, len(ready))
        if omit is not None:
            assert omit in ready and len(ready) == capacity
        ready = [] if omit is None else [omit]
        action = first
        done_count = prefix
        cycles = 0
        trace = [] if retain_trace else None
        while True:
            assert action and len(action) <= width
            if retain_trace:
                trace.append(action)
            cycles += 1
            for job in action:
                assert not completed[job] and remaining[job] == 0
                assert retired <= job < admitted
                completed[job] = True
            done_count += len(action)
            # The action was fixed before updating any predecessor count;
            # newly ready jobs cannot execute in the same cycle.
            for job in action:
                for successor in successors[job]:
                    remaining[successor] -= 1
                    assert remaining[successor] >= 0
                    if remaining[successor] == 0 and successor < admitted:
                        assert not completed[successor]
                        ready.append(successor)
            while retired < n and completed[retired]:
                retired += 1
            next_admitted = min(n, retired + capacity)
            for job in range(admitted, next_admitted):
                if remaining[job] == 0:
                    ready.append(job)
            admitted = next_admitted
            if done_count == retired:
                assert retired > prefix
                return cycles, retired, tuple(trace) if retain_trace else None
            # A completed but unretired entry leaves <=W unfinished slots.
            assert 1 <= len(ready) <= width
            action, ready = tuple(ready), []

    value = [0] * (n + 1)
    omitted = [None] * n
    endpoint = [n] * n
    macro_length = [0] * n
    evaluated_arcs = 0
    longest_macro = 0
    branching_prefixes = 0
    for prefix in range(n - 1, -1, -1):
        ready = initial_ready(prefix)
        assert ready and ready[0] == prefix
        if len(ready) <= width:
            choices = (None,)
        else:
            assert len(ready) == capacity
            choices = ready
            branching_prefixes += 1
        best = n + 1
        for omit in choices:
            length, target, _ = macro(prefix, omit)
            evaluated_arcs += 1
            longest_macro = max(longest_macro, length)
            if length + value[target] < best:
                best = length + value[target]
                omitted[prefix] = omit
                endpoint[prefix] = target
                macro_length[prefix] = length
        value[prefix] = best

    schedule = []
    prefix = 0
    while prefix < n:
        length, target, trace = macro(prefix, omitted[prefix], retain_trace=True)
        assert target == endpoint[prefix] and length == macro_length[prefix]
        schedule.extend(trace)
        prefix = target
    assert len(schedule) == value[0]
    return {
        "cycles": value[0], "schedule": tuple(schedule), "prefix_values": tuple(value),
        "chosen_omissions": tuple(omitted), "chosen_endpoints": tuple(endpoint),
        "chosen_macro_lengths": tuple(macro_length),
        "stats": {"N": n, "E_with_multiplicity": edge_count, "W": width,
                  "B": capacity, "macro_arcs": evaluated_arcs,
                  "branching_prefixes": branching_prefixes,
                  "longest_macro": longest_macro},
    }


def solve(deps, width):
    """Convenience adapter for one predecessor integer bit mask per job."""
    edges = []
    for j, mask in enumerate(deps):
        if not isinstance(mask, int) or mask < 0 or mask >> j:
            raise ValueError("predecessor masks must contain only smaller indices")
        while mask:
            bit = mask & -mask
            edges.append((bit.bit_length() - 1, j))
            mask ^= bit
    return solve_edges(len(deps), edges, width)
