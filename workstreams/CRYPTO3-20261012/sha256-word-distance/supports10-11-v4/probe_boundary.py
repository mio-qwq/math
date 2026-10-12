#!/usr/bin/env python3
"""Finite k=15 fixed-mask prefix; every found word fixture is rechecked."""
import hashlib
import json
import platform
import time
from pathlib import Path
import z3
from probe_masks import MASK,f,g

HERE=Path(__file__).resolve().parent


def sigma(v,kind):
    a,b,k=((7,18,3),(17,19,10))[kind]
    return z3.RotateRight(v,a)^z3.RotateRight(v,b)^z3.LShR(v,k)


def one(m,alpha,beta):
    start=time.monotonic()
    x,y=z3.BitVecs('x y',32)
    xp=x^alpha
    yp=y^beta
    A=xp-x
    E=m*A+sigma(xp,1)-sigma(x,1)
    s=z3.SolverFor('QF_BV');s.set(timeout=1000)
    s.add(yp-y==-(sigma(xp,0)-sigma(x,0)),sigma(yp,0)-sigma(y,0)==-E)
    s.add(A!=0,E!=0,yp!=y)
    outcome=s.check()
    result={'m':m,'alpha_X':alpha,'alpha_Y':beta,'status':str(outcome),
            'timeout_ms':1000,'elapsed_s':time.monotonic()-start,
            'reason_unknown':s.reason_unknown() if outcome==z3.unknown else None}
    if outcome==z3.sat:
        model=s.model();X=model.eval(x).as_long();Y=model.eval(y).as_long()
        XP=X^alpha;YP=Y^beta
        A0=(XP-X)&MASK;C0=(g(XP)-g(X))&MASK;E0=(m*A0+C0)&MASK
        residuals=[(YP-Y+f(XP)-f(X))&MASK,(f(YP)-f(Y)+E0)&MASK]
        assert residuals==[0,0] and A0 and E0 and YP!=Y
        assert (A0|E0)&((1<<15)-1)==0
        result.update({'witness':{'x':X,'x_prime':XP,'y':Y,'y_prime':YP},
                       'interfaces':{'A':A0,'C':C0,'E':E0},'residuals':residuals})
    return result


def main():
    source=HERE/'STRATUM_K15.json'
    cases=json.loads(source.read_text())['second_carry_survivors']
    outcomes=[]
    for m in (1,2):
        for alpha,beta in cases[str(m)][:12]:
            result=one(m,alpha,beta);outcomes.append(result)
            if result['status']=='sat':break
    data={'schema':'supports10-11-k15-local-boundary-discovery-v1',
          'scope':'two actual pairs only; bounded first 12 masks per m; stop at first SAT',
          'interpretation':'SAT fixtures prove local feasibility; no full active assignment or schedule',
          'python':platform.python_version(),'z3':z3.get_version_string(),
          'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'mask_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
          'cases':outcomes,'all_eligible_masks':cases}
    (HERE/'BOUNDARY_PROBE.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'case_statuses':[(x['m'],hex(x['alpha_X']),hex(x['alpha_Y']),x['status']) for x in outcomes],
          'fixtures':[x for x in outcomes if x['status']=='sat']},indent=2))


if __name__=='__main__':main()
