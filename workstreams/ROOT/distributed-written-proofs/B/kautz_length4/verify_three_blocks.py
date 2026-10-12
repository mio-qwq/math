"""Exact universal finite-state certificate plus independent original BFS tests.
No discovery import, SciPy, floating arithmetic or presumed shortest-path formula.
"""
from itertools import product
from collections import deque,Counter
from pathlib import Path
import json,platform,copy
HERE=Path(__file__).resolve().parent

def certificate(c):
 P=set(map(tuple,c['patterns']));assert len(P)==16
 assert all(len(p)==4 and all(x in (0,1,2) for x in p) for p in P)
 states=list(product(range(3),repeat=3));assert c['states']==[list(s) for s in states]
 # Backward Bellman recurrence, using a different orientation to discovery.
 d={s:0 for s in states}; maxima=[0]
 for t in range(1,6):
  d={s:max(int(s+(x,) in P)+d[s[1:]+(x,)] for x in (0,1,2)) for s in states}
  maxima.append(max(d.values()))
 assert maxima==[0,1,1,2,2,2]
 # Check submitted FORWARD state-specific table as well.
 f={s:0 for s in states};assert c['max_window_counts_by_steps'][0]==list(f.values())
 for t in range(1,6):
  f={s:max(int((x,)+s in P)+f[(x,)+s[:2]] for x in (0,1,2)) for s in states}
  assert c['max_window_counts_by_steps'][t]==list(f.values())
 assert max(f.values())==2
 hist=Counter()
 for w in product(range(3),repeat=8):
  k=sum(w[i:i+4] in P for i in range(5));assert k<=2;hist[k]+=1
 return P,dict(hist)

def original(sizes,P):
 m=sum(sizes);blocks=[i for i,n in enumerate(sizes) for _ in range(n)]
 W=[w for w in product(range(m),repeat=4) if all(w[i]!=w[i+1] for i in range(3))]
 ids=[i for i,w in enumerate(W) if tuple(blocks[x] for x in w) in P]
 count=0
 for p in P:
  n=sizes[p[0]]
  for i in range(1,4):n*=sizes[p[i]]-int(p[i]==p[i-1])
  count+=n
 assert count==len(ids)
 a,b,c=sizes
 if b==c:assert count==b*(a**3+4*a*a*b-3*a*a+8*a*b*b-9*a*b+2*a+3*b**3-4*b*b+b)
 adj=[[j for j,v in enumerate(W) if w[1:]==v[:-1]] for w in W]
 D={}
 for s in ids:
  ds=[-1]*len(W);ds[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if ds[v]<0:ds[v]=ds[u]+1;q.append(v)
  assert all(0<=x<=4 for x in ds);D[s]=ds
 tests=0
 for u in ids:
  for v in ids:
   if u==v:continue
   for z in ids:
    if z!=u and z!=v:
     assert D[u][v]+D[v][z]!=D[u][z];tests+=1
 return {'sizes':sizes,'vertices':len(W),'selected':count,'ordered_triples':tests}

def run():
 c=json.loads((HERE/'three_block_certificate.json').read_text());P,hist=certificate(c)
 checks=[original(s,P) for s in [(1,1,1),(1,1,2),(1,2,2),(2,2,2)]]
 rejected=0
 for bad in [dict(c,patterns=c['patterns']+[[0,0,0,0]]),copy.deepcopy(c)]:
  if len(bad['patterns'])==16:bad['max_window_counts_by_steps'][5][0]=99
  try:certificate(bad)
  except AssertionError:rejected+=1
  else:raise AssertionError('accepted corrupt certificate')
 assert rejected==2
 print(json.dumps({'python':platform.python_version(),'status':'PASS','universal_block_words':3**8,'histogram':hist,'state_transitions_each_direction':27*3*5,'original_checks':checks,'rejected_controls':rejected},sort_keys=True))
if __name__=='__main__':run()
