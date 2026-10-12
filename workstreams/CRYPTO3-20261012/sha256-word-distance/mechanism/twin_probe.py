#!/usr/bin/env python3
"""Discovery query for a new coupled derivative core, not a schedule."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import z3


def sigma(x, kind):
    a,b,s = ((7,18,3),(17,19,10))[kind]
    return z3.RotateRight(x,a)^z3.RotateRight(x,b)^z3.LShR(x,s)


def run(timeout_ms, fixed_delta=None):
    x, xp, y, yp = z3.BitVecs('x xp y yp',32)
    delta = xp-x
    fx = sigma(xp,0)-sigma(x,0)
    fy = sigma(yp,0)-sigma(y,0)
    gx = sigma(xp,1)-sigma(x,1)
    gy = sigma(yp,1)-sigma(y,1)
    solver=z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(delta != 0, delta != 1<<31, yp-y == delta,
               fx == fy, gy-gx == delta+delta)
    if fixed_delta is not None:
        solver.add(delta == fixed_delta)
    started=time.monotonic()
    status=solver.check()
    result={'scope':'four independent words; no message/base recurrence',
            'status':str(status),'seconds':time.monotonic()-started,
            'timeout_ms':timeout_ms,'z3':z3.get_version_string(),
            'fixed_delta':fixed_delta}
    if status == z3.sat:
        model=solver.model()
        result['words']={str(v):model.eval(v).as_long() for v in (x,xp,y,yp)}
        result['delta']=model.eval(delta).as_long()
    elif status == z3.unknown:
        result['reason']=solver.reason_unknown()
    return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--timeout-ms',type=int,default=10000)
    parser.add_argument('--fixed-delta',type=lambda x:int(x,0))
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=run(args.timeout_ms,args.fixed_delta)
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
