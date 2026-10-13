"""Independent completion-corridor solver and exact feasibility/bound audits."""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
from random import Random
from time import perf_counter

from constraint_solver import feasible, operational_check


def layer_candidates(n,W,c,H,t):
    slack = W*H-n
    left, right = max(0,t*W-c-slack), min(n,t*W+c)
    assert 0 <= left <= right <= n
    prefix = (1 << left)-1
    lower,upper = max(0,t*W-slack),min(n,t*W)
    return [prefix | (bits << left) for bits in range(1 << (right-left))
            if lower <= left+bits.bit_count() <= upper]


def corridor_schedule(n,edges,W,c,H):
    if W < 1 or c < 0 or H < 0:
        raise ValueError("requires W>=1, c>=0, H>=0")
    if W*H < n:
        return None
    B,full = W+c,(1 << n)-1
    pred = [0]*n
    for a,b in edges:
        assert 0 <= a < b < n
        pred[b] |= 1 << a
    reachable = {0:[]}
    for t in range(H):
        candidates = layer_candidates(n,W,c,H,t+1)
        following = {}
        for done,history in reachable.items():
            oldest = next((j for j in range(n) if not done >> j & 1),n)
            window_mask = ((1 << min(n,oldest+B))-1) ^ ((1 << oldest)-1)
            for target in candidates:
                if done & ~target:
                    continue
                added = target ^ done
                if added.bit_count() > W or added & ~window_mask:
                    continue
                action = [j for j in range(n) if added >> j & 1]
                if any(pred[j] & ~done for j in action):
                    continue
                if target not in following:
                    following[target] = history+[action]
        reachable = following
    result = reachable.get(full)
    if result is not None:
        assert operational_check(n,edges,B,W,result)
    return result


def all_graphs(n):
    pairs = list(combinations(range(n),2))
    for mask in range(1 << len(pairs)):
        yield tuple(edge for bit,edge in enumerate(pairs) if mask >> bit & 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary-module", type=Path)
    args = parser.parse_args()
    start = perf_counter()
    comparisons = random_cases = assignments = boundaries = 0
    primary = None
    primary_hash = None
    primary_checks = primary_replays = 0
    if args.primary_module:
        primary_hash = hashlib.sha256(args.primary_module.read_bytes()).hexdigest()
        spec = importlib.util.spec_from_file_location("reviewed_primary_corridor", args.primary_module)
        primary = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(primary)

    def check_primary(n,edges,B,W,H,expected):
        nonlocal primary_checks,primary_replays
        if primary is None:
            return
        result = primary.solve(n,edges,B,W,H)
        assert result["feasible"] == expected, (n,edges,B,W,H,result)
        primary_checks += 1
        if expected:
            assert len(result["schedule"]) <= H
            assert operational_check(n,edges,B,W,result["schedule"])
            primary_replays += 1
        else:
            assert result["schedule"] is None
        if result["reason"] == "exact corridor reachability":
            for t,count in enumerate(result["candidate_sizes"]):
                independent_count = len(layer_candidates(n,result["W"],result["window_excess"],H,t))
                assert count == independent_count
                assert count <= result["states_per_layer_bound"]
    for n in range(0,5):
        for edges in all_graphs(n):
            for W in range(1,5):
                for c in range(3):
                    for H in range(0,n+1):
                        expected = feasible(n,edges,W+c,W,H)
                        obtained = corridor_schedule(n,edges,W,c,H)
                        assert (expected is not None) == (obtained is not None), (n,edges,W,c,H)
                        check_primary(n,edges,W+c,W,H,expected is not None)
                        comparisons += 1
    # These checks use direct ROB replay of every time assignment, independently
    # of corridor generation or augmented-precedence validity.
    for n in range(1,4):
        for edges in all_graphs(n):
            for W in range(1,4):
                for c in range(3):
                    for H in range(1,5):
                        slack = W*H-n
                        if slack < 0:
                            continue
                        for times in product(range(H),repeat=n):
                            schedule = [[j for j,time in enumerate(times) if time == t] for t in range(H)]
                            if not operational_check(n,edges,W+c,W,schedule):
                                continue
                            assignments += 1
                            for t in range(H+1):
                                done = {j for j,time in enumerate(times) if time < t}
                                r = next((j for j in range(n) if j not in done),n)
                                d,holes = t*W-len(done),len(done)-r
                                assert 0 <= d <= slack
                                assert r >= t*W-c-slack
                                assert all(j < t*W+c for j in done)
                                if t < H:
                                    delta = W-len(schedule[t])
                                    assert holes <= c+delta and d+delta <= slack
                                boundaries += 1
    rng = Random(2026101409)
    for _ in range(300):
        W,c,H,S = rng.randrange(1,9),rng.randrange(4),rng.randrange(1,7),rng.randrange(4)
        n = W*H-S
        if n < 0:
            continue
        edges = tuple((parent,child) for child in range(n)
                      for parent in rng.sample(range(child),rng.randrange(min(2,child)+1)))
        expected = feasible(n,edges,W+c,W,H)
        obtained = corridor_schedule(n,edges,W,c,H)
        assert (expected is not None) == (obtained is not None), (n,edges,W,c,H)
        check_primary(n,edges,W+c,W,H,expected is not None)
        random_cases += 1
    # Positive cases preserve substantial issue width with constant c+S.
    positive = 0
    for W in range(2,13):
        for c in (0,1,2):
            for S in (0,1,2):
                H,n = 4,4*W-S
                assert corridor_schedule(n,[],W,c,H) is not None
                check_primary(n,[],W+c,W,H,True)
                positive += 1
    boundary_cases = [(0,[],9,17,0),(0,[],9,17,5),(1,[],1,7,0),
                      (1,[],1,7,1),(1,[],9,17,3),(5,[(0,1)],4,3,2),
                      (6,[(0,1)],4,3,2),(6,[(0,1)],4,3,3)]
    for n,edges in [(4,[]),(4,[(0,1),(1,2),(2,3)])]:
        for B,W in [(1,7),(2,7),(7,2),(7,7),(2,1)]:
            for H in range(6):
                boundary_cases.append((n,edges,B,W,H))
    for n,edges,B,W,H in boundary_cases:
        expected = feasible(n,edges,B,W,H)
        check_primary(n,edges,B,W,H,expected is not None)
    assert feasible(5,[(0,1)],4,3,2) is not None
    assert feasible(6,[(0,1)],4,3,2) is None
    if primary is not None:
        assert primary_hash == hashlib.sha256(args.primary_module.read_bytes()).hexdigest()
    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"all_small_CSP_comparisons":comparisons,
              "small_N_range":[0,4],"small_W_range":[1,4],"small_c_range":[0,2],
              "direct_ROB_legal_time_assignments":assignments,"boundary_inequality_checks":boundaries,
              "assignment_N_range":[1,3],"assignment_H_range":[1,4],
              "seed":2026101409,"random_CSP_comparisons":random_cases,
              "random_W_range":[1,8],"random_c_range":[0,3],"random_S_range":[0,3],
              "random_H_range":[1,6],"independent_positive_cases":positive,
              "additional_resource_boundary_cases":len(boundary_cases),
              "primary_comparisons":primary_checks,"primary_schedule_replays":primary_replays,
              "primary_source_sha256":primary_hash,
              "scope":"The independent solver enumerates pairs of narrow-strip candidates, never all ready subsets. It deliberately has no H>=N shortcut so the full small range is checked.",
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                               for name in ("constraint_solver.py","corridor_audit.py")}}
    Path(__file__).with_name("corridor_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({key:report[key] for key in ("status","all_small_CSP_comparisons","direct_ROB_legal_time_assignments","boundary_inequality_checks","random_CSP_comparisons","independent_positive_cases","primary_comparisons","primary_schedule_replays","elapsed_seconds")}))


if __name__ == "__main__":
    main()
