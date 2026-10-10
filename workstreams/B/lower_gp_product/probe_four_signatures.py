"""Local necessary constraints only, not a factor realization or conjecture proof."""
from itertools import combinations,product
from functools import lru_cache
import json,time
from pathlib import Path
P=Path(__file__).parent;start=time.monotonic()
def partitions(n):
 def rec(a):
  if len(a)==n:yield tuple(a);return
  for x in range(max(a)+2):yield from rec(a+[x])
 yield from rec([0])
def gp(D,S):
 return all(D[a][b]+D[b][c]!=D[a][c] and D[a][c]+D[c][b]!=D[a][b] and D[b][a]+D[a][c]!=D[b][c] for a,b,c in combinations(S,3))
def extends(D,S,v):
 return all(v[a]+v[b]!=D[a][b] and abs(v[a]-v[b])!=D[a][b] for a,b in combinations(S,2))
def models():
 out=[]
 for labels in partitions(4):
  q=max(labels)+1;edges=list(combinations(range(q),2))
  for bits in product((1,2),repeat=len(edges)):
   D=[[0]*q for _ in range(q)]
   for (i,j),d in zip(edges,bits):D[i][j]=D[j][i]=d
   V=list(product((1,2),repeat=q));dem=[]
   for mask in range(1,1<<q):
    S=[i for i in range(q) if mask>>i&1]
    if gp(D,S) and all(not gp(D,S+[i]) for i in range(q) if i not in S):
     dem.append(sum(1<<j for j,v in enumerate(V) if extends(D,S,v)))
   out.append(dict(labels=labels,D=D,V=V,dem=dem,known=[tuple(D[i][a] for a in labels) for i in range(q)],external=[tuple(v[a] for a in labels) for v in V]))
 return out
@lru_cache(None)
def hitsets(dem):
 if not dem:return (0,)
 if not dem[0]:return ()
 bitrow=min(dem,key=int.bit_count);ans=set()
 while bitrow:
  b=bitrow&-bitrow;bitrow-=b
  for x in hitsets(tuple(d for d in dem if not d&b)):ans.add(x|b)
 ordered=sorted(ans,key=int.bit_count);minimal=[]
 for x in ordered:
  if not any(y&x==y for y in minimal):minimal.append(x)
 return tuple(minimal)
M=models();counts=dict(models=len(M),pairs=0,gp=0,already_extend=0,local_infeasible=0,local_feasible=0);examples=[]
for i,G in enumerate(M):
 for j in range(i,len(M)):
  H=M[j];counts['pairs']+=1
  if len(set(zip(G['labels'],H['labels'])))<4:continue
  D=[[G['D'][G['labels'][a]][G['labels'][b]]+H['D'][H['labels'][a]][H['labels'][b]] for b in range(4)] for a in range(4)]
  if not gp(D,range(4)):continue
  counts['gp']+=1
  def compatible(v,w):
   t=[a+b for a,b in zip(v,w)]
   return all(t) and extends(D,range(4),t)
  if any(compatible(v,w) for v in G['known'] for w in H['known']):counts['already_extend']+=1;continue
  ga=sum(1<<a for a,v in enumerate(G['external']) if not any(compatible(v,w) for w in H['known']))
  ha=sum(1<<b for b,w in enumerate(H['external']) if not any(compatible(v,w) for v in G['known']))
  gdem=tuple(sorted(set(d&ga for d in G['dem'])))
  forbid=[sum(1<<b for b,w in enumerate(H['external']) if compatible(v,w)) for v in G['external']]
  witness=None
  for X in hitsets(gdem):
   allowed=ha;xx=X
   while xx:
    bit=xx&-xx;xx-=bit;allowed&=~forbid[bit.bit_length()-1]
   if all(d&allowed for d in H['dem']):witness=(X,allowed);break
  if witness is None:counts['local_infeasible']+=1
  else:
   counts['local_feasible']+=1
   if len(examples)<10:examples.append(dict(G=G,H=H,allowed_G=witness[0],allowed_H=witness[1],product_distances=D))
result=dict(status='LOCAL_RELAXATION_ONLY',counts=counts,examples=examples,seconds=time.monotonic()-start)
(P/'four_signatures_probe.json').write_text(json.dumps(result,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in result.items() if k!='examples'}),flush=True)
