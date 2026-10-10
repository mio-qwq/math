from transfer_probe import mul,diag,rs
I=tuple(1<<i for i in range(6));Z=(0,)*6
E=tuple(40 if i in (3,5) else 0 for i in range(6))
def add(A,B):return tuple(a|b for a,b in zip(A,B))
seen={(I,Z):()};queue=[(I,Z)]
for A,B in queue:
 word=seen[(A,B)]
 if word and not(diag(A) or diag(B)):print('FAILED',word,A,B)
 for L in range(2,11):
  C=mul(A,rs[L]);D=mul(B,rs[L])
  if L==4:D=add(D,mul(A,E))
  state=(C,D)
  if state not in seen:seen[state]=word+(L,);queue.append(state)
 if len(seen)>100000:print('CAP',len(seen));break
else:print('CLOSED',len(seen),'maximum representative length',max(map(len,seen.values())))
