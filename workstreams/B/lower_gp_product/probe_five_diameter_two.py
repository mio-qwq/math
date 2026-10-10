"""Five-point diameter-two local relaxation, with first-coordinate index symmetry."""
from itertools import combinations,product,permutations
from functools import lru_cache
from pathlib import Path
import time,json
P=Path(__file__).parent;start=time.monotonic();k=5;E=list(combinations(range(k),2));T=[(a,b,c) for a,c in E for b in range(k) if b not in (a,c)];perms=list(permutations(range(k)))
def partition(a=(0,)):
 if len(a)==k:yield a;return
 for x in range(max(a)+2):yield from partition(a+(x,))
def gp(D,S):return all(D[a][b]+D[b][c]!=D[a][c] and D[a][c]+D[c][b]!=D[a][b] and D[b][a]+D[a][c]!=D[b][c] for a,b,c in combinations(S,3))
def profile(D,v):return sum((int(v[a]+v[b]==D[a][b])<<(3*i))|(int(v[a]+D[a][b]==v[b])<<(3*i+1))|(int(v[b]+D[a][b]==v[a])<<(3*i+2)) for i,(a,b) in enumerate(E))
models=[]
for L in partition():
 q=max(L)+1;edges=list(combinations(range(q),2));reps=[L.index(i) for i in range(q)]
 for bits in product((1,2),repeat=len(edges)):
  d=[[0]*q for _ in range(q)]
  for (a,b),x in zip(edges,bits):d[a][b]=d[b][a]=x
  D=[[d[L[a]][L[b]] for b in range(k)] for a in range(k)]
  easy=q>=4 and gp(D,reps)
  if easy:continue
  packed=tuple(D[a][b] for a,b in E)
  canonical=min(tuple(D[p[a]][p[b]] for a,b in E) for p in perms)
  profiles=sorted(set(profile(D,[v[L[a]] for a in range(k)]) for v in product((1,2),repeat=q)))
  known=[(profile(D,D[z]),sum(int(D[z][a]==0)<<a for a in range(k))) for z in reps]
  dem=[]
  for s in range(1,1<<q):
   S=[reps[i] for i in range(q) if s>>i&1]
   if not gp(D,S) or any(gp(D,S+[z]) for z in reps if z not in S):continue
   f=sum(7<<(3*i) for i,(a,b) in enumerate(E) if a in S and b in S)
   dem.append(sum(int(not p&f)<<j for j,p in enumerate(profiles)))
  zero=sum(int(D[a][b]==0)<<i for i,(a,b) in enumerate(E));eq=sum(int(D[a][b]+D[b][c]==D[a][c])<<i for i,(a,b,c) in enumerate(T))
  models.append(dict(D=D,key=packed,canonical=canonical,profiles=profiles,known=known,demands=dem,zero=zero,equalities=eq))
first=[i for i,m in enumerate(models) if m['key']==m['canonical']]
print(json.dumps(dict(stage='models',hard_models=len(models),canonical_first=len(first),max_profiles=max(len(m['profiles']) for m in models),seconds=time.monotonic()-start)),flush=True)
counts=dict(pairs=0,gp=0,known_extend=0,infeasible=0,feasible=0);nodes=0;witness=None
for index,gi in enumerate(first):
 G=models[gi]
 for hi,H in enumerate(models):
  counts['pairs']+=1
  if G['zero']&H['zero'] or G['equalities']&H['equalities']:continue
  counts['gp']+=1
  if any(not e&f and not z&w for e,z in G['known'] for f,w in H['known']):counts['known_extend']+=1;continue
  PG=G['profiles'];PH=H['profiles'];ga=sum(int(all(p&e for e,z in H['known']))<<i for i,p in enumerate(PG));ha=sum(int(all(p&e for e,z in G['known']))<<i for i,p in enumerate(PH))
  ds=tuple(sorted(set(d&ga for d in G['demands'])));forbid=[sum(int(not p&q)<<j for j,q in enumerate(PH)) for p in PG]
  @lru_cache(None)
  def solve(dem,allowed):
   global nodes
   nodes+=1
   if any(not d&allowed for d in H['demands']):return None
   if not dem:return (0,allowed)
   row=min(dem,key=int.bit_count)
   while row:
    bit=row&-row;row-=bit;j=bit.bit_length()-1
    got=solve(tuple(d for d in dem if not d&bit),allowed&~forbid[j])
    if got is not None:return(got[0]|bit,got[1])
   return None
  got=solve(ds,ha)
  if got is None:counts['infeasible']+=1
  else:counts['feasible']+=1;witness=dict(G=G,H=H,X=got[0],Y=got[1]);break
 print(json.dumps(dict(stage='first_model_done',index=index+1,counts=counts,seconds=time.monotonic()-start)),flush=True)
 if witness is not None:break
result=dict(status='LOCAL_FEASIBLE' if witness else 'ALL_LOCAL_INFEASIBLE',counts=counts,nodes=nodes,first_models=len(first),hard_models=len(models),witness=witness,seconds=time.monotonic()-start)
(P/'five_diameter_two_probe.json').write_text(json.dumps(result,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in result.items() if k!='witness'}),flush=True)
