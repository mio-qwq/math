"""Direct Floyd-Warshall and triple equalities; no discovery imports."""
from pathlib import Path
from itertools import combinations,permutations
import json
P=Path(__file__).parent;count=0;triples=0;outside=0
for filename in ('cubic_probe.json','subdivision_probe.json'):
 for r in json.loads((P/filename).read_text()):
  if r['status']!='WITNESS':continue
  n=r['order'];S=r['selected'];D=[[0 if u==v else n+1 for v in range(n)] for u in range(n)]
  for u,v in r['edges']:assert u!=v;D[u][v]=D[v][u]=1
  for k in range(n):
   for i in range(n):
    for j in range(n):D[i][j]=min(D[i][j],D[i][k]+D[k][j])
  assert max(map(max,D))==r['diameter'] and max(map(max,D))<=n-1
  for a,b,c in combinations(S,3):
   triples+=1
   assert D[a][b]+D[b][c]!=D[a][c] and D[a][c]+D[c][b]!=D[a][b] and D[b][a]+D[a][c]!=D[b][c]
  for u in set(range(n))-set(S):
   outside+=1
   assert any(D[u][a]+D[a][b]==D[u][b] for a,b in permutations(S,2))
  count+=1
# A maximal GP set need not be terminal: endpoints of P3 violate endpoint coverage.
D=[[0,1,2],[1,0,1],[2,1,0]];S=[0,2]
assert not any(D[1][a]+D[a][b]==D[1][b] for a,b in permutations(S,2))
print(json.dumps(dict(status='PASS',positive_witnesses=count,gp_triples=triples,outside_endpoint_checks=outside,negative_controls=1,scope='finite witnesses only; no universal theorem or independent reviewer')))
