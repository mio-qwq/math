#!/usr/bin/env python3
"""Can the shared five-equation tail alone be excluded without forcing delta=H?"""
import argparse
import json
from pathlib import Path
import time
import z3

ap = argparse.ArgumentParser()
ap.add_argument('output', type=Path)
a = ap.parse_args()
s = z3.SolverFor('QF_BV')
s.set(timeout=15000, random_seed=0)
pairs = {name: (z3.BitVec(name+'0', 32), z3.BitVec(name+'1', 32)) for name in 'xarb'}
f = lambda x: z3.RotateRight(x, 7)^z3.RotateRight(x, 18)^z3.LShR(x, 3)
g = lambda x: z3.RotateRight(x, 17)^z3.RotateRight(x, 19)^z3.LShR(x, 10)
d = {k: v-u for k, (u, v) in pairs.items()}
F = {k: f(v)-f(u) for k, (u, v) in pairs.items()}
G = {k: g(v)-g(u) for k, (u, v) in pairs.items()}
s.add(*[v != 0 for v in d.values()])
s.add(d['r'] == -d['x'], F['r'] == F['x'], d['a'] == -F['x'],
      d['b'] == F['a'], G['b'] == d['x'])
start = time.monotonic()
result = s.check()
out = dict(status=str(result), seconds=time.monotonic()-start, timeout_ms=15000,
           z3=z3.get_version_string(), scope='shared tail only, not a full support or message pair')
if result == z3.sat:
    model = s.model()
    out['pairs'] = {k: [model.eval(w).as_long() for w in v] for k, v in pairs.items()}
elif result == z3.unknown:
    out['reason'] = s.reason_unknown()
a.output.write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out))
