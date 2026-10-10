"""Construct a finite invariant for the second requested packing palette."""
import json
from pathlib import Path
pairs=[(a,b) for a in range(3) for b in range(3) if a!=b]
P=tuple(sum(1<<j for j,(b,c) in enumerate(pairs) if b==s[1] and (c==0 or c!=s[0])) for s in pairs)
def mul(A,B):
 rows=[]
 for row in A:
  ans=0
  for j in range(6):
   if row>>j&1:ans|=B[j]
  rows.append(ans)
 return tuple(rows)
def add(A,B):return tuple(x|y for x,y in zip(A,B))
I=tuple(1<<i for i in range(6));Z=(0,)*6;power=I;R={}
for k in range(1,12):
 power=mul(power,P)
 if k>=3:
  L=k-1;R[L]=power
  if L==2:R[L]=tuple(row & sum(1<<j for j,s in enumerate(pairs) if not(0 in pairs[i] and 0 in s)) for i,row in enumerate(power))
E=tuple(40 if i in (3,5) else 0 for i in range(6))
seen={(I,Z)};queue=[(I,Z)]
for A,B in queue:
 for L in range(2,11):
  C=mul(A,R[L]);D=mul(B,R[L])
  if L==4:D=add(D,mul(A,E))
  state=(C,D)
  if state not in seen:seen.add(state);queue.append(state)
assert len(seen)==139
cert={'encoding':'six row bitmasks for A, then six for B; fixed pair order 01,02,10,12,20,21','states':[list(A+B) for A,B in sorted(seen)]}
p=Path(__file__).with_name('transfer_certificate.json');p.write_text(json.dumps(cert,indent=2)+'\n');print('Generated',len(seen),'invariant states')
