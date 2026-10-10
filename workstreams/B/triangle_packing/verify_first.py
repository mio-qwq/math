"""Original-definition reconstruction and finite invariant check for (1,2,3,3)."""
from itertools import product
from collections import deque
from pathlib import Path
import json,hashlib,copy,sys,time
RAD=(1,2,3,3)

def distances(n,edges):
 a=[set() for _ in range(n)]
 for u,v in edges:a[u].add(v);a[v].add(u)
 D=[]
 for s in range(n):
  ds={s:0};q=deque([s])
  while q:
   u=q.popleft()
   for v in a[u]:
    if v not in ds:ds[v]=ds[u]+1;q.append(v)
  D.append(ds)
 return D

def valid(w,D):return all(w[u]!=w[v] or D[u][v]>RAD[w[u]] for u in range(len(w)) for v in range(u))
def compose(A,B):return tuple(frozenset(k for j in row for k in B[j]) for row in A)
def trace(A):return any(i in row for i,row in enumerate(A))
def masks(A):return tuple(sum(1<<j for j in row) for row in A)
def decode(A,n):
 assert len(A)==n and all(type(row) is int and 0<=row<2**n for row in A)
 return tuple(frozenset(j for j in range(n) if row>>j&1) for row in A)

def relations():
 gadget=[(0,1),(1,2),(1,3),(2,3),(3,4)]
 D=distances(5,gadget);S=[w for w in product(range(4),repeat=5) if valid(w,D)];assert len(S)==42
 pathD=distances(3,[(0,1),(1,2)]);W=[w for w in product(range(4),repeat=3) if valid(w,pathD)];assert len(W)==27
 path4=distances(4,[(0,1),(1,2),(2,3)])
 T=tuple(frozenset(j for j,v in enumerate(W) if u[1:]==v[:2] and valid(u+v[-1:],path4)) for u in W)
 D6=distances(6,gadget+[(4,5)])
 F=tuple(frozenset(W.index(s[3:]+(c,)) for c in range(4) if valid(s+(c,),D6)) for s in S)
 B=tuple(frozenset(j for j,s in enumerate(S) if W.index(w[::-1]) in F[S.index(s[::-1])]) for w in W)
 R={};power=tuple(frozenset([i]) for i in range(27))
 for exponent in range(1,11):
  power=compose(power,T)
  if exponent>=2:R[exponent+2]=compose(compose(F,power),B)
 J=tuple(frozenset(range(27)) for _ in range(27));assert power==J and compose(J,T)==J
 for L in (2,3):
  path=[1]+list(range(8,8+L-1))+[3];n=8+L-1
  edges=[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(6,0),(4,7)]+list(zip(path,path[1:]));D=distances(n,edges)
  slots=(6,0,2,1,path[1]);slots2=(path[-2],3,5,4,7);rows=[]
  for s in S:
   row=set()
   for j,t in enumerate(S):
    assignments=list(zip(slots,s))+list(zip(slots2,t));color={};consistent=True
    for u,c in assignments:
     if u in color and color[u]!=c:consistent=False;break
     color[u]=c
    if consistent and len(color)==n and valid(tuple(color[u] for u in range(n)),D):row.add(j)
   rows.append(frozenset(row))
  R[L]=tuple(rows)
 assert all(trace(R[L]) for L in range(3,13))
 return S,R

def verify(cert,R):
 n=42;C=[decode(A,n) for A in cert['matrices']];CC=set(C)
 assert len(C)==len(CC) and all(trace(A) for A in C)
 for A in R.values():
  for B in R.values():assert compose(A,B) in CC
 for A in CC:
  for B in R.values():assert compose(A,B) in CC
 return {'result':'PASS','invariant_matrices':len(CC),'initial_two_connector_products':len(R)**2,'closure_transitions':len(CC)*len(R),'boundary_states':42,'path_states':27,'long_gap_threshold':12}

def main():
 start=time.monotonic();root=Path(__file__).parent;p=root/'first_invariant.json';cert=json.loads(p.read_text());S,R=relations()
 raw=json.loads((root/'richer_relations.json').read_text());assert [list(s) for s in S]==raw['states']
 assert all(masks(R[L])==tuple(raw['relations'][str(L)]) for L in R)
 out=verify(cert,R);bad=copy.deepcopy(cert);bad['matrices'].pop();negative=[]
 try:verify(bad,R)
 except AssertionError:negative.append('missing invariant matrix rejected')
 else:raise AssertionError('accepted incomplete invariant')
 bad=copy.deepcopy(cert);bad['matrices'].append([0]*42)
 try:verify(bad,R)
 except AssertionError:negative.append('zero-trace matrix rejected')
 else:raise AssertionError('accepted zero-trace matrix')
 out.update(negative_controls=negative,python=sys.version,elapsed=time.monotonic()-start,certificate_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
