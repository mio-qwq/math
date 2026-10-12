"""Discovery only: finite marginals of a 3-dependent 2-in-5 process.
No numerical result from this script is a rigorous universal certificate.
"""
import sys,time,json
import numpy as np
from scipy.sparse import coo_matrix
from scipy.optimize import linprog

def allowed(n):
 a=[0]
 for k in range(n):
  a=[(x<<1)|b for x in a for b in (0,1) if (((x<<1)|b)&31).bit_count()<=2]
 return a

def matrix(n,p):
 words=allowed(n); nvar=len(words); rows=[];cols=[];vals=[]; rhs=[]
 def row(terms,b):
  r=len(rhs);rhs.append(b)
  for j,v in terms:
   if v: rows.append(r); cols.append(j); vals.append(v)
 row(((j,1) for j in range(nvar)),1)
 row(((j,(x&1)-p) for j,x in enumerate(words)),0)
 # Stationarity of consecutive (n-1)-marginals.
 bins={}
 for j,x in enumerate(words):
  bins.setdefault(x>>1,[]).append((j,1))
  bins.setdefault(x&((1<<(n-1))-1),[]).append((j,-1))
 for k,terms in bins.items(): row(terms,0)
 # Each singleton is independent of its joint remote exterior.
 for i in range(n):
  mask=sum(1<<j for j in range(n) if abs(i-j)>=4)
  if not mask:continue
  bins={}
  for j,x in enumerate(words):
   bins.setdefault(x&mask,[]).append((j,((x>>i)&1)-p))
  for k,terms in bins.items():row(terms,0)
 A=coo_matrix((vals,(rows,cols)),shape=(len(rhs),nvar)).tocsr()
 return words,A,np.array(rhs)

def run(n,p):
 t=time.monotonic();words,A,b=matrix(n,p)
 result=linprog(np.zeros(len(words)),A_eq=A,b_eq=b,bounds=(0,None),method='highs',options={'time_limit':25})
 print(json.dumps({'n':n,'p':p,'variables':len(words),'rows':A.shape[0],'status':result.status,'message':result.message,'seconds':time.monotonic()-t}))
 return result
if __name__=='__main__':
 n=int(sys.argv[1]);
 for p in map(float,sys.argv[2:]):run(n,p)
