"""Independent exact audit of the B=3,W=2 randomized-potential proof.

F is obtained from the time-variable CSP. E is obtained by direct ROB
completed-set replay of the policy, not by the scalar recurrence under review.
The finite checks support the separate arbitrary-size proof review.
"""

from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import platform
from time import perf_counter

from constraint_solver import solve


@lru_cache(None)
def optimum(n, edges):
    return solve(n, edges, 3, 2)[0]


def direct_policy_values(n, edges):
    """Direct eager-ROB expectation for every clear-prefix initial state."""
    pred = [0] * n
    for a, b in edges:
        pred[b] |= 1 << a
    full = (1 << n) - 1

    @lru_cache(None)
    def expected(done):
        if done == full:
            return Fraction(0)
        oldest = next(j for j in range(n) if not done >> j & 1)
        ready = [j for j in range(oldest, min(n, oldest + 3))
                 if not done >> j & 1 and pred[j] & ~done == 0]
        assert ready[0] == oldest
        if len(ready) == 3:
            actions = [(oldest, ready[1]), (oldest, ready[2])]
        else:
            actions = [tuple(ready)]
        tails = [expected(done | sum(1 << j for j in action))
                 for action in actions]
        return 1 + sum(tails, Fraction(0)) / len(tails)

    return [expected((1 << i) - 1) for i in range(n + 1)]


def effective_graphs(n):
    pairs = [(j - gap, j) for j in range(n) for gap in (1, 2) if j >= gap]
    for mask in range(1 << len(pairs)):
        yield tuple(sorted(edge for bit, edge in enumerate(pairs) if mask >> bit & 1))


def rational(value):
    return [value.numerator, value.denominator]


def main():
    start = perf_counter()
    counts, witnesses = Counter(), {}
    max_ratio = Fraction(0)
    for n in range(0, 7):
        for edges in effective_graphs(n):
            edge_set = set(edges)
            F = [optimum(n-i, tuple((a-i, b-i) for a, b in edges if a >= i))
                 for i in range(n+1)] + [0]*4
            E = direct_policy_values(n, edges) + [Fraction(0)]*4
            K = [3*F[i] + max(0, n-i) - 4*E[i] for i in range(n+5)]
            counts["graphs_including_empty"] += 1
            assert all(k >= 0 for k in K), (n, edges, "negative K", K)
            if n:
                max_ratio = max(max_ratio, E[0]/F[0])
            for i in range(n):
                counts["nonempty_suffixes"] += 1
                assert 0 <= F[i]-F[i+1] <= 1
                if F[i] == F[i+1]:
                    counts["adjacent_equal_value_checks"] += 1
                    assert K[i]+K[i+1] >= 1
                b_ready = i+1 < n and (i, i+1) not in edge_set
                c_ready = (i+2 < n and (i, i+2) not in edge_set
                           and (i+1, i+2) not in edge_set)
                q = i+4 if i+3 < n and (i+1, i+3) not in edge_set else i+3
                if b_ready and c_ready:
                    p, ell = i+2, q-i
                    x = F[p]-F[q]
                    assert F[i] == min(1+F[p], 2+F[q])
                    assert E[i] == (3+E[p]+E[q])/2
                    if ell == 3:
                        assert x in (0, 1)
                        increment = Fraction(-1, 2) if x == 0 else Fraction(1)
                    else:
                        assert x in (0, 1, 2)
                        increment = Fraction(3, 2) if x == 1 else Fraction(0)
                    assert K[i] == (K[p]+K[q])/2 + increment
                    key = f"random_length_{ell}_difference_{x}"
                    if ell == 4 and x == 0:
                        key += "_cd_edge_" + str(int((i+2, i+3) in edge_set))
                    counts[key] += 1
                    if key not in witnesses:
                        witnesses[key] = {
                            "N": n, "edges": edges, "index": i,
                            "F": F[:n+1], "E": list(map(rational, E[:n+1])),
                            "K": list(map(rational, K[:n+1]))}
                    if ell == 3 and x == 0:
                        assert i+3 < n and (i+1, i+3) in edge_set
                        assert F[p] == F[q] and K[p]+K[q] >= 1
                        assert K[i+1] == 1+K[i+3]
                    if ell == 4 and x == 2:
                        assert (i+2, i+3) in edge_set
                        assert K[i+1] == 1+K[i+3]
                    if ell == 4 and x == 0:
                        if (i+2, i+3) in edge_set:
                            assert K[i+1] == 1+K[i+3]
                        else:
                            # The delicate local implication of the written proof.
                            assert i+5 < n
                            assert (i+2, i+4) not in edge_set
                            assert (i+3, i+4) not in edge_set
                            assert (i+3, i+5) not in edge_set
                            assert F[i+4]-F[i+5] == F[i+5]-F[i+6] == 1
                            assert F[i+3] == F[i+4]
                            assert K[i+1] == (K[i+3]+K[i+5])/2 + Fraction(3, 2)
                else:
                    ell, cost = (q-i, 2) if c_ready else ((2, 1) if b_ready else (1, 1))
                    assert F[i] == cost+F[i+ell]
                    assert E[i] == cost+E[i+ell]
                    assert K[i] == ell-cost+K[i+ell]
                    counts[f"forced_length_{ell}_cost_{cost}"] += 1

    required = {"random_length_3_difference_0", "random_length_3_difference_1",
                "random_length_4_difference_0_cd_edge_0",
                "random_length_4_difference_0_cd_edge_1",
                "random_length_4_difference_1", "random_length_4_difference_2"}
    assert required <= witnesses.keys(), "not all proof classifications were exercised"
    assert max_ratio == Fraction(5, 4)
    # Boundary guard: the adjacent-equality invariant deliberately excludes empty tails.
    assert not (Fraction(0)+Fraction(0) >= 1)
    pair = []
    for hidden in (1, 2):
        edges = ((hidden, 3),)
        F, E = optimum(4, edges), direct_policy_values(4, edges)[0]
        assert F == 2 and E == Fraction(5, 2)
        pair.append({"N": 4, "edges": edges, "F": F, "E": rational(E)})
    report = {
        "status": "PASS", "utc_finished": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": perf_counter()-start, "python": platform.python_version(),
        "scope": "All gap-one/gap-two graphs through N=6, including empty; no random sampling.",
        "method": "Time-variable CSP for each suffix optimum; independent direct ROB policy expectation.",
        "counts": dict(counts), "distinct_CSP_inputs": optimum.cache_info().misses,
        "maximum_expected_ratio": rational(max_ratio), "first_case_witnesses": witnesses,
        "lower_bound_pair": pair,
        "source_sha256": {name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                          for name in ("constraint_solver.py", "randomized_bound_audit.py")}}
    Path(__file__).with_name("randomized_bound_results.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps({"status": "PASS", "counts": dict(counts),
                      "distinct_CSP_inputs": report["distinct_CSP_inputs"],
                      "elapsed_seconds": report["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
