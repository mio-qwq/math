"""Exact distance/line-mask diagnostic for the ORIGINAL lower-GP bound.
Targets factor lowerGP>=4 and a product maximal GP set of size<=3.
"""
from itertools import combinations
from collections import deque,Counter
from pathlib import Path
import random,time,json
P=Path(__file__).parent

def metric(n,E):
 adj=[set() for _ in range(n)]
 for a,b in E:adj[a].add(b);adj[b].add(a)
 D=[]
 for root in range(n):
  ds=[-1]*n;ds[root]=0;q=deque([root])
  while q:
   a=q.popleft()
   for b in adj[a]:
    if ds[b]<0:ds[b]=ds[a]+1;q.append(b)
  D.append(ds)
 return D

def lines(D):
 n=len(D);L=[[0]*n for _ in range(n)]
 for a,b in combinations(range(n),2):
  L[a][b]=L[b][a]=sum(1<<u for u in range(n) if D[a][u]+D[u][b]==D[a][b] or abs(D[u][a]-D[u][b])==D[a][b])
 return L

def small_maximal(D,k=3):
 n=len(D);full=(1<<n)-1;L=lines(D);tested=0
 if n==1:return [0],1
 for a,b in combinations(range(n),2):
  tested+=1
  if L[a][b]==full:return [a,b],tested
 if k>=3:
  for a,b,c in combinations(range(n),3):
   tested+=1
   if L[a][b]>>c&1:continue
   if L[a][b]|L[a][c]|L[b][c]==full:return [a,b,c],tested
 return None,tested

def main():
 rng=random.Random(202610101103);factors=[];seen=set();attempts=0;start=time.monotonic()
 initial=[]
 for t,r in ((3,4),(3,5),(4,4),(4,5)):
  n=t+r;E=[(u,v) for u,v in combinations(range(n),2) if u<t or v<t];initial.append((n,E,'split'))
 while len(factors)<16 and attempts<3000:
  attempts+=1
  if initial:n,E,kind=initial.pop(0)
  else:
   n=rng.choice((7,8,9,10));p=rng.choice((.55,.7,.8,.9));E=[e for e in combinations(range(n),2) if rng.random()<p];kind='seeded_dense'
  key=(n,tuple(E))
  if key in seen or len(E)==n*(n-1)//2:continue
  seen.add(key);D=metric(n,E)
  if any(d<0 for d in D[0]):continue
  small,_=small_maximal(D)
  if small is None:factors.append(dict(order=n,edges=E,kind=kind,distances=D,lower_bound=4))
 print(json.dumps(dict(stage='factors',accepted=len(factors),attempts=attempts,seconds=time.monotonic()-start)),flush=True)
 checks=[];candidate=None
 for i,j in combinations(range(len(factors)),2):
  if time.monotonic()-start>60:break
  G,H=factors[i],factors[j];g=G['order'];h=H['order'];N=g*h
  D=[[G['distances'][a//h][b//h]+H['distances'][a%h][b%h] for b in range(N)] for a in range(N)]
  S,tested=small_maximal(D);checks.append(dict(factors=[i,j],product_order=N,tested=tested,selected=S))
  if S is not None:
   candidate=dict(G=G,H=H,product_selected=[divmod(v,h) for v in S],selected_indices=S)
   (P/'candidate.json').write_text(json.dumps(candidate,indent=2)+'\n');break
 (P/'product_probe.json').write_text(json.dumps(dict(factors=factors,checks=checks),separators=(',',':'))+'\n')
 print(json.dumps(dict(status='CANDIDATE' if candidate else 'NO_CANDIDATE_IN_WINDOW',factor_count=len(factors),products=len(checks),subsets_tested=sum(c['tested'] for c in checks),seconds=time.monotonic()-start)))
if __name__=='__main__':main()
