"""Exact certificate reconstruction for the (2,2,2,2,r) coloring argument.
Does not import or use the exploratory packing solver.
"""
from collections import deque
from itertools import product
import json,hashlib,platform,sys
from pathlib import Path

def bfs(a,s):
 d={s:0};q=deque([s])
 while q:
  u=q.popleft()
  for v in a[u]:
   if v not in d:d[v]=d[u]+1;q.append(v)
 return d

def hypotheses(a):
 n=len(a)
 for u,ns in enumerate(a):
  assert u not in ns and len(ns)<=3
  assert all(0<=v<n and u in a[v] for v in ns)
  if len(ns)==3:
   assert sum(len(a[v])==3 for v in ns)<=1
   assert any(v!=w and w in a[v] for v in ns for w in ns)

def certificate(a):
 hypotheses(a);n=len(a);D=[bfs(a,u) for u in range(n)]
 square=[{v for v,d in D[u].items() if 0<d<=2} for u in range(n)]
 comps=[];unseen=set(range(n))
 while unseen:
  s=min(unseen);comp=set(D[s]);unseen-=comp;comps.append(comp)
 records=[];colors=[None]*n
 for comp in comps:
  # Find, not assume, a deletable vertex. The full theorem is the written proof.
  for exceptional in [None]+sorted(comp):
   rem=comp-({exceptional} if exceptional is not None else set());order=[]
   while rem:
    opts=[v for v in rem if len(square[v]&rem)<=3]
    if not opts:break
    v=min(opts);order.append(v);rem.remove(v)
   if not rem:break
  else:raise AssertionError('No deletion has a 3-degenerate square')
  if exceptional is not None:colors[exceptional]=4
  for v in reversed(order):
   forbidden={colors[w] for w in square[v] if colors[w] is not None}
   colors[v]=next(c for c in range(4) if c not in forbidden)
  records.append({'component':sorted(comp),'exceptional':exceptional,'elimination_order':order})
 return {'adjacency':[sorted(ns) for ns in a],'colors':colors,'components':records}

def verify(cert,r=100):
 a=[set(ns) for ns in cert['adjacency']];hypotheses(a);n=len(a)
 assert all(len(ns)==len(set(ns)) for ns in cert['adjacency'])
 D=[bfs(a,u) for u in range(n)];cols=cert['colors'];assert len(cols)==n
 assert all(type(c) is int and 0<=c<=4 for c in cols)
 seen=set()
 for item in cert['components']:
  comp=set(item['component']);assert comp and not(seen&comp)
  assert comp==set(D[next(iter(comp))]);seen|=comp
  v=item['exceptional'];assert v is None or v in comp
  order=item['elimination_order'];rem=comp-({v} if v is not None else set())
  assert len(order)==len(rem) and set(order)==rem
  for u in order:
   assert sum(w!=u and D[u].get(w,10**9)<=2 for w in rem)<=3
   rem.remove(u)
  assert sum(cols[u]==4 for u in comp)<=1
 assert seen==set(range(n))
 for u in range(n):
  for v,d in D[u].items():
   if u<v and cols[u]==cols[v]:assert d>(r if cols[u]==4 else 2)
 return True

def main():
 # Generator imported only for fixtures; no coloring/search decision reused.
 from explore import graph
 count=0
 for kind in ['cycle','chain']:
  for m in range(1,6):
   for gaps in product(range(2,7),repeat=m):
    if kind=='cycle' and gaps!=min(gaps[i:]+gaps[:i] for i in range(m)):continue
    if kind=='chain' and gaps>gaps[::-1]:continue
    c=certificate(graph(gaps,kind).a);verify(c);count+=1
 root=Path(__file__).parent;sample=certificate(graph((2,3,2,4,2),'cycle').a)
 (root/'degeneracy_certificate.json').write_text(json.dumps(sample,indent=2)+'\n')
 neg=[]
 import copy
 for name,mutate in [
  ('same_color_edge',lambda c:c['colors'].__setitem__(c['adjacency'][0][0],c['colors'][0])),
  ('missing_vertex',lambda c:c['components'][0]['elimination_order'].pop()),
  ('too_many_special',lambda c:c['colors'].__setitem__(0,4) or c['colors'].__setitem__(1,4))]:
  c=copy.deepcopy(sample);mutate(c)
  try:verify(c)
  except (AssertionError,ValueError,IndexError):neg.append({'name':name,'rejected':True})
  else:raise AssertionError('Negative control accepted: '+name)
 print(json.dumps({'graphs':count,'result':'PASS','negative_controls':neg,'python':sys.version,'platform':platform.platform(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
if __name__=='__main__':main()
