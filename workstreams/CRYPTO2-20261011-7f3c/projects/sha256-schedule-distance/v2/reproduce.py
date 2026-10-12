#!/usr/bin/env python3
"""Reproduce v2 equality supports and checks without NumPy, Z3 or Lean."""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time

here = Path(__file__).resolve().parent
runs = []
with tempfile.TemporaryDirectory(prefix='crypto2-sha-v2-') as tmp:
    generated = Path(tmp)/'supports.json'
    commands = [[sys.executable, str(here/'enumerate_supports.py'), str(generated)],
                [sys.executable, str(here/'check.py'), '--negative']]
    for cmd in commands:
        start = time.monotonic()
        p = subprocess.run(cmd, capture_output=True, text=True)
        runs.append(dict(argv=cmd, exit_code=p.returncode,
                         seconds=time.monotonic()-start, stdout=p.stdout, stderr=p.stderr))
        if p.returncode:
            print(json.dumps(runs, indent=2))
            raise SystemExit(p.returncode)
    assert generated.read_bytes() == (here/'supports.json').read_bytes()
report = dict(python=sys.version, platform=platform.platform(),
              scope='v2 only; v1 potential is hash-pinned to the previously checked certificate',
              regenerated_byte_identically=True,
              support_sha256=hashlib.sha256((here/'supports.json').read_bytes()).hexdigest(),
              runs=runs)
print(json.dumps(report, indent=2))
