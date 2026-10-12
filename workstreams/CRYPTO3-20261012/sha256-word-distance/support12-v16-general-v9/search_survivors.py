#!/usr/bin/env python3
"""Bounded positive-model search over the 21 frozen twin fixtures."""
import json
from pathlib import Path
import time
import z3

HERE=Path(__file__).resolve().parent
MASK=(1<<32)-1

def rr(x,n): return z3.RotateRight(x,n)
def f(x): return rr(x,7)^rr(x,18)^z3.LShR(x,3)
def g(x): return rr(x,17)^rr(x,19)^z3.LShR(x,10)

def query(name,var,constraints):
    s=z3.SolverFor('QF_BV');s.set(timeout=30000);s.add(*constraints)
    started=time.monotonic();status=s.check();elapsed=time.monotonic()-started
    out={'name':name,'status':str(status),'elapsed_seconds':elapsed,
         'reason_unknown':s.reason_unknown() if status==z3.unknown else None}
    if status==z3.sat:
        out['word']=s.model().eval(var,model_completion=True).as_long()
    return out

cert=json.loads((HERE/'CERTIFICATE.json').read_text())
results=[]
for case in cert['cases']:
  q=case['q'];d=q<<16
  for index,w in enumerate(case['unique_recovered_fixtures']):
    a=int(w['common_F'],16);c=int(w['G_x'],16);t=(c+d)&MASK
    z=z3.BitVec(f'z_{q}_{index}',32)
    u=z3.BitVec(f'u_{q}_{index}',32)
    third=query('third_joint_member',z,[
        f(z+z3.BitVecVal(d,32))-f(z)==z3.BitVecVal((-a)&MASK,32),
        g(z+z3.BitVecVal(d,32))-g(z)==z3.BitVecVal((-t)&MASK,32)])
    reciprocal=query('reciprocal_sigma0_edge',u,[
        f(u+z3.BitVecVal(a,32))-f(u)==z3.BitVecVal(d,32)])
    results.append({'q':q,'fixture_index':index,'D':d,'A':a,'c':c,'T':t,
                    'third':third,'reciprocal':reciprocal})
print(json.dumps({'schema':'CRYPTO3-v16-frozen-survivor-screen-v9',
                  'z3_version':z3.get_version_string(),'query_count':2*len(results),
                  'results':results},indent=2,sort_keys=True))
