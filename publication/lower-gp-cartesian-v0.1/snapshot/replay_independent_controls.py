"""Replay the preserved independent controls with package-local paths only.

The reviewer's original source and original output remain unchanged. Only its
four top-level path assignments are replaced in memory; all mathematics and
control code are executed as written. New output goes to a separate directory.
"""
from pathlib import Path
import ast,hashlib,json

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'review/scratch/independent_small_controls.py'
tree=ast.parse(SOURCE.read_text(encoding='utf-8'),filename=str(SOURCE))
names={'REPO','WRITTEN','FIXED','OUT'}
removed=[]; kept=[]
for statement in tree.body:
    if isinstance(statement,ast.Assign) and len(statement.targets)==1 and isinstance(statement.targets[0],ast.Name) and statement.targets[0].id in names:
        removed.append(statement.targets[0].id)
    else: kept.append(statement)
assert set(removed)==names and len(removed)==4
tree.body=kept
out=ROOT/'verification/replayed-independent-controls'
out.mkdir(parents=True,exist_ok=True)
namespace={'__name__':'__main__','__file__':str(SOURCE),'REPO':ROOT/'supplement',
           'WRITTEN':ROOT/'supplement/universal','FIXED':ROOT/'supplement/fixed319',
           'OUT':out}
exec(compile(tree,str(SOURCE),'exec'),namespace)
(out/'path-adapter-receipt.json').write_text(json.dumps({
    'preserved_control_source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    'replacement_scope':'four top-level path assignments only; original functions unchanged',
    'output':'verification/replayed-independent-controls/independent_small_controls.json'},indent=2)+'\n',encoding='utf-8')
