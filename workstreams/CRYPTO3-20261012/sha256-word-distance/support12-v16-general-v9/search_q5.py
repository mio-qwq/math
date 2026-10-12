#!/usr/bin/env python3
"""Two bounded discovery queries for the frozen q=5 twin fixture."""
import json
import time
import z3

MASK=(1<<32)-1
D=0x00050000
A=0x40406e02
C=0x1ff8913e
T=(C+D)&MASK

def rr(x,n): return z3.RotateRight(x,n)
def f(x): return rr(x,7)^rr(x,18)^z3.LShR(x,3)
def g(x): return rr(x,17)^rr(x,19)^z3.LShR(x,10)

def query(name,constraints,vars_):
    s=z3.SolverFor('QF_BV');s.set(timeout=30000);s.add(*constraints)
    t=time.monotonic(); status=s.check(); elapsed=time.monotonic()-t
    out={'name':name,'status':str(status),'elapsed_seconds':elapsed,
         'reason_unknown':s.reason_unknown() if status==z3.unknown else None}
    if status==z3.sat:
        m=s.model();out['model']={str(v):m.eval(v,model_completion=True).as_long()
                                 for v in vars_}
    return out

z=z3.BitVec('z',32)
u=z3.BitVec('u',32)
out=[query('third_joint_member',
           [f(z+z3.BitVecVal(D,32))-f(z)==z3.BitVecVal((-A)&MASK,32),
            g(z+z3.BitVecVal(D,32))-g(z)==z3.BitVecVal((-T)&MASK,32)], [z]),
     query('reciprocal_sigma0_edge',
           [f(u+z3.BitVecVal(A,32))-f(u)==z3.BitVecVal(D,32)], [u])]
print(json.dumps({'z3_version':z3.get_version_string(),'queries':out},
                 indent=2,sort_keys=True))
