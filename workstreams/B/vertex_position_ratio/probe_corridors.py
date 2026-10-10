"""Exact diagnostic of an independently designed fixed-width geodesic corridor.
Known root p_v=k; position sets computed through prior poset/matching reduction.
"""
from collections import deque
from itertools import combinations
from pathlib import Path
import random,json,time
P=Path(__file__).parent;rng=random.Random(202610101218);start=time.monotonic()
def root_data(adj,u):
 n=len(adj);D=[-1]*n;D[u]=0;q=deque([u])
 while q:
  a=q.popleft()
  for b in adj[a]:
   if D[b]<0:D[b]=D[a]+1;q.append(b)
 assert min(D)>=0
 R=[0]*n
 for a in sorted(range(n),key=lambda a:D[a],reverse=True):
  for b in adj[a]:
   if D[b]==D[a]+1:R[a]|=(1<<b)|R[b]
 reach=[[b for b in range(n) if R[a]>>b&1] for a in range(n)];match=[-1]*n
 def augment(a,seen):
  for b in reach[a]:
   if b in seen:continue
   seen.add(b)
   if match[b]<0 or augment(match[b],seen):match[b]=a;return True
  return False
 size=sum(augment(a,set()) for a in sorted(range(n),key=lambda a:len(reach[a])))
 lm=[-1]*n
 for b,a in enumerate(match):
  if a>=0:lm[a]=b
 zl={a for a in range(n) if lm[a]<0};zr=set();todo=list(zl)
 while todo:
  a=todo.pop()
  for b in reach[a]:
   if lm[a]==b or b in zr:continue
   zr.add(b)
   if match[b]>=0 and match[b] not in zl:zl.add(match[b]);todo.append(match[b])
 antichain=sorted(zl-zr);assert len(antichain)==n-size
 assert all(not(R[a]>>b&1 or R[b]>>a&1) for a,b in combinations(antichain,2))
 chains=[]
 for a in range(n):
  if match[a]>=0:continue
  chain=[a]
  while lm[chain[-1]]>=0:chain.append(lm[chain[-1]])
  chains.append(chain)
 assert len(chains)==n-size and sorted(x for c in chains for x in c)==list(range(n))
 return dict(root=u,value=n-size,antichain=antichain,chains=chains,distances=D)

def graph(k,L,kind,t):
 n=1+k*L;adj=[set() for _ in range(n)];level=[0]+[1+(i-1)//k for i in range(1,n)]
 def v(a,j):return 0 if j==0 else 1+(j-1)*k+a
 def add(a,b):
  if a!=b:adj[a].add(b);adj[b].add(a)
 for a in range(k):
  for j in range(L):add(v(a,j),v(a,j+1))
 possible=[]
 for j in range(1,L+1):
  for a,b in combinations(range(k),2):
   possible.append((v(a,j),v(b,j)))
   if j<L:possible.extend([(v(a,j),v(b,j+1)),(v(b,j),v(a,j+1))])
 if kind=='random':
  p=(.015,.04,.1,.25)[t%4]
  for a,b in possible:
   if rng.random()<p:add(a,b)
 elif kind=='alternating_gates':
  period=2+t%5
  for j in range(1,L+1):
   if j%period==0:
    a=(j//period)%(k-1);add(v(a,j),v(a+1,j))
 else:
  # Sparse diagonal shortcuts with changing track pairs, not an imported template.
  for j in range(1,L):
   if j%(2+t%4)==0:
    a=(j+t)%k;b=(a+1+(t//4)%(k-1))%k;add(v(a,j),v(b,j+1))
 assert all(abs(level[a]-level[b])<=1 for a in range(n) for b in adj[a])
 return adj,level
results=[];best=None;trials=0
for k in (2,3,4):
 for L in (12,24,48):
  for kind in ('random','alternating_gates','diagonal_gates'):
   for t in range(8):
    adj,level=graph(k,L,kind,t);trials+=1
    # Certified v-root width k from explicit monotone path cover and last layer.
    for a in (0,k-1):
     u=1+(L//2-1)*k+a;data=root_data(adj,u)
     record=dict(k=k,L=L,kind=kind,trial=t,root=u,value=data['value'],ratio_numerator=data['value'],ratio_denominator=k)
     results.append(record)
     if best is None or data['value']*best['k']>best['data']['value']*k:
      best=dict(k=k,L=L,kind=kind,trial=t,edges=[(a,b) for a in range(len(adj)) for b in adj[a] if a<b],levels=level,data=data)
  row=[r for r in results if r['k']==k and r['L']==L];print(json.dumps(dict(stage='length_done',k=k,L=L,best_width=max(r['value'] for r in row),seconds=time.monotonic()-start)),flush=True)
(P/'corridor_probe.json').write_text(json.dumps(dict(status='DIAGNOSTIC_ONLY',trials=trials,root_evaluations=len(results),results=results,best=best,seconds=time.monotonic()-start),separators=(',',':'))+'\n')
print(json.dumps(dict(status='DIAGNOSTIC_ONLY',trials=trials,root_evaluations=len(results),best_ratio=[best['data']['value'],best['k']],seconds=time.monotonic()-start)),flush=True)
