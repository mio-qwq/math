"""Exact subset search for terminal sets, with explicit incomplete status on cap.
No claim from a sample of positive witnesses. All graph metrics are direct BFS.
"""
from collections import deque,Counter
from itertools import combinations
from pathlib import Path
import random,json,time
OUT=Path(__file__).parent

def distances(n,edges):
 a=[set() for _ in range(n)]
 for u,v in edges:a[u].add(v);a[v].add(u)
 D=[]
 for root in range(n):
  ds=[-1]*n;ds[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v in a[u]:
    if ds[v]<0:ds[v]=ds[u]+1;q.append(v)
  D.append(ds)
 return a,D

def search(D,cap=1000000):
 n=len(D);full=(1<<n)-1;forbid=[[0]*n for _ in range(n)];cover=[[0]*n for _ in range(n)]
 for a,b in combinations(range(n),2):
  for u in range(n):
   if u in (a,b):continue
   if abs(D[u][a]-D[u][b])==D[a][b]:cover[a][b]|=1<<u
   if abs(D[u][a]-D[u][b])==D[a][b] or D[u][a]+D[u][b]==D[a][b]:forbid[a][b]|=1<<u
  forbid[b][a]=forbid[a][b];cover[b][a]=cover[a][b]
 nodes=0
 def dfs(S,candidates,blocked,covered):
  nonlocal nodes
  nodes+=1
  if nodes>cap:raise TimeoutError
  if covered==full:return S
  candidates&=~blocked
  while candidates:
   bit=candidates&-candidates;candidates-=bit;v=bit.bit_length()-1
   newblocked=blocked;newcovered=covered|bit
   for u in S:newblocked|=forbid[u][v];newcovered|=cover[u][v]
   ans=dfs(S+[v],candidates,newblocked,newcovered)
   if ans is not None:return ans
  return None
 try:
  ans=dfs([],full,0,0)
  return ('WITNESS' if ans is not None else 'NO_TERMINAL_SET'),ans,nodes
 except TimeoutError:return 'INCOMPLETE',None,nodes

def main():
 rng=random.Random(202610101055);records=[];stats=Counter();start=time.monotonic()
 for n in (12,14,16,18,20,22,24,26,28,30,32):
  accepted=0;trials=0
  while accepted<20 and trials<3000:
   trials+=1;stubs=[i for i in range(n) for _ in range(3)];rng.shuffle(stubs)
   E={tuple(sorted(stubs[i:i+2])) for i in range(0,len(stubs),2)}
   if len(E)!=3*n//2 or any(u==v for u,v in E):continue
   adj,D=distances(n,E)
   if any(x<0 for x in D[0]) or max(map(max,D))<4:continue
   # Exclude bipartite and bridge cases already covered by the source.
   if all((D[0][u]-D[0][v])%2 for u,v in E):continue
   bridge=False
   for edge in E:
    _,T=distances(n,E-{edge})
    if any(x<0 for x in T[0]):bridge=True;break
   if bridge:continue
   status,S,nodes=search(D);accepted+=1;stats[status]+=1
   record=dict(order=n,edges=sorted(E),diameter=max(map(max,D)),status=status,selected=S,nodes=nodes)
   records.append(record)
   if status=='NO_TERMINAL_SET':
    (OUT/'candidate.json').write_text(json.dumps(record,indent=2)+'\n');break
  print(json.dumps(dict(order=n,accepted=accepted,trials=trials,stats=dict(stats),max_nodes=max((r['nodes'] for r in records),default=0),seconds=time.monotonic()-start)),flush=True)
  if stats['NO_TERMINAL_SET'] or time.monotonic()-start>90:break
 (OUT/'cubic_probe.json').write_text(json.dumps(records,indent=2)+'\n')
 print(json.dumps(dict(status='DIAGNOSTIC_COMPLETE',graphs=len(records),stats=dict(stats),witness_sizes=dict(Counter(len(r['selected']) for r in records if r['selected'] is not None)),seconds=time.monotonic()-start)))
if __name__=='__main__':main()
