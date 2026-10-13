"""Independent repeated finite-lookahead family: CSP, barriers, visibility, traces."""

from datetime import datetime, timezone
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
from time import perf_counter

from constraint_solver import augmented_edges, feasible, operational_check, solve


def chain_job(M, arm, k):
    assert 0 <= k <= M and arm in (0,1)
    if k == 0:
        return 3 if arm == 0 else 2
    return 2*k+2+arm


def instance(M,bits,barriers=True):
    assert M >= 1
    length = 2*M+5
    edges = []
    for block,chosen in enumerate(bits):
        offset = block*length
        for arm in (0,1):
            for k in range(1,M+1):
                edges.append((offset+chain_job(M,arm,k-1),offset+chain_job(M,arm,k)))
        edges.append((offset+chain_job(M,chosen,M),offset+length-1))
        if block and barriers:
            previous = offset-length
            parents = (offset-1,previous+chain_job(M,1-bits[block-1],M))
            edges.extend((parent,offset+root) for root in range(4) for parent in parents)
    return length*len(bits),tuple(sorted(edges))


def block_policy(M,chosen,guess):
    """A fixed guessed priority, followed by the revealed final dependence."""
    schedule = [(0,1,chain_job(M,guess,0))]
    other = 1-guess
    for k in range(1,M+1):
        schedule.append((chain_job(M,other,k-1),chain_job(M,guess,k)))
    last = (chain_job(M,other,M),)
    if guess == chosen:
        schedule.append(last+(2*M+4,))
    else:
        schedule.extend((last,(2*M+4,)))
    return schedule


def policy(M,bits,guesses):
    length = 2*M+5
    return [tuple(job+block*length for job in action)
            for block,(chosen,guess) in enumerate(zip(bits,guesses))
            for action in block_policy(M,chosen,guess)]


def ancestors(n,edges):
    result = [set() for _ in range(n)]
    pred = [[] for _ in range(n)]
    for u,v in edges:
        pred[v].append(u)
    for v in range(n):
        for u in pred[v]:
            result[v].add(u)
            result[v].update(result[u])
    return result


def main():
    start = perf_counter()
    programs = first_actions = traces = barriers = visibility = 0
    first_sets = set()
    for M in range(1,4):
        length,K = 2*M+5,M+2
        for q in range(1,4):
            for bits in product((0,1),repeat=q):
                n,edges = instance(M,bits)
                assert all(sum(v==j for _,v in edges) <= 2 for j in range(n))
                optimum,_ = solve(n,edges,4,3)
                assert optimum == q*K,(M,bits,optimum)
                programs += 1
                possible = []
                for size in range(4):
                    for action in combinations(range(4),size):
                        answer = feasible(n,edges,4,3,q*K,first_action=action)
                        expected = set(action) in ({0,3},{0,1,3},{0,2,3}) if bits[0] == 0 else set(action)=={0,1,2}
                        assert (answer is not None) == expected,(M,bits,action,answer)
                        first_actions += 1
                        if answer is not None:
                            possible.append(action)
                first_sets.add((bits[0],tuple(possible)))
                durations = []
                for guesses in product((0,1),repeat=q):
                    schedule = policy(M,bits,guesses)
                    assert operational_check(n,edges,4,3,schedule),(M,bits,guesses,schedule)
                    duration = q*K+sum(bit!=guess for bit,guess in zip(bits,guesses))
                    assert len(schedule) == duration
                    durations.append(duration)
                    traces += 1
                assert Fraction(sum(durations),len(durations)) == q*Fraction(2*K+1,2)
                reach = ancestors(n,augmented_edges(n,edges,4))
                for block in range(1,q):
                    start_block = block*length
                    for v in range(start_block,start_block+length):
                        assert set(range(start_block)) <= reach[v]
                        barriers += 1
                for block in range(q):
                    changed = list(bits)
                    changed[block] ^= 1
                    _,flipped_edges = instance(M,changed)
                    for lookahead in range(2*M+1):
                        frontier = block*length+4+lookahead
                        visible = tuple(edge for edge in edges if edge[1] < frontier)
                        flipped_visible = tuple(edge for edge in flipped_edges if edge[1] < frontier)
                        assert visible == flipped_visible,(M,bits,block,lookahead)
                        visibility += 1
    # Removing barriers permits inter-block overlap, even when this sample's
    # optimum happens not to improve. A first probe expecting a strict optimum
    # reduction returned six; do not silently upgrade the negative control.
    no_barrier_n,no_barrier_edges = instance(1,(0,0),barriers=False)
    no_barrier_value,no_barrier_trace = solve(no_barrier_n,no_barrier_edges,4,3)
    overlap_trace = [[j] for j in range(6)]+[[6,7,8]]+[[j] for j in range(9,14)]
    assert operational_check(no_barrier_n,no_barrier_edges,4,3,overlap_trace)
    _,barrier_edges = instance(1,(0,0))
    assert not operational_check(no_barrier_n,barrier_edges,4,3,overlap_trace)
    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"M_range":[1,3],"q_range":[1,3],
              "all_bit_vector_programs":programs,"exact_first_action_checks":first_actions,
              "direct_policy_trace_replays":traces,"cross_block_ancestor_checks":barriers,
              "visible_incoming_edge_flip_checks":visibility,
              "first_action_sets":[[bit,[list(action) for action in actions]] for bit,actions in sorted(first_sets)],
              "barriers_removed_negative_control":{"M":1,"bits":[0,0],"cycles":no_barrier_value,
                                                   "optimal_schedule":[list(action) for action in no_barrier_trace],
                                                   "overlap_schedule":overlap_trace,
                                                   "scope":"The optimum remains six in this sample. The explicit overlap trace is legal only without barriers."},
              "scope":"All finite bit vectors in the stated range; no primary solver. Expected values are exact Fractions over all fixed guessed-bit traces. Visibility is incoming-edge-only prefix access, not successor lists.",
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                               for name in ("constraint_solver.py","repeated_lookahead_audit.py")}}
    Path(__file__).with_name("repeated_lookahead_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
