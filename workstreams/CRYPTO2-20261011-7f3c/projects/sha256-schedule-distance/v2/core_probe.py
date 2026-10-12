#!/usr/bin/env python3
"""Extract a small candidate contradiction; solver cores are not proof certificates."""
import json,time
from pathlib import Path
import z3
here=Path(__file__).resolve().parent
S=json.loads((here/'supports.json').read_text())['supports'][3]
s=z3.Solver();s.set(timeout=20000,unsat_core=True,random_seed=0)
x={i:z3.BitVec('x'+str(i),32) for i in S};y={i:z3.BitVec('y'+str(i),32) for i in S}
f=lambda x:z3.RotateRight(x,7)^z3.RotateRight(x,18)^z3.LShR(x,3)
g=lambda x:z3.RotateRight(x,17)^z3.RotateRight(x,19)^z3.LShR(x,10)
D={i:y[i]-x[i] for i in S};F={i:f(y[i])-f(x[i]) for i in S};G={i:g(y[i])-g(x[i]) for i in S}
forms={}
for i in S:forms['nz'+str(i)]=D[i]!=0
for t in range(16,64):
 forms['eq'+str(t)]=D.get(t,0)==G.get(t-2,0)+D.get(t-7,0)+F.get(t-15,0)+D.get(t-16,0)
for name,p in forms.items():
 if isinstance(p,bool):
  assert p
 else:s.assert_and_track(p,name)
start=time.monotonic();r=s.check();print(str(r),time.monotonic()-start,flush=True)
if r==z3.unsat:
 core=[str(x) for x in s.unsat_core()];print(core,flush=True)
 for name in list(core):
  q=z3.Solver();q.set(timeout=5000,random_seed=0)
  q.add(*[forms[k] for k in core if k!=name]);r=q.check()
  if r==z3.unsat:core.remove(name)
  print(name,str(r),len(core),flush=True)
 (here/'CORE.json').write_text(json.dumps({'support_index':3,'constraints':core,'warning':'solver-derived only; requires separate proof'},indent=2)+'\n')
