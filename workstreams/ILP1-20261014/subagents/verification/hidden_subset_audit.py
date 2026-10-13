"""Fresh checks of hidden-subset instances beyond the B=W+1 family."""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
from time import perf_counter

from constraint_solver import feasible, operational_check, solve


def main():
    start = perf_counter()
    parameters = [(5, 7, 2), (5, 8, 2), (6, 8, 2), (5, 7, 3)]
    programs = first_actions = replays = 0
    cases = []
    for W, B, m in parameters:
        n = B+m
        subsets = list(combinations(range(m, B), W-m))
        for hidden in subsets:
            edges = tuple((root, B+k % m) for k, root in enumerate(hidden))
            assert solve(n, edges, B, W)[0] == 2
            unique = set(range(m)) | set(hidden)
            for first in combinations(range(B), W):
                assert (feasible(n, edges, B, W, 2, first_action=first) is not None) == (set(first) == unique)
                first_actions += 1
            # A two-cycle schedule must use W distinct roots on its first action;
            # one representative underfull action is a negative boundary control.
            assert feasible(n, edges, B, W, 2, first_action=tuple(sorted(unique)[:-1])) is None
            first_actions += 1
            total = 0
            for guess in subsets:
                first = sorted(set(range(m)) | set(guess))
                roots_left = sorted(set(range(B)) - set(first))
                ready_sinks = [sink for sink in range(B, n)
                               if all(root in first for root, target in edges if target == sink)]
                last = [sink for sink in range(B, n) if sink not in ready_sinks]
                schedule = [first, roots_left+ready_sinks] + ([last] if last else [])
                assert operational_check(n, edges, B, W, schedule)
                assert len(schedule) == (2 if guess == hidden else 3)
                total += len(schedule)
                replays += 1
            ratio = Fraction(total, 2*len(subsets))
            assert ratio == Fraction(3,2)-Fraction(1,2*len(subsets))
            programs += 1
        cases.append({"W":W,"B":B,"m":m,"N":n,"number_hidden_subsets":len(subsets),
                      "maximum_indegree": (W-1)//m, "exact_family_ratio":str(ratio)})
    report = {"status":"PASS", "utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"programs":programs,
              "first_action_checks":first_actions,"policy_replays":replays,"cases":cases,
              "scope":"Selected new B>W+1 parameter cases; prior full audits were not rerun.",
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                               for name in ("constraint_solver.py","hidden_subset_audit.py")}}
    Path(__file__).with_name("hidden_subset_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({key:report[key] for key in ("status","programs","first_action_checks","policy_replays","elapsed_seconds")}))


if __name__ == "__main__":
    main()
