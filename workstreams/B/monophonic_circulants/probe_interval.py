"""Bounded diagnostic of a new interval-generator route, not exhaustive originals.
For each tested circulant, every triple containing0 is searched for an induced
path, which suffices by translation. Search stops on first failed graph or budget.
"""
from itertools import combinations
from collections import deque,Counter
from pathlib import Path
import time,json

class Budget(Exception):pass

def adjacency(n,steps):
 S={s%n for x in steps for s in (x,-x)};assert 0 not in S
 return [{(u+s)%n for s in S} for u in range(n)]

def covering_path(a,target,budget,deadline):
 n=len(a);am=[sum(1<<v for v in ns) for ns in a];goal=sum(1<<v for v in target);full=(1<<n)-1
 def dfs(path,used,blocked):
  budget[0]+=1
  if budget[0]>1000000 or time.monotonic()>deadline:raise Budget
  if used&goal==goal:return path
  u=path[-1];choices=am[u]&~(used|blocked)&full
  order=sorted((v for v in range(n) if choices>>v&1),key=lambda v:(not (goal>>v&1),v))
  for v in order:
   out=dfs(path+[v],used|1<<v,blocked|am[u])
   if out is not None:return out
  return None
 for s in target:
  out=dfs([s],1<<s,0)
  if out is not None:return out
 return None

def test(n,steps):
 a=adjacency(n,steps);d=[-1]*n;d[0]=0;q=deque([0])
 while q:
  u=q.popleft()
  for v in a[u]:
   if d[v]<0:d[v]=d[u]+1;q.append(v)
 assert min(d)>=0;triangles=sum(1 for u,v in combinations(a[0],2) if v in a[u])
 out=dict(n=n,steps=steps,degree=len(a[0]),diameter=max(d),triangles_at_zero=triangles)
 if max(d)!=2 or triangles:out['status']='hypothesis-route-failure';return out
 witnesses={};budget=[0];deadline=time.monotonic()+20
 try:
  for u,v in combinations(range(1,n),2):
   path=covering_path(a,(0,u,v),budget,deadline)
   if path is None:out.update(status='mp-at-least-3',obstruction=[0,u,v],nodes=budget[0]);return out
   witnesses[f'0,{u},{v}']=path
 except Budget:out.update(status='UNKNOWN-budget',tested_triples=len(witnesses),nodes=budget[0]);return out
 out.update(status='mp2-finite',triples=len(witnesses),nodes=budget[0],path_edge_histogram=dict(Counter(len(p)-1 for p in witnesses.values())),witnesses=witnesses);return out

if __name__=='__main__':
 reports=[]
 for n in range(11,34):
  if n==14:steps=list(range(5,10))
  elif n==15:steps=[1,4,6]
  else:
   aa=next(a for a in range(2,n) if 6*a-2<=n<=8*a-3);steps=list(range(aa,2*aa))
  r=test(n,steps);reports.append(r);print(json.dumps({k:v for k,v in r.items() if k!='witnesses'}),flush=True)
  if r['status']!='mp2-finite':break
 Path(__file__).with_name('interval_probe.json').write_text(json.dumps(reports,indent=2)+'\n')
