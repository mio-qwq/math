"""Exact six-state compatibility experiment for palette (1,2,2,4)."""
from itertools import product
import json
states=[(a,b) for a in range(3) for b in range(3) if a!=b];n=len(states)
P=tuple(sum(1<<j for j,(b,c) in enumerate(states) if b==s[1] and (c==0 or c!=s[0])) for s in states)
def mul(A,B):return tuple(__import__('functools').reduce(int.__or__,(B[j] for j in range(n) if row>>j&1),0) for row in A)
def diag(A):return any(row>>i&1 for i,row in enumerate(A))
pow=tuple(1<<i for i in range(n));rs={}
for k in range(1,17):
 pow=mul(pow,P)
 if k>=3:
  L=k-1;R=pow
  if L==2:R=tuple(row & sum(1<<j for j,s in enumerate(states) if not(0 in states[i] and 0 in s)) for i,row in enumerate(R))
  rs[L]=R
print('states',states,'P',P,'relations',rs,flush=True)
gens=list(dict.fromkeys(rs.values()));seen={A:(L,) for L,A in rs.items()};queue=list(seen)
for A in queue:
 if not diag(A):print('EMPTY TRACE',seen[A],A,flush=True)
 for B in gens:
  C=mul(A,B)
  if C not in seen:
   seen[C]=seen[A]+(next(L for L,R in rs.items() if R==B),);queue.append(C)
 if len(seen)>100000:print('CAP',len(seen),flush=True);break
else:print('CLOSED NORMAL SEMIGROUP (zero-trace states listed above)',len(seen),flush=True)
