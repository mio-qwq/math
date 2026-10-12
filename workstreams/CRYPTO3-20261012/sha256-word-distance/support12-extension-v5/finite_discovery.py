#!/usr/bin/env python3
"""New odd valuation-18 cases; use v4 only as a frozen discovery routine."""
import hashlib
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'support12-v4'
manifest=json.loads((OLD/'manifest.json').read_text())['files']
for name in ('explore.py','explore_triple.py'):
    assert hashlib.sha256((OLD/name).read_bytes()).hexdigest()==manifest[name]
sys.path.insert(0,str(OLD))
import explore_triple

if __name__=='__main__':
    start=time.monotonic();completed=[]
    for q in range(1,16,2):
        result=explore_triple.run(q<<18)
        result['v5_wrapper_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        (HERE/f'FINITE-{q}-V18.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        completed.append(q)
        print(json.dumps({k:v for k,v in result.items() if k!='cases'},sort_keys=True),flush=True)
        if result['sat_count']: break
    print(json.dumps({'completed':completed,'seconds':time.monotonic()-start},sort_keys=True))
