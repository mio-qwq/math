"""Constructive universal three-point extension, conditional on factor extensions.
No graph generator or finite-search certificate is imported.
"""
from itertools import combinations

def gp(D,S):
 return all(D[a][b]+D[b][c]!=D[a][c] and D[a][c]+D[c][b]!=D[a][b] and D[b][a]+D[a][c]!=D[b][c] for a,b,c in combinations(S,3))

def extension(D,S):
 S=list(dict.fromkeys(S))
 assert gp(D,S)
 return next((u for u in range(len(D)) if u not in S and gp(D,S+[u])),None)

def extend_three(A,B,S):
 assert len(S)==len(set(S))==3
 def good(z):
  if z in S:return False
  T=S+[z]
  def d(x,y):return A[x[0]][y[0]]+B[x[1]][y[1]]
  return all(d(x,y)+d(y,z)!=d(x,z) and d(x,z)+d(z,y)!=d(x,y) and d(y,x)+d(x,z)!=d(y,z) for x,y,z in combinations(T,3))
 for side,D in ((0,A),(1,B)):
  V=[s[side] for s in S]
  if len(set(V))==3 and gp(D,V):
   u=extension(D,V);assert u is not None
   z=(u,S[0][1]) if side==0 else (S[0][0],u)
   return z,'gp_projection_'+str(side)
 for side,D,E in ((0,A,B),(1,B,A)):
  V=[s[side] for s in S]
  if len(set(V))==2:
   i,j=next((i,j) for i,j in combinations(range(3),2) if V[i]==V[j])
   u=extension(D,V);v=extension(E,[S[i][1-side],S[j][1-side]])
   assert u is not None and v is not None
   return ((u,v) if side==0 else (v,u)),'repeated_projection_'+str(side)
 def middle(D,V):return next(i for i in range(3) if D[V[(i+1)%3]][V[i]]+D[V[i]][V[(i+2)%3]]==D[V[(i+1)%3]][V[(i+2)%3]])
 i=middle(A,[s[0] for s in S]);j=middle(B,[s[1] for s in S]);assert i!=j
 k=next(t for t in range(3) if t not in (i,j));T=[S[k],S[i],S[j]]
 u=extension(A,[T[0][0],T[2][0]]);v=extension(B,[T[0][1],T[1][1]])
 assert u is not None and v is not None
 for number,z in enumerate(((u,T[0][1]),(T[0][0],v),(u,v)),1):
  if good(z):return z,'opposite_middles_'+str(number)
 raise AssertionError('universal three-candidate extension failed')
