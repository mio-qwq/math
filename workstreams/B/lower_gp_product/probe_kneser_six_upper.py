"""A new upper mechanism, not an inference from the lower-bound search.
Try all correlations of the known six-edge K4 GP-set in the two factors.
Six symbols cover every outside distance signature to a four-symbol support.
"""
from itertools import combinations,permutations,product
from pathlib import Path
import json
P=Path(__file__).parent;A=list(combinations(range(4),2));V=list(combinations(range(6),2))
def d(a,b):return 0 if a==b else (1 if set(a).isdisjoint(b) else 2)
def pd(x,y):return d(x[0],y[0])+d(x[1],y[1])
best=10**9;bestS=None;count=0
for B in permutations(A):
 count+=1;S=list(zip(A,B));M=[[pd(x,y) for y in S] for x in S];miss=[]
 assert all(M[i][j]+M[j][k]!=M[i][k] and M[i][k]+M[k][j]!=M[i][j] and M[j][i]+M[i][k]!=M[j][k] for i,j,k in combinations(range(6),3))
 for z in product(V,repeat=2):
  if z in S:continue
  ds=[pd(z,s) for s in S]
  if all(ds[i]+ds[j]!=M[i][j] and abs(ds[i]-ds[j])!=M[i][j] for i,j in combinations(range(6),2)):miss.append(z)
 if len(miss)<best:best=len(miss);bestS=S
 if not miss:
  (P/'kneser_six_upper_candidate.json').write_text(json.dumps(dict(selected=S,support=4,signature_alphabet=6,scope='candidate maximal GP six-set for all n,m>=6, pending verification'),indent=2)+'\n');break
print(json.dumps(dict(status='CANDIDATE' if best==0 else 'NO_CANDIDATE_IN_FAMILY',permutations=count,minimum_uncovered=best,selected=bestS)))
