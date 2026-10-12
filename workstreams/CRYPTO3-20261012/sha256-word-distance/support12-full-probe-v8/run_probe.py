#!/usr/bin/env python3
"""Run the single pre-registered support12 independent-pair query."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import time
import z3

N = 1 << 32
MASK = N - 1
SUPPORT = (10,11,13,15,18,20,26,28,29,34,42,43,57)


def ror(x, n):
    return z3.RotateRight(x, n)


def f(x):
    return ror(x,7) ^ ror(x,18) ^ z3.LShR(x,3)


def g(x):
    return ror(x,17) ^ ror(x,19) ^ z3.LShR(x,10)


def build():
    words = {i:(z3.BitVec(f'x_{i}',32),z3.BitVec(f'xp_{i}',32)) for i in SUPPORT}
    zero = z3.BitVecVal(0,32)
    d={}; F={}; G={}
    for i in range(64):
        if i in words:
            x,xp=words[i];d[i]=xp-x;F[i]=f(xp)-f(x);G[i]=g(xp)-g(x)
        else:d[i]=F[i]=G[i]=zero
    solver=z3.SolverFor('QF_BV');solver.set(timeout=30000)
    for i in SUPPORT:solver.add(d[i]!=zero)
    D=d[18]
    solver.add((D & z3.BitVecVal(0xffff,32))==zero)
    solver.add((D & z3.BitVecVal(0x10000,32))!=zero)
    for t in range(16,64):
        solver.add(d[t]==G[t-2]+d[t-7]+F[t-15]+d[t-16])
    return solver,words,d,F,G


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path);a=p.parse_args()
    solver,words,d,F,G=build()
    smt=solver.sexpr().encode(); smt_sha=hashlib.sha256(smt).hexdigest()
    started=time.monotonic();answer=solver.check();seconds=time.monotonic()-started
    result={'schema':'crypto3-support12-full-pair-probe-v8','z3_version':z3.get_version_string(),
            'python':sys.version,'timeout_ms':30000,'solver_checks':1,'seconds':seconds,
            'result':str(answer),'reason_unknown':solver.reason_unknown() if answer==z3.unknown else None,
            'support':list(SUPPORT),'valuation_d18':16,'smt2_sha256':smt_sha,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'base_schedule_constraints':False}
    if answer==z3.sat:
        m=solver.model(); result['model']={}
        for i,(x,xp) in words.items():
            result['model'][str(i)]={'x':f'{m.eval(x,model_completion=True).as_long():08x}',
                                     'xp':f'{m.eval(xp,model_completion=True).as_long():08x}'}
    if a.output:
        a.output.mkdir(parents=True,exist_ok=False)
        (a.output/'MODEL.smt2').write_bytes(smt)
        (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
