"""A separate restrictive construction: at most two selected windows per4 shifts.
Generic distinct letters make block constraints necessary for full block templates
when every block has at least8 symbols. This is not a full GP upper bound.
"""
from itertools import product
import json
P=list(product(range(2),repeat=4));index={p:i for i,p in enumerate(P)}
constraints=set()
for L in range(2,5):
 for w in product(range(2),repeat=4+L):
  for i in range(1,L):constraints.add(sum(1<<j for j in {index[w[:4]],index[w[i:i+4]],index[w[-4:]]}))
valid=[s for s in range(1<<16) if all(s&c!=c for c in constraints)]
rows=[]
for m in [4,6,12,40]:
 best=(-1,None)
 for a in range(1,m):
  sizes=[a,m-a];weights=[]
  for p in P:
   n=sizes[p[0]]
   for i in range(1,4):n*=sizes[p[i]]-(p[i]==p[i-1])
   weights.append(n)
  for s in valid:
   value=sum(weights[i] for i in range(16) if s>>i&1)
   if value>best[0]:best=(value,{'block_sizes':sizes,'patterns':[P[i] for i in range(16) if s>>i&1]})
 rows.append({'m':m,'best_restricted':best[0],**best[1],'order_pattern_lower':m*(m-1)*(m*m-2*m+3)//6})
print(json.dumps({'valid_code_subsets':len(valid),'constraints':len(constraints),'results':rows}))
