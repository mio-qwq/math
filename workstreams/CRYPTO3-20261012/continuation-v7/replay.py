#!/usr/bin/env python3
"""Replay exact accepted local structure; preserve all frozen evidence."""
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
    [PREFIX+'dyadic-width-v7/check.py'],
    [PREFIX+'dyadic-width-review-v7/check_independent.py'],
    [PREFIX+'dyadic-width-review-v7/compare_author.py'],
    [PREFIX+'support12-structure-v7/check.py', '--negative'],
    [PREFIX+'support12-structure-review-v7/check_signatures_independent.py'],
    [PREFIX+'support12-structure-review-v7/compare_author.py'],
    [PREFIX+'actual-boundary-v6/check_actual_boundary.py'],
    [PREFIX+'actual-boundary-review-v7/replay_readonly.py'],
]


def check_manifest():
    path = ROOT/'continuation-v7/SHA256.json'
    packet = json.loads(path.read_text())
    seen = set()
    for entry in packet['files']:
        relative = entry['path']
        assert relative not in seen, 'duplicate stage7 path'
        seen.add(relative)
        target = (ROOT/relative).resolve()
        assert target.is_relative_to(ROOT) and target != path
        raw = target.read_bytes()
        assert len(raw) == entry['bytes'], 'stage7 length: '+relative
        assert hashlib.sha256(raw).hexdigest() == entry['sha256'], 'stage7 hash: '+relative
    return {'files_checked': len(seen), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def prior_integrity():
    result = {}
    for phase, function in [(4, 'manifest_check'), (5, 'check_manifest'), (6, 'check_manifest')]:
        path = ROOT/('continuation-v'+str(phase))/'replay.py'
        spec = importlib.util.spec_from_file_location('crypto3_integrity'+str(phase), path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        result['stage'+str(phase)] = getattr(module, function)()
    return result


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
    integrity = {'scope': 'first execution before freeze'} if args.freeze_run else check_manifest()
    result = {'schema': 'crypto3-stage7-isolated-replay-v1', 'python': sys.version,
              'base_commit': '78d0b1395cbcfca1d647c8bfeb30493d2a351473',
              'prior_frozen_integrity': prior_integrity(), 'stage7_integrity': integrity, 'runs': []}
    with tempfile.TemporaryDirectory(prefix='crypto3-stage7-') as temp:
        target = Path(temp)/'CRYPTO3-20261012'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'check-subsets'))
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
                      'older_large_enumerations_rerun': False,
                      'seconds': sum(r['seconds'] for r in result['runs'])}, sort_keys=True))


if __name__ == '__main__':
    main()
