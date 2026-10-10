"""Realize the finite invariant as actual original-graph colorings."""
from itertools import permutations,product
from collections import deque
import json
from pathlib import Path
from explore import graph
pairs=list(permutations(range(3),2))

def path_word(a,b,L):
 # Full backbone pair followed by L+1 shifts. Labels 0,1,2 have radii1,2,2.
 current={a:list(a)}
 for _ in range(L+1):
  nxt={}
  for (x,y),word in current.items():
   for z in range(3):
    if z!=y and (z==0 or z!=x):nxt.setdefault((y,z),word+[z])
  current=nxt
 return current.get(b)

def color_necklace(gaps):
 m=len(gaps);options={}
 for L in set(gaps):
  for i,a in enumerate(pairs):
   for j,b in enumerate(pairs):
    w=path_word(a,b,L)
    if w is not None and not(L==2 and 0 in a and 0 in b):options[L,i,j,False]=w[2:-2]
    if L==4 and 0 not in a and 0 not in b:options[L,i,j,True]=[0,3,0]
 chosen=None
 for s in range(6):
  states={(s,False):[]}
  for L in gaps:
   nxt={}
   for (i,used),history in states.items():
    for j in range(6):
     for special in (False,True):
      if used and special:continue
      key=(L,i,j,special)
      if key in options:nxt.setdefault((j,used or special),history+[(i,j,options[key],special)])
   states=nxt
  for used in (False,True):
   if (s,used) in states:chosen=states[s,used];break
  if chosen is not None:break
 assert chosen is not None
 a=graph(gaps,'cycle').a;cols=[]
 for i,j,w,sp in chosen:
  x,y=pairs[i];cols.extend([x,y,3 if 0 in (x,y) else 0])
 for i,j,w,sp in chosen:cols.extend(w)
 return {'gaps':list(gaps),'adjacency':[sorted(ns) for ns in a],'colors':cols,'sequence':[1,2,2,4]}

def verify_original(cert):
 a=cert['adjacency'];c=cert['colors'];s=cert['sequence'];assert len(a)==len(c)
 for u,row in enumerate(a):
  assert len(row)==len(set(row)) and u not in row and len(row)<=3
  assert all(u in a[v] for v in row)
  if len(row)==3:
   assert sum(len(a[v])==3 for v in row)<=1
   assert any(v!=w and w in a[v] for v in row for w in row)
  d={u:0};q=deque([u])
  while q:
   v=q.popleft()
   for w in a[v]:
    if w not in d:d[w]=d[v]+1;q.append(w)
  assert type(c[u]) is int and 0<=c[u]<4
  assert all(v==u or c[v]!=c[u] or dist>s[c[u]] for v,dist in d.items())
 return True

if __name__=='__main__':
 count=0
 for m in range(1,6):
  for gaps in product(range(2,7),repeat=m):
   if gaps!=min(gaps[i:]+gaps[:i] for i in range(m)):continue
   cert=color_necklace(gaps);verify_original(cert);count+=1
 for gaps in [(2,4,2,3),(2,3)*15+(2,4),(2,10,3,11),(23,),(2,4)]:
  verify_original(color_necklace(gaps));count+=1
 p=Path(__file__).with_name('second_sample.json');p.write_text(json.dumps(color_necklace((2,4,2,3)),indent=2)+'\n')
 print(json.dumps({'result':'PASS','original_graph_colorings_checked':count,'palette':[1,2,2,4],'sample':'second_sample.json'},indent=2))
