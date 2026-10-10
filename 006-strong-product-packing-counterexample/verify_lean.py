"""Serial source-specific Lean replay in a fresh artifact directory.

Uses the existing pinned Mathlib package, without changing dependency versions.
No project .olean is accepted as a substitute for compiling its actual source.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import subprocess


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


EXPECTED_LEAN = '4.34.1'
EXPECTED_MATHLIB = 'd13f23b723b8a846827a245b89c10fc7d3f11612'


def inspect_environment(package, lake):
    """Query the actual toolchain and checkout; constants are expectations only."""
    def command(arguments, cwd=package):
        result = subprocess.run(arguments, cwd=cwd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, encoding='utf-8',
                                errors='strict', timeout=60)
        if result.returncode:
            raise RuntimeError('Environment command failed: ' + result.stdout)
        return result.stdout.strip()

    version_output = command([lake, 'env', 'lean', '--version'])
    match = re.search(r'\bLean \(version ([^,\s)]+)', version_output)
    if not match:
        raise RuntimeError('Unrecognized actual Lean version: ' + version_output)
    manifest = json.loads((package / 'lake-manifest.json').read_text(encoding='utf-8'))
    dependency = [p for p in manifest['packages'] if p['name'] == 'mathlib']
    if len(dependency) != 1:
        raise RuntimeError('Manifest must identify exactly one Mathlib dependency.')
    checkout = (package / manifest.get('packagesDir', '.lake/packages') / 'mathlib').resolve()
    actual_root = Path(command(['git', '-C', str(checkout), 'rev-parse', '--show-toplevel'])).resolve()
    if actual_root != checkout:
        raise RuntimeError('Mathlib must be its own Git checkout, not a parent repository.')
    actual_revision = command(['git', '-C', str(checkout), 'rev-parse', 'HEAD'])
    dirty = command(['git', '-C', str(checkout), 'status', '--porcelain', '--untracked-files=no'])
    toolchain = (package / 'lean-toolchain').read_text(encoding='utf-8').strip()
    observed = {'checked_utc': utc(), 'lean_version': match[1],
                'lean_version_output': version_output,
                'mathlib_commit': actual_revision,
                'manifest_mathlib_commit': dependency[0]['rev'],
                'lean_toolchain': toolchain,
                'mathlib_tracked_worktree_clean': not dirty,
                'configuration_sha256': {p: digest(package / p) for p in
                                         ['lean-toolchain', 'lakefile.lean', 'lake-manifest.json']}}
    if (observed['lean_version'] != EXPECTED_LEAN or actual_revision != EXPECTED_MATHLIB
            or dependency[0]['rev'] != EXPECTED_MATHLIB
            or toolchain != 'leanprover/lean4:v' + EXPECTED_LEAN or dirty):
        raise RuntimeError('Pinned environment mismatch: ' + json.dumps(observed))
    return observed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--lake', default='lake')
    parser.add_argument('--check-environment', action='store_true',
                        help='check the actual pinned environment without compiling any proof')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = here.parent
    package = repo / '002-weighted-rectangular-pruning/proof/mathlib'
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    try:
        observed = inspect_environment(package, args.lake)
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        (out / 'environment.json').write_text(json.dumps(
            {'status': 'ENVIRONMENT_CHECK_FAILED', 'checked_utc': utc(),
             'message': str(error), 'proof_compiled': False}, indent=2)+'\n', encoding='utf-8')
        raise SystemExit(str(error))
    (out / 'environment.json').write_text(json.dumps(
        {'status': 'PINNED_ENVIRONMENT_PASS', 'observed': observed,
         'proof_compiled': False}, indent=2)+'\n', encoding='utf-8')
    if args.check_environment:
        print(json.dumps({'status': 'PINNED_ENVIRONMENT_PASS', 'observed': observed,
                          'proof_compiled': False}), flush=True)
        return
    objects = out / 'objects'
    objects.mkdir()
    env = os.environ.copy()
    env['LEAN_PATH'] = str(objects) + os.pathsep + env.get('LEAN_PATH', '')
    expected = [
        (repo / 'notes/proof/Q6PackingDomination.lean', 12),
        (here / 'proof/Q6PackingComplexGeometry.lean', 12),
        (here / 'proof/Q6PackingComplexCounterexample.lean', 26),
    ]
    runs = []
    for source, count in expected:
        before = digest(source)
        target = objects / (source.stem + '.olean')
        started = utc()
        process = subprocess.run(
            [args.lake, 'env', 'lean', '--root=' + str(source.parent),
             '-o', str(target), str(source)], cwd=package, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            encoding='utf-8', errors='strict')
        ended = utc()
        log = out / (source.stem + '.log')
        log.write_text(process.stdout, encoding='utf-8', newline='\n')
        declarations = []
        for match in re.finditer(
                r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",
                process.stdout):
            axioms = [] if match[2] is None else [a.strip() for a in match[2].split(',') if a.strip()]
            declarations.append({'declaration': match[1], 'axioms': axioms})
        nonstandard = sorted({a for d in declarations for a in d['axioms']
                              if a not in {'propext', 'Classical.choice', 'Quot.sound'}})
        warnings = len(re.findall(r'\bwarning(?:\([^)]*\))?:', process.stdout))
        errors = len(re.findall(r'\berror(?:\([^)]*\))?:', process.stdout))
        panics = len(re.findall(r'\bPANIC\b', process.stdout))
        after = digest(source)
        configuration_unchanged = all(digest(package / p) == value for p, value in
                                      observed['configuration_sha256'].items())
        observed_after = None
        if len(runs) + 1 == len(expected):
            try:
                observed_after = inspect_environment(package, args.lake)
                configuration_unchanged = configuration_unchanged and all(
                    observed_after[p] == observed[p] for p in
                    ['lean_version', 'mathlib_commit', 'manifest_mathlib_commit',
                     'lean_toolchain', 'mathlib_tracked_worktree_clean', 'configuration_sha256'])
            except (OSError, RuntimeError, subprocess.TimeoutExpired):
                configuration_unchanged = False
        passed = (process.returncode == 0 and before == after and target.is_file()
                  and len(declarations) == count and not nonstandard
                  and warnings == errors == panics == 0 and configuration_unchanged)
        run = {'source': source.relative_to(repo).as_posix(),
               'source_sha256': before, 'source_after_sha256': after,
               'start_utc': started, 'end_utc': ended,
               'exit_code': process.returncode, 'expected_audits': count,
               'audits': len(declarations), 'declaration_axioms': declarations,
               'nonstandard_axioms': nonstandard, 'warnings': warnings,
               'errors': errors, 'panics': panics, 'object_exists': target.is_file(),
               'dependency_configuration_unchanged': configuration_unchanged,
               'log_sha256': digest(log), 'pass': passed}
        runs.append(run)
        receipt = {'checker_sha256': digest(Path(__file__).resolve()),
                   'fresh_project_artifacts': True, 'serial_compilation': True,
                   'lean_version': observed['lean_version'],
                   'mathlib_commit': observed['mathlib_commit'],
                   'observed_environment': observed,
                   'observed_environment_after': observed_after,
                   'runs': runs, 'complete': len(runs) == len(expected),
                   'pass': len(runs) == len(expected) and all(r['pass'] for r in runs)}
        (out / 'lean-verification.json').write_text(json.dumps(receipt, indent=2) + '\n',
                                                    encoding='utf-8', newline='\n')
        print(json.dumps({'source': run['source'], 'audits': run['audits'],
                          'pass': passed}), flush=True)
        if not passed:
            print(process.stdout, flush=True)
            raise SystemExit(1)


if __name__ == '__main__':
    main()
