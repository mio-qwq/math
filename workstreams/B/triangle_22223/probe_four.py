"""Probe a stronger four-square-color route, not the original conjecture."""
import importlib.util,itertools,json
from pathlib import Path
spec=importlib.util.spec_from_file_location('new_exp',Path(__file__).with_name('explore.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
from collections import Counter
stats=Counter();bad=[]
for lengths in itertools.product(range(2,8),repeat=3):
 if tuple(sorted(lengths))!=lengths:continue
 a=m.expand(2,[(0,1)]*3,lengths)
 state,c,nodes=m.solve(a,(2,2,2,2),limit=2);stats[state]+=1
 if state=='UNSAT':
  result,cc,nn=m.solve(a,(2,2,2,2,3),limit=2)
  bad.append({'lengths':lengths,'original':result,'special_count':cc.count(4) if cc else None})
print(json.dumps({'four_color_stats':dict(stats),'obstructions':bad},indent=2))
