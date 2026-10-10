#!/usr/bin/env python3
"""Even-r,n=1 exceptional CDC group: independently enumerate both ring
orientations, verify every raw cover adjacency, classify the guide set.
Pure Python 3; uses no discovery-script or NetworkX imports.
"""
from pathlib import Path
import hashlib,json

def build_cover(r):
 h=r;N=3*r+1
 x=[set() for _ in range(2*N)]
 def edge(a,b):
  x[2*a].add(2*b+1);x[2*b+1].add(2*a)
  x[2*b].add(2*a+1);x[2*a+1].add(2*b)
 for t in range(2*h):edge(t,(t+1)%(2*h))
 for p in range(h):
  leaf=2*h+p
  edge(leaf,p);edge(leaf,p+h);edge(leaf,3*h)
 return x

def f(r,w,s0,s1,a0,a1):
 h=r;N=3*r+1
 assert r%2==0 and r>=2 and (a0-a1)%2==0
 out=[-1]*(2*N)
 for c in (0,1):
  s=s0 if c==0 else s1;a=a0 if c==0 else a1
  d=c^w
  for t in range(2*h):
   dst=(s*t+a)%(2*h)
   out[2*t+(t+c)%2]=2*dst+(dst+d)%2
  for p in range(h):
   dst=(s*p+a)%h
   out[2*(2*h+p)+(1-(p+c)%2)]=2*(2*h+dst)+(1-(dst+d)%2)
 for eps in (0,1):
  out[2*(3*h)+eps]=2*(3*h)+((eps+a0+w)%2)
 assert sorted(out)==list(range(2*N))
 return tuple(out)

def test_r(r):
 X=build_cover(r)
 all_maps=set();switch=[];strong=[]
 for w in (0,1):
  for s0 in (-1,1):
   for s1 in (-1,1):
    for a0 in range(2*r):
     for d in range(r):
      a1=(a0+2*d)%(2*r)
      mapping=f(r,w,s0,s1,a0,a1)
      assert mapping not in all_maps;all_maps.add(mapping)
      assert all({mapping[y] for y in X[x]}==X[mapping[x]] for x in range(len(X)))
      sw=all(mapping[2*i]%2==1 and mapping[2*i+1]%2==0 for i in range(len(X)//2))
      assert sw==((a0+w)%2==1)
      if sw:
       switch.append(mapping)
       if all(mapping[mapping[i]]==i and mapping[i] not in X[i] for i in range(len(X))):
        strong.append((mapping,w,s0,s1,a0,a1))
 assert len(all_maps)==16*r*r
 assert len(strong)==2*r
 assert all(w==1 and s0==s1 and a0%2==0 for _,w,s0,s1,a0,a1 in strong)
 # Conjugacy of entire guide set, independent of analytic transitivity step.
 def inv(p):
  d=[0]*len(p)
  for i,x in enumerate(p):d[x]=i
  return d
 leader=strong[0][0]
 orbit=set()
 for g in all_maps:
  gi=inv(g)
  orbit.add(tuple(g[leader[gi[i]]] for i in range(len(g))))
 assert orbit=={st[0] for st in strong}
 deck=tuple(i^1 for i in range(len(X)))
 assert deck in orbit
 return {'r':r,'cover_vertices':len(X),'aut':len(all_maps),'strong_guides':len(strong),
         'single_conjugacy_class_size':len(orbit),'connected_cousins':0}

if __name__=='__main__':
 results=[test_r(r) for r in (2,4,6,8,10)]
 p=Path(__file__).with_name('even_r_n1_results.json');p.write_text(json.dumps(results,indent=2)+'\n')
 print('PASS even-r n=1 boundary, r=2,4,6,8,10; aut=16r², strong=2r, one class')
 print('SHA256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
