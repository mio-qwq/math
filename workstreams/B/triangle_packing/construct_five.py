"""Realize five-color relations and verify actual original-graph distances."""
from pathlib import Path
from itertools import product
import json
from explore import graph
from verify_five import distances,valid,RAD
from verify_colored_graph import verify_original
raw=json.loads(Path(__file__).with_name('five_relations.json').read_text());S=[tuple(w) for w in raw['states']];R={int(k):v for k,v in raw['relations'].items()}

def bridge(s,t,L):
 path=[1]+list(range(8,8+L-1))+[3];n=8+L-1
 E=[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(6,0),(4,7)]+list(zip(path,path[1:]));D=distances(n,E)
 fixed={}
 for u,c in list(zip((6,0,2,1,path[1]),s))+list(zip((path[-2],3,5,4,7),t)):
  assert u not in fixed or fixed[u]==c;fixed[u]=c
 free=[u for u in path if u not in fixed]
 def rec(i):
  if i==len(free):return [fixed[u] for u in path[1:-1]]
  u=free[i]
  for c in range(4):
   if all(c!=d or D[u][v]>RAD[c] for v,d in fixed.items()):
    fixed[u]=c;ans=rec(i+1)
    if ans is not None:return ans
    del fixed[u]
  return None
 ans=rec(0);assert ans is not None;return ans

def construct(gaps):
 g=graph(gaps,'cycle');m=len(gaps)
 if gaps==(2,):return {'adjacency':[sorted(ns) for ns in g.a],'colors':[0,1,2,3],'sequence':[1,2,3,4,5],'gaps':gaps}
 choice=None
 for initial in range(90):
  paths={initial:[]}
  for L in gaps:
   nxt={};matrix=R[min(L,16)]
   for i,hist in paths.items():
    for j in range(90):
     if matrix[i]>>j&1:nxt.setdefault(j,hist+[i])
   paths=nxt
  if initial in paths:choice=paths[initial];break
 assert choice is not None
 cs=[]
 for i in choice:cs.extend([S[i][1],S[i][3],S[i][2]])
 for k,L in enumerate(gaps):cs.extend(bridge(S[choice[k]],S[choice[(k+1)%m]],L))
 return {'adjacency':[sorted(ns) for ns in g.a],'colors':cs,'sequence':[1,2,3,4,5],'gaps':gaps}

if __name__=='__main__':
 count=0
 for m in range(1,6):
  for gaps in product(range(2,7),repeat=m):
   if gaps!=min(gaps[i:]+gaps[:i] for i in range(m)):continue
   verify_original(construct(gaps));count+=1
 for gaps in [(2,4,2,3),(2,3)*15+(2,4),(2,10,3,11),(23,),(2,4)]:verify_original(construct(gaps));count+=1
 p=Path(__file__).with_name('five_sample.json');p.write_text(json.dumps(construct((2,3,2,4)),indent=2)+'\n')
 print(json.dumps({'result':'PASS','original_necklaces_checked':count,'sequence':[1,2,3,4,5]},indent=2))
