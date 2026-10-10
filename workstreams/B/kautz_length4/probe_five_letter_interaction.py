"""Discovery only: unrestricted distinct-letter words on five symbols.
Unlike previous block templates, this includes every subset of these120 words.
A numerical upper bound is NOT an exact certificate.
"""
from itertools import permutations,combinations
from pathlib import Path
import json,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix
W=list(permutations(range(5),4));n=len(W)
def distance(u,v):
    if u==v:return 0
    return next((s for s in range(1,4) if u[s:]==v[:-s]),4)
D=[[distance(u,v) for v in W] for u in W]
bad=[]
for a,b,c in combinations(range(n),3):
    if any(D[u][v]+D[v][w]==D[u][w] for u,v,w in permutations((a,b,c))):bad.append((a,b,c))
rr=[];cc=[]
for i,t in enumerate(bad):
    rr.extend([i]*3);cc.extend(t)
A=coo_matrix((np.ones(len(rr)),(rr,cc)),shape=(len(bad),n)).tocsc()
start=time.monotonic()
r=milp(-np.ones(n),integrality=np.ones(n),bounds=Bounds(0,1),constraints=LinearConstraint(A,-np.inf,2),options={'time_limit':20})
ids=[] if r.x is None else [i for i,x in enumerate(r.x) if x>.5]
chosen=set(ids);assert all(not set(t)<=chosen for t in bad)
out=dict(vertices=n,forbidden_triples=len(bad),solver_status=int(r.status),message=str(r.message),witness_size=len(ids),numerical_upper=None if getattr(r,'mip_dual_bound',None) is None else float(-r.mip_dual_bound),seconds=round(time.monotonic()-start,3),witness=[W[i] for i in ids],scope='discovery only; numerical upper is not certified')
print(json.dumps(out),flush=True)
Path(__file__).with_name('five_letter_interaction_probe.json').write_text(json.dumps(out,indent=2)+'\n')
