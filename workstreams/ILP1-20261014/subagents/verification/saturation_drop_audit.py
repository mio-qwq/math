"""Independent exact checks of two structural resource-saturation families."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from time import perf_counter

from constraint_solver import feasible, operational_check, solve


def main():
    start = perf_counter()
    depth_two = []
    depth_two_checks = 0
    for m in range(2, 11):
        for r in range(1, m//2+1):
            n = 2*m
            roots = list(range(r, r+m))
            parents = [roots[2*k:2*k+2] for k in range(r)]
            parents += [[j] for j in roots[2*r:]]
            edges = [(i, m+r+k) for k, group in enumerate(parents) for i in group]
            assert len(parents) == m-r
            table = {}
            for B in range(1, n+1):
                for W in range(1, n+1):
                    depth_two_checks += 1
                    possible = feasible(n, edges, B, W, 2) is not None
                    expected = B >= m+r and W >= m+min(r, 2*m-B)
                    assert possible == expected, (m, r, B, W, edges)
                    table[B, W] = possible
            w_sat = []
            for B in range(m+r, n+1):
                actual = next(W for W in range(1, B+1) if table[B, W])
                assert actual == m+min(r, 2*m-B)
                assert solve(n, edges, B, actual)[0] == 2
                w_sat.append([B, actual])
            b_sat = []
            for W in range(m, n+1):
                actual = next(B for B in range(1, n+1) if table[B, W])
                expected = 2*m-(W-m) if W < m+r else m+r
                assert actual == expected
                assert solve(n, edges, actual, W)[0] == 2
                b_sat.append([W, actual])
            depth_two.append({"m": m, "r": r, "N": n, "edges": edges,
                              "W_sat_by_B_for_B_ge_m_plus_r": w_sat,
                              "B_sat_by_W_for_W_ge_m": b_sat})

    layered = []
    layered_checks = 0
    for K in range(2, 11):
        n = 2*K
        layers = [[2*k+1, 2*k+2] for k in range(K-1)] + [[n-1]]
        edges = [(i, j) for left, right in zip(layers, layers[1:]) for i in left for j in right]
        schedule_w2 = layers[:-1] + [[0, n-1]]
        schedule_w3 = [[0]+layers[0]] + layers[1:]
        assert operational_check(n, edges, n, 2, schedule_w2)
        assert operational_check(n, edges, 3, 3, schedule_w3)
        assert solve(n, edges, n, 2)[0] == K
        assert solve(n, edges, 3, 3)[0] == K
        horizons = []
        for B in range(1, n+1):
            for W in (2, 3):
                layered_checks += 1
                times = feasible(n, edges, B, W, K)
                expected = B == n if W == 2 else B >= 3
                assert (times is not None) == expected, (K, B, W, times)
                horizons.append([B, W, times is not None])
        layered.append({"K": K, "N": n, "edges": edges,
                        "unrestricted_optimum_W2_and_W3": K,
                        "B_sat_W2": n, "B_sat_W3": 3,
                        "witness_W2": schedule_w2, "witness_W3": schedule_w3,
                        "all_horizon_K_decisions": horizons})
    report = {"status": "PASS", "utc_finished": datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds": perf_counter()-start,
              "scope": "Exact finite time-assignment search, independent of primary operational DP.",
              "source_sha256": {name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("constraint_solver.py", "saturation_drop_audit.py")},
              "depth_two_family": {"m_range": [2,10], "r_range": "1..floor(m/2)",
                                    "programs": len(depth_two), "horizon_two_resource_checks": depth_two_checks,
                                    "instances": depth_two},
              "layered_family": {"K_range": [2,10], "programs": len(layered),
                                  "horizon_K_resource_checks": layered_checks, "instances": layered}}
    Path(__file__).with_name("saturation_drop_results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "elapsed_seconds": report["elapsed_seconds"],
                      "depth_two_programs": len(depth_two), "depth_two_checks": depth_two_checks,
                      "layered_programs": len(layered), "layered_checks": layered_checks}))


if __name__ == "__main__":
    main()
