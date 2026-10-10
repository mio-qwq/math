"""Exact fresh graph replay and optimizer checks; no imported project code."""
from itertools import permutations
from collections import deque,Counter
from math import prod
import json,platform

def falling(n,r):return prod(range(n-r+1,n+1))
params=0
for k in range(3,31):
 for d in range(2*k,501):
  values=[t*falling(d+k-t,k-1) for t in range(1,d+2)]
  best=max(values)
  arg=[i+1 for i,v in enumerate(values) if v==best]
  t=(d+1+k-1)//k
  assert arg==([t,t+1] if (d+1)%k==0 else [t]);params+=1
k,d,t=3,9,4;N=d+k
words=list(permutations(range(N),k));idx={w:i for i,w in enumerate(words)}
adj=[[idx[w[1:]+(b,)] for b in range(N) if b not in w] for w in words]
selected=[i for i,w in enumerate(words) if all(x<N-t for x in w[:-1]) and w[-1]>=N-t]
assert len(words)==1320 and len(selected)==224
hist=Counter();checks=0
for s in selected:
 dist=[-1]*len(words);dist[s]=0;q=deque([s])
 while q:
  u=q.popleft()
  for v in adj[u]:
   if dist[v]<0:dist[v]=dist[u]+1;q.append(v)
 for v in selected:
  if v==s:continue
  hist[dist[v]]+=1;checks+=1
assert min(hist)>=3 and max(hist)<=5
# The strict gap proves every ordered distinct triple, without cubic looping.
assert 2*min(hist)>max(hist)
assert len(selected)>2*falling(N-2,k-1)
# Negative optimizer claims: a non-maximizing t and false uniqueness at a tie.
assert 3*falling(9,2)<224
assert 3*falling(8,2)==4*falling(7,2) # d=8,k=3 ties t=3,4
print(json.dumps({'status':'PASS','python':platform.python_version(),'integer_parameter_cases':params,
 'vertices':len(words),'arcs':sum(map(len,adj)),'selected':len(selected),
 'ordered_selected_pairs':checks,'distance_histogram':dict(hist),'source_proposed_value':180,
 'strict_gap_gp_check':True,'negative_optimizer_controls':2},sort_keys=True))
