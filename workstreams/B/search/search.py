import json,random,time,itertools,sys,os
ROOT=os.path.dirname(__file__)
class Graph:
 def __init__(self):self.a=[]
 def v(self):self.a.append(set());return len(self.a)-1
 def e(self,u,v):assert u!=v;self.a[u].add(v);self.a[v].add(u)
 def path(self,u,v,L):
  for k in range(L-1):w=self.v();self.e(u,w);u=w
  self.e(u,v)
 def square(self):
  vs=[self.v() for _ in range(4)]
  for i in range(4):self.e(vs[i],vs[(i+1)%4])
  return vs[0],vs[2]
 def triangle(self):
  vs=[self.v() for _ in range(3)]
  for i in range(3):self.e(vs[i],vs[(i+1)%3])
  return vs[0]
 def valid(self):
  if any(len(a)>3 for a in self.a):return False
  for v,a in enumerate(self.a):
   if len(a)!=3:continue
   if any(len(self.a[u])==3 for u in a):return False
   if not any((y in self.a[x] or self.a[x]&self.a[y]-{v}) for x,y in itertools.combinations(a,2)):return False
  return True

def necklace(ls):
 g=Graph();ss=[g.square() for _ in ls]
 for i,L in enumerate(ls):g.path(ss[i][1],ss[(i+1)%len(ss)][0],L)
 return g

def chain(ls):
 g=Graph();left=g.triangle();ss=[g.square() for _ in range(len(ls)-1)];right=g.triangle();ends=[(None,left)]+ss+[(right,None)]
 for i,L in enumerate(ls):g.path(ends[i][1],ends[i+1][0],L)
 return g

def solve(g,limit=10):
 n=len(g.a);conf=[[[] for _ in range(4)] for v in range(n)]
 for s in range(n):
  d={s:0};q=[s]
  for v in q:
   if d[v]==4:continue
   for w in g.a[v]:
    if w not in d:d[w]=d[v]+1;q.append(w)
  for v,dist in d.items():
   if dist:
    for c in range(dist-1,4):conf[s][c].append(v)
 degree=[sum(map(len,cs)) for cs in conf];nodes=0;deadline=time.time()+limit
 def rec(ds):
  nonlocal nodes
  nodes+=1
  if nodes%1024==0 and time.time()>deadline:raise TimeoutError
  best=-1;score=(5,0)
  for v,x in enumerate(ds):
   k=x.bit_count()
   if k>1 and (k,-degree[v])<score:score=(k,-degree[v]);best=v
  if best<0:return ds
  opts=[c for c in range(4) if ds[best]>>c&1]
  opts.sort(key=lambda c:sum(bool(ds[w]>>c&1) for w in conf[best][c]))
  for c in opts:
   nd=ds.copy();nd[best]=1<<c;todo=[best];ok=True
   while todo and ok:
    v=todo.pop();bit=nd[v];cc=bit.bit_length()-1
    for w in conf[v][cc]:
     if nd[w]&bit:
      nd[w]^=bit
      if not nd[w]:ok=False;break
      if nd[w].bit_count()==1:todo.append(w)
   if ok:
    r=rec(nd)
    if r:return r
  return None
 try:r=rec([15]*n);return ('SAT' if r else 'UNSAT'),nodes,r
 except TimeoutError:return 'TIMEOUT',nodes,None

def run():
 random.seed(329)
 log=open(ROOT+'/runs.jsonl','a',buffering=1)
 families=[]
 for k in range(1,8):
  for ls in itertools.product(range(2,6),repeat=k):
   if k>1 and ls!=min(ls[i:]+ls[:i] for i in range(k)):continue
   families.append(('necklace',ls))
   if k<=6:families.append(('chain',ls))
 random.shuffle(families)
 families.sort(key=lambda x:len(x[1]))
 for i,(fam,ls) in enumerate(families):
  g=globals()[fam](ls);assert g.valid();t=time.time();status,nodes,r=solve(g,2)
  row=dict(i=i,family=fam,lengths=ls,n=len(g.a),status=status,nodes=nodes,seconds=time.time()-t)
  log.write(json.dumps(row)+'\n')
  if i%100==0 or status!='SAT':print(row,flush=True)
  if status=='UNSAT':
   row['adjacency']=[sorted(a) for a in g.a];json.dump(row,open(ROOT+'/candidate.json','w'),indent=2);return
 print('ALL DONE',len(families))
if __name__=='__main__':run()
