"""Definition-first finite checks for the all-m written theorem; stdlib only.

No discovery imports, no optimizer, no closed-form distances used for checking
geodesics. All distances are recomputed by BFS in the original full graph.
The mathematical proof is universal; these finite checks are supplementary.
"""
from itertools import product,permutations,combinations
from collections import deque,Counter
import json,platform

def graph(m):
 w=[x for x in product(range(m),repeat=3) if x[0]!=x[1] and x[1]!=x[2]]
 index={x:i for i,x in enumerate(w)}
 # Independent ordered-pair adjacency, rather than append constructor.
 a=[[j for j,y in enumerate(w) if x[1:]==y[:2] and x[2]!=y[2]] for x in w]
 D=[]
 for root in range(len(w)):
  d=[-1]*len(w);d[root]=0;q=deque([root])
  while q:
   u=q.popleft()
   for v in a[u]:
    if d[v]<0:d[v]=d[u]+1;q.append(v)
  D.append(d)
 return w,index,a,D

def violates(D,t):
 return any(D[u][v]+D[v][z]==D[u][z] for u,v,z in permutations(t))

def is_gp(D,ids):return all(not violates(D,t) for t in combinations(ids,3))

def exhaustive(w,D,allowed):
 bad=[]
 for t in combinations(range(len(allowed)),3):
  if violates(D,[allowed[i] for i in t]):bad.append(sum(1<<i for i in t))
 count=0;maximum=0;weighted=0;missing_tests=0
 for mask in range(1<<len(allowed)):
  if any(mask&b==b for b in bad):continue
  count+=1;ids=[allowed[i] for i in range(len(allowed)) if mask>>i&1]
  maximum=max(maximum,len(ids));weighted=max(weighted,sum(len(set(w[i])) for i in ids))
  for z in range(max(max(x) for x in w)+1):
   if any(w[i][0]==z for i in ids):continue
   B=set(range(max(max(x) for x in w)+1))-{z}
   M={(w[i][0],w[i][2]) for i in ids if w[i][1]==z}
   E={(w[i][0],w[i][1]) for i in ids if w[i][2]==z}
   image=[]
   for x,y in E:
    cell=(y,x) if (y,x) not in M else (x,x)
    assert cell not in M;image.append(cell)
   assert len(set(image))==len(E)
   assert sum(z in w[i] for i in ids)<=len(B)**2;missing_tests+=1
 return {'subsets_considered':1<<len(allowed),'GP_sets':count,'maximum':maximum,
         'max_distinct_letter_weight':weighted,'injection_tests':missing_tests}

def run():
 stats=Counter();lower=[];base=None;restricted=None
 for m in range(3,9):
  w,index,a,D=graph(m);N=len(w)
  assert N==m*(m-1)**2 and all(len(ns)==m-1 for ns in a)
  assert max(map(max,D))<=3 and all(d>=0 for row in D for d in row)
  for i,u in enumerate(w):
   for j,v in enumerate(w):
    formula=0 if i==j else 1 if u[1:]==v[:2] else 2 if u[-1]==v[0] else 3
    assert D[i][j]==formula;stats['distance_formula_pairs']+=1
  selected=[i for i,x in enumerate(w) if x[1]<x[0] and x[1]<x[2]]
  target=m*(m-1)*(2*m-1)//6
  assert len(selected)==target and all(v not in selected for u in selected for v in a[u])
  # Explicitly test every ordered triple of each fixed lower-bound set.
  assert is_gp(D,selected);stats['lower_unordered_triples']+=len(selected)*(len(selected)-1)*(len(selected)-2)//6
  lower.append({'m':m,'vertices':N,'size':target})
  def bad(*xs):
   ids=[index[x] for x in xs];assert len(set(ids))==3
   assert violates(D,ids);stats['local_geodesic_checks']+=1
  # All local patterns in the missing-first-letter injection.
  for x,y in permutations(range(1,m),2):
   bad((x,y,0),(y,0,x),(x,0,x))
   for z in set(range(1,m))-{x,y}:bad((x,y,0),(y,0,x),(x,z,0))
  # All selected arc cases, without assuming any count/deletion theorem.
  for i,u in enumerate(w):
   aa,b,c=u
   for j in a[i]:
    v=w[j];d=v[2]
    if d!=aa and d!=b:
     for x in w:
      if x[0]==d:bad(u,v,x)
     stats['case_I_arcs']+=1
    elif d==b and c!=aa:
     for x in w:
      if x[2]==aa:bad(u,v,x)
     stats['case_II_arcs']+=1
    elif d==aa:
     for x in w:
      if (x[0]==aa and x!=u) or (x[2]==aa and x!=v):bad(u,v,x)
     bad((b,aa,b),u,v);bad(u,v,(c,aa,c));stats['case_III_arcs']+=1
    else:
     assert c==aa and d==b
     for x in w:
      if x in (u,v):continue
      if x[0] in (aa,b) or x[2] in (aa,b):bad(u,v,x)
     stats['case_IV_arcs']+=1
  if m==3:
   base=exhaustive(w,D,list(range(N)));assert base['maximum']==5
   # All base-case exclusion patterns in Section5.
   for aa,b,d in permutations(range(3)):
    bad((b,aa,b),(aa,b,aa),(b,aa,d))
   for aa,b,c in permutations(range(3)):bad((aa,b,c),(b,c,b),(c,b,c))
   # Deliberately corrupted lower-bound set must violate a true BFS geodesic.
   extra=next(i for i in range(N) if i not in selected and not is_gp(D,selected+[i]))
   assert not is_gp(D,selected+[extra]);stats['negative_controls']+=1
  if m==4:
   allowed=[i for i,x in enumerate(w) if 0 in x and x[0]!=0]
   assert len(allowed)==15
   restricted=exhaustive(w,D,allowed);assert restricted['maximum']==9
  # Verify alphabet restriction using a separately rebuilt smaller graph.
  sw,si,sa,sd=graph(m-1)
  for x in sw:
   for y in sw:
    assert sd[si[x]][si[y]]==D[index[x]][index[y]];stats['isometry_pairs']+=1
 # Essential range/definition controls.
 w,index,a,D=graph(2);assert len(w)==2 and is_gp(D,[0,1])
 assert len(w)>2*1*3//6;stats['negative_controls']+=1
 assert index[(1,0,1)] in a[index[(0,1,0)]] # full-old-word exclusion would be WRONG
 stats['negative_controls']+=1
 print(json.dumps({'status':'PASS','python':platform.python_version(),'stats':dict(stats),
  'lower_bounds':lower,'exhaustive_m3':base,'restricted_m4':restricted,
  'scope':'finite original-definition replay; universal proof is in PROOF.md'},sort_keys=True))
if __name__=='__main__':run()
