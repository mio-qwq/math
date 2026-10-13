#!/usr/bin/env python3
"""Replay the two-module C66 structural chain and audit all printed theorems."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import time

from verify_component_support import digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--adapter', type=Path)
    parser.add_argument('--build-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    compiler = args.lean.resolve()
    build, output = args.build_dir.resolve(), args.output_dir.resolve()
    build.mkdir(parents=True,exist_ok=True)
    output.mkdir(parents=True,exist_ok=True)
    env = os.environ.copy()
    env['LEAN_PATH'] = str(build)
    if args.adapter:
        env['STRUCT2_LEAN_BIN'] = str(compiler)
        env['LD_PRELOAD'] = str(args.adapter.resolve())
    version = subprocess.check_output([str(compiler),'--version'],env=env,text=True).strip()
    assert 'version 4.34.1,' in version
    assert '5045d0056413266e57c625dcd7c365b10e377c52' in version
    start = time.perf_counter()
    modules = []
    all_axioms = set()
    for module, expected in [('ComponentSupport',12),('SingletonComponent',9)]:
        source = root/(module+'.lean')
        code = re.sub(r'/-.*?-/', '', source.read_text(), flags=re.S)
        code = re.sub(r'--[^\n]*', '', code)
        assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b',code)
        names = re.findall(r'^#print axioms (\w+)$',code,flags=re.M)
        assert len(names) == expected
        command = [str(compiler),'-j1','-o',str(build/(module+'.olean')),source.name]
        run = subprocess.run(command,cwd=root,env=env,capture_output=True,text=True,timeout=120)
        text = run.stdout+run.stderr
        log = output/(module+'_compile.txt')
        log.write_text(version+'\n'+' '.join(command)+'\n'+text+
                       '\nEXIT CODE: '+str(run.returncode)+'\n')
        assert run.returncode == 0 and not re.search(r'\b(error|warning):',text),text
        audits = {}
        for name in names:
            full = 'Struct2.C66.'+module+'.'+name
            if "'"+full+"' does not depend on any axioms" in text:
                axioms = []
            else:
                match = re.search("'"+re.escape(full)+r"' depends on axioms:\s*\[([\s\S]*?)\]",text)
                assert match,full
                axioms = [x.strip() for x in match.group(1).split(',') if x.strip()]
            assert set(axioms) <= {'propext','Classical.choice','Quot.sound'}
            audits[full] = axioms
            all_axioms.update(axioms)
        modules.append({'module':module,'command':command,'exit_code':run.returncode,
                        'source_sha256':digest(source),'log_sha256':digest(log),
                        'olean_sha256':digest(build/(module+'.olean')),
                        'audit_count':len(audits),'axioms':audits})
    report = {
        'utc':datetime.now(timezone.utc).isoformat(),'success':True,
        'lean_version':version,'compiler_sha256':digest(compiler),
        'driver_sha256':digest(__file__),
        'driver_dependency_sha256':digest(root/'verify_component_support.py'),
        'modules':modules,'audit_count':sum(m['audit_count'] for m in modules),
        'axiom_union':sorted(all_axioms),'seconds':round(time.perf_counter()-start,6),
        'adapter_source_sha256':digest(root.parents[1]/'cg/lean/runtime_path.c') if args.adapter else None,
        'adapter_binary_sha256':digest(args.adapter) if args.adapter else None,
        'scope':('Original full ordered-equation closure and canonical component support; '
                 'an actual ungrounded singleton iff both endpoints are commonly fixed '
                 'or commonly transposed. No assumed singleton invariance. The cardinality, '
                 'probability, cycle-count and asymptotic statements are not formalized.')}
    (output/'lean_verification.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print('PASS:',report['audit_count'],'audits in two modules;',report['seconds'],
          'seconds; axioms:',report['axiom_union'])


if __name__ == '__main__':
    main()
