"""Probe a NEW sufficient condition, not original-palette UNSAT."""
import random,json,itertools

def test(n,es):
 a=[set() for _ in range(n)]
 for u,v in es:a[u].add(v);a[v].add(u)
 for mask in range(1<<n):
  I={u for u in range(n) if mask>>u&1}
  if any(a[u]&I for u in I):continue
  if any(not any(a[w]&I=={u} for w in a[u]) for u in I):continue
  c={};ok=True
  for root in range(n):
   if root in I or root in c:continue
   c[root]=0;q=[root]
   for u in q:
    for v in a[u]-I:
     if v not in c:c[v]=1-c[u];q.append(v)
     elif c[v]==c[u]:ok=False;break
    if not ok:break
   if not ok:break
  if ok:return sorted(I)
 return None

def core(n,rng):
 for _ in range(10000):
  stubs=list(range(n))*3;rng.shuffle(stubs);es=[tuple(sorted(stubs[i:i+2])) for i in range(0,len(stubs),2)]
  if any(u==v for u,v in es):continue
  seen={0}
  while True:
   new=seen|{v for u,v in es if u in seen}|{u for u,v in es if v in seen}
   if new==seen:break
   seen=new
  if len(seen)==n:return sorted(es)
 raise RuntimeError
if __name__=='__main__':
 rng=random.Random(13579)
 for n in [2,4,6,8,10,12,14]:
  good=bad=0
  for rep in range(30):
   es=core(n,rng)
   if n==4 and len(set(es))==6:continue
   witness=test(n,es)
   if witness is None:
    bad+=1;print(json.dumps({'route_failure':True,'n':n,'edges':es}),flush=True)
   else:good+=1
  print(json.dumps({'n':n,'success':good,'failure':bad}),flush=True)
