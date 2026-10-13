"""Exact offset averaging, causal callback checks, and strategy-sharp examples."""

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
from random import Random
import sys
from time import perf_counter

from causal_chunk_audit import Environment
from constraint_solver import operational_check, solve


def intervals(n,Q,U):
    start,next_size = 0,U
    while start < n:
        end = min(n,start+next_size)
        yield start,end
        start,next_size = end,Q


def offset_schedule(n,edges,B,W,L,U):
    Q = B+L
    assert 1 <= U <= Q
    schedule = []
    for start,end in intervals(n,Q,U):
        local_edges = tuple((u-start,v-start) for u,v in edges if start <= u < v < end)
        _,local = solve(end-start,local_edges,B,W)
        schedule.extend(tuple(start+j for j in action) for action in local)
    assert operational_check(n,edges,B,W,schedule)
    return schedule


def sharp_instance(B,q):
    k = B-1
    n,edges = 2*k*q,[]
    for block in range(q):
        start = 2*k*block
        for arm in (0,1):
            root = start+arm*k
            edges.extend((root+j-1,root+j) for j in range(1,k))
            if block:
                edges.extend((parent,root) for parent in (start-k-1,start-1))
    return n,tuple(edges)


def all_graphs(n):
    pairs = tuple(combinations(range(n),2))
    for mask in range(1 << len(pairs)):
        yield tuple(pair for bit,pair in enumerate(pairs) if mask >> bit & 1)


class FixedDraw:
    """Enumerate one possible result of an otherwise uniform RNG interface."""
    def __init__(self,Q,U):
        self.Q,self.U,self.calls = Q,U,0

    def randrange(self,start,stop):
        assert (start,stop) == (1,self.Q+1)
        self.calls += 1
        return self.U


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary-directory",type=Path,default=Path(__file__).parent.parent/"theory")
    args = parser.parse_args()
    primary = args.primary_directory.resolve()
    paths = [primary/name for name in ("chunk_lookahead.py","forced_segment_dp.py")]
    hashes = {path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    sys.path.insert(0,str(primary))
    spec = importlib.util.spec_from_file_location("reviewed_offset_chunk",paths[0])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert Path(sys.modules["forced_segment_dp"].__file__).resolve() == paths[1]
    sys.path.remove(str(primary))
    start = perf_counter()
    cases = offsets = reads = issue_cycles = sharp_cases = sharp_offsets = 0

    def audit(n,edges,L):
        nonlocal cases,offsets,reads,issue_cycles
        B,W,Q = 4,3,4+L
        optimum,global_schedule = solve(n,edges,B,W)
        spans = sum(max(action)-min(action) for action in global_schedule if action)
        costs,projections = [],[]
        for U in range(1,Q+1):
            reference = offset_schedule(n,edges,B,W,L,U)
            env,draw = Environment(n,edges,L),FixedDraw(Q,U)
            result = module.run_random_policy(n,L,env.read,env.issue,rng=draw)
            assert draw.calls == 1 and result["initial_chunk_size"] == U
            assert result["cycles"] == len(env.trace) == len(reference)
            assert env.done == set(range(n)) and [j for j,_ in env.reads] == list(range(n))
            assert result["largest_block"] == max((end-begin for begin,end in intervals(n,Q,U)),default=0)
            assert operational_check(n,edges,B,W,env.trace)
            projected = 0
            for begin,end in intervals(n,Q,U):
                local_edges = tuple((u-begin,v-begin) for u,v in edges if begin <= u < v < end)
                local = [tuple(j-begin for j in action if begin <= j < end) for action in global_schedule]
                local = [action for action in local if action]
                assert operational_check(end-begin,local_edges,B,W,local)
                projected += len(local)
            assert len(reference) <= projected
            costs.append(len(reference))
            projections.append(projected)
            offsets += 1
            reads += len(env.reads)
            issue_cycles += len(env.trace)
        average = Fraction(sum(costs),Q)
        assert Fraction(sum(projections),Q) == optimum+Fraction(spans,Q)
        assert average <= optimum+Fraction(spans,Q) <= (1+Fraction(B-1,Q))*optimum
        cases += 1

    for n in range(5):
        for edges in all_graphs(n):
            for L in (0,1,4):
                audit(n,edges,L)
    small_cases,small_offsets = cases,offsets
    rng = Random(2026101413)
    for _ in range(50):
        n,L = rng.randrange(5,16),rng.randrange(8)
        edges = tuple((u,v) for v in range(n)
                      for u in rng.sample(range(v),rng.randrange(min(2,v)+1)))
        audit(n,edges,L)

    # The improved valid threshold is Q>=max(B,2(B-1)-1).
    for B in range(2,7):
        k = B-1
        for W in (2,3):
            for Q in sorted({max(B,2*k-1),max(B,2*k),3*k+1}):
                for q in range(1,4):
                    n,edges = sharp_instance(B,q)
                    assert all(sum(v==j for _,v in edges) <= 2 for j in range(n))
                    assert all(sum(u==j for u,_ in edges) <= 2 for j in range(n))
                    optimum,_ = solve(n,edges,B,W)
                    assert optimum == q*k
                    costs = [len(offset_schedule(n,edges,B,W,Q-B,U)) for U in range(1,Q+1)]
                    assert Fraction(sum(costs),Q) == q*k+Fraction(q*k*k,Q),(B,W,Q,q,costs)
                    sharp_cases += 1
                    sharp_offsets += Q
    boundary_n,boundary_edges = sharp_instance(4,1)
    boundary_costs = [len(offset_schedule(boundary_n,boundary_edges,4,3,0,U)) for U in range(1,5)]
    assert boundary_costs == [4,5,6,5]
    assert Fraction(sum(boundary_costs),4*3) == Fraction(5,3)
    assert Fraction(5,3) < Fraction(7,4)

    # Exercise the actual seeded RNG wrapper, not only its enumerated draw outputs.
    seeded_env = Environment(9,((1,4),(2,4),(2,5),(5,8)),1)
    seeded = module.run_random_policy(9,1,seeded_env.read,seeded_env.issue,rng=Random(2026101413))
    invalid_offsets = 0
    for U in (0,6,1.5):
        env = Environment(3,(),1)
        try:
            module.run_policy(3,1,env.read,env.issue,initial_chunk_size=U)
        except ValueError:
            assert not env.reads and not env.trace
            invalid_offsets += 1
        else:
            raise AssertionError("malformed offset accepted")
    assert hashes == {path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}
    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"all_DAG_N_range":[0,4],
              "all_DAG_L_values":[0,1,4],"all_DAG_cases":small_cases,
              "all_DAG_exact_offsets":small_offsets,"seed":2026101413,
              "random_cases":50,"random_N_range":[5,15],"random_L_range":[0,7],
              "random_indegree_at_most":2,"total_B4_W3_cases":cases,
              "total_exact_offsets_and_callback_runs":offsets,
              "frontier_checked_operand_reads":reads,"operational_issue_cycles":issue_cycles,
              "sharp_B_range":[2,6],"sharp_W_values":[2,3],"sharp_q_range":[1,3],
              "sharp_Q_values":"distinct max(B,2k-1), max(B,2k), 3k+1, k=B-1",
              "sharp_family_resource_cases":sharp_cases,"sharp_family_exact_offsets":sharp_offsets,
              "below_threshold_control":{"B":4,"W":3,"L":0,"q":1,"offset_costs":boundary_costs,
                                         "ratio":"5/3","universal_upper":"7/4"},
              "seeded_wrapper_result":seeded,"invalid_offsets_rejected":invalid_offsets,
              "primary_source_sha256":hashes,
              "scope":"Exact finite uniform averages, not random sampling of expected values. Every callback run uses an independent persistent eager-window environment. Sharpness is for this policy, not the entire online class.",
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                               for name in ("constraint_solver.py","causal_chunk_audit.py","random_offset_audit.py")}}
    Path(__file__).with_name("random_offset_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
