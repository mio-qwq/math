"""Independent weighted-tree check of the four-input fixed-rank-bias formulas."""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from time import perf_counter

from wider_policy_independent import full_tree


def weighted_mean(n,edges,paths,probabilities):
    pred = [set() for _ in range(n)]
    for a,b in edges:
        pred[b].add(a)
    total = expected = Fraction(0)
    for path in paths:
        done,probability = set(),Fraction(1)
        for action in path["actions"]:
            r = next(j for j in range(n) if j not in done)
            ready = [j for j in range(r,min(n,r+4)) if j not in done and pred[j] <= done]
            if len(ready) == 4:
                omitted = list(set(ready)-set(action))
                assert len(omitted) == 1 and omitted[0] != r
                probability *= probabilities[ready[1:].index(omitted[0])]
            else:
                assert set(action) == set(ready)
            done.update(action)
        total += probability
        expected += len(path["actions"])*probability
    assert total == 1
    return expected


def main():
    start = perf_counter()
    nine_edges = ((1,4),(2,4),(2,5),(5,8))
    nine_tree = full_tree(9,nine_edges,3)
    five_inputs = []
    for omitted in (1,2,3):
        edges = tuple((parent,4) for parent in (1,2,3) if parent != omitted)
        five_inputs.append((omitted,edges,full_tree(5,edges,3)))
    vectors = program_checks = 0
    for i in range(13):
        for j in range(13-i):
            p,q,r = Fraction(i,12),Fraction(j,12),Fraction(12-i-j,12)
            probabilities = (p,q,r)
            E9 = weighted_mean(9,nine_edges,nine_tree["paths"],probabilities)
            assert E9 == 4-r*r+(1-r)*p
            t = min(probabilities)
            assert E9 >= 3+4*t-2*t*t
            ratios = [E9/3]
            for omitted,edges,tree in five_inputs:
                E5 = weighted_mean(5,edges,tree["paths"],probabilities)
                assert E5 == 3-probabilities[omitted-1]
                ratios.append(E5/2)
                program_checks += 1
            assert max(ratios[1:]) == (3-t)/2
            program_checks += 1
            vectors += 1
    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"probability_vectors":vectors,
              "denominator":12,"weighted_program_tree_checks":program_checks,
              "exact_nine_job_formula":"4-r^2+(1-r)p",
              "exact_four_input_fixed_bias_value":"(13+sqrt(73))/16",
              "optimal_vector":"p=q=(11-sqrt(73))/8, r=1-2p",
              "scope":"The same conditional rank-bias vector is used at all windows and lengths. This is not a minimax value for arbitrary adaptive online policies.",
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("wider_policy_independent.py","fixed_bias_audit.py")}}
    Path(__file__).with_name("fixed_bias_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({key:report[key] for key in ("status","probability_vectors","weighted_program_tree_checks","elapsed_seconds")}))


if __name__ == "__main__":
    main()
