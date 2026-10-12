#!/usr/bin/env python3
"""Full modulo-2^32 triple sharpness discovery at valuation 17."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import z3

def sig(x,kind):
    a,b,c=((7,18,3),(17,19,10))[kind]
    return z3.RotateRight(x,a)^z3.RotateRight(x,b)^z3.LShR(x,c)

def query(q,h,timeout):
    D=(q<<17)+(h<<31)
    words={n:z3.BitVec(n,32) for n in ('x','xp','y','yp','r','rp')}
    d=lambda n:words[n+'p']-words[n]
    f=lambda n:sig(words[n+'p'],0)-sig(words[n],0)
    g=lambda n:sig(words[n+'p'],1)-sig(words[n],1)
    solver=z3.Solver();solver.set(timeout=timeout)
    solver.add(d('x')==D,d('y')==D,d('r')==-D,
               f('x')==f('y'),f('y')==f('r'),
               g('y')-g('x')==2*D,g('y')-g('r')==D)
    start=time.monotonic();status=solver.check()
    result={'q':q,'h':h,'delta':D,'status':str(status),
            'seconds':time.monotonic()-start,'timeout_ms':timeout,
            'arithmetic':'all constraints modulo2^32, no mod2^31 relaxation'}
    if status==z3.sat:
        model=solver.model()
        result['words']={n:model.eval(v).as_long() for n,v in words.items()}
    elif status==z3.unknown: result['reason']=solver.reason_unknown()
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--timeout-ms',default=2000,type=int)
    p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();cases=[];stop=False
    for q in range(1,32,2):
        for h in (0,1):
            r=query(q,h,a.timeout_ms);cases.append(r)
            result={'schema':'support12-valuation17-discovery-v6',
                    'scope':'six actual words in necessary local core only; solver UNSAT is not a proof',
                    'cases':cases,'z3':z3.get_version_string(),
                    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
            # Preserve evidence after every query, including bounded failures.
            a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
            print(json.dumps(r,sort_keys=True),flush=True)
            if r['status']=='sat': stop=True;break
        if stop: break
