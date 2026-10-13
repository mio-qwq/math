"""Package-local replay of the preserved independent program.

Execute the original source unchanged, then change only its SOURCE and REVIEW
path globals before calling main. No checking function or asserted hash is
replaced. New output has a separate location; historical evidence is preserved.
"""
from pathlib import Path
import hashlib, json

ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT/'review/independent_bfs_checks.py'
EXPECTED = '41fcbebed9e58f15c29867f490e9e08ffe416337102e973713b5b7b1cb688e17'
if hashlib.sha256(SCRIPT.read_bytes()).hexdigest() != EXPECTED:
    raise ValueError('Independent program differs from its reviewed version')
namespace = {'__file__': str(SCRIPT), '__name__': 'preserved_independent_check'}
exec(compile(SCRIPT.read_bytes(), str(SCRIPT), 'exec'), namespace)
out = ROOT/'verification/replayed-independent'
out.mkdir(parents=True, exist_ok=True)
namespace['SOURCE'] = ROOT/'supplement/frozen'
namespace['REVIEW'] = out
namespace['main']()
result = json.loads((out/'independent-bfs-results.json').read_text(encoding='utf-8'))
if result['status'] != 'PASS' or result['script_sha256'] != EXPECTED:
    raise ValueError('Independent replay did not return its source-bound PASS')
print('PASS: unchanged independent functions; only input/output path globals adapted.')
