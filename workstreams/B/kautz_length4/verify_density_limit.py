"""Independent-definition checks for seven-window bounds and alphabet averaging.
Standard library; no imports from any B proof/discovery checker or solver.
"""
from itertools import product,permutations,combinations
from collections import deque,Counter
import math,json,platform

def graph(m):
 W=[w for w in product(range(m),repeat=4) if all(w[i]!=w[i+1] for i in range(3))]
 ix={w:i for i,w in enumerate(W)}
 adj=[[ix[w[1:]+(x,)] for x in range(m) if x!=w[-1]] for w in W]
 return W,ix,adj

def bfs(a,s):
 d=[-1]*len(a);d[s]=0;q=deque([s])
 while q:
  u=q.popleft()
  for v in a[u]:
   if d[v]<0:d[v]=d[u]+1;q.append(v)
 assert min(d)>=0
 return d

counts=[];triples=0;pairs=0;entries=0;controls=0
for m in (7,8):
 W,ix,a=graph(m)
 windows=[tuple((i+j)%7 for j in range(4)) for i in range(7)]
 D=[bfs(a,ix[w]) for w in windows];indices=[ix[w] for w in windows]
 entries+=7*len(W)
 for i in range(7):
  for offset in range(1,5):
   assert D[i][indices[(i+offset)%7]]==offset;pairs+=1
 for tri in combinations(range(7),3):
  assert any(D[u][indices[v]]+D[v][indices[w]]==D[u][indices[w]] for u,v,w in permutations(tri));triples+=1
 # A deliberately selected triple fails GP in the full original graph.
 assert D[0][indices[1]]+D[1][indices[2]]==D[0][indices[2]];controls+=1
 freq=Counter();tuples=0
 for p in permutations(range(m),7):
  tuples+=1
  for i in range(7):freq[tuple(p[(i+j)%7] for j in range(4))]+=1
 expected=7*math.prod(range(m-6,m-3))
 assert len(freq)==math.prod(range(m-3,m+1)) and set(freq.values())=={expected}
 assert expected*math.prod(range(m-3,m+1))==7*tuples
 counts.append(dict(m=m,ordered_seven_tuples=tuples,four_letter_words=len(freq),inclusion_multiplicity=expected))

# Verify alphabet inclusion multiplicities directly for all 5-subsets of 7 symbols.
freq=Counter()
for subset in combinations(range(7),5):
 for w in permutations(subset,4):freq[w]+=1
assert len(freq)==840 and set(freq.values())=={3}
assert 3*840==math.comb(7,5)*120

# Negative control: replacing seven by eight windows does NOT justify capacity2.
W,ix,a=graph(8);words=[tuple((i+j)%8 for j in range(4)) for i in (0,3,6)]
D=[bfs(a,ix[w]) for w in words]
assert all(D[u][ix[words[v]]]+D[v][ix[words[w]]]!=D[u][ix[words[w]]] for u,v,w in permutations(range(3)))
controls+=1
print(json.dumps(dict(status='PASS',python=platform.python_version(),seven_window_triples=triples,short_offset_pairs=pairs,bfs_distance_entries=entries+3*len(W),cycle_incidence_checks=counts,alphabet_subset_words=840,alphabet_subset_multiplicity=3,negative_controls=controls,scope='finite original-definition checks; universal proof in DENSITY_LIMIT.md, pending independent review'),sort_keys=True))
