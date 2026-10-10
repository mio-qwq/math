#!/usr/bin/env python3
"""Fail closed on missing Python import modules in an Agent-A code checkout.

Static AST pass over sibling *.py source names. It does not execute the code,
so it is an import-check preflight rather than a test of all runtime behaviour.
The audit would have detected the earlier accidental import of unshipped
verify_general_all_regular in the old execution freeze.
"""
import ast
from pathlib import Path
import sys
import tempfile


def scan_directory(path):
    directory=Path(path)
    names={p.stem for p in directory.glob('*.py')}
    stdlib=set(sys.stdlib_module_names)|{'__future__'}
    result=[];errors=[]
    for p in sorted(directory.glob('*.py')):
        try:tree=ast.parse(p.read_text(encoding='utf8'),filename=p.name)
        except SyntaxError as e:
            errors.append((p.name,'syntax',str(e)));continue
        uses=[]
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                uses.extend(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node,ast.ImportFrom):
                if node.level == 0 and node.module:
                    uses.append(node.module.split('.')[0])
        missing=sorted({m for m in uses if m not in names and m not in stdlib})
        if missing:errors.append((p.name,'missing import',missing))
        result.append(p.name)
    return result,errors


def main():
    paths,problems=scan_directory(Path(__file__).parent)
    if problems:
        for p in problems:print('FAIL',p)
        raise SystemExit(1)
    # Negative control demonstrates precisely the old failure mode.
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp)/'missing.py').write_text('from verify_general_all_regular import f\n')
        files,errs=scan_directory(tmp)
        assert errs==[('missing.py','missing import',['verify_general_all_regular'])],errs
    print('PASS parsed',len(paths),'Agent-A Python modules; all absolute imports resolve')
    print('PASS missing-module negative control: verify_general_all_regular detected')

if __name__=='__main__':main()
