"""Reproducible finite audit of the operational solver and derived formulas."""
import argparse
import hashlib
import itertools
import json
import pathlib
import platform
import random
import sys
import time

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"src"))
from rob import Program,solve,earliest_times,required_window,schedule_times
from checker import check_certificate,replay


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--max-n",type=int,default=5)
    parser.add_argument("--random",type=int,default=100)
    parser.add_argument("--seed",type=int,default=20261014)
    parser.add_argument("--output")
    args=parser.parse_args()
    start=time.perf_counter()
    counts={"programs":0,"parameter_cases":0,"certificates":0,"states_checked":0}
    max_states=0
    def audit(p):
        nonlocal max_states
        counts["programs"]+=1
        n=p.n
        table={}
        for b in range(1,max(2,n+1)):
            h=max(earliest_times(p,b),default=-1)+1
            for w in range(1,max(2,n+1)):
                x=solve(p,b,w,True)
                result=check_certificate(x)
                counts["parameter_cases"]+=1;counts["certificates"]+=1
                counts["states_checked"]+=result["checked_states"]
                max_states=max(max_states,result["checked_states"])
                assert result["checked_states"]<=1+n*2**(b-1)
                t=required_window(schedule_times(x["schedule"],n))
                assert t<=b or n==0
                table[b,w]=x["cycles"]
                assert h<=x["cycles"]<=n
                if w>=b: assert h==x["cycles"]
                if b>1: assert table[b,w]<=table[b-1,w]
                if w>1: assert table[b,w]<=table[b,w-1]
                if b==1 or w==1: assert x["cycles"]==n
    for n in range(args.max_n+1):
        pairs=list(itertools.combinations(range(n),2))
        for mask in range(1<<len(pairs)):
            audit(Program(n,tuple(e for k,e in enumerate(pairs) if mask>>k&1)))
    exhaustive=dict(counts)
    rng=random.Random(args.seed)
    for _ in range(args.random):
        n=rng.randint(6,9)
        e=[]
        for j in range(n):
            for i in rng.sample(range(j),rng.randint(0,min(2,j))):e.append((i,j))
        audit(Program(n,tuple(sorted(e))))
    out={"scope":"finite tests only; not a proof for arbitrary DAGs", "max_n_all_forward_dags":args.max_n,
         "random_programs_indegree_at_most_two":args.random,"seed":args.seed,
         "exhaustive_counts":exhaustive,"total_counts":counts,"maximum_states_in_one_case":max_states,
         "python":platform.python_version(),"seconds":time.perf_counter()-start,
         "source_sha256":{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in [ROOT/"src/rob.py",ROOT/"src/checker.py",pathlib.Path(__file__)]},
         "result":"PASS"}
    text=json.dumps(out,indent=2)+"\n"
    if args.output:pathlib.Path(args.output).write_text(text)
    print(text,end="")


if __name__=="__main__":main()
