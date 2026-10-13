"""Independent exact verification: a serial prefix followed by independent jobs."""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from time import perf_counter

from constraint_solver import operational_check, solve


def ceildiv(a, b):
    return (a+b-1)//b


def explicit_schedule(K, B, W):
    if W == 1:
        return [[j] for j in range(2*K)]
    schedule = [[j] for j in range(K)]
    if B >= K+1:
        for j in range(K):
            schedule[j].append(K+j)
        return schedule
    for j in range(B-1):
        schedule[K+1-B+j].append(K+j)
    remaining = list(range(K+B-1, 2*K))
    capacity = min(B, W)
    schedule += [remaining[k:k+capacity] for k in range(0, len(remaining), capacity)]
    return schedule


def main():
    started = perf_counter()
    cases = approximation_checks = 0
    instances = []
    for K in range(1, 11):
        n = 2*K
        edges = [(j, j+1) for j in range(K-1)]
        values = {}
        for B in range(1, n+3):
            for W in range(1, n+3):
                expected = n if W == 1 else K + ceildiv(max(0, K-B+1), min(B, W))
                optimum, schedule = solve(n, edges, B, W)
                assert optimum == expected, (K, B, W, optimum, expected)
                witness = explicit_schedule(K, B, W)
                assert len(witness) == expected
                assert operational_check(n, edges, B, W, witness)
                values[B, W] = optimum
                cases += 1
        approximation = []
        for W in range(2, n+3):
            for q in range(K+3):
                # Rational epsilon=q/K exercises every possible integer slack
                # regime through and beyond the B=1 saturation point.
                epsilon = Fraction(q, K)
                actual = next(B for B in range(1, n+1) if values[B,W] <= K+q)
                predicted = max(ceildiv(K+1, q+1), K+1-q*W)
                assert actual == predicted, (K, W, q, actual, predicted)
                if W == 2:
                    specialized = 1 if q >= K else max(2, K+1-2*q)
                    assert actual == specialized
                approximation_checks += 1
                approximation.append({"W": W, "q": q,
                                      "epsilon": [epsilon.numerator, epsilon.denominator],
                                      "B_epsilon": actual})
        instances.append({"K": K, "N": n, "edges": edges,
                          "B_range": [1,n+2], "W_range": [1,n+2],
                          "approximation_thresholds": approximation})
    report = {"status": "PASS", "utc_finished": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": perf_counter()-started, "K_range": [1,10],
              "exact_optimum_and_replay_cases": cases,
              "approximation_threshold_checks": approximation_checks,
              "boundary_cases": ["K=1", "B=1", "B>N", "W=1", "W>B", "epsilon=0", "epsilon>=1"],
              "scope": "Finite exact time-assignment search and direct ROB replay; no universal Lean claim.",
              "source_sha256": {name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("constraint_solver.py", "approximate_saturation_audit.py")},
              "instances": instances}
    Path(__file__).with_name("approximate_saturation_results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in {"instances","source_sha256"}}))


if __name__ == "__main__":
    main()
