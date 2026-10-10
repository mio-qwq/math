"""Independent original-definition finite quotient for all K(n,2) products.
No discovery imports. Generates all endpoint set partitions, not stepwise edges;
uses BFS factor metrics, index-permutation orbits in one projection, and direct
extension checks. The written support-stability theorem supplies all n,m.
"""
from itertools import combinations,permutations,product
from collections import deque,Counter
import hashlib,json,platform,time
start=time.monotonic()

def partitions(slots,prefix=(),top=-1):
 if len(prefix)==slots:
  yield prefix;return
 for x in range(top+2):
  if len(prefix)%2 and prefix[-1]==x:continue
  yield from partitions(slots,prefix+(x,),max(top,x))

def normalize(seq):
 ren={};E=[]
 for j in range(0,len(seq),2):
  edge=[]
  for x in sorted(seq[j:j+2]):
   if x not in ren:ren[x]=len(ren)
   edge.append(ren[x])
  E.append(tuple(sorted(edge)))
 return tuple(E)

def original_graph(n):
 V=list(combinations(range(n),2));N=len(V);adj=[[] for _ in V]
 for i,j in combinations(range(N),2):
  if not set(V[i])&set(V[j]):adj[i].append(j);adj[j].append(i)
 D=[]
 for root in range(N):
  ds=[-1]*N;ds[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v in adj[u]:
    if ds[v]<0:ds[v]=ds[u]+1;q.append(v)
  D.append(ds)
 assert all(x>=0 for row in D for x in row)
 return V,adj,D

def is_gp_matrix(M):
 return all(M[i][j]+M[j][k]!=M[i][k] and M[i][k]+M[k][j]!=M[i][j] and M[j][i]+M[i][k]!=M[j][k] for i,j,k in combinations(range(len(M)),3))

def main(k):
 n=2*k+2;V,adj,D=original_graph(n);N=len(V);index={v:i for i,v in enumerate(V)}
 # Full original-product BFS from one root, independently of the additive formula.
 rootD=[-1]*(N*N);rootD[0]=0;q=deque([0])
 while q:
  z=q.popleft();u,v=divmod(z,N)
  for w in [a*N+v for a in adj[u]]+[u*N+b for b in adj[v]]:
   if rootD[w]<0:rootD[w]=rootD[z]+1;q.append(w)
 assert all(rootD[u*N+v]==D[0][u]+D[0][v] for u in range(N) for v in range(N))
 presentations=set();partitions_count=0
 for seq in partitions(2*k):partitions_count+=1;presentations.add(normalize(seq))
 bykey={}
 for E in sorted(presentations):
  selected=tuple(index[e] for e in E);M=tuple(tuple(D[a][b] for b in selected) for a in selected)
  if len(set(selected))==k and is_gp_matrix(M):continue
  representatives={}
  for u in range(N):representatives.setdefault(tuple(D[u][a] for a in selected),u)
  key=(M,tuple(sorted(representatives)))
  bykey.setdefault(key,dict(edges=E,selected=selected,M=M,reps=representatives))
 keys=sorted(bykey);types=[bykey[key] for key in keys];ids={key:i for i,key in enumerate(keys)}
 # Simultaneously permute the k product points to put the first projection into
 # a canonical orbit representative; the second projection remains unrestricted.
 visited=set();first=[];perms=list(permutations(range(k)))
 for i,A in enumerate(types):
  if i in visited:continue
  first.append(i)
  for p in perms:
   M=tuple(tuple(A['M'][p[a]][p[b]] for b in range(k)) for a in range(k))
   rows=tuple(sorted(tuple(r[p[a]] for a in range(k)) for r in A['reps']))
   assert (M,rows) in ids
   visited.add(ids[M,rows])
 assert len(visited)==len(types)
 pairs=0;valid=0;witness_digest=hashlib.sha256();max_candidates=0
 for i in first:
  A=types[i]
  for j,B in enumerate(types):
   pairs+=1
   if len(set(zip(A['selected'],B['selected'])))<k:continue
   M=[[A['M'][a][b]+B['M'][a][b] for b in range(k)] for a in range(k)]
   if not is_gp_matrix(M):continue
   valid+=1;witness=None;tries=0
   for u,v in product(A['reps'].values(),B['reps'].values()):
    tries+=1;ds=[D[u][A['selected'][a]]+D[v][B['selected'][a]] for a in range(k)]
    if 0 in ds:continue
    if all(ds[a]+ds[b]!=M[a][b] and abs(ds[a]-ds[b])!=M[a][b] for a,b in combinations(range(k),2)):
     witness=(u,v);break
   assert witness is not None,(k,A['edges'],B['edges'])
   # A second direct three-term check on the actual factor-BFS product metric.
   u,v=witness;Z=list(zip(A['selected'],B['selected']))+[(u,v)]
   actual=[[D[a][c]+D[b][d] for c,d in Z] for a,b in Z]
   assert len(set(Z))==k+1 and is_gp_matrix(actual)
   witness_digest.update(json.dumps([i,j,u,v],separators=(',',':')).encode()+b'\n')
   max_candidates=max(max_candidates,tries)
 # Corrupted product metric and false GP conclusion must be rejected.
 assert rootD[1] != D[0][0]+D[0][1]+1
 assert not is_gp_matrix([[0,1,2],[1,0,1],[2,1,0]])
 out=dict(k=k,signature_alphabet=n,factor_vertices=N,original_factor_bfs_entries=N*N,original_product_root_entries=N*N,endpoint_partitions=partitions_count,normalized_presentations=len(presentations),metric_types=len(types),first_projection_orbits=len(first),type_pairs=pairs,gp_sets_extended=valid,max_candidate_trials=max_candidates,witness_digest=witness_digest.hexdigest(),negative_controls=2)
 print(json.dumps(out,sort_keys=True),flush=True);return out

if __name__=='__main__':
 rows=[main(4),main(5)]
 print(json.dumps(dict(status='PASS',python=platform.python_version(),seconds=time.monotonic()-start,scope='exact all-pattern finite quotient; universal transfer requires written support-stability proof; pending independent review',rows=rows),sort_keys=True))
