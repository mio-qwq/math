"""Constructive proof for line graphs of complete graphs; discovery-independent."""
from itertools import combinations
from collections import Counter

def dist(a,b):return 0 if a==b else (1 if set(a)&set(b) else 2)
def gp(V):
 return all(dist(a,b)+dist(b,c)!=dist(a,c) and dist(a,c)+dist(c,b)!=dist(a,b) and dist(b,a)+dist(a,c)!=dist(b,c) for a,b,c in combinations(V,3))
def extension(n,V):
 V=list(dict.fromkeys(V));return next((e for e in combinations(range(n),2) if e not in V and gp(V+[e])),None)
def construct(n,m,S):
 k=len(S);assert k>=4 and n>=2*k-1 and m>=2*k-1
 assert k<(n//2 if n%2==0 else (n+3)//2) and k<(m//2 if m%2==0 else (m+3)//2)
 for side,r,t in ((0,n,m),(1,m,n)):
  A=[s[side] for s in S];B=[s[1-side] for s in S];distinct=list(dict.fromkeys(A))
  if len(distinct)==k and gp(distinct):
   u=extension(r,distinct);assert u is not None;v=B[0];mode='distinct_gp'
  elif len(distinct)==k-1 and gp(distinct):
   i,j=next((i,j) for i,j in combinations(range(k),2) if A[i]==A[j])
   u=extension(r,distinct);v=extension(t,[B[i],B[j]]);assert u is not None and v is not None;mode='one_repeated_gp'
  elif len(distinct)==k:
   used=set().union(*map(set,A));unused=sorted(set(range(r))-used)
   assert unused
   if len(unused)>=2:
    u=tuple(unused[:2]);v=next(e for e in combinations(range(t),2) if e not in B);mode='distinct_two_unused'
   else:
    degrees=Counter(x for e in A for x in e)
    i=next(i for i,e in enumerate(A) if all(degrees[x]==1 for x in e))
    u=tuple(sorted((unused[0],A[i][0])))
    v=next(e for e in combinations(range(t),2) if e not in B and set(e).isdisjoint(B[i]));mode='critical_one_unused'
  else:continue
  return ((u,v) if side==0 else (v,u)),mode+'_'+str(side)
 U=sorted(set(range(n))-set().union(*(set(a) for a,b in S)))
 V=sorted(set(range(m))-set().union(*(set(b) for a,b in S)))
 assert len(U)>=3 and len(V)>=3
 return (tuple(U[:2]),tuple(V[:2])),'both_unused'
