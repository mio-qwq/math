"""Discovery gate for independent deletion leaving a 3-degenerate original square.
Unlike the rejected maximum-degree criterion, this allows large initial degrees.
Stop at the first obstruction; no universal coloring inference from finite success.
"""
from itertools import combinations
from collections import Counter
from pathlib import Path
import json,time

def matchings(vertices,edges):
 if not vertices:yield [];return
 u=min(vertices)
 for v in sorted(vertices-{u}):
  if tuple(sorted((u,v))) in edges:
   for rest in matchings(vertices-{u,v},edges):yield [(u,v)]+rest

def core_graphs():
 yield 'K4',4,set(combinations(range(4),2))
 yield 'K33',6,{(u,v) for u in range(3) for v in range(3,6)}
 yield 'cube',8,{(u,v) for u in range(8) for v in range(u+1,8) if (u^v).bit_count()==1}
 yield 'Wagner',8,{tuple(sorted((i,(i+d)%8))) for i in range(8) for d in (1,4)}
 yield 'pentagonal_prism',10,{tuple(sorted(e)) for i in range(5) for e in [(i,(i+1)%5),(i+5,(i+1)%5+5),(i,i+5)]}
 yield 'Petersen',10,{tuple(sorted(e)) for i in range(5) for e in [(i,(i+1)%5),(i+5,(i+2)%5+5),(i,i+5)]}

def independent_sets(adj,remaining,chosen=0):
 if not remaining:yield chosen;return
 bit=remaining&-remaining;u=bit.bit_length()-1
 yield from independent_sets(adj,remaining^bit,chosen)
 yield from independent_sets(adj,(remaining^bit)&~adj[u],chosen|bit)

def degeneracy(F,remaining):
 maximum=0;order=[]
 while remaining:
  vs=[i for i in range(len(F)) if remaining>>i&1]
  u=min(vs,key=lambda i:(F[i]&remaining).bit_count());maximum=max(maximum,(F[u]&remaining).bit_count())
  remaining^=1<<u;order.append(u)
 return maximum,order

if __name__=='__main__':
 start=time.monotonic();reports=[]
 for name,n0,E in core_graphs():
  for matching in matchings(set(range(n0)),E):
   es=sorted(E-set(matching));n=n0
   for u,v in matching:es.extend([(u,n),(v,n)]);n+=1
   adj=[0]*n
   for u,v in es:adj[u]|=1<<v;adj[v]|=1<<u
   F=adj[:]
   for u in range(n):
    for v in range(n):
     if adj[u]>>v&1:F[u]|=adj[v]
    F[u]&=~(1<<u)
   full=(1<<n)-1;hist=Counter();best=(n,None,None)
   for I in independent_sets(adj,full):
    d,order=degeneracy(F,full^I);hist[d]+=1
    if d<best[0]:best=(d,I,order)
    if d<=3:break
   row=dict(core=name,vertices=n,matching=matching,best_degeneracy=best[0],independent_sets_tested=sum(hist.values()))
   reports.append(row);print(json.dumps(row),flush=True)
   if best[0]>3:
    out=dict(scope='restricted 3-degeneracy route obstruction, original coloring undecided',vertices=n,edges=es,core=name,matching=matching,minimum_degeneracy=best[0],histogram=dict(hist),reports=reports,seconds=round(time.monotonic()-start,3))
    Path(__file__).with_name('degeneracy_route_probe.json').write_text(json.dumps(out,indent=2)+'\n')
    raise SystemExit(0)
 print(json.dumps(dict(scope='finite gate only',reports=len(reports),seconds=round(time.monotonic()-start,3))),flush=True)
