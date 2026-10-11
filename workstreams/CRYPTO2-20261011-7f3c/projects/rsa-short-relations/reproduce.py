"""Regenerate finite diagnostics and compare exact certificate bytes.

Use the pinned isolated discovery dependencies documented in RUNS.md.
The definition checker itself needs only the Python standard library.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

base=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory(prefix='crypto2-rsa-replay-') as td:
    count=0
    for path in sorted((base/'evidence').glob('*.json')):
        record=json.loads(path.read_text())
        args=[sys.executable,str(base/'probe.py')]
        for k,v in record['parameters'].items():
            args += ['--'+k,str(v)]
        if not record.get('factorization_checked',True):
            args.append('--skip-factor')
        target=Path(td)/path.name
        args += ['--out',str(target)]
        result=subprocess.run(args,capture_output=True,text=True,timeout=45)
        if result.returncode:
            raise RuntimeError(result.stderr or result.stdout)
        if path.read_bytes()!=target.read_bytes():
            raise AssertionError('certificate mismatch: '+path.name)
        count+=1
    target=Path(td)/'synthetic.json'
    subprocess.run([sys.executable,str(base/'make_quadratic.py'),'--out',str(target)],
                   capture_output=True,text=True,check=True,timeout=10)
    if target.read_bytes()!=(base/'evidence/quadratic/synthetic.json').read_bytes():
        raise AssertionError('quadratic control mismatch')
    count+=1
    target=Path(td)/'general.json'
    subprocess.run([sys.executable,str(base/'make_general.py'),'--out',str(target)],
                   capture_output=True,text=True,check=True,timeout=10)
    if target.read_bytes()!=(base/'evidence/general/synthetic.json').read_bytes():
        raise AssertionError('general control mismatch')
    count+=1
    extraction=subprocess.run([sys.executable,str(base/'recover_general.py'),str(target)],
                              capture_output=True,text=True,check=True,timeout=45)
    expected={c['m']:c['expected'] for c in json.loads(target.read_text())['cases']}
    for row in json.loads(extraction.stdout):
        if row['recovered']!=expected[row['m']]:
            raise AssertionError('public-input extraction mismatch')
    print(json.dumps(dict(result='PASS',byte_identical_certificates=count)))
