"""Independent chunk-policy and projected-global-schedule verification."""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
from random import Random
from time import perf_counter

from constraint_solver import operational_check, solve


def chunk_schedule(n,edges,B,W,L):
    size = B+L
    result = []
    for start in range(0,n,size):
        end = min(n,start+size)
        local_edges = tuple((u-start,v-start) for u,v in edges if start <= u < v < end)
        _,schedule = solve(end-start,local_edges,B,W)
        result.extend(tuple(start+j for j in action) for action in schedule)
    return result


def check(n,edges,B,W,L,global_result=None):
    optimum,global_schedule = global_result or solve(n,edges,B,W)
    size = B+L
    cuts = tuple(range(size,n,size))
    chunks = chunk_schedule(n,edges,B,W,L)
    assert operational_check(n,edges,B,W,chunks)
    assert len(chunks) <= optimum+(B-1)*len(cuts)
    if n:
        assert len(cuts) == (n-1)//size
        assert Fraction(len(chunks),optimum) <= 1+Fraction(W*(B-1),size)
        assert Fraction(len(chunks),optimum) <= 1+Fraction(min(W,B)*(B-1),size)
    else:
        assert not cuts and not chunks and optimum == 0
    projected_cycles = projections = 0
    for start in range(0,n,size):
        end = min(n,start+size)
        local_edges = tuple((u-start,v-start) for u,v in edges if start <= u < v < end)
        local_schedule = [tuple(j-start for j in action if start <= j < end)
                          for action in global_schedule]
        local_schedule = [action for action in local_schedule if action]
        assert operational_check(end-start,local_edges,B,W,local_schedule)
        projected_cycles += len(local_schedule)
        projections += 1
    crossing = 0
    for cut in cuts:
        charged = []
        for action in global_schedule:
            left,right = [j for j in action if j < cut],[j for j in action if j >= cut]
            if left and right:
                assert all(cut-B+1 <= j < cut for j in left)
                charged.append(min(left))
        assert len(charged) == len(set(charged)) <= B-1
        crossing += len(charged)
    for action in global_schedule:
        assert len(set(j//size for j in action)) <= 2
    assert projected_cycles <= optimum+crossing <= optimum+(B-1)*len(cuts)
    assert len(chunks) <= projected_cycles
    return projections,len(cuts),crossing


def all_graphs(n):
    pairs = tuple(combinations(range(n),2))
    for mask in range(1 << len(pairs)):
        yield tuple(pair for bit,pair in enumerate(pairs) if mask >> bit & 1)


def main():
    start = perf_counter()
    cases = global_solves = projection_checks = cut_checks = crossing_cycles = 0
    for n in range(5):
        for edges in all_graphs(n):
            for B in range(1,5):
                for W in range(1,5):
                    result = solve(n,edges,B,W)
                    global_solves += 1
                    for L in range(4):
                        p,c,x = check(n,edges,B,W,L,result)
                        cases += 1
                        projection_checks += p
                        cut_checks += c
                        crossing_cycles += x
    small_cases = cases
    rng = Random(2026101412)
    for _ in range(100):
        n,B,W,L = rng.randrange(6,15),rng.randrange(1,7),rng.randrange(1,9),rng.randrange(7)
        edges = tuple((u,v) for v in range(n)
                      for u in rng.sample(range(v),rng.randrange(min(2,v)+1)))
        p,c,x = check(n,edges,B,W,L)
        cases += 1
        global_solves += 1
        projection_checks += p
        cut_checks += c
        crossing_cycles += x
    for _ in range(60):
        n,L = rng.randrange(7,19),rng.randrange(7)
        edges = tuple((u,v) for v in range(n)
                      for u in rng.sample(range(v),rng.randrange(min(2,v)+1)))
        p,c,x = check(n,edges,4,3,L)
        cases += 1
        global_solves += 1
        projection_checks += p
        cut_checks += c
        crossing_cycles += x
    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"all_DAG_N_range":[0,4],
              "all_DAG_B_W_ranges":[1,4],"all_DAG_L_range":[0,3],
              "all_DAG_chunk_cases":small_cases,"seed":2026101412,
              "general_random_cases":100,"general_random_N_range":[6,14],
              "general_random_B_range":[1,6],"general_random_W_range":[1,8],
              "random_L_range":[0,6],"fixed_B4_W3_random_cases":60,
              "fixed_B4_W3_random_N_range":[7,18],"all_random_indegree_at_most":2,
              "total_chunk_cases":cases,"independent_global_CSP_solves":global_solves,
              "projected_schedule_ROB_replays":projection_checks,
              "cut_charging_checks":cut_checks,"actual_crossing_cycles":crossing_cycles,
              "scope":"Independent exact CSP for global and chunk schedules. Every concatenation and projected local trace directly ROB-replayed; all crossing jobs and multiplicative bounds checked. No primary solver.",
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                               for name in ("constraint_solver.py","chunk_lookahead_audit.py")}}
    Path(__file__).with_name("chunk_lookahead_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
