"""Exact ROB horizon feasibility parameterized by window excess and idle slots.

Completed sets are enumerated in time-dependent strips, not by enumerating
subsets of all B ready positions. See CORRIDOR.md for the general proof.
The Python implementation is not Lean verified.
"""
from itertools import combinations
from math import comb


def solve(n, edges, window, width, horizon):
    """Return feasibility and a legal schedule of duration at most horizon.

    Resource caps preserve the original model. If the horizon is at least N,
    a sequential witness avoids an unnecessarily large binary-encoded horizon.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("N must be a nonnegative integer")
    if not isinstance(horizon, int) or horizon < 0:
        raise ValueError("horizon must be a nonnegative integer")
    if not isinstance(window, int) or window < 1:
        raise ValueError("window must be positive")
    if not isinstance(width, int) or width < 1:
        raise ValueError("width must be positive")
    predecessors = [0] * n
    for u, v in edges:
        if not isinstance(u, int) or not isinstance(v, int) or not 0 <= u < v < n:
            raise ValueError("true edges must be forward and inside the program")
        predecessors[v] |= 1 << u
    if n == 0:
        return {"feasible": True, "schedule": [], "reason": "empty"}
    if horizon >= n:
        return {"feasible": True, "schedule": [[j] for j in range(n)],
                "reason": "sequential witness"}
    b = min(window, n)
    w = min(width, b)
    slack = w * horizon - n
    if slack < 0:
        return {"feasible": False, "schedule": None, "reason": "work lower bound"}
    excess = b - w
    strip_bound = 2 * excess + slack
    state_bound = sum(comb(strip_bound, j) for j in range(excess, excess + slack + 1))
    full = (1 << n) - 1

    def candidates(t):
        lo = max(0, t * w - excess - slack)
        hi = min(n, t * w + excess)
        prefix = (1 << lo) - 1
        low_count = max(0, t * w - slack - lo)
        high_count = min(hi - lo, t * w - lo)
        for count in range(low_count, high_count + 1):
            for picked in combinations(range(lo, hi), count):
                mask = prefix
                for j in picked:
                    mask |= 1 << j
                yield mask

    def ready(done):
        missing = full ^ done
        if not missing:
            return 0
        oldest = (missing & -missing).bit_length() - 1
        result = 0
        for j in range(oldest, min(n, oldest + b)):
            if not (done >> j) & 1 and not predecessors[j] & ~done:
                result |= 1 << j
        return result

    parents = [{0: None}]
    layer_sizes = [1]
    candidate_sizes = [1]
    pairs_checked = 0
    for t in range(1, horizon + 1):
        options = list(candidates(t))
        assert len(options) <= state_bound
        previous = [(done, ready(done)) for done in parents[-1]]
        reached = {}
        for following in options:
            for done, enabled in previous:
                pairs_checked += 1
                if done & ~following:
                    continue
                issued = following ^ done
                if issued.bit_count() > w or issued & ~enabled:
                    continue
                reached[following] = done
                break
        parents.append(reached)
        layer_sizes.append(len(reached))
        candidate_sizes.append(len(options))
        if not reached:
            break
    feasible = len(parents) == horizon + 1 and full in parents[-1]
    schedule = None
    if feasible:
        done = full
        schedule = []
        for t in range(horizon, 0, -1):
            earlier = parents[t][done]
            issued = done ^ earlier
            schedule.append([j for j in range(n) if (issued >> j) & 1])
            done = earlier
        schedule.reverse()
        while schedule and not schedule[-1]:
            schedule.pop()
    return {"feasible": feasible, "schedule": schedule, "N": n,
            "B": b, "W": w, "horizon": horizon,
            "window_excess": excess, "idle_slot_budget": slack,
            "strip_width_bound": strip_bound,
            "states_per_layer_bound": state_bound,
            "candidate_sizes": candidate_sizes, "reachable_sizes": layer_sizes,
            "candidate_pairs_checked": pairs_checked,
            "reason": "exact corridor reachability"}
