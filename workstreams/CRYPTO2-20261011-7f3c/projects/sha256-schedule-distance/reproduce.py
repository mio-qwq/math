#!/usr/bin/env python3
"""Rebuild the finite certificate byte for byte and run its separate checker."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();records=[]
    with tempfile.TemporaryDirectory(prefix='sha256-distance-') as tmp:
        dest=Path(tmp)/'certificate.json'
        for cmd in ([sys.executable,str(HERE/'discover.py'),str(dest)],
                    [sys.executable,str(HERE/'check.py'),str(dest),'--negative']):
            started=time.monotonic()
            p=subprocess.run(cmd,text=True,capture_output=True,timeout=60)
            if p.returncode:
                raise RuntimeError(p.stdout+p.stderr)
            records.append(dict(command=cmd,exit_code=p.returncode,seconds=time.monotonic()-started,
                                stdout=p.stdout,stderr=p.stderr))
        if dest.read_bytes()!=(HERE/'certificate.json').read_bytes():
            raise ValueError('discovery did not reproduce frozen bytes')
    import numpy
    paths=['discover.py','check.py','reproduce.py','certificate.json','lift_probe.py','LIFT-RUNS.json']
    hashes={f:hashlib.sha256((HERE/f).read_bytes()).hexdigest() for f in paths}
    result=dict(schema='sha256-distance-runs-v1',python=platform.python_version(),
                platform=platform.platform(),numpy=numpy.__version__,
                deterministic_reproduction=True,runs=records,sha256=hashes)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('PASS: byte-identical certificate, 5308416 inequalities, inverse bases, zero-base contradiction, 5 negative controls')

if __name__=='__main__':
    main()
