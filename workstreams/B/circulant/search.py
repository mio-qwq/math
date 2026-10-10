import numpy as np,time,json,platform,sys,hashlib,random
from itertools import permutations
from collections import deque
from pathlib import Path
ROOT=Path(__file__).parent
rng=random.Random(15909)
def prepare(n,d):
 D=((np.arange(n)[None,:]-np.arange(n)[:,None])%n+d-1)//d
 bad={}
 for u in range(n):
  for v in range(u+1,n):
   b=(D[u,v]==D[u,:]+D[:,v])|(D[v,u]==D[v,:]+D[:,u])|(D[u,:]==D[u,v]+D[v,:])|(D[:,u]==D[:,v]+D[v,u])|(D[v,:]==D[v,u]+D[u,:])|(D[:,v]==D[:,u]+D[u,v])
   bad[u,v]=sum(1<<int(w) for w in np.flatnonzero(b))
 return bad
def verify(n,d,S):
 D=[]
 for u in range(n):
  ds=[-1]*n;ds[u]=0; Q=deque([u])
  while Q:
   v=Q.popleft()
   for step in range(1,d+1):
    w=(v+step)%n
    if ds[w]<0:ds[w]=ds[v]+1;Q.append(w)
  D.append(ds)
 violations=[(u,v,w) for u,v,w in permutations(S,3) if D[u][w]==D[u][v]+D[v][w]]
 return {'bfs_all_vertices':n,'ordered_triples_checked':len(S)*(len(S)-1)*(len(S)-2),'violations':violations,'distance_matrix_subset':[[D[u][v] for v in S] for u in S]}
def search(n,d,seconds=0.2):
 bad=prepare(n,d); bound=max(n%d,(d+1+n%d-1)//(n%d)); target=bound+1
 end=time.monotonic()+seconds;nodes=0;best=[0]
 def dfs(S,C):
  nonlocal nodes,best
  nodes+=1
  if len(S)>len(best):best=S
  if len(S)>=target:return S
  if time.monotonic()>end:raise TimeoutError
  while C.bit_count()+len(S)>=target:
   b=C&-C;C-=b;v=b.bit_length()-1;N=C
   for u in S:N &= ~bad[min(u,v),max(u,v)]
   r=dfs(S+[v],N)
   if r:return r
  return None
 try:r=dfs([0],(1<<n)-2);status='exhausted' if r is None else 'witness'
 except TimeoutError:r=None;status='timeout'
 return r,{'n':n,'d':d,'q':n//d,'a':n%d,'bound':bound,'status':status,'nodes':nodes,'best':best}
def main():
 cases=[]
 for d in range(16,61):
  for a in range(2,min(d,13)):
   if max(a,(d+a)//a)<=12:
    for q in [1,2,3,5]:cases.append((q*d+a,d))
 rng.shuffle(cases)
 with open(ROOT/'search.jsonl','w') as log:
  for i,(n,d) in enumerate(cases):
   r,data=search(n,d);log.write(json.dumps(data)+'\n');log.flush()
   if i%20==0:print(i,data,flush=True)
   if r:
    data['S']=r;data['verification']=verify(n,d,r);(ROOT/'candidate.json').write_text(json.dumps(data,indent=2));print('FOUND',data,flush=True);break
if __name__=='__main__':main()
