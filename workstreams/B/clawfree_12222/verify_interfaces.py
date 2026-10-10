"""Original-definition exact checker for the candidate theorem's finite interfaces.
Does not import the discovery program, search solver, or its judgments.
"""
from itertools import product,combinations
from collections import deque
from pathlib import Path
import json,platform,copy
SEQ=[1,2,2,2,2]
HERE=Path(__file__).resolve().parent

def distances(n,E):
 A=[set() for _ in range(n)]
 for u,v in E:
  assert 0<=u<n and 0<=v<n and u!=v and v not in A[u]
  A[u].add(v);A[v].add(u)
 D=[]
 for s in range(n):
  d=[-1]*n;d[s]=0;q=deque([s])
  while q:
   u=q.popleft()
   for v in A[u]:
    if d[v]<0:d[v]=d[u]+1;q.append(v)
  D.append(d)
 return A,D

def valid(c,D):
 return all(c[u]!=c[v] or D[u][v]>SEQ[c[u]] for u,v in combinations(range(len(c)),2))

def verify_caps(rows):
 triangles=lambda a,b,c:[(a,b),(a,c),(b,c)]
 defs={
 'diamond_loop_cap':(7,0,triangles(0,1,2)+[(1,3),(2,4),(3,5),(3,6),(4,5),(4,6),(5,6)]),
 'parallel_pendant_cap':(6,2,triangles(0,1,2)+triangles(3,4,5)+[(0,3),(1,4)]),
 'parallel_same_neighbor_cap':(9,8,triangles(0,1,2)+triangles(3,4,5)+triangles(6,7,8)+[(0,3),(1,4),(2,6),(5,7)])}
 seen=set();pairs=0
 for row in rows:
  n,root,E=defs[row['name']];E=E+[(root,n)]
  assert row['root']==root and row['outside']==n
  assert {tuple(sorted(e)) for e in E}=={tuple(sorted(e)) for e in row['edges']}
  assert len(row['colors'])==n+1
  c=row['colors'];assert [c[root],c[n]]==row['pre']
  A,D=distances(n+1,E);assert valid(c,D)
  assert all(len(ns)<=3 for ns in A)
  assert all(any(y in A[x] for x,y in combinations(ns,2)) for ns in A if len(ns)==3)
  assert all(D[v][n]>=2 for v in range(n) if v!=root)
  seen.add((row['name'],tuple(row['pre'])));pairs+=(n+1)*n//2
 assert seen==set(product(defs,[(0,1),(1,0),(1,2)]))
 return pairs

def boundary_tests():
 # Maximal outside boundary stars; no assumption that they are claw-free.
 base=[(0,1),(0,2),(0,3),(1,4),(1,5)]
 _,D0=distances(6,base)
 DE=[e for e in base if e!=(0,1)]+[(0,6),(1,7),(6,8),(6,9),(7,8),(7,9),(8,9)]
 QE=[e for e in base if e!=(0,1)]+[(0,6),(1,9),(6,7),(6,8),(7,8),(9,10),(9,11),(10,11),(7,10),(8,11)]
 _,DD=distances(10,DE);_,DQ=distances(12,QE)
 count=0;pairs=0
 for c in product(range(5),repeat=6):
  if not valid(c,D0):continue
  old_u,old_v=c[:2];a,b=old_v,old_u
  spare=[x for x in range(1,5) if x not in (a,b)]
  dc=list(c)+[a,b,spare[0],spare[1]];assert valid(dc,DD)
  if a and b:x,w=0,0;y,z=spare
  elif a==0:z=0;x,y,w=spare
  else:x=0;z,w,y=spare
  qc=list(c)+[a,x,y,b,z,w];assert valid(qc,DQ)
  count+=1;pairs+=45+66
 return count,pairs

def main():
 rows=json.loads((HERE/'cap_witnesses.json').read_text());cp=verify_caps(rows)
 b,p=boundary_tests()
 damaged=copy.deepcopy(rows);r=damaged[0];r['colors'][r['root']]=r['colors'][r['outside']]
 try:verify_caps(damaged)
 except AssertionError:pass
 else:raise AssertionError('corruption not rejected')
 # Independent literal leaf-extension check with all valid old neighbor colors.
 leaf=0
 for deg in range(1,4):
  E=[(0,i) for i in range(1,deg+1)];_,D=distances(deg+1,E)
  for c in product(range(5),repeat=deg):
   # Old star is on0..deg-1, new leaf is deg.
   _,oldD=distances(deg,[(0,i) for i in range(1,deg)])
   if valid(c,oldD):assert any(valid(list(c)+[x],D) for x in range(5));leaf+=1
 print(json.dumps({'python':platform.python_version(),'status':'PASS','cap_rows':len(rows),'cap_distance_pairs':cp,'boundary_colorings':b,'expanded_boundary_distance_pairs':p,'leaf_precolorings':leaf,'negative_controls':1,'scope':'finite interfaces only; universal reduction and imported incidence theorem are in CUBIC_PROOF.md'},sort_keys=True))
if __name__=='__main__':main()
