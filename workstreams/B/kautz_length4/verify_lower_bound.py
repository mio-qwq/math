"""Independent of discovery: original words, ordered-pair adjacency and BFS."""
from itertools import product
from collections import deque,Counter
from math import comb
import json,platform

def check(m,mode="ordered"):
 words=[w for w in product(range(m),repeat=4) if all(w[i]!=w[i+1] for i in range(3))]
 adj=[[j for j,v in enumerate(words) if u[1:]==v[:-1]] for u in words]
 ids=[i for i,(a,b,c,d) in enumerate(words) if (a==c and b==d and a<b) or (a>b and a>c and d>=b and d>c and b!=c)]
 if mode=="blocks":
  a=m//2;b=m-a;patterns={(0,0,1,0),(0,1,1,0),(0,1,1,1)}
  ids=[i for i,w in enumerate(words) if tuple(int(x>=a) for x in w) in patterns]
  assert len(ids)==a*b*((m-1)**2-a*b)
 else:assert len(ids)==comb(m,2)+3*comb(m,3)+4*comb(m,4)
 selected=set(ids);distances={}
 for s in ids:
  D=[-1]*len(words);D[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if D[v]<0:D[v]=D[u]+1;q.append(v)
  assert all(0<=d<=4 for d in D)
  assert not selected.intersection(adj[s]);distances[s]=D
  if mode=="blocks":assert all(D[t]>=3 for t in selected-{s})
 tests=0
 for v in ids:
  pred=[u for u in ids if u!=v and distances[u][v]==2]
  succ=[z for z in ids if z!=v and distances[v][z]==2]
  for u in pred:
   for z in succ:
    if u!=z:
     assert distances[u][z]!=4;tests+=1
 # Exhaustiveness: independence and diameter4 leave only 2+2=4.
 return {'m':m,'mode':mode,'vertices':len(words),'selected':len(ids),'BFS_rows':len(ids),'two_step_pairs':tests}

def controls():
 # Independent does NOT imply GP in diameter4: these three words refute it.
 u,v,w=(0,1,0,2),(0,2,1,0),(1,0,1,2)
 def d(a,b):
  if a==b:return 0
  return next((s for s in range(1,4) if a[s:]==b[:-s]),4)
 # Search the small original graph for a genuine independent non-GP triple.
 W=[x for x in product(range(3),repeat=4) if all(x[i]!=x[i+1] for i in range(3))]
 bad=next((a,b,c) for a in W for b in W for c in W if len({a,b,c})==3 and all(d(x,y)>=2 for x,y in [(a,b),(a,c),(b,a),(b,c),(c,a),(c,b)]) and d(a,b)+d(b,c)==d(a,c))
 assert d(bad[0],bad[1])+d(bad[1],bad[2])==d(bad[0],bad[2])
 assert comb(3,2)+3*comb(3,3)+4*comb(3,4)==6<7
 return {'independent_not_GP':bad,'not_exact_m3':True}
if __name__=='__main__':
 print(json.dumps({'python':platform.python_version(),'checks':[check(m,mode) for mode in ('ordered','blocks') for m in range(3,7)],'negative_controls':controls(),'status':'PASS','scope':'finite original-definition supplement to universal analytical proof'},sort_keys=True))
