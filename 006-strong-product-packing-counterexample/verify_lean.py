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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--lake', default='lake')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = here.parent
    package = repo / '002-weighted-rectangular-pruning/proof/mathlib'
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
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
        passed = (process.returncode == 0 and before == after and target.is_file()
                  and len(declarations) == count and not nonstandard
                  and warnings == errors == panics == 0)
        run = {'source': source.relative_to(repo).as_posix(),
               'source_sha256': before, 'source_after_sha256': after,
               'start_utc': started, 'end_utc': ended,
               'exit_code': process.returncode, 'expected_audits': count,
               'audits': len(declarations), 'declaration_axioms': declarations,
               'nonstandard_axioms': nonstandard, 'warnings': warnings,
               'errors': errors, 'panics': panics, 'object_exists': target.is_file(),
               'log_sha256': digest(log), 'pass': passed}
        runs.append(run)
        receipt = {'checker_sha256': digest(Path(__file__).resolve()),
                   'fresh_project_artifacts': True, 'serial_compilation': True,
                   'lean_version': '4.34.1',
                   'mathlib_commit': 'd13f23b723b8a846827a245b89c10fc7d3f11612',
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
