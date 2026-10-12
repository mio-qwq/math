#!/usr/bin/env python3
"""Finite-budget exact fixed-mask two-pair probe; UNSAT is discovery only."""
import hashlib
import json
import platform
import time
from pathlib import Path
import z3
from probe_masks import MASK, f, g

HERE=Path(__file__).resolve().parent


def sigma(v,kind):
    a,b,k=((7,18,3),(17,19,10))[kind]
    return z3.RotateRight(v,a)^z3.RotateRight(v,b)^z3.LShR(v,k)


def one(m,alpha):
    start=time.monotonic()
    x,y=z3.BitVecs('x y',32)
    xp=x^0x44ab0000
    yp=y^alpha
    A=xp-x
    C=sigma(xp,1)-sigma(x,1)
    E=m*A+C
    s=z3.SolverFor('QF_BV')
    s.set(timeout=5000)
    s.add(yp-y==-(sigma(xp,0)-sigma(x,0)))
    s.add(sigma(yp,0)-sigma(y,0)==-E)
    s.add(A!=0,yp!=y,E!=0)
    status=s.check()
    result={'m':m,'alpha_Y':alpha,'timeout_ms':5000,'status':str(status),
            'reason_unknown':s.reason_unknown() if status==z3.unknown else None,
            'elapsed_s':time.monotonic()-start}
    if status==z3.sat:
        model=s.model()
        X=model.eval(x).as_long()
        Y=model.eval(y).as_long()
        XP=X^0x44ab0000
        YP=Y^alpha
        A0=(XP-X)&MASK
        C0=(g(XP)-g(X))&MASK
        E0=(m*A0+C0)&MASK
        residuals=[(YP-Y+f(XP)-f(X))&MASK,
                   (f(YP)-f(Y)+E0)&MASK]
        assert residuals==[0,0]
        assert A0 and E0 and YP!=Y
        assert (A0|E0)&0xffff==0
        result.update({'witness':{'x':X,'x_prime':XP,'y':Y,'y_prime':YP},
                       'interfaces':{'A':A0,'C':C0,'E':E0},
                       'direct_residuals':residuals})
    return result


def main():
    inputfile=HERE/'MASK_PROBE.json'
    masks=json.loads(inputfile.read_text())['survivors']
    results=[one(m,mask) for m in (1,2) for mask in masks]
    data={'schema':'supports10-11-local-fixed-mask-core-discovery-v1',
          'scope':'two actual pairs at indices 18 and 26 only; no full schedule',
          'interpretation':'UNSAT is uncertified discovery; SAT is only a local fixture',
          'python':platform.python_version(),'z3':z3.get_version_string(),
          'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'mask_source_sha256':hashlib.sha256(inputfile.read_bytes()).hexdigest(),
          'cases':results}
    (HERE/'CORE_PROBE.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'statuses':[(x['m'],hex(x['alpha_Y']),x['status']) for x in results],
                      'witnesses':[x for x in results if x['status']=='sat']},indent=2))


if __name__=='__main__':main()
