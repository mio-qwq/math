"""Additional original-hypothesis boundary fixtures for the written theorem."""
import json
from explore import Graph,graph
from degeneracy_check import certificate,verify
cases={}
for n in range(1,12):
 g=Graph();[g.v() for _ in range(n)]
 for u in range(n-1):g.e(u,u+1)
 cases['path'+str(n)]=[set(ns) for ns in g.a]
 if n>=3:
  g.e(n-1,0);cases['cycle'+str(n)]=[set(ns) for ns in g.a]
g=Graph();a=g.tri();b=g.tri();g.e(a[0],b[0]);cases['direct_caps']=g.a
for tail in [1,2,3]:
 g=Graph();u=g.tri()[0];v=g.v();g.path(u,v,tail);cases['cap_leaf_'+str(tail)]=g.a
g=graph((2,3,2),'cycle');g.a[9].remove(1);g.a[1].remove(9)
cases['cut_necklace']=g.a
joined=[]
for a in [cases['cycle5'],cases['cycle5'],cases['direct_caps']]:
 off=len(joined);joined.extend({v+off for v in row} for row in a)
cases['disjoint']=joined
for name,a in cases.items():verify(certificate(a))
print(json.dumps({'boundary_cases':len(cases),'names':list(cases),'result':'PASS'},indent=2))
