#!/usr/bin/env python3
"""Replay the universal strong-fold semantics and its axiom audits."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

THEOREMS = ['fold_symmetric', 'fold_loopless', 'decode_adjacency',
            'foldDoubleCoverIso', 'encode_switch', 'decode_deck',
            'liftFoldIso', 'fold_iso_has_conjugating_automorphism',
            'restrictConjugator', 'automorphism_colour_uniform',
            'folds_isomorphic_iff_conjugate']


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--adapter', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    source = root / 'StrongFold.lean'
    lean = args.lean.resolve()
    env = os.environ.copy()
    if args.adapter:
        env['STRUCT2_LEAN_BIN'] = str(lean)
        env['LD_PRELOAD'] = str(args.adapter.resolve())
    version = subprocess.check_output([str(lean), '--version'], env=env, text=True).strip()
    assert 'version 4.34.1,' in version
    assert '5045d0056413266e57c625dcd7c365b10e377c52' in version
    code = re.sub(r'/-.*?-/', '', source.read_text(), flags=re.S)
    code = re.sub(r'--[^\n]*', '', code)
    assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', code)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir.resolve()
    command = [str(lean), '-j1', '-o', str(output / 'StrongFold.olean'), 'StrongFold.lean']
    start = time.perf_counter()
    run = subprocess.run(command, cwd=root, env=env, text=True, capture_output=True, timeout=60)
    transcript = version + '\n' + ' '.join(command) + '\n' + run.stdout + run.stderr
    transcript += '\nEXIT CODE: ' + str(run.returncode) + '\n'
    (output / 'strong_fold_compile.log').write_text(transcript)
    assert run.returncode == 0, transcript
    audits = {}
    for short in THEOREMS:
        name = 'Struct2.StrongFold.' + short
        lines = [x for x in run.stdout.splitlines() if x.startswith("'" + name + "'")]
        assert len(lines) == 1, (name, lines)
        if 'does not depend on any axioms' in lines[0]:
            audits[name] = []
        else:
            match = re.search(r'depends on axioms: \[(.*)\]', lines[0])
            assert match
            audits[name] = [x.strip() for x in match.group(1).split(',') if x.strip()]
    union = sorted({x for xs in audits.values() for x in xs})
    assert set(union) <= {'propext', 'Quot.sound', 'Classical.choice'}
    receipt = {
        'utc': datetime.now(timezone.utc).isoformat(), 'lean_version': version,
        'command': command, 'exit_code': run.returncode,
        'seconds': round(time.perf_counter() - start, 6),
        'source_sha256': sha(source), 'compiler_sha256': sha(lean),
        'script_sha256': sha(__file__), 'axioms': audits, 'axiom_union': union,
        'compile_log_sha256': sha(output / 'strong_fold_compile.log'),
        'adapter_source_sha256': sha(root / 'runtime_path.c') if args.adapter else None,
        'adapter_binary_sha256': sha(args.adapter) if args.adapter else None,
        'success': True,
        'scope': 'Arbitrary bipartite graphs: actual simple fold, CDC isomorphism and deck intertwining; for nonempty connected graphs, actual fold isomorphism iff full graph-automorphism conjugacy. No all-n CG automorphism classification.'
    }
    (output / 'strong_fold_verification.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(transcript)
    print('PASS', receipt['seconds'], 'seconds; axiom union:', union)


if __name__ == '__main__':
    main()
