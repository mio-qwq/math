#!/usr/bin/env python3
"""A restricted construction ansatz, not a universal exclusion checker."""
import argparse
import datetime
import json
from pathlib import Path
import time
import z3


def f(x):
    return z3.RotateRight(x,7)^z3.RotateRight(x,18)^z3.LShR(x,3)


def g(x):
    return z3.RotateRight(x,17)^z3.RotateRight(x,19)^z3.LShR(x,10)


def run(timeout_ms):
    q, qp, p, r = z3.BitVecs('q qp p r',32)
    d = qp-q
    pp = p+d
    a = f(pp)-f(p)
    rp = r+a
    solver = z3.Solver()
    solver.set(timeout=timeout_ms)
    solver.add(d!=0,a!=0,g(qp)-g(q)==-d,a==-(f(qp)-f(q)),
               g(rp)-g(r)==-a,f(rp)-f(r)==-(g(pp)-g(p))-d)
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    tick = time.monotonic()
    status = solver.check()
    result = {'schema':'crypto3-periodic-active-pair-ansatz-v1','started_utc':started,
              'seconds':time.monotonic()-tick,'z3':z3.get_version_string(),
              'timeout_ms':timeout_ms,'status':str(status),
              'scope':'A period-14 assignment to active word pairs only; inactive base completion is not imposed.'}
    if status == z3.sat:
        model = solver.model()
        result['pairs']={name:[model.eval(x).as_long(),model.eval(y).as_long()]
                         for name,x,y in [('Q',q,qp),('P',p,pp),('R',r,rp)]}
        result['D']=model.eval(d).as_long()
        result['A']=model.eval(a).as_long()
    if status == z3.unknown:
        result['reason_unknown']=solver.reason_unknown()
    if status == z3.unsat:
        result['proof_status']='Uncertified solver outcome; not used as a mathematical exclusion.'
    return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--timeout-ms',type=int,default=20000)
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('PERIODIC_PAIR_RUN.json'))
    args=parser.parse_args()
    result=run(args.timeout_ms)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
