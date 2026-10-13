"""Independent finite certificates for the two online lower-bound families."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
from time import perf_counter

from constraint_solver import feasible, operational_check, solve


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="online_results.json")
    args = p.parse_args()
    start = perf_counter()
    report = {"utc_start": datetime.now(timezone.utc).isoformat(), "indexing": "zero-based",
              "scope": "Finite computational verification only; accompanying review gives proof audit.",
              "source_sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("constraint_solver.py", "online_audit.py")}}

    binomial = []
    program_count = action_checks = 0
    for q in range(1, 5):
        n, B, W = 4*q, 3*q, 2*q
        common = None
        expected_actions = []
        for A in combinations(range(q, 3*q), q):
            program_count += 1
            edges = [(a, 3*q + k) for k, a in enumerate(A)]
            opt, schedule = solve(n, edges, B, W)
            assert opt == 2
            required = tuple(range(q)) + A
            actual = []
            for action in combinations(range(B), W):
                action_checks += 1
                possible2 = feasible(n, edges, B, W, 2, first_action=action) is not None
                assert possible2 == (action == required), (q, A, action)
                if possible2:
                    actual.append(action)
                # An explicit universal three-cycle completion for any full action.
                done = set(action)
                head = next((j for j in range(B) if j not in done), B)
                roots_left = set(range(B)) - done
                ready_suffix = {j for a, j in edges if a in done and j < head + B}
                second = sorted(roots_left | ready_suffix)
                third = sorted(set(range(n)) - done - set(second))
                proposed = [list(action), second] + ([third] if third else [])
                assert operational_check(n, edges, B, W, proposed), (q, A, action, proposed)
                assert len(proposed) == (2 if action == required else 3)
            assert actual == [required]
            expected_actions.append(required)
            common = set(actual) if common is None else common & set(actual)
        assert common == set()
        assert len(set(expected_actions)) == comb(2*q, q)
        binomial.append({"q": q, "N": n, "B": B, "W": W,
                         "number_of_indistinguishable_programs": comb(2*q, q),
                         "distinct_required_first_actions": len(set(expected_actions)),
                         "randomized_minimax_expected_ratio": [3*comb(2*q,q)-1, 2*comb(2*q,q)],
                         "sufficient_necessary_fixed_length_advice_bits": (comb(2*q,q)-1).bit_length()})
    report["binomial_family"] = {"q_range": [1, 4], "programs_checked": program_count,
                                  "full_first_action_checks": action_checks, "instances": binomial}

    # Chain family for every checked B>W>=2. A first-cycle action is optimal
    # exactly when it contains root zero and the hidden parent x.
    chain_parameters = []
    chain_programs = chain_actions = 0
    for B in range(3, 9):
        n = 2 * B
        for W in range(2, B):
            common = None
            for x in range(1, B):
                edges = [(x, B)] + [(j, j+1) for j in range(B, 2*B-1)]
                opt, schedule = solve(n, edges, B, W)
                assert opt == B + 1
                chain_programs += 1
                possible_actions = []
                for size in range(W + 1):
                    for action in combinations(range(B), size):
                        chain_actions += 1
                        possible = feasible(n, edges, B, W, B+1, first_action=action) is not None
                        assert possible == (0 in action and x in action), (B, W, x, action)
                        if possible:
                            possible_actions.append(action)
                common = set(possible_actions) if common is None else common & set(possible_actions)
            assert common == set()
            chain_parameters.append({"B": B, "W": W, "N": n, "offline_optimum": B+1,
                                     "all_programs_optimal_first_action_intersection": []})
    report["chain_family"] = {"B_range": [3, 8], "W_range": "2..B-1",
                               "programs_checked": chain_programs,
                               "all_first_actions_checked": chain_actions,
                               "parameters": chain_parameters}
    report["elapsed_seconds"] = perf_counter() - start
    report["status"] = "PASS"
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "elapsed_seconds": report["elapsed_seconds"],
                      "binomial_programs": program_count, "binomial_actions": action_checks,
                      "chain_programs": chain_programs, "chain_actions": chain_actions,
                      "output": args.output}), flush=True)


if __name__ == "__main__":
    main()
