#!/usr/bin/env python3
"""Local-core sharpness query; never a full-message witness."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import z3


def sigma(x,k):
    a,b,s=((7,18,3),(17,19,10))[k]
    return z3.RotateRight(x,a)^z3.RotateRight(x,b)^z3.LShR(x,s)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--delta',type=lambda s:int(s,0),default=1<<20)
    p.add_argument('--timeout-ms',type=int,default=10000)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    words={name:z3.BitVec(name,32) for name in ('x','xp','y','yp','r','rp')}
    d={name:words[name+'p']-words[name] for name in ('x','y','r')}
    f={name:sigma(words[name+'p'],0)-sigma(words[name],0) for name in ('x','y','r')}
    g={name:sigma(words[name+'p'],1)-sigma(words[name],1) for name in ('x','y','r')}
    s=z3.Solver();s.set(timeout=a.timeout_ms)
    s.add(d['x']==a.delta,d['y']==a.delta,d['r']==-a.delta,
          f['x']==f['y'],f['y']==f['r'],
          g['y']-g['x']==2*a.delta,g['y']-g['r']==a.delta)
    started=time.monotonic();status=s.check()
    result={'status':str(status),'delta':a.delta,'seconds':time.monotonic()-started,
            'timeout_ms':a.timeout_ms,'z3':z3.get_version_string(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'three independent word pairs; no actual base-schedule equations'}
    if status==z3.sat:
        m=s.model();result['words']={name:m.eval(v).as_long() for name,v in words.items()}
    elif status==z3.unknown:
        result['reason']=s.reason_unknown()
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
