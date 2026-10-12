#!/usr/bin/env python3
"""Build each mathematically distinct case once, in a fresh bounded process."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    completed=[]
    for q in range(1,32,2):
        for h in (0,1):
            receipt=HERE/f'BUILD-{q}-{h}.json'
            command=[sys.executable,'-B',str(HERE/'check.py'),'--q',str(q),'--h',str(h),
                     '--build','--output',str(receipt)]
            try:
                p=subprocess.run(command,capture_output=True,text=True,timeout=55)
                record={'q':q,'h':h,'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
            except subprocess.TimeoutExpired as e:
                record={'q':q,'h':h,'status':'timeout','budget_seconds':55,
                        'scope':'this one proof case remains uncertified; no timeout extension'}
            completed.append(record)
            result={'schema':'support12-v6-build-case-executions','cases':completed,
                    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
            (HERE/'BUILD-EXECUTION.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
            if record.get('exit_code')!=0:
                print(json.dumps(record,sort_keys=True),flush=True)
                sys.exit(1)
            data=json.loads(receipt.read_text())
            print(json.dumps(data,sort_keys=True),flush=True)
            if data['summary']['actual_witnesses']:
                sys.exit(0)
