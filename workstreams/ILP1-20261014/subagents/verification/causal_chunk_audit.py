"""Targeted independent access-boundary audit of the theory callback policy."""

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from time import perf_counter

from chunk_lookahead_audit import chunk_schedule
from constraint_solver import operational_check
from repeated_lookahead_audit import instance


class Environment:
    def __init__(self,n,edges,L):
        self.n,self.L = n,L
        self.pred = [set() for _ in range(n)]
        for u,v in edges:
            self.pred[v].add(u)
        self.done,self.window = set(),set()
        self.retired = self.admitted = 0
        self.reads,self.trace = [],[]
        self.fill()

    def fill(self):
        while self.admitted < self.n and len(self.window) < 4:
            self.window.add(self.admitted)
            self.admitted += 1

    def read(self,j):
        assert 0 <= j < min(self.n,self.retired+4+self.L)
        self.reads.append((j,self.retired))
        return sum(1 << u for u in self.pred[j])

    def issue(self,action):
        jobs = set(action)
        assert 0 < len(action) <= 3 and len(jobs) == len(action)
        assert jobs <= self.window-self.done
        assert all(self.pred[j] <= self.done for j in jobs)
        self.done.update(jobs)
        self.trace.append(tuple(action))
        while self.retired in self.done:
            self.window.remove(self.retired)
            self.retired += 1
        self.fill()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary-directory",type=Path,default=Path(__file__).parent.parent/"theory")
    args = parser.parse_args()
    primary = args.primary_directory.resolve()
    source = primary/"chunk_lookahead.py"
    dependency = primary/"forced_segment_dp.py"
    hashes = {path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in (source,dependency)}
    sys.path.insert(0,str(primary))
    spec = importlib.util.spec_from_file_location("reviewed_causal_chunk",source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert Path(sys.modules["forced_segment_dp"].__file__).resolve() == dependency
    sys.path.remove(str(primary))
    start = perf_counter()
    cases = [(0,(),0),(0,(),20),(1,(),0),(1,(),20),
             (5,((0,1),),0),(5,((0,1),),1),(5,((0,1),),20),
             (9,((1,4),(2,4),(2,5),(5,8)),0),
             (9,((1,4),(2,4),(2,5),(5,8)),4),
             (9,((1,4),(2,4),(2,5),(5,8)),20),
             (13,tuple((j-1,j) for j in range(1,13)),1),
             (13,((0,8),(2,8),(1,12),(8,12)),0),
             (13,((0,8),(2,8),(1,12),(8,12)),2),
             (13,(),0),(13,(),3),(13,(),20)]
    for M,bits,L in ((1,(0,1),0),(1,(1,0),2),(2,(0,1,0),1),(3,(1,0),6)):
        n,edges = instance(M,bits)
        cases.append((n,edges,L))
    reads = issues = 0
    for n,edges,L in cases:
        env = Environment(n,edges,L)
        result = module.run_policy(n,L,env.read,env.issue)
        assert env.done == set(range(n))
        assert [j for j,_ in env.reads] == list(range(n))
        assert operational_check(n,edges,4,3,env.trace)
        independent = chunk_schedule(n,edges,4,3,L)
        assert result["cycles"] == len(env.trace) == len(independent)
        assert result["largest_block"] == min(n,4+L)
        reads += len(env.reads)
        issues += len(env.trace)
    invalid_masks = 0
    for returned_mask in (-1,1,1.5):
        issued = []
        try:
            module.run_policy(1,0,lambda j:returned_mask,lambda action:issued.append(action))
        except ValueError:
            assert not issued
            invalid_masks += 1
        else:
            raise AssertionError("invalid read mask was accepted")
    assert hashes == {path.name:hashlib.sha256(path.read_bytes()).hexdigest() for path in (source,dependency)}
    report = {"status":"PASS","utc_finished":datetime.now(timezone.utc).isoformat(),
              "elapsed_seconds":perf_counter()-start,"targeted_cases":len(cases),
              "actual_frontier_checked_reads":reads,"operationally_checked_issue_cycles":issues,
              "invalid_callback_masks_rejected":invalid_masks,"primary_source_sha256":hashes,
              "scope":"Own persistent eager-window environment checks every callback access and issue; independent CSP chunk values agree. No repeat of the earlier large mathematical audit.",
              "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_name("causal_chunk_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))


if __name__ == "__main__":
    main()
