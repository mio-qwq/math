#!/usr/bin/env python3
"""Compile the complete generic-fold / all-odd coordinate dependency chain."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

MODULES = [('StrongFold', 'Struct2.StrongFold'),
           ('OddCoordinates', 'Struct2.OddCoordinates'),
           ('OddCoverIso', 'Struct2.OddCoverIso')]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--adapter', type=Path)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--include-structure', action='store_true')
    parser.add_argument('--include-six-cycles', action='store_true',
                        help='also rebuild ModelStructure and SixCycleInvariant')
    parser.add_argument('--include-ring-rigidity', action='store_true',
                        help='also rebuild all structural modules, RingAction and CycleRigidity')
    parser.add_argument('--include-model-actions', action='store_true',
                        help='also rebuild explicit cycle/model actions and exact 24n parametrization')
    parser.add_argument('--include-strong-switches', action='store_true',
                        help='also rebuild the exact strongly switching parameter classification')
    parser.add_argument('--include-strong-conjugacy', action='store_true',
                        help='also rebuild three conjugacy/fold classes and the two-cousin certificate')
    parser.add_argument('--include-external-base', action='store_true',
                        help='also rebuild arbitrary external-base transport into the exact three folds')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    build = args.build_dir.resolve()
    output = args.output_dir.resolve()
    build.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    compiler = args.lean.resolve()
    env = os.environ.copy()
    env['LEAN_PATH'] = str(build)
    if args.adapter:
        env['STRUCT2_LEAN_BIN'] = str(compiler)
        env['LD_PRELOAD'] = str(args.adapter.resolve())
    version = subprocess.check_output([str(compiler), '--version'], env=env, text=True).strip()
    assert 'version 4.34.1,' in version
    assert '5045d0056413266e57c625dcd7c365b10e377c52' in version
    start = time.perf_counter()
    runs = []
    strong_conjugacy = args.include_strong_conjugacy or args.include_external_base
    strong_switches = args.include_strong_switches or strong_conjugacy
    model_actions = args.include_model_actions or strong_switches
    ring_rigidity = args.include_ring_rigidity or model_actions
    six_cycles = args.include_six_cycles or ring_rigidity
    structure = args.include_structure or six_cycles
    modules = MODULES + ([('ModelStructure', 'Struct2.ModelStructure')]
                         if structure else [])
    if six_cycles:
        modules += [('SixCycleInvariant', 'Struct2.SixCycleInvariant')]
    if ring_rigidity:
        modules += [('RingAction', 'Struct2.RingAction'),
                    ('CycleRigidity', 'Struct2.CycleRigidity')]
    if model_actions:
        modules += [('CycleActions', 'Struct2.CycleActions'),
                    ('ModelActions', 'Struct2.ModelActions')]
    if strong_switches:
        modules += [('StrongSwitchClassification',
                     'Struct2.StrongSwitchClassification')]
    if strong_conjugacy:
        modules += [('StrongConjugacy', 'Struct2.StrongConjugacy')]
    if args.include_external_base:
        modules += [('ExternalBaseTransport', 'Struct2.ExternalBaseTransport')]
    for module, namespace in modules:
        source = root / (module + '.lean')
        raw = source.read_text()
        code = re.sub(r'/-.*?-/', '', raw, flags=re.S)
        code = re.sub(r'--[^\n]*', '', code)
        assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b', code)
        names = re.findall(r'^#print axioms (\w+)$', code, flags=re.M)
        assert names
        command = [str(compiler), '-j1', '-o', str(build / (module + '.olean')), source.name]
        run_start = time.perf_counter()
        run = subprocess.run(command, cwd=root, env=env, capture_output=True,
                             text=True, timeout=120)
        text = version + '\n' + ' '.join(command) + '\n' + run.stdout + run.stderr
        text += '\nEXIT CODE: ' + str(run.returncode) + '\n'
        log = output / (module + '_compile.txt')
        log.write_text(text)
        assert run.returncode == 0, text
        assert not re.search(r'\b(error|warning):', run.stdout + run.stderr), text
        audits = {}
        for name in names:
            full = namespace + '.' + name
            lines = [line for line in run.stdout.splitlines() if line.startswith("'" + full + "'")]
            assert len(lines) == 1, (full, lines)
            if 'does not depend on any axioms' in lines[0]:
                audits[full] = []
            else:
                match = re.search("'" + re.escape(full) +
                                  r"' depends on axioms:\s*\[([\s\S]*?)\]", run.stdout)
                assert match
                audits[full] = [x.strip() for x in match.group(1).split(',') if x.strip()]
        union = sorted({x for xs in audits.values() for x in xs})
        assert set(union) <= {'propext', 'Quot.sound', 'Classical.choice'}, union
        runs.append({'module': module, 'source_sha256': digest(source),
                     'command': command, 'exit_code': run.returncode,
                     'seconds': round(time.perf_counter() - run_start, 6),
                     'log_sha256': digest(log), 'olean_sha256': digest(build / (module + '.olean')),
                     'axioms': audits, 'axiom_union': union})
        print(module, 'PASS;', len(audits), 'audits;', runs[-1]['seconds'], 'seconds', flush=True)
    report = {'utc': datetime.now(timezone.utc).isoformat(), 'lean_version': version,
              'compiler_sha256': digest(compiler), 'driver_sha256': digest(__file__),
              'adapter_source_sha256': digest(root / 'runtime_path.c') if args.adapter else None,
              'adapter_binary_sha256': digest(args.adapter) if args.adapter else None,
              'seconds': round(time.perf_counter() - start, 6), 'runs': runs,
              'audit_count': sum(len(r['axioms']) for r in runs), 'success': True,
              'scope': ('Every odd n>=1: original named-leaf bijection, typed CG CDC/model graph isomorphism, all adjacency and deck intertwining. '
                        + ('Actual connected bipartite model and original CDC, actual strong decks, original deck fold recovery and instantiated full-automorphism fold/conjugacy equivalence. ' if structure else '')
                        + ('Symbolic six-cycle characterization for the model at n>=2 and original CDC at odd n>=3; arbitrary actual automorphisms preserve centre, leaf and ring types; explicit n=1 exception. ' if six_cycles else 'No all-n six-cycle invariant. ')
                        + ('Synchronized actual ring actions, uniqueness from cyclic index/direction/swap and an injective encoding of all original CDC automorphisms into Fin(24*n) at every odd n>=3. ' if ring_rigidity else '')
                        + ('Explicit cyclic rotations/reflections, centre-residue compatibility, exhaustive actual model/original automorphism parametrization and a two-sided bijection with Fin(24*n). Abstract group laws are not separately formalized. ' if model_actions else 'No full automorphism-family Lean classification. ')
                        + ('Exact necessity-and-sufficiency classification of all actual strong switches as the two half-turn rotations or odd reflected ring swaps. ' if strong_switches else 'No exhaustive strong-switch classification. ')
                        + ('Exactly three strong-switch conjugacy and fold-isomorphism classes, with the original deck identified and two nonoriginal fold classes. ' if strong_conjugacy else 'No universal conjugacy/fold-class Lean theorem. ')
                        + ('Every arbitrary simple external graph whose canonical double cover is isomorphic to the model is transported to a strong switch and hence isomorphic to exactly one of those three folds. Finiteness is not required. ' if args.include_external_base else 'No formal arbitrary-external-base transport.'))}
    (output / 'verification.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('TOTAL PASS:', report['audit_count'], 'audits;', report['seconds'], 'seconds')


if __name__ == '__main__':
    main()
