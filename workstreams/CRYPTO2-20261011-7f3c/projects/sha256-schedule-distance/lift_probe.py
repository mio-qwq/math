#!/usr/bin/env python3
"""Bounded SMT discovery only. UNSAT/unknown is not a checked proof here."""
import argparse
import json
from pathlib import Path
import time
import z3

def main():
    ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--timeout-ms',type=int,default=20000)
    args=ap.parse_args()
    support=set(json.loads(args.certificate.read_text())['support_witness'])
    records=[]
    for mode in ('zero-base','unrestricted-base'):
        s=z3.Solver();s.set(timeout=args.timeout_ms,random_seed=0)
        a=[z3.BitVec(f'a{i}',32) for i in range(64)]
        b=[z3.BitVec(f'b{i}',32) if i in support else a[i] for i in range(64)]
        if mode=='zero-base':
            s.add(*[v==0 for v in a])
        s.add(*[a[i]!=b[i] for i in support])
        s0=lambda x:z3.RotateRight(x,7)^z3.RotateRight(x,18)^z3.LShR(x,3)
        s1=lambda x:z3.RotateRight(x,17)^z3.RotateRight(x,19)^z3.LShR(x,10)
        for w in (a,b):
            for t in range(16,64):
                s.add(w[t]==s1(w[t-2])+w[t-7]+s0(w[t-15])+w[t-16])
        started=time.monotonic();res=s.check()
        rec=dict(mode=mode,result=str(res),seconds=time.monotonic()-started,
                 timeout_ms=args.timeout_ms,reason_unknown=s.reason_unknown() if res==z3.unknown else None)
        if res==z3.sat:
            m=s.model()
            rec['messages']=[[m.eval(x,model_completion=True).as_long() for x in w[:16]] for w in (a,b)]
            rec['warning']='SAT model must be checked independently from the FIPS recurrence'
        records.append(rec)
        print(json.dumps(rec),flush=True)
    args.output.write_text(json.dumps(dict(z3_version=z3.get_version_string(),support=sorted(support),
                       interpretation='discovery only; no UNSAT proof certificate',runs=records),indent=2)+'\n')

if __name__=='__main__':
    main()
