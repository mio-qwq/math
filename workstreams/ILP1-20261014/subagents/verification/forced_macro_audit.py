"""Independent set-based forced-segment exact schedulers and CSP cross-check.

This deliberately simple verifier scans ready sets rather than sharing the
primary/theory implementation's transition code or optimizing its complexity.
"""

import argparse
from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import importlib.util
from itertools import combinations
import json
from math import comb
from pathlib import Path
from random import Random
from time import perf_counter

from constraint_solver import operational_check, solve, validate_input


def state_helpers(n, edges, B, W):
    edges = validate_input(n, edges, B, W)
    pred = [set() for _ in range(n)]
    for a,b in edges:
        pred[b].add(a)

    def retired(done):
        return next((j for j in range(n) if j not in done),n)

    def ready(done):
        r = retired(done)
        return tuple(j for j in range(r,min(n,r+B))
                     if j not in done and pred[j] <= done)

    def advance(done, action, stop):
        assert set(action) <= set(ready(done))
        assert len(action) == min(W,len(ready(done))) and action
        state = set(done)
        state.update(action)
        macro = [tuple(action)]
        while len(state) < n and not stop(state):
            enabled = ready(state)
            assert 1 <= len(enabled) <= W
            state.update(enabled)
            macro.append(enabled)
        assert len(macro) <= n-len(done)
        return frozenset(state),tuple(macro)

    return retired,ready,advance


def clear_prefix_solve(n, edges, W):
    """Bottom-up all-N exact solver for B=W+1 using only clear-prefix nodes."""
    B = W+1
    retired,ready,advance = state_helpers(n,edges,B,W)
    best = [None]*(n+1)
    best[n] = (0,())
    evaluated = longest = 0
    for i in reversed(range(n)):
        done = frozenset(range(i))
        enabled = ready(done)
        actions = combinations(enabled,min(W,len(enabled)))
        choice = None
        for action in actions:
            target,macro = advance(done,action,lambda state:len(state)==retired(state))
            j = len(target)
            assert j > i and target == frozenset(range(j))
            cost = len(macro)+best[j][0]
            if choice is None or cost < choice[0]:
                choice = (cost,macro+best[j][1])
            evaluated += 1
            longest = max(longest,len(macro))
        assert choice is not None
        best[i] = choice
    duration,schedule = best[0]
    assert operational_check(n,edges,B,W,schedule)
    return duration,schedule,{"clear_nodes":n+1,"macro_actions":evaluated,
                              "longest_macro":longest,
                              "prefix_values":tuple(result[0] for result in best)}


def excess_solve(n, edges, B, W):
    """Exact reachable cut-state DP with forced segments when h>=B-W."""
    validate_input(n,edges,B,W)
    if n == 0:
        return 0,(),{"cut_nodes":0,"branch_nodes":0,"macro_actions":0,
                      "state_bound":0,"action_bound":1,"longest_macro":0}
    B,W = min(B,n),min(W,B,n)
    c = B-W
    retired,ready,advance = state_helpers(n,edges,B,W)
    cut_nodes = branch_nodes = macro_actions = longest = 0
    state_bound = n*sum(comb(B-1,h) for h in range(c)) if c else 0
    action_bound = comb(B,c)

    @lru_cache(None)
    def best(done):
        nonlocal cut_nodes,branch_nodes,macro_actions,longest
        if len(done) == n:
            return 0,()
        r = retired(done)
        assert len(done)-r < c
        assert all(j < r+B for j in done)
        cut_nodes += 1
        enabled = ready(done)
        assert enabled
        branch_nodes += len(enabled) > W
        actions = tuple(combinations(enabled,min(W,len(enabled))))
        assert len(actions) <= action_bound
        choice = None
        for action in actions:
            target,macro = advance(done,action,lambda state:len(state)-retired(state)<c)
            cost,tail = best(target)
            cost += len(macro)
            if choice is None or cost < choice[0]:
                choice = cost,macro+tail
            macro_actions += 1
            longest = max(longest,len(macro))
        return choice

    if c == 0:
        enabled = ready(frozenset())
        _,schedule = advance(frozenset(),enabled,lambda state:False)
        duration = len(schedule)
        longest = duration
    else:
        duration,schedule = best(frozenset())
    assert cut_nodes <= state_bound
    assert operational_check(n,edges,B,W,schedule)
    return duration,schedule,{"cut_nodes":cut_nodes,"branch_nodes":branch_nodes,
                              "macro_actions":macro_actions,"state_bound":state_bound,
                              "action_bound":action_bound,"longest_macro":longest}


def all_graphs(n):
    pairs = tuple(combinations(range(n),2))
    for mask in range(1 << len(pairs)):
        yield tuple(pair for bit,pair in enumerate(pairs) if mask >> bit & 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary-module",type=Path)
    args = parser.parse_args()
    start = perf_counter()
    prefix_checks = excess_checks = random_checks = normalization_checks = 0
    primary_checks = primary_prefix_values = 0
    primary = primary_hash = None
    if args.primary_module:
        primary_hash = hashlib.sha256(args.primary_module.read_bytes()).hexdigest()
        spec = importlib.util.spec_from_file_location("reviewed_forced_segment",args.primary_module)
        primary = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(primary)
    longest = 0
    def check(n,edges,W,c):
        nonlocal prefix_checks,excess_checks,longest,primary_checks,primary_prefix_values
        expected,_ = solve(n,edges,W+c,W)
        obtained,schedule,stats = excess_solve(n,edges,W+c,W)
        assert obtained == expected, (n,edges,W,c,expected,obtained)
        assert len(schedule) == obtained
        longest = max(longest,stats["longest_macro"])
        excess_checks += 1
        if c == 1:
            prefix_value,prefix_schedule,prefix_stats = clear_prefix_solve(n,edges,W)
            assert prefix_value == expected, (n,edges,W,expected,prefix_value)
            assert len(prefix_schedule) == expected
            assert prefix_stats["macro_actions"] <= n*(W+1)
            longest = max(longest,prefix_stats["longest_macro"])
            prefix_checks += 1
            if primary is not None:
                result = primary.solve_edges(n,edges,W)
                assert result["cycles"] == expected
                assert operational_check(n,edges,W+1,W,result["schedule"])
                assert result["prefix_values"] == prefix_stats["prefix_values"]
                primary_checks += 1
                primary_prefix_values += n+1

    # Complete arbitrary-fan-in graph range, not merely binary-input graphs.
    for n in range(6):
        for edges in all_graphs(n):
            for W in range(1,5):
                for c in range(3):
                    check(n,edges,W,c)
    small_prefix,small_excess = prefix_checks,excess_checks
    rng = Random(2026101410)
    for _ in range(180):
        n,W,c = rng.randrange(6,13),rng.randrange(1,9),rng.randrange(1,4)
        edges = tuple((a,b) for b in range(n)
                      for a in rng.sample(range(b),rng.randrange(min(2,b)+1)))
        check(n,edges,W,c)
        random_checks += 1
    for n,edges in ((1,()),(5,()),(5,((0,1),(1,2),(2,3),(3,4)))):
        for B,W in ((1,7),(2,7),(3,9),(9,2),(9,9)):
            expected,_ = solve(n,edges,B,W)
            obtained,_,_ = excess_solve(n,edges,B,W)
            assert obtained == expected
            normalization_checks += 1

    if primary is not None:
        assert primary_hash == hashlib.sha256(args.primary_module.read_bytes()).hexdigest()

    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"all_DAG_N_range":[0,5],
              "all_DAG_W_range":[1,4],"all_DAG_c_range":[0,2],
              "all_DAG_prefix_CSP_comparisons":small_prefix,
              "all_DAG_excess_CSP_comparisons":small_excess,
              "random_seed":2026101410,"random_indegree_at_most":2,
              "random_N_range":[6,12],"random_W_range":[1,8],"random_c_range":[1,3],
              "random_CSP_comparisons":random_checks,
              "resource_normalization_comparisons":normalization_checks,
              "total_prefix_CSP_comparisons":prefix_checks,
              "total_excess_CSP_comparisons":excess_checks,
              "primary_CSP_comparisons_and_replays":primary_checks,
              "primary_prefix_value_comparisons":primary_prefix_values,
              "primary_source_sha256":primary_hash,
              "longest_observed_forced_macro":longest,
              "scope":"Independent set-based prefix and excess macro algorithms; all returned schedules directly ROB-replayed. Optional primary import is used only for cross-check, never in the independent solvers. These finite checks do not prove the general theorem.",
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                               for name in ("constraint_solver.py","forced_macro_audit.py")}}
    Path(__file__).with_name("forced_macro_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
