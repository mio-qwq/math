"""Fresh small audits of an approximation corollary and oldest-inclusive optimum."""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import random
from time import perf_counter

from constraint_solver import augmented_edges, bounds, operational_check, solve, times_to_schedule
from run_audit import all_dags


def beta(K, W, epsilon):
    q = (epsilon*K).numerator // (epsilon*K).denominator
    return max((K+q+1)//(q+1), K+1-q*W)


def oldest_feasible(n, edges, B, W, horizon):
    """Time-variable CSP with an additional oldest-every-cycle restriction.

    Oldest inclusion is equivalent to t[0]=0 and each new prefix-record
    time being at most one greater than the preceding prefix maximum.
    """
    if n == 0:
        return []
    pred, _, _, tail = bounds(n, augmented_edges(n, edges, B))
    times = [-1]*n
    used = [0]*horizon

    def visit(j, prefix_max):
        if j == n:
            return times.copy()
        lo = max([0] + [times[i]+1 for i in pred[j]])
        hi = min(horizon-1-tail[j], prefix_max+1)
        for t in range(lo, hi+1):
            if used[t] == W:
                continue
            times[j] = t
            used[t] += 1
            result = visit(j+1, max(prefix_max, t))
            if result is not None:
                return result
            used[t] -= 1
        times[j] = -1
        return None

    return visit(0, -1)


def check_oldest(schedule, n):
    done = set()
    for action in schedule:
        oldest = next(i for i in range(n) if i not in done)
        assert oldest in action
        done.update(action)
    assert done == set(range(n))


def main():
    start = perf_counter()
    corollary_checks = 0
    endpoint_examples = []
    for W in range(2, 9):
        left, right = Fraction(1, W+1), Fraction(1, W)
        for epsilon in (left, (left+right)/2, (left+99*right)/100):
            for K in range(1, 21):
                b_old, b_new = beta(K, W, epsilon), beta(K, W+1, epsilon)
                assert b_old >= (1-W*epsilon)*K+1
                assert b_new <= W+1
                corollary_checks += 1
            endpoint_examples.append({"W": W,
                                      "epsilon": [epsilon.numerator, epsilon.denominator],
                                      "K20_thresholds": [beta(20,W,epsilon), beta(20,W+1,epsilon)]})

    exhaustive = random_count = 0
    for n in range(1, 5):
        for edges in all_dags(n):
            for W in range(1, 4):
                B = W+1
                optimum, _ = solve(n, edges, B, W)
                times = oldest_feasible(n, edges, B, W, optimum)
                assert times is not None, (n, edges, B, W, optimum)
                schedule = times_to_schedule(times)
                assert operational_check(n, edges, B, W, schedule)
                check_oldest(schedule, n)
                exhaustive += 1
    rng = random.Random(2026101403)
    for _ in range(200):
        n, W = rng.randrange(5, 11), rng.randrange(1, 5)
        edges = [(i, j) for j in range(n)
                 for i in rng.sample(range(j), rng.randrange(min(2, j)+1))]
        B = W+1
        optimum, _ = solve(n, edges, B, W)
        times = oldest_feasible(n, edges, B, W, optimum)
        assert times is not None, (n, edges, B, W, optimum)
        schedule = times_to_schedule(times)
        assert operational_check(n, edges, B, W, schedule)
        check_oldest(schedule, n)
        random_count += 1
    # Negative scope control: the analogous claim is false at B=4,W=2.
    negative_edges = [(1, 3), (2, 3)]
    assert solve(4, negative_edges, 4, 2)[0] == 2
    assert oldest_feasible(4, negative_edges, 4, 2, 2) is None
    report = {"status": "PASS", "utc_finished": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": perf_counter()-start, "seed": 2026101403,
              "one_slot_corollary": {"rational_boundary_checks": corollary_checks,
                                      "W_range": [2,8], "K_range": [1,20],
                                      "epsilon_samples": endpoint_examples},
              "oldest_inclusion": {"exhaustive_instances_N1_through4": exhaustive,
                                    "exhaustive_W_range": [1,3], "random_instances": random_count,
                                    "random_N_range": [5,10], "random_W_range": [1,4],
                                    "B": "W+1", "outside_domain_negative_control": {
                                        "N":4,"B":4,"W":2,"edges":negative_edges,"optimum":2,
                                        "oldest_inclusive_two_cycle_schedule_exists": False}},
              "scope": "Small fresh checks; earlier full audits were not rerun.",
              "source_sha256": {name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("constraint_solver.py","run_audit.py","one_slot_oldest_audit.py")}}
    Path(__file__).with_name("one_slot_oldest_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":"PASS", "rational_boundary_checks":corollary_checks,
                      "oldest_exhaustive_instances":exhaustive,"oldest_random_instances":random_count,
                      "elapsed_seconds":report["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
