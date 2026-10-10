"""Exact finite local certificate; global corollaries use the written proof."""
from itertools import permutations,product
import json
C=range(4);P=set(permutations(C,2));R={(0,1)};rows=[sorted(R)]
for t in range(1,7):
 R={(b,c) for a,b in R for c in C if c not in (a,b)};rows.append(sorted(R))
assert [len(r) for r in rows]==[1,2,4,7,10,11,12] and R==P
# Independently enumerate literal path color words for all initial/end pairs,
# rather than copying the transfer multiplication's reachability.
for L in range(2,8):
 allowed=set()
 for w in product(C,repeat=L+1):
  if all(w[i]!=w[j] for i in range(L+1) for j in range(i+1,min(L+1,i+3))):allowed.add((w[:2],w[-2:]))
 if L==7:assert allowed==set(product(P,P))
 if L==3:
  for p,t,u,q in product(C,repeat=4):
   expected=(p!=t and t!=u and u!=q and p!=u and t!=q)
   assert (((p,t),(u,q)) in allowed)==expected
# Hall assertion tested against all literal port permutations.
local=0
for t in C:
 others=set(C)-{t}
 for neighbors in product(sorted(others),repeat=3):
  choices=[p for p in permutations(others) if all(x!=y for x,y in zip(p,neighbors))]
  assert bool(choices)==(len(set(neighbors))>1);local+=1
# Boundary controls: L=6 is not yet universally flexible; monochrome neighbors fail.
R5=set(map(tuple,rows[5]));assert len(R5)==11 and len(P-R5)==1
assert not any(all(x!=1 for x in p) for p in permutations([1,2,3]))
print(json.dumps({'status':'PASS','reachable_pairs':rows,'local_neighbor_label_cases':local,'negative_controls':2,'scope':'exact connector and Hall certificate; prior dynamic-coloring theorem imported, full Conjecture5 unresolved'}))
