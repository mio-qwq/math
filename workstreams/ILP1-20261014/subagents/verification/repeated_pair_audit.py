"""Independent exact audit of the barrier-separated four-job pair family."""

from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import product
import json
from math import comb
from pathlib import Path
from time import perf_counter

from constraint_solver import augmented_edges, operational_check, solve
from wider_policy_independent import full_tree, values


def repeated_pair(bits):
    edges = []
    for k, bit in enumerate(bits):
        a = 4*k
        edges.append((a+1+bit, a+3))
        if k:
            edges.extend((parent, root) for root in range(a, a+3) for parent in (a-2, a-1))
    return 4*len(bits), tuple(sorted(edges))


def explicit_optimum(bits):
    schedule = []
    for k, bit in enumerate(bits):
        a = 4*k
        chosen = a+1+bit
        other = a+2-bit
        schedule += [[a, chosen], [other, a+3]]
    return schedule


def main():
    start = perf_counter()
    programs = barrier_pairs = 0
    for q in range(0, 7):
        for bits in product((0, 1), repeat=q):
            n, edges = repeated_pair(bits)
            assert max(Counter(b for a,b in edges).values(), default=0) <= 2
            F, schedule = solve(n, edges, 3, 2)
            assert F == 2*q
            assert operational_check(n, edges, 3, 2, explicit_optimum(bits))
            direct_F, E = values(n, edges, 2)
            assert direct_F == F and E == Fraction(5*q, 2)
            augmented = set(augmented_edges(n, edges, 3))
            for k in range(1, q):
                # Every later root has every preceding block job as a direct
                # augmented predecessor. The later final job is also separated.
                for old in range(4*k-4, 4*k):
                    for new in range(4*k, 4*k+4):
                        assert (old, new) in augmented
                        barrier_pairs += 1
            for k in range(q):
                a = 4*k
                # At the clear-prefix decision, the hidden final job is unadmitted.
                window = list(range(a, min(n, a+3)))
                assert window == [a, a+1, a+2] and a+3 not in window
                visible = [(u,v) for u,v in edges if v in window]
                expected = [] if k == 0 else [(u,v) for u in (a-2,a-1) for v in window]
                assert set(visible) == set(expected)
            programs += 1

    # The complete policy tree on one six-block input has one fair choice per
    # block. Its exact duration distribution must be 2q+Binomial(q,1/2).
    bits = (0,1,0,1,1,0)
    n, edges = repeated_pair(bits)
    tree = full_tree(n, edges, 2)
    q = len(bits)
    expected_distribution = {str(2*q+k):str(Fraction(comb(q,k), 2**q)) for k in range(q+1)}
    assert tree["distribution"] == expected_distribution
    assert len(tree["paths"]) == 2**q and tree["expected"] == str(Fraction(5*q,2))
    for observation in tree["observations"]:
        if len(observation["ready"]) == 3:
            done = observation["done"]
            a = len(done)
            assert a % 4 == 0 and done == list(range(a))
            assert observation["window"] == observation["ready"] == [a,a+1,a+2]
    report = {
        "status":"PASS", "utc_finished":datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds":perf_counter()-start, "q_range":[0,6],"all_bit_programs":programs,
        "direct_cross_block_augmented_edges_checked":barrier_pairs,
        "optimum":"2q", "uniform_policy_expected":"5q/2",
        "policy_tree":{"bits":bits,"leaves":len(tree["paths"]),"distribution":tree["distribution"],
                       "expected":tree["expected"],"all_random_decisions_have_hidden_final_job_unadmitted":True},
        "scope":"Finite checks support the separate all-q proof; no general online policy is simulated here.",
        "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                         for name in ("constraint_solver.py","wider_policy_independent.py","repeated_pair_audit.py")}}
    Path(__file__).with_name("repeated_pair_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({key:report[key] for key in ("status","all_bit_programs","direct_cross_block_augmented_edges_checked","elapsed_seconds")}))


if __name__ == "__main__":
    main()
