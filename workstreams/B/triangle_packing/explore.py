"""B's bounded discovery experiment. SAT/UNSAT is exact; timeout is UNKNOWN."""
from collections import deque,Counter
from itertools import product
import time,json,sys
from pathlib import Path

class Graph:
 def __init__(self): self.a=[]
 def v(self): self.a.append(set());return len(self.a)-1
 def e(self,u,v): assert u!=v;self.a[u].add(v);self.a[v].add(u)
 def tri(self):
  u,v,w=[self.v() for _ in range(3)]
  for x,y in [(u,v),(v,w),(w,u)]:self.e(x,y)
  return u,v
 def path(self,u,v,n):
  for _ in range(n-1):w=self.v();self.e(u,w);u=w
  self.e(u,v)
 def valid(self):
  for v,ns in enumerate(self.a):
   if len(ns)>3:return False
   if len(ns)==3:
    if sum(len(self.a[u])==3 for u in ns)>1:return False
    if not any(self.a[u]&ns for u in ns):return False
  return True

def graph(gaps,kind):
 g=Graph()
 if kind=='cycle':
  ts=[g.tri() for _ in gaps]
  for i,L in enumerate(gaps):g.path(ts[i][1],ts[(i+1)%len(ts)][0],L)
 else:
  ts=[g.tri() for _ in range(len(gaps)+1)]
  if kind=='leaves':ts[0]=(None,g.v());ts[-1]=(g.v(),None) # unused endpoint triangles stay components; excluded below
  for i,L in enumerate(gaps):g.path(ts[i][1],ts[i+1][0],L)
 assert g.valid()
 return g

def distances(a):
 out=[]
 for s in range(len(a)):
  d=[10**6]*len(a);d[s]=0;q=deque([s])
  while q:
   v=q.popleft()
   for w in a[v]:
    if d[w]==10**6:d[w]=d[v]+1;q.append(w)
  out.append(d)
 return out

def solve(a,seq,limit=2):
 n=len(a);D=distances(a);k=len(seq)
 conf=[[[w for w in range(n) if w!=v and D[v][w]<=s] for s in seq] for v in range(n)]
 deg=[sum(map(len,x)) for x in conf];nodes=0;deadline=time.monotonic()+limit
 def rec(ds):
  nonlocal nodes
  nodes+=1
  if nodes%256==0 and time.monotonic()>deadline:raise TimeoutError
  vs=[v for v in range(n) if ds[v].bit_count()>1]
  if not vs:return [x.bit_length()-1 for x in ds]
  v=min(vs,key=lambda v:(ds[v].bit_count(),-deg[v]))
  cs=[c for c in range(k) if ds[v]>>c&1]
  cs.sort(key=lambda c:sum(bool(ds[w]>>c&1) for w in conf[v][c]))
  for c in cs:
   nd=ds.copy();nd[v]=1<<c;q=[v];ok=True
   while q and ok:
    u=q.pop();bit=nd[u];color=bit.bit_length()-1
    for w in conf[u][color]:
     if nd[w]&bit:
      nd[w]^=bit
      if not nd[w]:ok=False;break
      if nd[w].bit_count()==1:q.append(w)
   if ok:
    ans=rec(nd)
    if ans is not None:return ans
  return None
 try:
  ans=rec([(1<<k)-1]*n)
  if ans is not None:
   assert all(ans[u]!=ans[v] or D[u][v]>seq[ans[u]] for u in range(n) for v in range(u))
  return ('SAT' if ans is not None else 'UNSAT'),ans,nodes
 except TimeoutError:return 'UNKNOWN',None,nodes

def main():
 root=Path(__file__).parent;stats=Counter();start=time.monotonic();witnesses=[]
 seqs=[(1,2,3,3),(1,2,2,4),(2,2,2,2,4),(1,2,3,4,5)]
 for kind in ['cycle','chain']:
  for m in range(1,6):
   for gaps in product(range(2,7),repeat=m):
    if kind=='cycle' and gaps!=min(gaps[i:]+gaps[:i] for i in range(m)):continue
    if kind=='chain' and gaps>gaps[::-1]:continue
    g=graph(gaps,kind)
    for seq in seqs:
     if any(w['sequence']==list(seq) for w in witnesses):continue
     state,ans,nodes=solve(g.a,seq)
     stats[str(seq)+':'+state]+=1
     if state=='UNSAT':
      w={'kind':kind,'gaps':gaps,'sequence':list(seq),'adjacency':[sorted(ns) for ns in g.a],'nodes':nodes}
      witnesses.append(w);(root/('candidate_'+''.join(map(str,seq))+'.json')).write_text(json.dumps(w,indent=2)+'\n');print('CANDIDATE',json.dumps(w),flush=True)
    if time.monotonic()-start>90:break
   else:continue
   break
  if time.monotonic()-start>90:break
 out={'elapsed_seconds':time.monotonic()-start,'stats':dict(stats),'candidate_sequences':[w['sequence'] for w in witnesses]}
 (root/'experiment.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
