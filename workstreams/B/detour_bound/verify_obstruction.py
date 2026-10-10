"""Definition-first subset DP, no imports from either discovery program."""
from pathlib import Path
from itertools import combinations
import json,platform
p=Path(__file__).with_name('strong_lemma_obstruction.json');c=json.loads(p.read_text())
n=c['order'];S=c['selected'];adj=[0]*n
assert n==12 and S==[5,7,10]
for u,v in c['edges']:
 assert 0<=u<v<n and not adj[u]>>v&1
 adj[u]|=1<<v;adj[v]|=1<<u
lengths=[[-1]*n for _ in range(n)];unions=[[0]*n for _ in range(n)];states=0
for root in range(n):
 reachable=[0]*(1<<n);reachable[1<<root]=1<<root
 for bits in range(1<<n):
  endpoints=reachable[bits]
  for end in range(n):
   if not endpoints>>end&1:continue
   states+=1;k=bits.bit_count()-1
   if k>lengths[root][end]:lengths[root][end]=k;unions[root][end]=bits
   elif k==lengths[root][end]:unions[root][end]|=bits
   for nxt in range(n):
    if adj[end]>>nxt&1 and not bits>>nxt&1:reachable[bits|1<<nxt]|=1<<nxt
assert all(x>=0 for row in lengths for x in row)
D=max(map(max,lengths));assert D==10
assert lengths==c['detour_lengths'] and unions==c['detour_unions']
def irredundant(T):
 return all(not(unions[a][b]>>z&1) for a,b in combinations(T,2) for z in T if z not in (a,b))
assert irredundant(S)
P=[9,0,1,2,8,10,4,3,5,6,7]
assert len(set(P))==len(P)==D+1 and set(S)<=set(P)
assert all(adj[a]>>b&1 for a,b in zip(P,P[1:]))
# Establish that this graph SATURATES, not violates, the actual numerical bound.
assert all(not irredundant(T) for T in combinations(range(n),4))
assert len(S)==n-D+1
# Reject a corrupt selected set and a false stronger detour diameter.
assert not irredundant([0,1,2]);assert D!=11
print(json.dumps(dict(status='PASS',python=platform.python_version(),order=n,edges=len(c['edges']),diameter=D,detour_irredundance=3,bound=3,selected=S,global_longest_path=P,reachable_subset_endpoint_states=states,four_sets_rejected=495,negative_controls=2,scope='strong every-longest-path lemma is false; original numerical bound NOT refuted'),sort_keys=True))
