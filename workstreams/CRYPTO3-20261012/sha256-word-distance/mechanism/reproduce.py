#!/usr/bin/env python3
"""Read-only replay of the written lemma's finite dependencies and controls."""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--supports',type=Path,required=True)
    p.add_argument('--cross-check',action='store_true')
    a=p.parse_args()
    here=Path(__file__).resolve().parent
    commands=[('check_structural.py',[str(a.supports),'--negative']),
              ('check_twin_witness.py',[])]
    if a.cross_check:
        commands.append(('check_valuation.py',[str(a.supports),'--negative']))
    results=[]
    for name,args in commands:
        path=here/name
        proc=subprocess.run([sys.executable,str(path),*args],capture_output=True,text=True)
        entry={'script':name,'script_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
               'exit_code':proc.returncode,'stdout':proc.stdout.strip(),'stderr':proc.stderr.strip()}
        results.append(entry)
        if proc.returncode:
            print(json.dumps({'runs':results,'status':'failed'},indent=2,sort_keys=True))
            raise SystemExit(proc.returncode)
    result={'status':'passed','python':platform.python_version(),
            'support_source_sha256':hashlib.sha256(a.supports.read_bytes()).hexdigest(),
            'scope':'written v2(D)<=20 lemma finite dependencies; independent review pending',
            'runs':results}
    print(json.dumps(result,indent=2,sort_keys=True))
