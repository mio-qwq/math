#!/usr/bin/env python3
"""Recompute GP2 second-stage SHA256 manifest, rejecting missing and unexpected files."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

here = Path(__file__).resolve().parent
spec = json.loads((here / 'MANIFEST.json').read_text(encoding='utf-8'))
expected = {x['path']: x['sha256'] for x in spec['files']}
actual = {}
for p in here.rglob('*'):
    if not p.is_file() or '__pycache__' in p.parts or p.name == 'MANIFEST.json':
        continue
    rel = p.relative_to(here).as_posix()
    actual[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
assert set(actual) == set(expected), (sorted(set(expected)-set(actual)), sorted(set(actual)-set(expected)))
assert all(actual[k] == expected[k] for k in expected), [k for k in expected if actual[k]!=expected[k]]
print('PASS:', len(expected), 'stage-two files match SHA256 manifest')
