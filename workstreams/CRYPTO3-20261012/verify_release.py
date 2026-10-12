#!/usr/bin/env python3
"""Run the release's exact checks in a temporary copy, preserving frozen bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

HERE=Path(__file__).resolve().parent
SHA='sha256-word-distance/'


def nested_manifests(release_manifest):
    """Check the separately frozen packages before running any checker."""
    summaries=[]
    paths=[HERE/entry['path'] for entry in release_manifest['files']
           if entry['path'].endswith('/SHA256.json')]
    for manifest_path in sorted(paths):
        content=json.loads(manifest_path.read_text())['files']
        if isinstance(content,dict):
            entries=[{'path':name, **({'sha256':value} if isinstance(value,str) else value)}
                     for name,value in content.items()]
        else:
            entries=content
        for entry in entries:
            target=(manifest_path.parent/entry['path']).resolve()
            assert target.is_relative_to(HERE),'nested manifest path outside release'
            raw=target.read_bytes()
            assert hashlib.sha256(raw).hexdigest()==entry['sha256'],str(target)
            if 'bytes' in entry:
                assert len(raw)==entry['bytes'],str(target)
        summaries.append({'path':str(manifest_path.relative_to(HERE)),
                          'entries_checked':len(entries),
                          'manifest_sha256':hashlib.sha256(manifest_path.read_bytes()).hexdigest()})
    return summaries


def commands():
    return [
        [SHA+'check_local.py','--negative'],
        [SHA+'local-review/check_independent.py','--selftest'],
        [SHA+'mechanism/check_structural.py',SHA+'supports-v2.json','--negative'],
        [SHA+'valuation-review/check_valuation_independent.py','--negative'],
        [SHA+'base-lift/verify_completion.py'],
        [SHA+'base-review/verify_independent.py','--author-directory',SHA+'base-lift',
         '--frozen-supports',SHA+'supports-v2.json'],
        [SHA+'coupled-boundary/check_bridges.py','--negative'],
        [SHA+'coupled-boundary/check_support5.py','--negative'],
        [SHA+'coupled-boundary/check_control.py','--negative'],
        [SHA+'coupled-boundary/check_drup.py'],
        [SHA+'coupled-review/check_hints.py'],
        [SHA+'coupled-review/audit_mapping.py'],
        [SHA+'coupled-review/audit_dependencies.py'],
        [SHA+'coupled-short-proof/check.py','--negative'],
        [SHA+'coupled-affine-review/verify_independent.py','--negative'],
        [SHA+'coupled-affine-review/compare_author.py','--negative'],
        [SHA+'coupled-sharpness/check.py','--negative'],
        [SHA+'coupled-sharpness-review/check.py'],
        [SHA+'active-pair-construction/verify.py','--negative'],
        [SHA+'active-pair-review/check_interfaces.py'],
        ['review/small_checks.py'],
    ]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--record',type=Path,
                        help='Optional new run record outside the frozen workstream')
    args=parser.parse_args()
    if args.record:
        assert not args.record.resolve().is_relative_to(HERE),'record outside frozen release'
    initial=subprocess.run([sys.executable,'-B','check_manifest.py'],cwd=HERE,
                           text=True,capture_output=True)
    if initial.returncode:
        raise RuntimeError(initial.stdout+initial.stderr)
    manifest=json.loads((HERE/'SHA256.json').read_text())
    result={'schema':'crypto3-isolated-release-replay-v1','manifest_check':json.loads(initial.stdout),
            'input_manifest':manifest,'nested_manifest_checks':nested_manifests(manifest),
            'python':sys.version,'runs':[]}
    with tempfile.TemporaryDirectory(prefix='crypto3-check-') as temp:
        target=Path(temp)/'CRYPTO3-20261012'
        target.mkdir()
        for item in manifest['files']:
            rel=Path(item['path'])
            destination=target/rel
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(HERE/rel,destination)
        shutil.copyfile(HERE/'SHA256.json',target/'SHA256.json')
        for command in commands():
            assert (target/command[0]).is_file(),'missing listed checker: '+command[0]
            start=time.monotonic()
            run=subprocess.run([sys.executable,'-B']+command,cwd=target,text=True,capture_output=True)
            entry={'argv':['python','-B']+command,'exit_code':run.returncode,
                   'seconds':time.monotonic()-start,'stdout':run.stdout,'stderr':run.stderr,
                   'stdout_sha256':hashlib.sha256(run.stdout.encode()).hexdigest()}
            result['runs'].append(entry)
            if run.returncode:
                if args.record:
                    args.record.write_text(json.dumps(result,indent=2)+'\n')
                raise RuntimeError('failed '+command[0]+'\n'+run.stdout+run.stderr)
    result['status']='PASS'
    if args.record:
        args.record.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','commands_passed':len(result['runs']),
                      'frozen_originals_preserved':True,
                      'elapsed_seconds':sum(r['seconds'] for r in result['runs'])},sort_keys=True))


if __name__=='__main__':
    main()
