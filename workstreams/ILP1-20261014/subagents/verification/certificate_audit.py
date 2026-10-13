"""Positive, malformed, and adversarial audits of the independent macro checker."""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from itertools import combinations
import json
from pathlib import Path
from random import Random
from time import perf_counter

from constraint_solver import operational_check, solve, validate_input
from forced_macro_audit import clear_prefix_solve
from macro_certificate import SCHEMA, all_prefix_macros, check_certificate


def make_certificate(n, edges, width):
    edges = validate_input(n,edges,width+1,width)
    cycles,schedule,stats = clear_prefix_solve(n,edges,width)
    return {"schema":SCHEMA,"n":n,"window":width+1,"width":width,
            "edges":[list(edge) for edge in edges],"cycles":cycles,
            "potentials":list(stats["prefix_values"]),
            "schedule":[list(action) for action in schedule]}


def all_graphs(n):
    pairs = tuple(combinations(range(n),2))
    for mask in range(1 << len(pairs)):
        yield tuple(pair for bit,pair in enumerate(pairs) if mask >> bit & 1)


def main():
    start = perf_counter()
    positives = inequalities = random_cases = 0
    rejected = {}
    def positive(n,edges,W):
        nonlocal positives,inequalities
        certificate = make_certificate(n,edges,W)
        result = check_certificate(n,edges,W+1,W,certificate)
        assert result["valid"],result
        expected,_ = solve(n,edges,W+1,W)
        assert certificate["cycles"] == expected
        inequalities += result["macro_inequalities_checked"]
        positives += 1
        return certificate

    for n in range(5):
        for edges in all_graphs(n):
            for W in range(1,5):
                positive(n,edges,W)
    small_positive_count = positives
    rng = Random(2026101411)
    for _ in range(60):
        n,W = rng.randrange(5,16),rng.randrange(1,9)
        edges = tuple((a,b) for b in range(n)
                      for a in rng.sample(range(b),rng.randrange(min(2,b)+1)))
        positive(n,edges,W)
        random_cases += 1

    n,edges,W = 4,((1,3),),2
    good = make_certificate(n,edges,W)
    def reject(name, mutate, instance=(n,edges,W+1,W)):
        certificate = deepcopy(good)
        mutate(certificate)
        result = check_certificate(*instance,certificate)
        assert not result["valid"],(name,certificate,result)
        rejected[name] = result
        return result

    reject("initial potential disagrees with duration",lambda c:c["potentials"].__setitem__(0,1))
    reject("intermediate potential too high within numeric bound",lambda c:c["potentials"].__setitem__(2,2))
    reject("intermediate potential lowered invalidates incoming macro",lambda c:c["potentials"].__setitem__(3,0))
    reject("terminal potential is nonzero",lambda c:c["potentials"].__setitem__(4,1))
    reject("negative potential",lambda c:c["potentials"].__setitem__(1,-1))
    reject("oversized potential",lambda c:c["potentials"].__setitem__(1,10**30))
    reject("short potential vector",lambda c:c["potentials"].pop())
    reject("boolean potential",lambda c:c["potentials"].__setitem__(1,True))
    reject("floating potential",lambda c:c["potentials"].__setitem__(1,2.0))
    reject("potential vector absent",lambda c:c.pop("potentials"))
    reject("unrecognized macro whitelist",lambda c:c.update(macro_choices=[[0,2]]))
    reject("wrong schema",lambda c:c.update(schema="different-retirement-model"))
    reject("wrong graph",lambda c:c.update(edges=[]))
    reject("wrong N",lambda c:c.update(n=5))
    reject("wrong window",lambda c:c.update(window=4))
    reject("wrong width",lambda c:c.update(width=3))
    reject("boolean width",lambda c:c.update(width=True))
    reject("wrong cycle count",lambda c:c.update(cycles=3))
    reject("nonintegral cycle count",lambda c:c.update(cycles=2.0))
    reject("missing job",lambda c:c["schedule"][-1].pop())
    reject("repeated issue job",lambda c:c["schedule"][-1].__setitem__(0,0))
    reject("duplicate in one action",lambda c:c.update(schedule=[[0,0],[1,2,3]]))
    reject("same cycle dependence",lambda c:c.update(schedule=[[0,2],[1,3]]))
    reject("too wide issue",lambda c:c.update(schedule=[[0,1,2],[3]]))
    reject("unadmitted first job",lambda c:c.update(schedule=[[0,3],[1,2]]))
    reject("out of range job",lambda c:c.update(schedule=[[0,1],[2,99]]))
    reject("boolean schedule job",lambda c:c["schedule"][0].__setitem__(0,False))
    reject("nonlist action",lambda c:c["schedule"].__setitem__(0,tuple(c["schedule"][0])))
    reject("illegal target resources",lambda c:None,instance=(n,edges,4,2))
    reject("zero issue width",lambda c:None,instance=(n,edges,1,0))
    reject("external graph mismatch",lambda c:None,instance=(n,(),3,2))
    reject("invalid backward external edge",lambda c:None,instance=(n,((3,1),),3,2))

    # This is a legal but nonoptimal trace. Checking only its chosen macro
    # would accept its inflated F0=3; the regenerated alternative rejects it.
    bad = deepcopy(good)
    bad.update(cycles=3,schedule=[[0,2],[1],[3]])
    bad["potentials"][0] = 3
    assert operational_check(n,edges,3,2,bad["schedule"])
    initial_macros = list(m for m in all_prefix_macros(n,edges,2) if m[0] == 0)
    chosen = next(m for m in initial_macros if m[1] == (0,2))
    assert bad["potentials"][0] <= chosen[2]+bad["potentials"][chosen[3]]
    omitted = check_certificate(n,edges,3,2,bad)
    assert not omitted["valid"] and omitted["first_action"] == [0,1]
    rejected["omitted optimal macro adversary"] = omitted

    # Potentials need only be lower bounds, not exact optima at every prefix.
    relaxed = make_certificate(3,(),2)
    relaxed["potentials"][1] = 0
    assert check_certificate(3,(),3,2,relaxed)["valid"]

    witness_edges = ((1,4),(2,4),(2,5),(5,8))
    witness = positive(9,witness_edges,3)
    Path(__file__).with_name("c1_certificate_example.json").write_text(json.dumps(witness,indent=2)+"\n")
    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"all_DAG_N_range":[0,4],
              "all_DAG_W_range":[1,4],"all_DAG_valid_certificates":small_positive_count,
              "random_seed":2026101411,"random_indegree_at_most":2,
              "random_N_range":[5,15],"random_W_range":[1,8],
              "random_valid_certificates":random_cases,"valid_certificates":positives,
              "checked_macro_inequalities":inequalities,"rejected_tampers":rejected,
              "valid_inexact_tail_potential_certificate":relaxed,
              "scope":"Certificate checker regenerates every macro itself; no submitted whitelist and no primary/theory optimizer calls. Time-variable CSP cross-checks positive claimed optima.",
              "source_sha256":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                               for name in ("constraint_solver.py","forced_macro_audit.py","macro_certificate.py","certificate_audit.py")}}
    Path(__file__).with_name("certificate_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({key:report[key] for key in ("status","valid_certificates","checked_macro_inequalities","elapsed_seconds")},indent=2))
    print("rejected_tampers",len(rejected))


if __name__ == "__main__":
    main()
