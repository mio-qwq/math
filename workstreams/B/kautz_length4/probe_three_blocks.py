"""Discovery only: fixed3-block sufficient window code, not original exactness."""
from itertools import product
import json,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
P=list(product(range(3),repeat=4));idx={p:i for i,p in enumerate(P)};C=set()
for L in range(2,5):
 for w in product(range(3),repeat=4+L):
  for i in range(1,L):C.add(tuple(sorted({idx[w[:4]],idx[w[i:i+4]],idx[w[-4:]]})))
C=sorted(C);A=lil_matrix((len(C),len(P)))
for j,c in enumerate(C):A[j,list(c)]=1
A=A.tocsc();bounds=np.array([len(c)-1 for c in C])
print(json.dumps({'patterns':len(P),'constraints':len(C)}),flush=True)
for sizes in [(2,2,2),(10,10,10),(8,11,11)]:
 weights=[]
 for p in P:
  w=sizes[p[0]]
  for i in range(1,4):w*=sizes[p[i]]-(p[i]==p[i-1])
  weights.append(w)
 t=time.time();r=milp(-np.array(weights,dtype=float),integrality=np.ones(len(P)),bounds=Bounds(0,1),constraints=LinearConstraint(A,-np.inf,bounds),options={'time_limit':10})
 selected=[] if r.x is None else [i for i,x in enumerate(r.x) if x>.5]
 assert all(not set(c)<=set(selected) for c in C)
 print(json.dumps({'sizes':sizes,'status':int(r.status),'seconds':round(time.time()-t,3),'size':sum(weights[i] for i in selected),'patterns':[P[i] for i in selected]}),flush=True)
