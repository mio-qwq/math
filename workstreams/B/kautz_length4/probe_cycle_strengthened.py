"""One bounded new upper-bound gate: add exact cyclic-window cuts and symmetry.
Goal is a certified finite f(5)<=34, which would sharpen the density bound by
subalphabet averaging. Solver output itself is NOT a certificate. No repeat
with a longer timeout unless a genuinely new inequality becomes available.
"""
from itertools import permutations,combinations
from pathlib import Path
from collections import Counter
import json,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
W=list(permutations(range(5),4));ix={w:i for i,w in enumerate(W)};n=len(W)
def d(u,v):
 if u==v:return 0
 return next((s for s in range(1,4) if u[s:]==v[:-s]),4)
D=[[d(u,v) for v in W] for u in W]
rows=set()
for tri in combinations(range(n),3):
 if any(D[u][v]+D[v][w]==D[u][w] for u,v,w in permutations(tri)):rows.add(tri)
triples=len(rows);cycles=set()
for k in (4,5):
 for p in permutations(range(5),k):
  ids=tuple(sorted(ix[tuple(p[(i+j)%k] for j in range(4))] for i in range(k)))
  # Every triple must be forbidden in the original metric before adding a cut.
  assert all(tuple(t) in rows for t in combinations(ids,3))
  cycles.add(ids)
rows=sorted(rows|cycles);rr=[];cc=[]
for i,row in enumerate(rows):rr.extend([i]*len(row));cc.extend(row)
A=coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(rows),n)).tocsc()
lo=np.zeros(n);lo[ix[(0,1,2,3)]]=1
start=time.monotonic();r=milp(-np.ones(n),integrality=np.ones(n),bounds=Bounds(lo,1),constraints=LinearConstraint(A,-np.inf,2),options={'time_limit':20})
ids=[] if r.x is None else [i for i,x in enumerate(r.x) if x>.5];chosen=set(ids)
assert all(len(set(row)&chosen)<=2 for row in rows)
o=dict(scope='discovery only; numerical upper not certified',solver_status=int(r.status),message=str(r.message),original_triples=triples,cyclic_cuts=len(cycles),fixed_word=[0,1,2,3],witness_size=len(ids),numerical_upper=None if getattr(r,'mip_dual_bound',None) is None else float(-r.mip_dual_bound),witness=[W[i] for i in ids],seconds=round(time.monotonic()-start,3))
print(json.dumps(o),flush=True);Path(__file__).with_name('cycle_strengthened_probe.json').write_text(json.dumps(o,indent=2)+'\n')
