"""Reproducible generated and exhaustive small original-graph regressions."""
import itertools,random,json
from construct import construct
from verify_original import verify

def admissible(a):
 if any(len(ns)>3 for ns in a):return False
 if any(len(ns)==3 and not any(a[v]&ns for v in ns) for ns in a):return False
 h={u for u,ns in enumerate(a) if len(ns)==3 and all(len(a[v])==3 for v in ns)}
 return all(not(a[u]&h) for u in h)

def build(types,es,lengths):
 a=[];blocks=[]
 def edge(u,v):assert u!=v;a[u].add(v);a[v].add(u)
 for typ in types:
  p=len(a);a.extend([set() for _ in range(3 if typ=='t' else 4)])
  if typ=='t':
   for u,v in [(0,1),(0,2),(1,2)]:edge(p+u,p+v)
   blocks.append([p,p+1,p+2])
  else:
   for u,v in [(0,1),(0,2),(1,2),(1,3),(2,3)]:edge(p+u,p+v)
   blocks.append([p])
 used=[0]*len(types)
 for (u,v),L in zip(es,lengths):
  x=blocks[u][used[u]];used[u]+=1;y=blocks[v][used[v]];used[v]+=1
  for _ in range(L-1):w=len(a);a.append(set());edge(x,w);x=w
  edge(x,y)
 return a

stats={'small_admissible':0,'core_presentations':0,'leaf_disconnected':0};pairs=0;exchanges=0

def run(a,key):
 global pairs,exchanges
 c,meta=construct(a);pairs+=verify(a,c);exchanges+=meta['cycle_exchanges'];stats[key]+=1

# Exhaustive labeled simple graphs up to order six, exact original hypotheses.
for n in range(7):
 es=list(itertools.combinations(range(n),2))
 for mask in range(1<<len(es)):
  a=[set() for _ in range(n)]
  for i,(u,v) in enumerate(es):
   if mask>>i&1:a[u].add(v);a[v].add(u)
  if admissible(a):run(a,'small_admissible')
# Loops, parallel connectors, all-direct even residual cycles, and diamond caps.
templates=[(['t'],[(0,0)]),(['t','t'],[(0,1)]),(['t','t'],[(0,1)]*2),(['t','t'],[(0,1)]*3),(['d','d'],[(0,1)]),(['d','t','d'],[(0,1),(1,2)]),(['t']*3,[(0,1),(1,2),(2,0)]),(['d'],[]),(['t'],[])]
for types,es in templates:
 for lens in itertools.product(range(1,7),repeat=len(es)):
  if any(u==v and L==1 for (u,v),L in zip(es,lens)):continue
  a=build(types,es,lens)
  if admissible(a):run(a,'core_presentations')
# Random cubic cores, partial matched-heavy interfaces, and long paths.
rng=random.Random(306112)
for n in [4,6,8,10,20,40]:
 for rep in range(40):
  es=[(u,(u+1)%n) for u in range(n)]+[(u,u+n//2) for u in range(n//2)]
  types=['t']*n;new=[];lens=[]
  for i,(u,v) in enumerate(es):
   if i>=n and rng.random()<0.6:
    w=len(types);types.append('t');new.extend([(u,w),(w,v)]);lens.extend([1,1])
   else:new.append((u,v));lens.append(rng.randrange(2,12))
  a=build(types,new,lens);assert admissible(a);run(a,'core_presentations')
  # Attach leaves only at degree-two vertices, retaining triangles for new 3-vertices.
  tri2=[u for u,ns in enumerate(a) if len(ns)==2 and any(a[v]&ns for v in ns)]
  b=[ns.copy() for ns in a]
  if tri2:
   u=rng.choice(tri2);w=len(b);b.append({u});b[u].add(w)
   if admissible(b):
    p=len(b);b.extend([{p+1},{p,p+2},{p+1}]);run(b,'leaf_disconnected')
# Explicit pendant paths and disconnected odd/even cycles (including leaf neighbors).
for typ in ['t','d']:
 for length in range(1,16):
  a=build([typ],[],[]);last=0
  for _ in range(length):
   w=len(a);a.append({last});a[last].add(w);last=w
  p=len(a);k=3+length%8;a.extend([set() for _ in range(k)])
  for i in range(k):a[p+i].add(p+(i+1)%k);a[p+(i+1)%k].add(p+i)
  assert admissible(a);run(a,'leaf_disconnected')
# Separate rejected controls: original hypothesis and two wrong colorings.
K4=[set(range(4))-{u} for u in range(4)]
try:construct(K4)
except AssertionError:pass
else:raise AssertionError('heavy-heavy graph admitted')
a=build(['t','t'],[(0,1)]*2,[2,3]);c,_=construct(a)
u=0;v=next(iter(a[u]));bad=c.copy();bad[v]=bad[u]
try:verify(a,bad)
except AssertionError:pass
else:raise AssertionError('adjacent color corruption accepted')
bad=c.copy();bad[0]=bad[1]=2
try:verify(a,bad)
except AssertionError:pass
else:raise AssertionError('radius-two corruption accepted')
print(json.dumps({'status':'PASS','counts':stats,'distance_pairs':pairs,'cycle_exchanges':exchanges,'negative_controls':3},sort_keys=True))
