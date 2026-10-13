"""Reproducible finite verification; does not import the primary agent solver."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import platform
import random
import time

from constraint_solver import (
    assignment_check, augmented_edges, bounds, feasible, greedy,
    operational_check, solve, times_to_schedule,
)


def all_dags(n, max_indegree=None):
    choices = []
    for j in range(n):
        cap = j if max_indegree is None else min(j, max_indegree)
        choices.append([tuple((i, j) for i in subset)
                        for size in range(cap + 1)
                        for subset in combinations(range(j), size)])
    for groups in product(*choices):
        yield tuple(edge for group in groups for edge in group)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="verification_results.json")
    parser.add_argument("--exhaustive-n", type=int, default=4)
    parser.add_argument("--greedy-exhaustive-n", type=int, default=5)
    parser.add_argument("--random-count", type=int, default=3000)
    args = parser.parse_args()
    started = time.perf_counter()
    report = {
        "utc_start": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "seed": 20261014,
        "indexing": "Jobs and cycles are zero-based.",
        "source_sha256": {},
        "scope": "Finite computational evidence only; no novelty or universal-proof claim.",
    }
    for name in ("constraint_solver.py", "run_audit.py"):
        report["source_sha256"][name] = hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()

    boundary_cases = []
    for n in range(9):
        for B in range(1, max(2, n + 2)):
            for W in range(1, max(2, n + 3)):
                for name, edges, expected in (
                    ("independent", [], (n + min(B, W) - 1) // min(B, W)),
                    ("serial", [(i, i + 1) for i in range(n - 1)], n),
                ):
                    value, schedule = solve(n, edges, B, W)
                    assert value == expected, (name, n, B, W, value, expected)
                    assert operational_check(n, edges, B, W, schedule)
                    boundary_cases.append((name, n, B, W, value))
    report["boundary_case_count"] = len(boundary_cases)

    exhaustive_count = graph_count = opt_count = 0
    for n in range(1, args.exhaustive_n + 1):
        assignment_schedules = [(times, times_to_schedule(times))
                                for times in product(range(n), repeat=n)]
        for edges in all_dags(n):
            graph_count += 1
            for B in range(1, n + 1):
                for W in range(1, n + 1):
                    brute_opt = n + 1
                    for times, schedule in assignment_schedules:
                        direct = operational_check(n, edges, B, W, schedule)
                        characterized = assignment_check(n, edges, B, W, schedule)
                        exhaustive_count += 1
                        assert direct == characterized, (n, edges, B, W, times)
                        if direct:
                            brute_opt = min(brute_opt, max(times) + 1)
                    value, _ = solve(n, edges, B, W)
                    assert value == brute_opt, (n, edges, B, W, value, brute_opt)
                    opt_count += 1
    report["exhaustive_equivalence"] = {
        "n_max": args.exhaustive_n, "graph_count": graph_count,
        "time_assignment_parameter_checks": exhaustive_count,
        "optimal_values_cross_checked": opt_count,
        "all_forward_dags": True,
        "time_domain": "0..N-1, including interior/leading idle cycles",
    }
    print(json.dumps({"stage": "equivalence", **report["exhaustive_equivalence"]}), flush=True)

    policies = ("oldest", "critical_path", "augmented_critical_path")
    failures = {}
    exhaustive_greedy_graphs = exhaustive_greedy_instances = 0
    for n in range(1, args.greedy_exhaustive_n + 1):
        for edges in all_dags(n, max_indegree=2):
            exhaustive_greedy_graphs += 1
            for B in range(1, n + 1):
                for W in range(1, n + 1):
                    optimal, schedule = solve(n, edges, B, W)
                    exhaustive_greedy_instances += 1
                    for policy in policies:
                        value, greedy_schedule = greedy(n, edges, B, W, policy)
                        if value > optimal and policy not in failures:
                            failures[policy] = {
                                "N": n, "B": B, "W": W, "edges": edges,
                                "optimum": optimal, "optimal_schedule": schedule,
                                "greedy_cycles": value, "greedy_schedule": greedy_schedule,
                                "discovery": "exhaustive, indegree <= 2",
                            }
                            print(json.dumps({"stage": "greedy_failure", "policy": policy, **failures[policy]}), flush=True)
    report["greedy_exhaustive"] = {
        "n_max": args.greedy_exhaustive_n,
        "max_indegree": 2,
        "graph_count": exhaustive_greedy_graphs,
        "instances": exhaustive_greedy_instances,
    }

    rng = random.Random(report["seed"])
    for _ in range(args.random_count):
        n = rng.randrange(6, 13)
        edges = [(i, j) for j in range(n)
                 for i in rng.sample(range(j), rng.randrange(min(2, j) + 1))]
        B, W = rng.randrange(2, n + 1), rng.randrange(2, min(n + 1, 5))
        optimal, schedule = solve(n, edges, B, W)
        for policy in policies:
            value, greedy_schedule = greedy(n, edges, B, W, policy)
            if value > optimal and policy not in failures:
                failures[policy] = {
                    "N": n, "B": B, "W": W, "edges": edges,
                    "optimum": optimal, "optimal_schedule": schedule,
                    "greedy_cycles": value, "greedy_schedule": greedy_schedule,
                    "discovery": "seeded random, indegree <= 2",
                }
                print(json.dumps({"stage": "greedy_failure", "policy": policy, **failures[policy]}), flush=True)
    report["greedy_failures"] = failures
    report["random_instances"] = args.random_count
    report["random_range"] = {"N": [6, 12], "B": [2, "N"], "W": [2, "min(N,4)"]}

    pair = []
    for edges in [[(1, 3)], [(2, 3)]]:
        optimal, schedule = solve(4, edges, 3, 2)
        actions = []
        for size in range(3):
            for first in combinations(range(3), size):
                if feasible(4, edges, 3, 2, optimal, first_action=first) is not None:
                    actions.append(first)
        pair.append({"N": 4, "B": 3, "W": 2, "edges": edges,
                     "optimum": optimal, "optimal_schedule": schedule,
                     "all_optimal_first_actions": actions})
    assert pair[0]["all_optimal_first_actions"] == [(0, 1)]
    assert pair[1]["all_optimal_first_actions"] == [(0, 2)]
    report["online_indistinguishability_pair"] = pair

    weak_schedule = [[1], [3], [0], [2]]
    weak_times = [2, 0, 3, 1]
    assert all(weak_times[j - 2] < weak_times[j] for j in range(2, 4))
    assert not operational_check(4, [], 2, 1, weak_schedule)
    report["single_lag_edge_characterization_refuted"] = {
        "N": 4, "B": 2, "W": 1, "edges": [],
        "schedule": weak_schedule,
        "reason": "Edges only (j-B,j) allow job 3 before the completed prefix releases it.",
    }
    report["elapsed_seconds"] = time.perf_counter() - started
    report["status"] = "PASS"
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "elapsed_seconds": report["elapsed_seconds"], "output": args.output}), flush=True)


if __name__ == "__main__":
    main()
