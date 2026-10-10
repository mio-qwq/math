"""Different diagnostic: sparse connected graphs, not assumed traceable.
Enumerates original simple paths, then all sets just above the conjectured bound.
"""
import itertools,json,random,time
from pathlib import Path
OUT=Path(__file__).parent

def inspect(n,edges):
 adj=[set() for _ in range(n)]
 for u,v in edges:adj[u].add(v);adj[v].add(u)
 L=[[-1]*n for _ in range(n)];U=[[0]*n for _ in range(n)]
 diameter=0;global_masks=set();nodes=0
 for start in range(n):
  stack=[(start,1<<start,0)]
  while stack:
   end,mask,length=stack.pop();nodes+=1
   if length>L[start][end]:L[start][end]=length;U[start][end]=mask
   elif length==L[start][end]:U[start][end]|=mask
   if length>diameter:diameter=length;global_masks={mask}
   elif length==diameter:global_masks.add(mask)
   for v in adj[end]:
    if not mask>>v&1:stack.append((v,mask|1<<v,length+1))
 bound=n-diameter+1
 good_triples=[]
 for tri in itertools.combinations(range(n),3):
  x,y,z=tri
  if not(U[x][y]>>z&1 or U[x][z]>>y&1 or U[y][z]>>x&1):good_triples.append(tri)
 good=set(good_triples)
 strong=next((tri for tri in good_triples if any(all(mask>>v&1 for v in tri) for mask in global_masks)),None)
 witness=next((S for S in itertools.combinations(range(n),bound+1) if all(tri in good for tri in itertools.combinations(S,3))),None)
 return witness,strong,dict(order=n,edges=edges,detour_diameter=diameter,bound=bound,detour_lengths=L,detour_unions=U,path_states=nodes)

def main():
 rng=random.Random(202610101048);counts={};total_nodes=0;start=time.monotonic();strong_count=0
 for n in range(6,15):
  for t in range(300):
   if time.monotonic()-start>60:
    print(json.dumps(dict(status='TIME_BUDGET',graphs=counts,path_states=total_nodes,strong_obstructions=strong_count,seconds=time.monotonic()-start)));return
   # Recursive spanning tree, with shuffled labels; add zero through six chords.
   E={(rng.randrange(v),v) for v in range(1,n)}
   rest=[e for e in itertools.combinations(range(n),2) if e not in E]
   E|=set(rng.sample(rest,min(t%7,len(rest))))
   witness,strong,data=inspect(n,sorted(E));counts[n]=counts.get(n,0)+1;total_nodes+=data['path_states']
   if witness:
    data['selected']=witness;(OUT/'candidate_general.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(dict(status='CANDIDATE',order=n,selected=witness,diameter=data['detour_diameter'],graphs=counts,seconds=time.monotonic()-start)));return
   if strong:
    strong_count+=1
    if not (OUT/'strong_lemma_obstruction.json').exists():
     data['selected']=strong;(OUT/'strong_lemma_obstruction.json').write_text(json.dumps(data,indent=2)+'\n')
  print(json.dumps(dict(status='stage_done',order=n,graphs=counts,path_states=total_nodes,strong_obstructions=strong_count,seconds=time.monotonic()-start)),flush=True)
 print(json.dumps(dict(status='NO_CANDIDATE_IN_WINDOW',graphs=counts,path_states=total_nodes,strong_obstructions=strong_count,seconds=time.monotonic()-start)))
if __name__=='__main__':main()
