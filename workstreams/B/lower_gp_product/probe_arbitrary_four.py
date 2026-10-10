"""Necessary local constraints for arbitrary graph metrics; MET5 face relaxation."""
import json,time
from pathlib import Path
from itertools import combinations
from functools import lru_cache
P=Path(__file__).parent;start=time.monotonic();raw=json.loads((P/'metric_faces.json').read_text());edges=list(map(tuple,raw['edges']));tri=list(map(tuple,raw['triangles']));ray=raw['rays'];e4=list(combinations(range(4),2));t4=[(a,b,c) for a,c in e4 for b in range(4) if b not in (a,c)];tnew=[t for a,c in e4 for t in ((a,4,c),(a,c,4),(c,a,4))]
def tid(t):
 a,b,c=t;return tri.index((min(a,c),b,max(a,c)))+10
def bits(f,positions):return sum(((f>>pos)&1)<<i for i,pos in enumerate(positions))
basepos=[edges.index(e) for e in e4]+[tid(t) for t in t4];profilepos=[tid(t) for t in tnew];outsidepos=[edges.index((i,4)) for i in range(4)]
def rm(D):return sum((int(D[a][b]>0)<<i) for i,(a,b) in enumerate(edges))|sum((int(D[a][b]+D[b][c]>D[a][c])<<(10+i)) for i,(a,b,c) in enumerate(tri))
rms=[rm(D) for D in ray];groups={}
for f in raw['positive_masks']:
 if not all(f>>p&1 for p in outsidepos):continue
 key=bits(f,basepos);groups.setdefault(key,set()).add(((1<<18)-1)^bits(f,profilepos))
models=[]
def gp(D,S):return all(D[a][b]+D[b][c]>D[a][c] and D[a][c]+D[c][b]>D[a][b] and D[b][a]+D[a][c]>D[b][c] for a,b,c in combinations(S,3))
for key,profile in sorted(groups.items()):
 # Any metric representative of this four-point equality face suffices for known rows.
 eligible=[D for D,r in zip(ray,rms) if bits(r,basepos)&~key==0];D=[[sum(R[a][b] for R in eligible) for b in range(4)] for a in range(4)]
 reps=[]
 for a in range(4):
  if all(D[a][b]>0 for b in reps):reps.append(a)
 known=[]
 for z in reps:
  v=D[z];eq=sum((int(v[a]+v[c]==D[a][c])<<(3*i))|(int(v[a]+D[a][c]==v[c])<<(3*i+1))|(int(v[c]+D[a][c]==v[a])<<(3*i+2)) for i,(a,c) in enumerate(e4));zero=sum(int(x==0)<<a for a,x in enumerate(v));known.append((eq,zero))
 profile=sorted(profile);dem=[]
 for s in range(1,1<<len(reps)):
  S=[reps[a] for a in range(len(reps)) if s>>a&1]
  if not gp(D,S) or any(gp(D,S+[z]) for z in reps if z not in S):continue
  mask=sum(7<<(3*i) for i,(a,c) in enumerate(e4) if a in S and c in S)
  dem.append(sum(1<<j for j,p in enumerate(profile) if not p&mask))
 models.append(dict(key=key,D=D,known=known,profiles=profile,demands=dem))
print(json.dumps(dict(stage='models',count=len(models),profiles=sum(len(m['profiles']) for m in models),max_profiles=max(map(lambda m:len(m['profiles']),models)))),flush=True)
counts=dict(pairs=0,gp=0,known_extend=0,infeasible=0,feasible=0);witness=None;nodes=0
for gi,G in enumerate(models):
 for hi in range(gi,len(models)):
  H=models[hi];counts['pairs']+=1
  # Product distinctness and no common tight triangle.
  if ((~G['key'])&(~H['key'])&63) or ((~(G['key']>>6))&(~(H['key']>>6))&4095):continue
  counts['gp']+=1
  if any(not(e&f) and not(z&w) for e,z in G['known'] for f,w in H['known']):counts['known_extend']+=1;continue
  PG=G['profiles'];PH=H['profiles']
  ga=sum(1<<i for i,p in enumerate(PG) if all(p&e for e,z in H['known']))
  ha=sum(1<<j for j,p in enumerate(PH) if all(p&e for e,z in G['known']))
  demands=tuple(sorted(set(d&ga for d in G['demands'])))
  forbid=[sum(1<<j for j,q in enumerate(PH) if not p&q) for p in PG]
  @lru_cache(None)
  def solve(ds,allowed):
   global nodes
   nodes+=1
   if any(not(d&allowed) for d in H['demands']):return None
   if not ds:return (0,allowed)
   d=min(ds,key=int.bit_count)
   while d:
    bit=d&-d;d-=bit;i=bit.bit_length()-1
    result=solve(tuple(x for x in ds if not x&bit),allowed&~forbid[i])
    if result is not None:return (result[0]|bit,result[1])
   return None
  result=solve(demands,ha)
  if result is None:counts['infeasible']+=1
  else:
   counts['feasible']+=1;witness=dict(G=G,H=H,X=result[0],Y=result[1]);break
 if witness is not None:break
result=dict(status='LOCAL_RELAXATION_FEASIBLE' if witness else 'LOCAL_RELAXATION_ALL_INFEASIBLE',counts=counts,nodes=nodes,witness=witness,seconds=time.monotonic()-start,scope='MET5 prior completeness required; no graph counterexample or universal proof claimed yet')
(P/'arbitrary_four_probe.json').write_text(json.dumps(result,separators=(',',':'))+'\n');print(json.dumps({k:v for k,v in result.items() if k!='witness'}),flush=True)
