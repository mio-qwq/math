#!/usr/bin/env python3
"""Isolated replay of the accepted valuation17 boundary; no solver rerun."""
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
COMMANDS = [[PREFIX+'support12-boundary-v6/check.py'],
            [PREFIX+'support12-review-v6/replay_readonly.py']]


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_manifest():
    path = ROOT/'continuation-v6/SHA256.json'
    packet = json.loads(path.read_text())
    seen = set()
    for entry in packet['files']:
        relative = entry['path']
        assert relative not in seen, 'duplicate stage6 path'
        seen.add(relative)
        target = (ROOT/relative).resolve()
        assert target.is_relative_to(ROOT) and target != path
        raw = target.read_bytes()
        assert len(raw) == entry['bytes'], 'stage6 length: '+relative
        assert hashlib.sha256(raw).hexdigest() == entry['sha256'], 'stage6 hash: '+relative
    return {'files_checked': len(seen), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def probe_audit(root):
    path = root/PREFIX/'support12-unrestricted-core-v6'
    packet = json.loads((path/'SHA256.json').read_text())
    for name, sha in packet['files'].items():
        file = (path/name).resolve()
        assert file.is_relative_to(path.resolve())
        assert hashlib.sha256(file.read_bytes()).hexdigest() == sha, name
    receipt = json.loads((path/'RECEIPT.json').read_text())
    assert receipt['solver_result'] == 'unknown' and receipt['reason_unknown'] == 'timeout'
    assert receipt['solver_check_calls'] == 1 and receipt['timeout_ms'] == 15000
    assert receipt['valuation_restriction_on_D'] is None
    assert receipt['SAT_model_obtained'] is False
    assert receipt['UNSAT_certificate_obtained'] is False
    assert receipt['independent_SAT_verifier_executed'] is False
    assert receipt['accepted_theorem_from_probe'] is None
    return {'files_checked': len(packet['files']), 'status': 'UNKNOWN record integrity only',
            'probe_rerun': False, 'mathematical_acceptance': False}


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
    v4 = load_module(ROOT/'continuation-v4/replay.py', 'stage4_frozen_integrity')
    v5 = load_module(ROOT/'continuation-v5/replay.py', 'stage5_frozen_integrity')
    prior = {'stage4': v4.manifest_check(), 'stage5': v5.check_manifest()}
    integrity = {'scope': 'first execution before freeze'} if args.freeze_run else check_manifest()
    result = {'schema': 'crypto3-stage6-isolated-replay-v1', 'python': sys.version,
              'base_commit': '24684c0207db415a60f7de57291d6aaf627eb287',
              'prior_frozen_integrity': prior, 'stage6_integrity': integrity, 'runs': []}
    with tempfile.TemporaryDirectory(prefix='crypto3-stage6-') as temp:
        target = Path(temp)/'CRYPTO3-20261012'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc',
                       'check-subsets', 'actual-boundary-v6', 'dyadic-width-v7',
                       'dyadic-width-review-v7', 'support12-structure-v7',
                       'support12-structure-review-v7'))
        result['stopped_probe_integrity'] = probe_audit(target)
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
                      'stopped_probe_rerun': False,
                      'seconds': sum(r['seconds'] for r in result['runs'])}, sort_keys=True))


if __name__ == '__main__':
    main()
