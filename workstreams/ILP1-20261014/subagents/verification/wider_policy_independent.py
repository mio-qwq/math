"""Reproduce the finite random probe and independently audit its later refutation."""

from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
import hashlib
from itertools import combinations
import json
from pathlib import Path
import platform
from random import Random
from time import perf_counter

from constraint_solver import operational_check, solve


def values(n, edges, W):
    """Completed-set optimum and exact uniform-younger-omission expectation."""
    B, full = W+1, (1 << n)-1
    pred = [0]*n
    for a, b in edges:
        pred[b] |= 1 << a

    @lru_cache(None)
    def rec(done):
        if done == full:
            return 0, Fraction(0)
        r = next(j for j in range(n) if not done >> j & 1)
        ready = [j for j in range(r, min(n, r+B))
                 if not done >> j & 1 and pred[j] & ~done == 0]
        actions = list(combinations(ready, min(W, len(ready))))
        tails = [(action, rec(done | sum(1 << j for j in action))) for action in actions]
        F = 1+min(tail[0] for action, tail in tails)
        kept = [tail[1] for action, tail in tails if r in action]
        E = 1+sum(kept, Fraction(0))/len(kept)
        return F, E

    return rec(0)


def sample():
    """Exactly reproduce the earlier 30,000-instance fixed-seed experiment."""
    rng = Random(2026101407)
    rows = []
    for W in (3, 4, 5):
        best, witness = Fraction(0), None
        for case in range(10000):
            n = rng.randrange(W+2, 41)
            p = rng.choice((.1, .2, .3, .4, .5, .6, .8))
            edges = []
            for j in range(n):
                parents = [i for i in range(max(0, j-W), j) if rng.random() < p]
                if len(parents) > 2:
                    parents = rng.sample(parents, 2)
                edges.extend((i, j) for i in parents)
            F, E = values(n, edges, W)
            ratio = E/F
            if ratio > best:
                best = ratio
                witness = {"N": n, "edges": edges, "F": F, "E": str(E), "ratio": str(ratio)}
        assert best == {3:Fraction(4,3), 4:Fraction(11,8), 5:Fraction(7,5)}[W]
        checked, schedule = solve(witness["N"], witness["edges"], W+1, W)
        assert checked == witness["F"]
        witness["independent_CSP_schedule"] = schedule
        rows.append({"W":W, "B":W+1, "instances":10000, "N_range":[W+2,40],
                     "maximum_indegree":2, "maximum_true_edge_gap":W, "best":witness})
    return rows


def full_tree(n, edges, W):
    B = W+1
    pred = [set() for _ in range(n)]
    for a, b in edges:
        pred[b].add(a)
    paths, observations = [], {}

    def visit(done, history, probability):
        if len(done) == n:
            assert operational_check(n, edges, B, W, history)
            paths.append((history, probability))
            return
        r = next(j for j in range(n) if j not in done)
        window = list(range(r, min(n, r+B)))
        ready = [j for j in window if j not in done and pred[j] <= done]
        key = tuple(sorted(done))
        observations[key] = {"done":list(key), "window":window, "ready":ready,
                             "visible_predecessors":{str(j):sorted(pred[j]) for j in window}}
        if len(ready) == B:
            actions = [tuple(j for j in ready if j != omitted) for omitted in ready[1:]]
        else:
            actions = [tuple(ready)]
        for action in actions:
            visit(done | set(action), history+[list(action)], probability/len(actions))

    visit(set(), [], Fraction(1))
    distribution = defaultdict(Fraction)
    branches = defaultdict(lambda:[Fraction(0), Fraction(0)])
    for history, probability in paths:
        distribution[len(history)] += probability
        branches[tuple(history[0])][0] += probability
        branches[tuple(history[0])][1] += probability*len(history)
    assert sum(distribution.values()) == 1
    return {
        "paths":[{"actions":h,"probability":str(p),"cycles":len(h)} for h,p in paths],
        "observations":list(observations.values()),
        "distribution":{str(t):str(p) for t,p in sorted(distribution.items())},
        "expected":str(sum(t*p for t,p in distribution.items())),
        "first_action_conditionals":[{"first_action":list(a), "probability":str(p),
                                      "conditional_total_time":str(e/p)} for a,(p,e) in branches.items()]}


def main():
    start = perf_counter()
    rows = sample()
    # This proposed extension of the width-two potential is already false at N=5.
    F, E = values(5, ((2,4),(3,4)), 3)
    assert (F, E) == (2, Fraction(8,3))
    failed_potential = 5+(2*3-1)*F-2*3*E
    assert failed_potential == -1
    # The theory agent subsequently found a genuine counterexample to the policy bound.
    n, W, edges = 9, 3, ((1,4),(2,4),(2,5),(5,8))
    F, schedule = solve(n, edges, W+1, W)
    direct_F, direct_E = values(n, edges, W)
    assert F == direct_F == 3 and direct_E == Fraction(37,9)
    tree = full_tree(n, edges, W)
    assert tree["expected"] == "37/9" and len(tree["paths"]) == 9
    assert tree["distribution"] == {"3":"1/9","4":"2/3","5":"2/9"}
    deletions = []
    for removed in range(1, 1 << len(edges)):
        remaining = tuple(e for bit,e in enumerate(edges) if not removed >> bit & 1)
        sub_F, sub_E = values(n, remaining, W)
        assert sub_E/sub_F <= Fraction(4,3)
        deletions.append({"removed_edge_mask":removed,"F":sub_F,"E":str(sub_E),"ratio":str(sub_E/sub_F)})
    vertex_deletions = []
    for removed in range(n):
        remaining = tuple((a-(a>removed),b-(b>removed)) for a,b in edges if a != removed and b != removed)
        sub_F, sub_E = values(n-1, remaining, W)
        assert solve(n-1, remaining, W+1, W)[0] == sub_F
        assert sub_E/sub_F <= Fraction(4,3)
        vertex_deletions.append({"removed_vertex":removed,"F":sub_F,"E":str(sub_E),"ratio":str(sub_E/sub_F)})
    report = {
        "status":"REFUTED_POLICY_CONJECTURE", "utc_finished":datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds":perf_counter()-start,"python":platform.python_version(),
        "seed":2026101407,"random_probe":rows,
        "random_probe_scope":"Finite sampling supported a conjecture later refuted; not proof of a universal bound.",
        "failed_potential":{"W":3,"B":4,"N":5,"edges":[[2,4],[3,4]],"F":2,
                            "E":"8/3","N_plus_2Wminus1_F_minus_2W_E":str(failed_potential)},
        "counterexample":{"N":n,"W":W,"B":W+1,"edges":edges,"F":F,
                          "independent_CSP_schedule":schedule,"E":str(direct_E),"ratio":str(direct_E/F),
                          "complete_policy_tree":tree,"proper_edge_deletions":deletions,
                          "vertex_deletions":vertex_deletions},
        "minimality_scope":"This reviewer checks edge-deletion minimality and all single-vertex deletions. Full N<=8 minimality uses the theory agent's separate exhaustive report, not a repeated run here.",
        "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                         for name in ("constraint_solver.py","wider_policy_independent.py")}}
    Path(__file__).with_name("wider_policy_independent_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({"status":report["status"],"random_instances":30000,"counterexample_F":F,
                      "counterexample_E":str(direct_E),"tree_paths":len(tree["paths"]),
                      "proper_edge_deletions":len(deletions),"vertex_deletions":len(vertex_deletions),
                      "elapsed_seconds":report["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
