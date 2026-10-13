"""Independent CSP audit of full-throughput A/B tiling at B=W+1, N=kW."""

from datetime import datetime, timezone
import hashlib
from itertools import product
import json
from pathlib import Path
from random import Random
from time import perf_counter

from constraint_solver import feasible, operational_check


def macro_flags(n, edges, W):
    if W < 2 or n < 0 or n % W:
        raise ValueError("requires W>=2 and N=kW")
    k = n//W
    singles, doubles = [True]*k, [True]*max(0,k-1)
    for u,v in edges:
        if not 0 <= u < v < n:
            raise ValueError("forward edges required")
        block_u, block_v = u//W, v//W
        if block_u == block_v:
            singles[block_u] = False
        for left in (block_u-1, block_u):
            if not 0 <= left < k-1 or not left <= block_u <= block_v <= left+1:
                continue
            start = left*W
            def phase(job):
                offset = job-start
                return 0 if offset < W-1 or offset == W else 1
            if phase(u) >= phase(v):
                doubles[left] = False
    return singles, doubles


def tiling(singles, doubles):
    k = len(singles)
    previous = [None]*(k+1)
    previous[0] = (-1,0)
    for i in range(k):
        if previous[i] is None:
            continue
        if singles[i] and previous[i+1] is None:
            previous[i+1] = (i,1)
        if i+1 < k and doubles[i] and previous[i+2] is None:
            previous[i+2] = (i,2)
    if previous[k] is None:
        return None
    answer = []
    i = k
    while i:
        old, length = previous[i]
        answer.append((old,length))
        i = old
    return list(reversed(answer))


def component_obstruction(singles, doubles):
    """Return a negative odd-component certificate, or None when feasible."""
    start, k = 0, len(singles)
    while start < k:
        end = start
        while end+1 < k and doubles[end]:
            end += 1
        if (end-start+1) % 2 and not any(singles[j] for j in range(start,end+1,2)):
            return (start,end)
        start = end+1
    return None


def to_schedule(tiles, W):
    schedule = []
    for block,length in tiles:
        a = block*W
        if length == 1:
            schedule.append(list(range(a,a+W)))
        else:
            schedule += [list(range(a,a+W-1))+[a+W],
                         [a+W-1]+list(range(a+W+1,a+2*W))]
    return schedule


def effective_graphs(n,W):
    pairs = [(i,j) for j in range(n) for i in range(max(0,j-W),j)]
    for mask in range(1 << len(pairs)):
        yield tuple(edge for bit,edge in enumerate(pairs) if mask >> bit & 1)


def check(n,edges,W):
    singles,doubles = macro_flags(n,edges,W)
    tiles = tiling(singles,doubles)
    obstruction = component_obstruction(singles,doubles)
    answer = feasible(n,edges,W+1,W,n//W)
    assert (tiles is not None) == (answer is not None) == (obstruction is None), (n,edges,W,singles,doubles)
    if tiles is not None:
        schedule = to_schedule(tiles,W)
        assert len(schedule) == n//W and all(len(cycle)==W for cycle in schedule)
        assert operational_check(n,edges,W+1,W,schedule)
    else:
        left,right = obstruction
        assert (right-left+1) % 2 == 1
        assert left == 0 or not doubles[left-1]
        assert right == len(singles)-1 or not doubles[right]
        assert all(doubles[j] for j in range(left,right))
        assert all(not singles[j] for j in range(left,right+1,2))
    return tiles is not None


def main():
    start = perf_counter()
    exhaustive = successes = 0
    cases = [(2,0),(2,2),(2,4),(2,6),(3,3),(3,6),(4,4)]
    for W,n in cases:
        for edges in effective_graphs(n,W):
            successes += check(n,edges,W)
            exhaustive += 1
    rng = Random(2026101408)
    random_cases = 0
    for W in range(2,11):
        for k in range(1,7):
            for _ in range(10):
                n = k*W
                edges = [(parent,child) for child in range(n)
                         for parent in rng.sample(range(child),rng.randrange(min(2,child)+1))]
                successes += check(n,edges,W)
                random_cases += 1
    # Force valid two-block swaps at a broad range of widths: a true edge
    # from the first job to its block's last job rules out A but permits B.
    swapped_witnesses = []
    for W in range(2,21):
        n,edges = 2*W,[(0,W-1)]
        assert check(n,edges,W)
        flags = macro_flags(n,edges,W)
        assert flags[0][0] is False and tiling(*flags) == [(0,2)]
        swapped_witnesses.append({"W":W,"N":n,"edges":edges})
    boolean_cases = 0
    for k in range(0,7):
        for a in product((False,True),repeat=k):
            for b in product((False,True),repeat=max(0,k-1)):
                assert (tiling(a,b) is None) == (component_obstruction(a,b) is not None)
                boolean_cases += 1
    # A nonintegral tail is deliberately outside the theorem's scope.
    try:
        macro_flags(5,[],3)
    except ValueError:
        pass
    else:
        raise AssertionError("nonintegral N/W must not be treated by this criterion")
    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"exhaustive_parameter_pairs_W_N":cases,
              "exhaustive_effective_graphs":exhaustive,"seed":2026101408,
              "random_indegree_at_most_two_cases":random_cases,"random_W_range":[2,10],
              "random_block_count_range":[1,6],"successful_graph_cases_before_forced_swap_tests":successes,
              "forced_swap_witnesses":swapped_witnesses,"boolean_component_cases":boolean_cases,
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                                for name in ("constraint_solver.py","packed_tiling_audit.py")}}
    Path(__file__).with_name("packed_tiling_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({key:report[key] for key in ("status","exhaustive_effective_graphs","random_indegree_at_most_two_cases","boolean_component_cases","elapsed_seconds")}))


if __name__ == "__main__":
    main()
