"""Exact arbitrary-metric four-point certificate. No discovery data or imports.
MET5 inequalities -> exact rays -> equality faces -> local profile nonexistence.
"""
from verify_metric_rays import extreme_metric_rays
from itertools import combinations,product
from collections import deque
from pathlib import Path
import hashlib,json,time,platform,sys
k=int(sys.argv[1]) if len(sys.argv)>1 else 4
assert 1<=k<=4
start=time.monotonic();edges,rows,rays,stages=extreme_metric_rays();pe=list(combinations(range(k),2));tr=[(a,b,c) for a,c in pe for b in range(k) if b not in (a,c)]
def to_matrix(r):
 D=[[0]*5 for _ in range(5)]
 for (a,b),v in zip(edges,r):D[a][b]=D[b][a]=v
 return D
# Zero faces of nonnegative coordinates/triangle slacks combine by intersection.
allrows=[tuple(int(i==j) for i in range(10)) for j in range(10)]+rows
full=(1<<40)-1
def zeros(r):return sum(int(sum(a*b for a,b in zip(row,r))==0)<<i for i,row in enumerate(allrows))
rayzeros=[zeros(r) for r in rays]
representatives={full:(0,)*10};queue=deque([full])
while queue:
 mask=queue.popleft();v=representatives[mask]
 for r,z in zip(rays,rayzeros):
  new=mask&z
  if new not in representatives:
   rep=tuple(a+b for a,b in zip(v,r));assert zeros(rep)==new
   representatives[new]=rep;queue.append(new)
assert len(representatives)==9484

def base_key(D):return tuple(D[a][b]==0 for a,b in pe)+tuple(D[a][b]+D[b][c]==D[a][c] for a,b,c in tr)
def extension_profile(D,x):
 flags=[]
 for a,b in pe:flags.extend((D[a][x]+D[x][b]==D[a][b],D[x][a]+D[a][b]==D[x][b],D[x][b]+D[b][a]==D[x][a]))
 return sum(int(z)<<i for i,z in enumerate(flags))
def gp(D,S):return all(D[a][b]+D[b][c]!=D[a][c] and D[a][c]+D[c][b]!=D[a][b] and D[b][a]+D[a][c]!=D[b][c] for a,b,c in combinations(S,3))
groups={}
for rep in representatives.values():
 D=to_matrix(rep)
 if any(D[a][4]==0 for a in range(k)):continue
 key=base_key(D)
 if key not in groups:groups[key]=dict(D=D,profiles=set())
 groups[key]['profiles'].add(extension_profile(D,4))
models=[]
for key,g in sorted(groups.items()):
 D=g['D'];P=sorted(g['profiles']);reps=[]
 for i in range(k):
  if all(D[i][j]>0 for j in reps):reps.append(i)
 known=[(extension_profile(D,x),sum(int(D[x][i]==0)<<i for i in range(k))) for x in reps];demands=[]
 for mask in range(1,1<<len(reps)):
  S=[reps[i] for i in range(len(reps)) if mask>>i&1]
  if not gp(D,S) or any(gp(D,S+[i]) for i in reps if i not in S):continue
  forbidden=sum(7<<(3*i) for i,(a,b) in enumerate(pe) if a in S and b in S)
  demands.append(sum(int(not p&forbidden)<<i for i,p in enumerate(P)))
 models.append(dict(key=key,D=D,P=P,known=known,demands=demands))
if k==4:assert len(models)==106 and sum(len(m['P']) for m in models)==9101

nodes=0;digest=hashlib.sha256()
def infeasible(G,H,record=False):
 global nodes
 if any(not p&q and not z&w for p,z in G['known'] for q,w in H['known']):return True
 AG=sum(int(all(p&q for q,z in H['known']))<<i for i,p in enumerate(G['P']))
 AH=sum(int(all(q&p for p,z in G['known']))<<j for j,q in enumerate(H['P']))
 hd=[d&AH for d in H['demands']]
 conflicts=[sum(int(not p&q)<<i for i,p in enumerate(G['P'])) for q in H['P']]
 covers=[sum(int(d>>j&1)<<i for i,d in enumerate(hd)) for j in range(len(H['P']))]
 stack=[((1<<len(hd))-1,AG)];seen=set()
 while stack:
  unhit,available=stack.pop()
  if (unhit,available) in seen:continue
  seen.add((unhit,available));nodes+=1
  if record:digest.update(f'{unhit}:{available};'.encode())
  if any(not available&d for d in G['demands']):continue
  if not unhit:return False
  row=min((hd[i] for i in range(len(hd)) if unhit>>i&1),key=int.bit_count)
  while row:
   bit=row&-row;row-=bit;j=bit.bit_length()-1
   stack.append((unhit&~covers[j],available&~conflicts[j]))
 return True
pairs=0;gp_pairs=0
for i,G in enumerate(models):
 for j in range(i,len(models)):
  H=models[j];pairs+=1
  if any(a and b for a,b in zip(G['key'],H['key'])):continue
  gp_pairs+=1;digest.update(f'pair:{i},{j};'.encode())
  assert infeasible(G,H,True),('feasible local system',i,j)
if k==4:assert gp_pairs==2381
# Original unweighted graph/BFS semantics for all25rays and8full face representatives.
bfs_entries=0;fixtures=list(rays)+[representatives[z] for z in sorted(representatives)[::max(1,len(representatives)//8)][:8]]
for r in fixtures:
 D=to_matrix(r);reps=[];cls=[]
 for i in range(5):
  old=next((j for j,a in enumerate(reps) if D[i][a]==0),None)
  if old is None:old=len(reps);reps.append(i)
  cls.append(old)
 adj=[set() for _ in reps]
 for a,b in combinations(range(len(reps)),2):
  length=D[reps[a]][reps[b]];assert length>=1;last=a
  for t in range(length-1):
   v=len(adj);adj.append({last});adj[last].add(v);last=v
  adj[last].add(b);adj[b].add(last)
 for root in range(len(adj)):
  ds=[-1]*len(adj);ds[root]=0;q=deque([root])
  while q:
   a=q.popleft()
   for b in adj[a]:
    if ds[b]<0:ds[b]=ds[a]+1;q.append(b)
  bfs_entries+=len(adj)
  if root<len(reps):assert all(ds[cls[i]]==D[reps[root]][i] for i in range(5))
# Negative controls: remove real factor-extension hypotheses and the theorem's
# finite nonexistence test MUST become feasible for a complete4 landmark model.
complete=next(m for m in models if not any(m['key']))
corrupt=dict(complete,demands=[]);assert not infeasible(corrupt,corrupt)
assert not gp([[0,1,2],[1,0,1],[2,1,0]],range(3))
bad=[1]*10;bad[0]=3;assert any(sum(a*b for a,b in zip(bad,row))<0 for row in rows)
result=dict(status='PASS',python=platform.python_version(),metric_rays=len(rays),ray_stage_counts=stages,five_point_faces=len(representatives),selected_size=k,landmark_models=len(models),outside_profiles=sum(len(m['P']) for m in models),model_pairs=pairs,gp_product_models=gp_pairs,search_states=nodes,certificate_sha256=digest.hexdigest(),original_bfs_fixtures=len(fixtures),original_bfs_entries=bfs_entries,negative_controls=3,seconds=time.monotonic()-start,scope=f'universal {k}-point product extension under factor lowerGP>{k}; complete reduction in UNIVERSAL_FIVE_PROOF.md; independent review pending')
print(json.dumps(result,sort_keys=True))
