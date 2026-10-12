#!/usr/bin/env python3
"""Word-pair difference relaxation; no base-schedule equations are assumed."""
import argparse,json,time
from pathlib import Path
import z3

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--indices',default='0,3,14')
    ap.add_argument('--timeout-ms',type=int,default=15000)
    ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    here=Path(__file__).resolve().parent
    supports=json.loads((here/'supports.json').read_text())['supports']
    results=[]
    for idx in map(int,a.indices.split(',')):
        S=supports[idx]; solver=z3.SolverFor('QF_BV')
        solver.set(timeout=a.timeout_ms,random_seed=0)
        left={t:z3.BitVec(f'x{t}',32) for t in S}
        right={t:z3.BitVec(f'y{t}',32) for t in S}
        s0=lambda x:z3.RotateRight(x,7)^z3.RotateRight(x,18)^z3.LShR(x,3)
        s1=lambda x:z3.RotateRight(x,17)^z3.RotateRight(x,19)^z3.LShR(x,10)
        delta={t:right[t]-left[t] for t in S}
        d0={t:s0(right[t])-s0(left[t]) for t in S}
        d1={t:s1(right[t])-s1(left[t]) for t in S}
        zero=z3.BitVecVal(0,32)
        for t in S:solver.add(delta[t]!=0)
        for t in range(16,64):
            solver.add(delta.get(t,zero)==d1.get(t-2,zero)+delta.get(t-7,zero)+d0.get(t-15,zero)+delta.get(t-16,zero))
        start=time.monotonic();r=solver.check()
        entry=dict(index=idx,support=S,status=str(r),seconds=time.monotonic()-start,timeout_ms=a.timeout_ms)
        if r==z3.sat:
            m=solver.model();entry['pairs']={str(t):[m.eval(left[t]).as_long(),m.eval(right[t]).as_long()] for t in S}
        elif r==z3.unknown:entry['reason']=solver.reason_unknown()
        results.append(entry);print(json.dumps(entry),flush=True)
        a.output.write_text(json.dumps({'scope':'difference equations only, not actual message-pair witness','z3':z3.get_version_string(),'runs':results},indent=2)+'\n')

if __name__=='__main__':main()
