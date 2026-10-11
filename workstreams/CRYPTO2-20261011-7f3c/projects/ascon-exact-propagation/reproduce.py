#!/usr/bin/env python3
"""Regenerate certificates in isolation and print an actual reproducibility log.
Usage: python reproduce.py > RUNS-new.json (does not alter frozen inputs).
"""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
log={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'python':sys.version,'platform':platform.platform(),
     'dependencies':'Python standard library only','runs':[],
     'source_hashes':{p.name:sha(p) for p in sorted(root.glob('*.py'))}}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def run(file,cwd,scope):
    st=time.monotonic()
    p=subprocess.run([sys.executable,file],cwd=cwd,env=env,text=True,capture_output=True)
    log['runs'].append({'command':['python',file],'cwd_role':scope,
                        'exit_code':p.returncode,'seconds':time.monotonic()-st,
                        'stdout':p.stdout,'stderr':p.stderr})
    if p.returncode:
        print(json.dumps(log,indent=2));sys.exit(p.returncode)

with tempfile.TemporaryDirectory(prefix='ascon-exact-reproduction-') as td:
    dest=Path(td)
    for name in ['discover.py','discover_triples.py']:shutil.copy2(root/name,dest/name)
    run('discover.py',dest,'isolated temporary directory')
    run('discover_triples.py',dest,'isolated temporary directory')
    names=['rank-certificate.json','mismatch-certificate.json','impossible-certificate.json',
           'triple-rank-certificate.json','triple-formula-certificate.json']
    log['certificate_regeneration']={name:{'sha256':sha(root/name),
        'byte_identical':(root/name).read_bytes()==(dest/name).read_bytes()} for name in names}
    if not all(x['byte_identical'] for x in log['certificate_regeneration'].values()):
        print(json.dumps(log,indent=2));sys.exit(1)
run('check.py',root,'project directory; read-only certificates')
run('check_triples.py',root,'project directory; read-only certificates')
log['status']='PASS'
log['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
print(json.dumps(log,indent=2))
