"""Pure mixed-family extension: first factor intersection, second disjointness."""
from itertools import combinations
from collections import Counter

def d(a,b,intersect):return 0 if a==b else (1 if bool(set(a)&set(b))==intersect else 2)
def gp(V,intersect):
 return all(d(a,b,intersect)+d(b,c,intersect)!=d(a,c,intersect) and d(a,c,intersect)+d(c,b,intersect)!=d(a,b,intersect) and d(b,a,intersect)+d(a,c,intersect)!=d(b,c,intersect) for a,b,c in combinations(V,3))
def extension(n,V,intersect):
 V=list(dict.fromkeys(V));return next((e for e in combinations(range(n),2) if e not in V and gp(V+[e],intersect)),None)
def construct(n,m,S):
 k=len(S);assert k in (4,5) and n>=2*k-1 and m>=2*k+2
 assert k<(n//2 if n%2==0 else (n+3)//2)
 A=[a for a,b in S];B=[b for a,b in S];unique=list(dict.fromkeys(A))
 if len(unique)==k and gp(unique,True):
  u=extension(n,unique,True);assert u is not None;return (u,B[0]),'distinct_gp'
 if len(unique)==k-1 and gp(unique,True):
  i,j=next((i,j) for i,j in combinations(range(k),2) if A[i]==A[j])
  u=extension(n,unique,True);v=extension(m,[B[i],B[j]],False)
  assert u is not None and v is not None;return (u,v),'one_repeated_gp'
 U=sorted(set(range(n))-set().union(*map(set,A)));V=sorted(set(range(m))-set().union(*map(set,B)))
 assert len(V)>=2
 if len(unique)==k and len(U)==1:
  degrees=Counter(x for a in A for x in a)
  i=next(i for i,a in enumerate(A) if all(degrees[x]==1 for x in a))
  u=tuple(sorted((U[0],A[i][0])))
  v=next(e for e in combinations(range(m),2) if e not in B and len(set(e)&set(B[i]))==1)
  return (u,v),'critical_one_unused'
 assert len(U)>=2
 return (tuple(U[:2]),tuple(V[:2])),'constant_three'
