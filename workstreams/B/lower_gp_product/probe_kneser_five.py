"""Third, genuinely new mechanism after the universal triple theorem.
Exact five-landmark distance signatures in K(12,2) x K(12,2), factor lowerGP=6 follows from the matching/star/K4 classification for n>=12;
this discovery still directly checks all GP sets of sizes2,3,4 are extendable. Every ordered list of five
edges is covered up to symbol relabeling; repeated landmarks are included.
No claim about arbitrary factors follows from absence of a candidate.
"""
from itertools import combinations,product
from collections import Counter
from pathlib import Path
import json,time
P=Path(__file__).parent;start=time.monotonic();vertices=list(combinations(range(12),2));N=len(vertices);index={e:i for i,e in enumerate(vertices)}
def distance(a,b):return 0 if a==b else (1 if set(a).isdisjoint(b) else 2)
D=[[distance(a,b) for b in vertices] for a in vertices]
L=[[0]*N for _ in range(N)]
for i,j in combinations(range(N),2):L[i][j]=L[j][i]=sum(1<<u for u in range(N) if D[i][u]+D[u][j]==D[i][j] or abs(D[u][i]-D[u][j])==D[i][j])
full=(1<<N)-1;factor_sets=0
for k in (2,3,4):
 for S in combinations(range(N),k):
  if any(L[a][b]>>c&1 for a,b,c in combinations(S,3)):continue
  covered=sum(1<<v for v in S)
  for a,b in combinations(S,2):covered|=L[a][b]
  assert covered!=full;factor_sets+=1

def normalize(edges):
 # All existing labels and one/two fresh labels, with no arbitrary label bound.
 if len(edges)==5:yield tuple(edges);return
 m=max(max(e) for e in edges)+1
 for e in list(combinations(range(m),2))+[(v,m) for v in range(m)]+[(m,m+1)]:
  yield from normalize(edges+[e])
patterns={};raw=0
for E in normalize([(0,1)]):
 raw+=1
 M=tuple(tuple(distance(a,b) for b in E) for a in E)
 # A projection that is distinct and GP is impossible in any minimal witness
 # here, by extension in that factor; skip without assuming a new theorem.
 if len(set(E))==5 and all(M[a][b]+M[b][c]!=M[a][c] and M[a][c]+M[c][b]!=M[a][b] and M[b][a]+M[a][c]!=M[b][c] for a,b,c in combinations(range(5),3)):continue
 sig=Counter(tuple(distance(v,e) for e in E) for v in vertices)
 key=(M,tuple(sorted(sig.items())))
 patterns.setdefault(key,dict(edges=E,matrix=M,signatures=list(sig.items())))
patterns=list(patterns.values());tested=0;gp_sets=0;candidate=None
print(json.dumps(dict(stage='patterns',factor_gp_sets_extendable=factor_sets,raw_landmark_presentations=raw,distinct_patterns=len(patterns),seconds=time.monotonic()-start)),flush=True)
for ia,A in enumerate(patterns):
 for ib in range(ia,len(patterns)):
  B=patterns[ib];tested+=1
  if len(set(zip(A['edges'],B['edges'])))<5:continue
  M=[[A['matrix'][i][j]+B['matrix'][i][j] for j in range(5)] for i in range(5)]
  if any(M[i][j]+M[j][k]==M[i][k] or M[i][k]+M[k][j]==M[i][j] or M[j][i]+M[i][k]==M[j][k] for i,j,k in combinations(range(5),3)):continue
  gp_sets+=1;extendable=False
  for (a,ca),(b,cb) in product(A['signatures'],B['signatures']):
   d=[a[i]+b[i] for i in range(5)]
   if 0 in d:continue # exactly a selected product point
   if all(d[i]+d[j]!=M[i][j] and abs(d[i]-d[j])!=M[i][j] for i,j in combinations(range(5),2)):
    extendable=True;break
  if not extendable:
   candidate=dict(graph='Kneser K(12,2) square itself',factor_order=N,selected=list(zip(A['edges'],B['edges'])),factor_lower_bound=6,product_upper_bound=5)
   (P/'candidate_kneser_five.json').write_text(json.dumps(candidate,indent=2)+'\n');break
 if candidate:break
 if time.monotonic()-start>120:break
complete=ia==len(patterns)-1 and candidate is None
print(json.dumps(dict(status='CANDIDATE' if candidate else ('NO_CANDIDATE_COMPLETE_FAMILY' if complete else 'INCOMPLETE_TIME_LIMIT'),pattern_pairs=tested,gp_quintuples=gp_sets,pattern_count=len(patterns),factor_gp_sets_extendable=factor_sets,seconds=time.monotonic()-start)))
(P/'kneser_five_probe.json').write_text(json.dumps(dict(candidate=candidate,complete=complete,raw_presentations=raw,pattern_count=len(patterns),pattern_pairs=tested,gp_quintuples=gp_sets,factor_gp_sets_extendable=factor_sets),indent=2)+'\n')
