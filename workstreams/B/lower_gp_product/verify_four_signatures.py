"""Independent exhaustive metric/signature certificate for diameter-two bound5.
No discovery imports. All profile subsets exhaustively enumerated by bit masks.
"""
import itertools as it,hashlib,json,time,platform
from collections import deque
start=time.monotonic();pairs=list(it.combinations(range(4),2))
def is_gp(ds):
 return all(ds[a][b]+ds[b][c]>ds[a][c] and ds[a][c]+ds[c][b]>ds[a][b] and ds[b][a]+ds[a][c]>ds[b][c] for a,b,c in it.combinations(range(len(ds)),3))
def admits(ds,subset,v):
 return all(abs(v[a]-v[b])<ds[a][b]<v[a]+v[b] for a,b in it.combinations(subset,2))
def metric_ok(D):
 return all(D[a][c]<=D[a][b]+D[b][c] for a,b,c in it.product(range(len(D)),repeat=3))
models=[];bfs_entries=0
for packed in it.product(range(3),repeat=6):
 D=[[0]*4 for _ in range(4)]
 for (a,b),d in zip(pairs,packed):D[a][b]=D[b][a]=d
 if not metric_ok(D):continue
 # A pseudometric with zero distance identifies equal original vertices.
 reps=[]
 for a in range(4):
  if all(D[a][b]>0 for b in reps):reps.append(a)
 profiles=[v for v in it.product((1,2),repeat=4) if all(abs(v[a]-v[b])<=D[a][b]<=v[a]+v[b] for a,b in pairs)]
 # Original adjacency realization: landmarks, all signature vertices, universal hub.
 # Only used to verify metric semantics, never to assert factor lowerGP>=5.
 q=len(reps);N=q+len(profiles)+1;adj=[set() for _ in range(N)]
 def edge(a,b):adj[a].add(b);adj[b].add(a)
 for a,b in it.combinations(range(q),2):
  if D[reps[a]][reps[b]]==1:edge(a,b)
 for j,v in enumerate(profiles):
  for a in range(q):
   if v[reps[a]]==1:edge(q+j,a)
 for a in range(N-1):edge(a,N-1)
 BD=[]
 for root in range(N):
  row=[-1]*N;row[root]=0;queue=deque([root])
  while queue:
   u=queue.popleft()
   for v in adj[u]:
    if row[v]<0:row[v]=row[u]+1;queue.append(v)
  BD.append(row)
 bfs_entries+=N*N
 assert all(BD[a][b]==D[reps[a]][reps[b]] for a,b in it.product(range(q),repeat=2))
 assert all(BD[q+j][a]==v[reps[a]] for j,v in enumerate(profiles) for a in range(q))
 demands=[]
 for mask in range(1,1<<len(reps)):
  S=[reps[a] for a in range(len(reps)) if mask>>a&1]
  if not is_gp([[D[a][b] for b in S] for a in S]):continue
  if any(admits(D,S,D[z]) for z in reps if z not in S):continue
  demands.append(sum(1<<i for i,v in enumerate(profiles) if admits(D,S,v)))
 # Enumerate ALL subsets independently of the discovery's recursive hitting sets.
 r=len(profiles);minimal=[]
 for mask in range(1<<r):
  if not all(mask&d for d in demands):continue
  # Immediate deletions suffice for inclusion-minimality of a monotone property.
  if any(all((mask^(1<<i))&d for d in demands) for i in range(r) if mask>>i&1):continue
  minimal.append(mask)
 models.append((D,[D[a] for a in reps],profiles,demands,minimal))
assert len(models)==127
count=0;checks=0;digest=hashlib.sha256();mincount=sum(len(z[4]) for z in models)
for gi,G in enumerate(models):
 A,knownA,profilesA,demA,minA=G
 for hi in range(gi,len(models)):
  B,knownB,profilesB,demB,minB=models[hi]
  Q=[[A[a][b]+B[a][b] for b in range(4)] for a in range(4)]
  if any(Q[a][b]==0 for a,b in pairs) or not is_gp(Q):continue
  count+=1
  def compatible(v,w):
   ds=[v[i]+w[i] for i in range(4)]
   return min(ds)>0 and admits(Q,range(4),ds)
  assert not any(compatible(v,w) for v in knownA for w in knownB)
  badA=sum(1<<i for i,v in enumerate(profilesA) if any(compatible(v,w) for w in knownB))
  availableB=sum(1<<j for j,w in enumerate(profilesB) if not any(compatible(v,w) for v in knownA))
  incompatible=[sum(1<<j for j,w in enumerate(profilesB) if compatible(v,w)) for v in profilesA]
  rejected=0
  for mask in minA:
   if mask&badA:continue
   allowed=availableB
   for i in range(len(profilesA)):
    if mask>>i&1:allowed&=~incompatible[i]
   failed=next((di for di,d in enumerate(demB) if not d&allowed),None)
   assert failed is not None,('LOCAL FEASIBILITY',gi,hi,mask,allowed)
   rejected+=1;checks+=1;digest.update(f'{gi},{hi},{mask},{failed};'.encode())
  digest.update(f'end:{gi},{hi},{rejected};'.encode())
assert count==3956
# Corrupted metric, collinear claimed GP, bad duplicate extension.
assert not is_gp([[0,1,2],[1,0,1],[2,1,0]])
assert not metric_ok([[0,1,3],[1,0,1],[3,1,0]])
assert not admits([[0,1],[1,0]],[0,1],[0,1])
print(json.dumps(dict(status='PASS',python=platform.python_version(),metric_models=len(models),gp_product_models=count,minimal_profile_sets=mincount,original_bfs_entries=bfs_entries,obstruction_checks=checks,certificate_sha256=digest.hexdigest(),negative_controls=3,seconds=time.monotonic()-start,scope='complete local necessary constraints; universal reduction in DIAMETER_TWO_FIVE_PROOF.md; independent review pending'),sort_keys=True))
