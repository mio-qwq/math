#!/usr/bin/env python3
"""Exact enumeration of CDC automorphisms and strong guide conjugacy for finite n.
Complete flag is true ONLY if the VF2++ iterator exhausts without a time limit.
Results constitute finite checks, not proof of a general n formula.
"""
import networkx as nx
from claw_graph_gate import claw,cdc
from time import perf_counter
from collections import Counter
import signal,sys,json
class Timeout(Exception): pass
def handle(*_):raise Timeout()
signal.signal(signal.SIGALRM,handle)

def classify(n,seconds=18):
 K=cdc(claw(n));V=len(K);num=0;sw=0;aut=[];gs=[]; complete=False
 signal.alarm(seconds)
 try:
  for p in nx.algorithms.isomorphism.vf2pp_all_isomorphisms(K,K):
   perm=tuple(p[u] for u in range(V));aut.append(perm);num+=1
   if all(perm[2*i]%2==1 for i in range(V//2)):
    sw+=1
    if all(perm[perm[u]]==u and not K.has_edge(u,perm[u]) for u in K):
     gs.append(perm)
  complete=True
 except Timeout:pass
 finally:signal.alarm(0)
 counts={'n':n,'vertices':V,'aut':num,'switching':sw,'strong_guides':len(gs),'complete':complete,'networkx_version':nx.__version__}
 if complete:
  # Compute each guide conjugacy class by whole automorphism group.
  guide_to_index={g:i for i,g in enumerate(gs)}
  assert len(guide_to_index)==len(gs)
  visited=set();reps=[];sizes=[];all_clusters=[]
  for i,g in enumerate(gs):
   if i in visited:continue
   orbit=set()
   for a in aut:
    ai=[0]*V
    for x,y in enumerate(a):ai[y]=x
    c=tuple(a[g[ai[x]]] for x in range(V))
    assert c in guide_to_index, 'conjugate guide missing from enumeration'
    orbit.add(guide_to_index[c])
   assert i in orbit
   visited.update(orbit);reps.append(i);sizes.append(len(orbit));all_clusters.append(sorted(orbit))
  assert len(visited)==len(gs)
  counts.update({'conjugacy_classes':len(reps),'conjugacy_sizes':sizes,
                 'strong_guide_representatives':[list(gs[i]) for i in reps],
                 'strong_guide_class_indices':all_clusters})
 return counts

if __name__=='__main__':
 nvals=[int(x) for x in sys.argv[1:]] or [1,3,5,7]
 for n in nvals:
  t=perf_counter();r=classify(n)
  print('CHECK',n,{k:v for k,v in r.items() if k not in ['strong_guide_representatives','strong_guide_class_indices']},'seconds',round(perf_counter()-t,3),flush=True)
  with open(f'/mnt/data/c_next_study/claw_guides_{n}.json','w') as f:json.dump(r,f,indent=2)
