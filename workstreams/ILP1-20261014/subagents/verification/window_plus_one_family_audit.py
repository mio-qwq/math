"""Audit the two-cycle hidden-omission family at B=W+1.

Uses the independent time-variable CSP for optimum and all first actions.
The family-specific policy is also checked by direct ROB replay.
"""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform
from time import perf_counter

from constraint_solver import feasible, operational_check, solve


def family(W, m, hidden):
    B = W+1
    pool = list(range(m, B))
    assert 1 <= m <= W-1 and hidden in pool
    required = [root for root in pool if root != hidden]
    edges = tuple((root, B+k % m) for k, root in enumerate(required))
    return B+m, edges


def family_policy(W, m, hidden, omitted):
    n, edges = family(W, m, hidden)
    B = W+1
    first = [root for root in range(B) if root != omitted]
    ready_sinks = [sink for sink in range(B, n)
                   if all(root in first for root, target in edges if target == sink)]
    second = [omitted] + ready_sinks
    third = [sink for sink in range(B, n) if sink not in ready_sinks]
    return [first, second] + ([third] if third else [])


def main():
    start = perf_counter()
    programs = action_checks = policy_checks = 0
    parameter_reports = []
    for W in range(2, 8):
        B = W+1
        for m in range(1, W):
            pool = list(range(m, B))
            actions = [action for size in range(W+1)
                       for action in combinations(range(B), size)]
            for hidden in pool:
                n, edges = family(W, m, hidden)
                assert solve(n, edges, B, W)[0] == 2
                unique = set(range(B)) - {hidden}
                for action in actions:
                    found = feasible(n, edges, B, W, 2, first_action=action)
                    assert (found is not None) == (set(action) == unique)
                    action_checks += 1
                costs = []
                for omitted in pool:
                    schedule = family_policy(W, m, hidden, omitted)
                    assert operational_check(n, edges, B, W, schedule)
                    assert len(schedule) == (2 if omitted == hidden else 3)
                    costs.append(len(schedule))
                    policy_checks += 1
                assert Fraction(sum(costs), len(costs)*2) == Fraction(3, 2)-Fraction(1, 2*len(pool))
                programs += 1
            d = (W-m+m-1)//m
            parameter_reports.append({"W": W, "B": B, "m": m, "N": B+m,
                                      "pool_size": len(pool), "maximum_indegree": d,
                                      "maximum_outdegree": 1,
                                      "exact_family_ratio": str(Fraction(3, 2)-Fraction(1, 2*len(pool)))})
    # Separately retain the simplest binary witness: four roots and a two-input sink.
    n, edges = family(3, 1, 1)
    assert n == 5 and sorted(edges) == [(2, 4), (3, 4)]
    # And the matching family with one excess window slot, through q=5.
    matching_checks = 0
    for q in range(1, 6):
        W, m, B = 2*q, q, 2*q+1
        for hidden in range(m, B):
            n, edges = family(W, m, hidden)
            assert len({a for a, _ in edges}) == len(edges) == len({b for _, b in edges}) == q
            assert solve(n, edges, B, W)[0] == 2
            for omitted in range(m, B):
                schedule = family_policy(W, m, hidden, omitted)
                assert operational_check(n, edges, B, W, schedule)
                assert len(schedule) == (2 if hidden == omitted else 3)
                matching_checks += 1
    report = {"status": "PASS", "utc_finished": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": perf_counter()-start, "python": platform.python_version(),
              "scope": "All W=2..7, m=1..W-1 and hidden roots; partitions are deterministic round-robin.",
              "programs": programs, "first_action_checks_including_empty_underfull": action_checks,
              "family_policy_replays": policy_checks, "matching_q_range": [1, 5],
              "matching_policy_replays": matching_checks, "parameters": parameter_reports,
              "binary_example": {"W": 3, "B": 4, "N": 5, "hidden": 1, "edges": [[2,4],[3,4]],
                                 "optimum": 2, "family_ratio": "4/3"},
              "source_sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("constraint_solver.py", "window_plus_one_family_audit.py")}}
    Path(__file__).with_name("window_plus_one_family_results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({key: report[key] for key in ("status", "programs", "first_action_checks_including_empty_underfull",
                                                   "family_policy_replays", "matching_policy_replays", "elapsed_seconds")}))


if __name__ == "__main__":
    main()
