"""Reproduce counterexamples/families and optional independently implemented DP cross-check."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random
import sys
from time import perf_counter

from constraint_solver import bounds, augmented_edges, feasible, greedy, operational_check, solve
from run_audit import all_dags


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--primary-directory", help="Directory containing independently written rob.py and checker.py")
    p.add_argument("--output", default="extended_results.json")
    args = p.parse_args()
    start = perf_counter()
    report = {"utc_start": datetime.now(timezone.utc).isoformat(), "seed": 20261014,
              "indexing": "zero-based", "source_sha256": {},
              "scope": "Finite computational checks; not a universal proof or novelty claim."}
    for name in ("constraint_solver.py", "run_audit.py", "extended_audit.py"):
        report["source_sha256"][name] = hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()

    # Exhaustively search the prefix until both requested monotonicities fail.
    graphs = instances = 0
    threshold_failures = {}
    for n in range(1, 5):
        for edges in all_dags(n, max_indegree=2):
            graphs += 1
            table = [[solve(n, edges, B, W)[0] for W in range(1, n + 1)]
                     for B in range(1, n + 1)]
            instances += n * n
            bs = [next(B for B in range(1, n + 1)
                       if table[B-1][W-1] == table[n-1][W-1]) for W in range(1, n + 1)]
            ws = [next(W for W in range(1, B + 1)
                       if table[B-1][W-1] == table[B-1][B-1]) for B in range(1, n + 1)]
            for name, seq in (("B_sat", bs), ("W_sat", ws)):
                if name not in threshold_failures and any(a > b for a, b in zip(seq, seq[1:])):
                    threshold_failures[name] = {"N": n, "edges": edges, "T_rows_B_cols_W": table,
                                                "B_sat_by_W": bs, "W_sat_by_B": ws}
            if len(threshold_failures) == 2:
                break
        if len(threshold_failures) == 2:
            break
    assert set(threshold_failures) == {"B_sat", "W_sat"}
    report["threshold_nonmonotonicity"] = {"checked_graph_prefix": graphs,
                                           "checked_instances": instances,
                                           "witnesses": threshold_failures,
                                           "minimal_N_scope": "All N<4 forward DAGs exhaustively checked."}

    # This precise complete finite prefix gives the smallest N, by the initial audit.
    graphs = instances = 0
    for edges in all_dags(6, max_indegree=2):
        graphs += 1
        for W in (2, 3):
            instances += 1
            optimal, schedule = solve(6, edges, 6, W)
            value, gs = greedy(6, edges, 6, W, "augmented_critical_path")
            if value > optimal:
                report["augmented_critical_path_failure"] = {
                    "N": 6, "B": 6, "W": W, "edges": edges, "optimum": optimal,
                    "optimal_schedule": schedule, "greedy_cycles": value,
                    "greedy_schedule": gs, "checked_graph_prefix_at_N6": graphs,
                    "checked_instances_at_N6": instances,
                    "minimal_N_scope": "No failure among all indegree<=2 DAGs N<=5 in initial audit.",
                }
                break
        if "augmented_critical_path_failure" in report:
            break

    # Family: W+1 indistinguishable roots, W-1 suffix jobs depending on hidden x.
    family = []
    for W in range(2, 9):
        all_actions = list(combinations(range(W + 1), W))
        common = set(all_actions)
        programs = []
        for x in range(1, W + 1):
            edges = [(x, j) for j in range(W + 1, 2 * W)]
            optimum, schedule = solve(2 * W, edges, W + 1, W)
            assert optimum == 2
            allowed = [a for a in all_actions
                       if feasible(2 * W, edges, W + 1, W, 2, first_action=a) is not None]
            required = set(range(W - 1)) | {x}
            assert allowed == [a for a in all_actions if required <= set(a)]
            common.intersection_update(allowed)
            for a in all_actions:
                constrained = next(T for T in range(2, 2 * W + 1)
                                   if feasible(2 * W, edges, W + 1, W, T, first_action=a) is not None)
                assert constrained == (2 if required <= set(a) else 3)
            programs.append({"x": x, "edges": edges, "optimal_schedule": schedule,
                             "all_optimal_full_first_actions": allowed})
        assert not common
        family.append({"W": W, "B": W + 1, "N": 2 * W,
                       "common_optimal_first_actions": [], "programs": programs})
    report["online_family"] = family

    # Theory agent's indegree-two block construction; synthetic prefix edges
    # complete all cross-block relations. Original height can only be smaller.
    block_family = []
    for m in range(1, 7):
        n = 3 * m
        edges = []
        for k in range(1, m):
            edges += [(3*k - 2, 3*k), (3*k - 1, 3*k), (3*k - 1, 3*k + 1)]
        optimal, schedule = solve(n, edges, 3, 2)
        _, _, early, _ = bounds(n, augmented_edges(n, edges, 3))
        height = max(early) + 1
        assert optimal == 2*m and height == m
        block_family.append({"m": m, "N": n, "edges": edges, "B": 3, "W": 2,
                             "height_augmented": height, "work_bound": (n + 1)//2,
                             "optimum": optimal, "schedule": schedule})
    report["work_height_nontight_family"] = block_family

    if args.primary_directory:
        primary = Path(args.primary_directory).resolve()
        sys.path.insert(0, str(primary))
        import rob
        import checker
        primary_hash = {name: hashlib.sha256((primary / name).read_bytes()).hexdigest()
                        for name in ("rob.py", "checker.py")}
        graphs = comparisons = certificates = 0
        for n in range(6):
            for edges in all_dags(n, max_indegree=2):
                graphs += 1
                for B in range(1, max(n, 1) + 1):
                    for W in range(1, max(n, 1) + 1):
                        opt, schedule = solve(n, edges, B, W)
                        result = rob.solve(rob.Program(n, edges), B, W, certificate=True)
                        assert opt == result["cycles"], (n, edges, B, W, opt, result)
                        assert operational_check(n, edges, B, W, result["schedule"])
                        assert checker.replay(n, edges, B, W, schedule) == opt
                        assert checker.check_certificate(result)["optimum"] == opt
                        comparisons += 1
                        certificates += 1
        rng = random.Random(report["seed"])
        for _ in range(1000):
            n = rng.randrange(6, 13)
            edges = tuple((i, j) for j in range(n)
                          for i in rng.sample(range(j), rng.randrange(min(2, j) + 1)))
            B, W = rng.randrange(1, n + 3), rng.randrange(1, n + 3)
            opt, schedule = solve(n, edges, B, W)
            result = rob.solve(rob.Program(n, edges), B, W, certificate=True)
            assert opt == result["cycles"], (n, edges, B, W, opt, result)
            assert operational_check(n, edges, B, W, result["schedule"])
            assert checker.replay(n, edges, B, W, schedule) == opt
            assert checker.check_certificate(result)["optimum"] == opt
            comparisons += 1
            certificates += 1
        report["independent_primary_crosscheck"] = {
            "primary_source_sha256": primary_hash, "exhaustive_graphs_N0_through5": graphs,
            "exhaustive_indegree_max": 2, "exhaustive_B_W": "1..max(N,1)",
            "random_count": 1000, "random_N": [6, 12], "random_B_W": "1..N+2",
            "optimal_values_compared": comparisons, "certificates_replayed": certificates,
            "note": "Independent solver never imports primary; this audit driver alone imports both for comparison.",
        }
    report["elapsed_seconds"] = perf_counter() - start
    report["status"] = "PASS"
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "elapsed_seconds": report["elapsed_seconds"],
                      "crosscheck": report.get("independent_primary_crosscheck"),
                      "output": args.output}), flush=True)


if __name__ == "__main__":
    main()
