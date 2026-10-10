"""Discovery only: optimize rank-pattern-uniform GP constructions.
Numerical optimization is not an original upper-bound certificate.
"""
from itertools import combinations
from math import comb
import json,time

def patterns(n):
 if n==1:
  yield (0,);return
 for w in patterns(n-1):
  r=max(w)+1
  for x in range(r):
   if x!=w[-1]:yield w+(x,)
  for x in range(r+1):yield tuple(a+(a>=x) for a in w)+(x,)

def rank(w):
 d={x:i for i,x in enumerate(sorted(set(w)))}
 return tuple(d[x] for x in w)

def distance(u,v):
 if u==v:return 0
 return next((d for d in range(1,4) if u[d:]==v[:-d]),4)

def main():
 import numpy as np
 from scipy.optimize import milp,Bounds,LinearConstraint
 P=sorted(patterns(4));idx={p:i for i,p in enumerate(P)};constraints=set();counts={}
 for L in range(2,5):
  count=0
  for w in patterns(4+L):
   count+=1
   if distance(w[:4],w[-4:])!=L:continue
   for i in range(1,L):
    vs=(w[:4],w[i:i+4],w[-4:])
    if len(set(vs))!=3:continue
    # For binary choices, all involved types cannot simultaneously be selected.
    constraints.add(tuple(sorted({idx[rank(v)] for v in vs})))
  counts[L]=count
 rows=sorted(constraints);A=np.zeros((len(rows),len(P)))
 for j,c in enumerate(rows):A[j,list(c)]=1
 bound=np.array([len(c)-1 for c in rows])
 print(json.dumps({'patterns':len(P),'constraints':len(rows),'geodesic_word_pattern_counts':counts}),flush=True)
 for m in (3,4,5,8,30):
  weights=np.array([comb(m,len(set(p))) if len(set(p))<=m else 0 for p in P])
  t=time.time();r=milp(-weights.astype(float),integrality=np.ones(len(P)),bounds=Bounds(0,1),constraints=LinearConstraint(A,-np.inf,bound),options={'time_limit':10})
  selected=[] if r.x is None else [P[i] for i,x in enumerate(r.x) if x>.5]
  ids={idx[p] for p in selected};assert all(not set(c)<=ids for c in rows)
  ans={'m':m,'solver_status':int(r.status),'message':str(r.message),'seconds':round(time.time()-t,3),'size':sum(comb(m,len(set(p))) for p in selected),'coefficients':[sum(len(set(p))==j for p in selected) for j in (2,3,4)],'selected':selected}
  print(json.dumps(ans),flush=True)
 if True:
  with open('workstreams/B/kautz_length4/order_pattern_candidate.json','w') as f:json.dump({'patterns':selected,'counts':counts,'constraint_count':len(rows)},f,indent=2);f.write('\n')
if __name__=='__main__':main()
