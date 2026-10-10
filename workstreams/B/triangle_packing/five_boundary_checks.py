"""Original-graph edge cases and negative controls for five-color theorem."""
import copy,json
from construct_five import construct
from verify_colored_graph import verify_original

def restrict(cert,keep):
 keep=sorted(keep);index={v:i for i,v in enumerate(keep)}
 return {'adjacency':[[index[w] for w in cert['adjacency'][v] if w in index] for v in keep],'colors':[cert['colors'][v] for v in keep],'sequence':[1,2,3,4,5]}
cases={}
for n in range(3,17):
 c=construct((n-1,));c=restrict(c,set(range(n+1))-{2});cases['cycle'+str(n)]=c
 p=copy.deepcopy(c);u=0;v=p['adjacency'][u][0];p['adjacency'][u].remove(v);p['adjacency'][v].remove(u);cases['path'+str(n)]=p
cases['isolated']={'adjacency':[[]],'colors':[0],'sequence':[1,2,3,4,5]}
cases['edge']={'adjacency':[[1],[0]],'colors':[0,1],'sequence':[1,2,3,4,5]}
cases['direct_caps']={'adjacency':[[1,2,3],[0,2],[0,1],[0,4,5],[3,5],[3,4]],'colors':[0,1,3,2,0,1],'sequence':[1,2,3,4,5]}
c=construct((2,3,2));u=1;v=9;c['adjacency'][u].remove(v);c['adjacency'][v].remove(u);cases['leaf_cap_chain']=c
combined={'adjacency':[],'colors':[],'sequence':[1,2,3,4,5]}
for c in [cases['cycle5'],cases['direct_caps'],cases['isolated']]:
 off=len(combined['adjacency']);combined['adjacency'] += [[v+off for v in ns] for ns in c['adjacency']];combined['colors']+=c['colors']
cases['disjoint']=combined
for c in cases.values():verify_original(c)
base=construct((2,3,2,4));negative=[]
for kind in ['same_color_edge','asymmetric_edge','close_color5']:
 bad=copy.deepcopy(base)
 if kind=='same_color_edge':bad['colors'][bad['adjacency'][0][0]]=bad['colors'][0]
 if kind=='asymmetric_edge':bad['adjacency'][0].pop()
 if kind=='close_color5':bad['colors'][2]=bad['colors'][5]=4 # consecutive apices at distance4
 try:verify_original(bad)
 except AssertionError:negative.append({'name':kind,'rejected':True})
 else:raise AssertionError('negative control accepted')
print(json.dumps({'result':'PASS','boundary_fixtures':len(cases),'names':list(cases),'negative_controls':negative},indent=2))
