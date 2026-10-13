#!/usr/bin/env python3
"""Finite checks for final-operand information loss and long forced macros."""

from functools import lru_cache
from itertools import combinations
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import time

from sanity_check import replay


def instance(m, padding, hidden_parent):
    assert m >= 1 and padding in (0, 1) and hidden_parent in ("A", "B")
    n = 2 * m + 5 + padding
    deps = [0] * n
    a = [3] + [2 * k + 2 for k in range(1, m + 1)]
    b = [2] + [2 * k + 3 for k in range(1, m + 1)]
    for k in range(1, m + 1):
        deps[a[k]] = 1 << a[k - 1]
        deps[b[k]] = 1 << b[k - 1]
    deps[-1] = 1 << (a[-1] if hidden_parent == "A" else b[-1])
    return tuple(deps), a, b


def leading_schedule(m, padding, hidden_parent, leading):
    deps, a, b = instance(m, padding, hidden_parent)
    left, right = (a, b) if leading == "A" else (b, a)
    actions = [(0, 1, left[0])]
    actions += [(right[k - 1], left[k]) for k in range(1, m + 1)]
    last = [right[-1]]
    if padding:
        last.append(len(deps) - 2)
    if hidden_parent == leading:
        last.append(len(deps) - 1)
    actions.append(tuple(last))
    if hidden_parent != leading:
        actions.append((len(deps) - 1,))
    times = [0] * len(deps)
    for cycle, action in enumerate(actions, 1):
        for j in action:
            assert not times[j]
            times[j] = cycle
    assert replay(deps, 4, 3, times)
    return tuple(actions)


def first_action_values(deps):
    """Separate complete-state oracle, allowing every nonempty future subset."""
    n = len(deps)
    full = (1 << n) - 1

    @lru_cache(None)
    def optimum(done):
        if done == full:
            return 0
        oldest = next(j for j in range(n) if not (done >> j & 1))
        ready = [j for j in range(oldest, min(n, oldest + 4))
                 if not (done >> j & 1) and deps[j] & ~done == 0]
        return 1 + min(optimum(done | sum(1 << j for j in action))
                       for size in range(1, min(3, len(ready)) + 1)
                       for action in combinations(ready, size))

    # The initial four jobs are roots. Empty/underfilled first actions
    # remain in this check even though an optimum can be non-delay.
    values = {action: 1 + optimum(sum(1 << j for j in action))
              for size in range(4) for action in combinations(range(4), size)}
    return optimum(0), values


def long_macro(m):
    n = 2 * m
    deps = tuple((1 << (j - 2)) if j >= 4 and j % 2 == 0 else 0
                 for j in range(n))
    actions = [(0, 1, 3)]
    actions += [(2 * t - 2, 2 * t + 1) for t in range(2, m)]
    actions += [(2 * m - 2,)]
    done = 0
    for cycle, action in enumerate(actions, 1):
        retired = next((j for j in range(n) if not (done >> j & 1)), n)
        ready = {j for j in range(retired, min(n, retired + 4))
                 if not (done >> j & 1) and deps[j] & ~done == 0}
        if cycle > 1:
            assert set(action) == ready and len(ready) <= 3
        done |= sum(1 << j for j in action)
        retired = next((j for j in range(n) if not (done >> j & 1)), n)
        if cycle < m:
            assert retired == 2 * cycle
            assert done.bit_count() - retired == 1
        else:
            assert retired == n
    assert len(actions) == m


def run():
    started = time.perf_counter()
    programs = first_actions = replays = 0
    exact_ratios = []
    optimal_a = {(0, 3), (0, 1, 3), (0, 2, 3)}
    optimal_b = {(0, 1, 2)}
    for m in range(1, 11):
        for padding in (0, 1):
            prior_values = {}
            for hidden_parent in ("A", "B"):
                deps, _, _ = instance(m, padding, hidden_parent)
                optimum, values = first_action_values(deps)
                assert optimum == m + 2
                assert {a for a, t in values.items() if t == optimum} == (
                    optimal_a if hidden_parent == "A" else optimal_b)
                prior_values[hidden_parent] = values
                programs += 1
                first_actions += len(values)
                for leading in ("A", "B"):
                    schedule = leading_schedule(m, padding, hidden_parent, leading)
                    assert len(schedule) == optimum + (hidden_parent != leading)
                    replays += 1
                deps_other, _, _ = instance(m, padding,
                                            "B" if hidden_parent == "A" else "A")
                assert deps[:-1] == deps_other[:-1] and deps[-1] != deps_other[-1]
                assert all(mask.bit_count() <= 1 for mask in deps)
                assert all(sum(mask >> j & 1 for mask in deps) <= 1
                           for j in range(len(deps)))
            average = min(Fraction(prior_values["A"][a] + prior_values["B"][a], 2)
                          for a in prior_values["A"])
            assert average == Fraction(2 * (m + 2) + 1, 2)
            exact_ratios.append({"M": m, "padding": padding,
                                 "N": 2 * m + 5 + padding,
                                 "uniform_prior_expected_lower_bound": str(average),
                                 "family_randomized_minimax_ratio": str(average / (m + 2))})
    for m in range(2, 41):
        long_macro(m)
    return {
        "status": "PASS", "python": platform.python_version(),
        "lookahead_programs": programs, "M_min": 1, "M_max": 10,
        "padding_values": [0, 1], "N_min": 7, "N_max": 26,
        "legal_first_action_checks_including_empty": first_actions,
        "canonical_correct_and_wrong_leader_replays": replays,
        "optimal_first_sets_A": [list(x) for x in sorted(optimal_a)],
        "optimal_first_sets_B": [list(x) for x in sorted(optimal_b)],
        "exact_family_ratios": exact_ratios,
        "long_forced_macros": {"m_min": 2, "m_max": 40, "cases": 39,
                               "assertions": "unique forced action and one completed hole at every interior boundary"},
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "scope": "finite verification; universal N/lookahead statements rely on the written proof"
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
