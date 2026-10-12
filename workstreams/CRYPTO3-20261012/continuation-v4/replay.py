#!/usr/bin/env python3
"""Replay the continuation in a temporary copy; preserve all frozen evidence."""
import argparse
from datetime import datetime, timezone
import hashlib
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
    [PREFIX+'inherited-gate-v4/check_independent.py', '--negative'],
    [PREFIX+'shift-review-v4/check_independent.py'],
    [PREFIX+'shift-review-v4/compare_candidate.py'],
    [PREFIX+'shift-review-v4/check_absorption.py'],
    [PREFIX+'support12-v4/check.py'],
    [PREFIX+'support12-review-v4/check_independent.py'],
    [PREFIX+'support12-review-v4/negative_control.py'],
    [PREFIX+'support12-review-v4/compare_author.py'],
    [PREFIX+'supports10-11-v4/check.py', '--negative'],
    [PREFIX+'supports10-11-review-v4/check_independent.py'],
    [PREFIX+'supports10-11-review-v4/compare_author.py'],
    [PREFIX+'width-reduction-v5/check.py'],
    [PREFIX+'width-review-v5/check_rows_independent.py'],
]


def manifest_check():
    path = ROOT/'continuation-v4/SHA256.json'
    data = json.loads(path.read_text())
    seen = set()
    for entry in data['files']:
        rel = entry['path']
        assert rel not in seen, 'duplicate continuation path'
        seen.add(rel)
        target = (ROOT/rel).resolve()
        assert target.is_relative_to(ROOT), 'path outside workstream'
        assert target != path, 'manifest cannot hash itself'
        raw = target.read_bytes()
        assert len(raw) == entry['bytes'], 'continuation size: '+rel
        assert hashlib.sha256(raw).hexdigest() == entry['sha256'], 'continuation hash: '+rel
    return {'files_checked': len(seen), 'manifest_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--record', type=Path, help='New detailed run record outside the frozen workstream')
    parser.add_argument('--manifest-only', action='store_true')
    parser.add_argument('--full-stage2', action='store_true', help='Additionally rerun all 21 stage-2 checks')
    parser.add_argument('--freeze-run', action='store_true', help='First run before writing the new manifest')
    args = parser.parse_args()
    if args.record:
        assert not args.record.resolve().is_relative_to(ROOT), 'run record outside frozen workstream'
    if args.manifest_only:
        print(json.dumps({'status': 'PASS', **manifest_check()}, sort_keys=True)); return
    if not args.freeze_run:
        integrity = manifest_check()
    else:
        integrity = {'scope': 'first execution before continuation manifest is frozen'}
    result = {'schema': 'crypto3-continuation-isolated-replay-v4', 'python': sys.version,
              'began_utc': datetime.now(timezone.utc).isoformat(), 'integrity': integrity,
              'runs': [], 'base_commit': 'b7eb3becacf474a6978b6acb2879fce3d505e395'}
    # Transport restoration is exact and leaves the compressed/frozen sources unchanged.
    recovery = subprocess.run([sys.executable, '-B', str(ROOT/PREFIX/'coupled-boundary/restore_evidence.py')],
                              text=True, capture_output=True)
    assert recovery.returncode == 0, recovery.stdout+recovery.stderr
    with tempfile.TemporaryDirectory(prefix='crypto3-continuation-') as temp:
        target = Path(temp)/'CRYPTO3-20261012'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        commands = [['check_manifest.py']]
        if args.full_stage2:
            commands.append(['verify_release.py'])
        commands.extend(COMMANDS)
        for command in commands:
            source = target/command[0]
            assert source.is_file(), 'missing continuation checker: '+command[0]
            start = time.monotonic()
            run = subprocess.run([sys.executable, '-B']+command, cwd=target,
                                 text=True, capture_output=True)
            entry = {'argv': ['python', '-B']+command, 'exit_code': run.returncode,
                     'seconds': time.monotonic()-start, 'stdout': run.stdout, 'stderr': run.stderr,
                     'checker_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                     'stdout_sha256': hashlib.sha256(run.stdout.encode()).hexdigest()}
            result['runs'].append(entry)
            assert source.read_bytes() == (ROOT/command[0]).read_bytes(), 'checker changed during replay: '+command[0]
            if run.returncode:
                if args.record:
                    args.record.write_text(json.dumps(result, indent=2)+'\n')
                raise RuntimeError('failed '+command[0]+'\n'+run.stdout+run.stderr)
    result['status'] = 'PASS'
    result['ended_utc'] = datetime.now(timezone.utc).isoformat()
    if args.record:
        args.record.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'continuation_commands_passed': len(COMMANDS),
                      'full_stage2_replay': args.full_stage2,
                      'frozen_originals_preserved': True,
                      'elapsed_seconds': sum(r['seconds'] for r in result['runs'])}, sort_keys=True))


if __name__ == '__main__':
    main()
