"""Second mechanism: all vertices have a true twin, forcing factor lowerGP>=4.
Every maximal GP set contains each used twin class in full; its projection is
maximal GP in the base. Base connected order>=2 has lowerGP>=2.
"""
from probe_product import metric,small_maximal
from itertools import combinations,combinations_with_replacement
from pathlib import Path
import json,time
P=Path(__file__).parent;start=time.monotonic();factors=[];checks=[]
# Different metric cores, including nonbipartite diameter>=3 cases.
for n,chords in [(5,[]),(6,[(0,2)]),(7,[]),(7,[(0,3)]),(8,[(0,3),(3,6)]),(9,[(0,4),(4,7)])]:
 core={tuple(sorted((i,(i+1)%n))) for i in range(n)}|set(chords)
 edges=[(u,v) for u,v in combinations(range(2*n),2) if u//2==v//2 or tuple(sorted((u//2,v//2))) in core]
 D=metric(2*n,edges);small,_=small_maximal(D);assert small is None
 factors.append(dict(order=2*n,edges=edges,distances=D,core_order=n,core_edges=sorted(core)))
for i,j in combinations_with_replacement(range(len(factors)),2):
 if time.monotonic()-start>60:break
 G,H=factors[i],factors[j];g=G['order'];h=H['order'];N=g*h
 D=[[G['distances'][a//h][b//h]+H['distances'][a%h][b%h] for b in range(N)] for a in range(N)]
 S,tested=small_maximal(D);checks.append(dict(factors=[i,j],order=N,tested=tested,selected=S))
 if S is not None:
  (P/'candidate_blowup.json').write_text(json.dumps(dict(G=G,H=H,product_selected=[divmod(v,h) for v in S]),indent=2)+'\n');break
 print(json.dumps(dict(factors=[i,j],product_order=N,status='NO_SMALL_MAXIMAL_GP',seconds=time.monotonic()-start)),flush=True)
(P/'blowup_probe.json').write_text(json.dumps(dict(factors=factors,checks=checks),separators=(',',':'))+'\n')
print(json.dumps(dict(status='CANDIDATE' if any(c['selected'] is not None for c in checks) else 'NO_CANDIDATE_IN_WINDOW',products=len(checks),subsets_tested=sum(c['tested'] for c in checks),seconds=time.monotonic()-start)))
