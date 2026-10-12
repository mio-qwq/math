#!/usr/bin/env python3
"""Isolated standard-library replay of the accepted valuation-18 exclusions."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent.parent
PREFIX = 'sha256-word-distance/'
COMMANDS = [
    [PREFIX+'support12-extension-v5/check.py'],
    [PREFIX+'support12-review-v5/replay_readonly.py'],
    [PREFIX+'shift-symbolic-v5/check_module_certificate.py'],
    [PREFIX+'shift-symbolic-review-v5/check_independent.py'],
]


def check_manifest():
    path = ROOT/'continuation-v5/SHA256.json'
    packet = json.loads(path.read_text())
    seen = set()
    for entry in packet['files']:
        assert entry['path'] not in seen, 'duplicate stage-5 path'
        seen.add(entry['path'])
        target = (ROOT/entry['path']).resolve()
        assert target.is_relative_to(ROOT) and target != path, 'invalid manifest path'
        raw = target.read_bytes()
        assert len(raw) == entry['bytes'], 'stage-5 length: '+entry['path']
        assert hashlib.sha256(raw).hexdigest() == entry['sha256'], 'stage-5 hash: '+entry['path']
    return {'files_checked': len(seen), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--freeze-run', action='store_true')
    parser.add_argument('--manifest-only', action='store_true')
    parser.add_argument('--record', type=Path)
    args = parser.parse_args()
    if args.record:
        assert not args.record.resolve().is_relative_to(ROOT), 'record outside frozen workstream'
    if args.manifest_only:
        print(json.dumps({'status': 'PASS', **check_manifest()}, sort_keys=True)); return
    module_path = ROOT/'continuation-v4/replay.py'
    spec = importlib.util.spec_from_file_location('frozen_continuation4_integrity', module_path)
    v4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(v4)
    v4_integrity = v4.manifest_check()
    integrity = {'scope': 'first execution before freeze'} if args.freeze_run else check_manifest()
    result = {'schema': 'crypto3-stage5-isolated-replay-v1', 'python': sys.version,
              'base_commit': 'f888115f03f2ef1e06189296378f6ca200d1264b',
              'stage4_integrity': v4_integrity, 'stage5_integrity': integrity, 'runs': []}
    with tempfile.TemporaryDirectory(prefix='crypto3-stage5-') as temp:
        target = Path(temp)/'CRYPTO3-20261012'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc',
                       'check-subsets', 'support12-boundary-v6'))
        for command in COMMANDS:
            source = target/command[0]
            start = time.monotonic()
            run = subprocess.run([sys.executable, '-B']+command, cwd=target,
                                 text=True, capture_output=True)
            entry = {'argv': ['python', '-B']+command, 'exit_code': run.returncode,
                     'seconds': time.monotonic()-start, 'stdout': run.stdout, 'stderr': run.stderr,
                     'checker_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                     'stdout_sha256': hashlib.sha256(run.stdout.encode()).hexdigest()}
            result['runs'].append(entry)
            assert source.read_bytes() == (ROOT/command[0]).read_bytes(), 'source changed during replay'
            if run.returncode:
                if args.record:
                    args.record.write_text(json.dumps(result, indent=2)+'\n')
                raise RuntimeError('failed '+command[0]+'\n'+run.stdout+run.stderr)
    result['status'] = 'PASS'
    if args.record:
        args.record.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'commands_passed': len(COMMANDS),
                      'frozen_originals_preserved': True,
                      'seconds': sum(r['seconds'] for r in result['runs'])}, sort_keys=True))


if __name__ == '__main__':
    main()
