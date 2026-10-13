"""Independently audit the shortened-chain online lower-bound construction."""

from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
from pathlib import Path
from time import perf_counter

from constraint_solver import feasible, operational_check, solve


def main():
    start = perf_counter()
    instances = []
    programs = actions = adverse_actions = 0
    for B in range(3, 11):
        for W in range(2, B):
            L = (B - W + W - 2) // (W - 1)
            n = B + L
            assert L >= 1 and B <= W + L * (W - 1)
            common = None
            for x in range(1, B):
                programs += 1
                edges = [(x, B)] + [(j, j + 1) for j in range(B, n - 1)]
                optimum, schedule = solve(n, edges, B, W)
                assert optimum == L + 1
                # Explicit construction in the written proof.
                first = set(range(W - 1)) | {x}
                first.update(list(j for j in range(B) if j not in first)[:W-len(first)])
                remaining = sorted(set(range(B)) - first)
                explicit = [sorted(first)]
                for chain_job in range(B, n):
                    explicit.append(remaining[:W-1] + [chain_job])
                    remaining = remaining[W-1:]
                assert not remaining and operational_check(n, edges, B, W, explicit)
                optimal_actions = set()
                for size in range(W + 1):
                    for action in combinations(range(B), size):
                        actions += 1
                        times = feasible(n, edges, B, W, L+1, first_action=action)
                        if times is not None:
                            assert 0 in action and x in action
                            optimal_actions.add(action)
                        if not (0 in action and x in action):
                            adverse_actions += 1
                            assert times is None
                        if len(action) == W:
                            assert (times is not None) == (0 in action and x in action)
                            forced = next(T for T in range(L+1, n+1)
                                          if feasible(n, edges, B, W, T, first_action=action) is not None)
                            assert forced == (L+1 if 0 in action and x in action else L+2)
                common = optimal_actions if common is None else common & optimal_actions
            assert not common
            instances.append({"B": B, "W": W, "L": L, "N": n,
                              "offline_optimum": L+1, "adverse_duration_lower_bound": L+2,
                              "competitive_ratio_lower_bound": [L+2, L+1]})
    report = {"status": "PASS", "utc_finished": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": perf_counter()-start, "B_range": [3,10], "W_range": "2..B-1",
              "programs_checked": programs, "all_first_actions_checked": actions,
              "adverse_first_actions_excluded_at_optimum": adverse_actions,
              "scope": "Finite verification; general written proof audited in REVIEW.md.",
              "source_sha256": {name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("constraint_solver.py", "sharpened_chain_audit.py")},
              "instances": instances}
    Path(__file__).with_name("sharpened_chain_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in {"instances","source_sha256"}}))


if __name__ == "__main__":
    main()
