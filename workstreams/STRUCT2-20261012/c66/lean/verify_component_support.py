#!/usr/bin/env python3
"""Compile the actual C66 component transport and audit every named result."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--adapter', type=Path)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    source = root / 'ComponentSupport.lean'
    compiler = args.lean.resolve()
    build = args.build_dir.resolve()
    output = args.output_dir.resolve()
    build.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env['LEAN_PATH'] = str(build)
    if args.adapter:
        env['STRUCT2_LEAN_BIN'] = str(compiler)
        env['LD_PRELOAD'] = str(args.adapter.resolve())
    version = subprocess.check_output([str(compiler), '--version'], env=env, text=True).strip()
    assert 'version 4.34.1,' in version
    assert '5045d0056413266e57c625dcd7c365b10e377c52' in version
    code = re.sub(r'/-.*?-/', '', source.read_text(), flags=re.S)
    code = re.sub(r'--[^\n]*', '', code)
    assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', code)
    names = re.findall(r'^#print axioms (\w+)$', code, flags=re.M)
    assert names
    command = [str(compiler), '-j1', '-o', str(build / 'ComponentSupport.olean'), source.name]
    start = time.perf_counter()
    run = subprocess.run(command, cwd=root, env=env, capture_output=True,
                         text=True, timeout=120)
    log = output / 'ComponentSupport_compile.txt'
    log.write_text(version + '\n' + ' '.join(command) + '\n' + run.stdout + run.stderr
                   + '\nEXIT CODE: ' + str(run.returncode) + '\n')
    assert run.returncode == 0, log.read_text()
    assert not re.search(r'\b(error|warning):', run.stdout + run.stderr), log.read_text()
    audits = {}
    for name in names:
        full = 'Struct2.C66.ComponentSupport.' + name
        lines = [line for line in run.stdout.splitlines() if line.startswith("'" + full + "'")]
        assert len(lines) == 1
        if 'does not depend on any axioms' in lines[0]:
            audits[full] = []
        else:
            match = re.search("'" + re.escape(full) + r"' depends on axioms:\s*\[([\s\S]*?)\]",
                              run.stdout)
            assert match
            audits[full] = [x.strip() for x in match.group(1).split(',') if x.strip()]
    union = sorted({a for values in audits.values() for a in values})
    assert set(union) <= {'propext', 'Classical.choice', 'Quot.sound'}
    report = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'lean_version': version, 'command': command, 'exit_code': run.returncode,
        'seconds': round(time.perf_counter() - start, 6),
        'source_sha256': digest(source), 'driver_sha256': digest(__file__),
        'compiler_sha256': digest(compiler), 'log_sha256': digest(log),
        'olean_sha256': digest(build / 'ComponentSupport.olean'),
        'adapter_source_sha256': digest(root.parents[1] / 'cg/lean/runtime_path.c') if args.adapter else None,
        'adapter_binary_sha256': digest(args.adapter) if args.adapter else None,
        'audit_count': len(audits), 'axioms': audits, 'axiom_union': union,
        'success': True,
        'scope': ('Actual original unordered variables and full ordered-equation closure; '
                  'canonical ungrounded component edge list, adjacency equivalence, '
                  'endpoint transport and distinct orbit-prefix length at most twice '
                  'the actual component edge-list length. Probability/excess estimates, '
                  'permutation entropy and the expectation limit remain written.')
    }
    (output / 'lean_verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('PASS:', len(audits), 'audits;', report['seconds'], 'seconds; axioms:', union)


if __name__ == '__main__':
    main()
