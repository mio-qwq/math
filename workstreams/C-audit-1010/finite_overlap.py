#!/usr/bin/env python3
"""Exact 6-vertex labelled normal form and duplicate minimal TF patterns.
Independent of orbit-theory checker. Standard library only.
"""
from itertools import combinations
from collections import Counter, defaultdict
N=6
es=list(combinations(range(N),2));ix={x:i for i,x in enumerate(es)}
def edge_mask(edges):return sum(1<<ix[tuple(sorted(e))] for e in edges)
def isgood(mask):
 A=[0]*N
 for i,(u,v) in enumerate(es):
  if mask>>i&1:A[u]|=1<<v;A[v]|=1<<u
 if len(set(A))!=N:return False
 d=[-1]*N;d[0]=0;todo=[0];odd=False
 for v in todo:
  for u in range(N):
   if A[v]>>u&1:
    if d[u]<0:d[u]=1-d[v];todo.append(u)
    elif d[u]==d[v]:odd=True
 return len(todo)==N and odd

occ=defaultdict(int)
for four in combinations(range(N),4):
 for pair in [tuple(x for x in four if x in e) for e in []]:pass
 # three unlabelled partitions into two 2-subsets
 pairs=set()
 for ab in combinations(four,2):
  cd=tuple(x for x in four if x not in ab)
  pairs.add(tuple(sorted((tuple(ab),tuple(cd)))))
 assert len(pairs)==3
 for A,B in pairs:
  W=tuple(x for x in range(N) if x not in four)
  for ed0 in range(2):
   for attA in range(4):
    for attB in range(4):
     for k in range(2):
      ed=[]
      if ed0:ed.append((W[0],W[1]))
      for i,w in enumerate(W):
       if attA>>i&1:ed.extend([(A[0],w),(A[1],w)])
       if attB>>i&1:ed.extend([(B[0],w),(B[1],w)])
      ed.extend([(A[0],B[k]),(A[1],B[k^1])])
      occ[edge_mask(ed)]+=1
print('total occurrences',sum(occ.values()))
print('distinct labelled',len(occ),'multiplicity',Counter(occ.values()))
print('qualifying',sum(isgood(mask) for mask in occ),
      'multi qualifying',sum(isgood(mask) and k>1 for mask,k in occ.items()))
assert sum(occ.values())==3*15*64
assert any(k>1 for k in occ.values())
