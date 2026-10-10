"""Deterministic bounded traceable-graph diagnostic; subset reachability discovery.
All graphs contain 0,1,...,n-1 as a spanning path. No negative existence theorem.
"""
import itertools,json,random,time
from pathlib import Path
OUT=Path(__file__).parent

def test(n,edges):
 a=[0]*n
 for u,v in edges:a[u]|=1<<v;a[v]|=1<<u
 longest=[[-1]*n for _ in range(n)];unions=[[0]*n for _ in range(n)]
 for s in range(n):
  reach=[0]*(1<<n);reach[1<<s]=1<<s
  for mask in range(1<<n):
   ends=reach[mask]
   if not ends:continue
   length=mask.bit_count()-1
   while ends:
    bit=ends&-ends;ends-=bit;v=bit.bit_length()-1
    if length>longest[s][v]:longest[s][v]=length;unions[s][v]=mask
    elif length==longest[s][v]:unions[s][v]|=mask
    nexts=a[v]&~mask
    while nexts:
     b=nexts&-nexts;nexts-=b;reach[mask|b]|=b
 for x,y,z in itertools.combinations(range(n),3):
  if not(unions[x][y]>>z&1 or unions[x][z]>>y&1 or unions[y][z]>>x&1):
   return dict(order=n,edges=edges,selected=[x,y,z],spanning_path=list(range(n)),detour_lengths=longest,detour_unions=unions)
 return None

def main():
 rng=random.Random(202610101047);start=time.monotonic();counts={}
 for n in range(4,13):
  base=[(i,i+1) for i in range(n-1)]
  chords=[(u,v) for u,v in itertools.combinations(range(n),2) if v!=u+1]
  trials=(1<<len(chords)) if n<=6 else 180
  for t in range(trials):
   if time.monotonic()-start>90:
    print(json.dumps(dict(status='TIME_BUDGET',graphs=counts,seconds=time.monotonic()-start)));return
   if n<=6:extra=[e for i,e in enumerate(chords) if t>>i&1]
   else:
    probability=(.06,.12,.2,.35,.55,.8)[t%6]
    extra=[e for e in chords if rng.random()<probability]
   candidate=test(n,base+extra);counts[n]=counts.get(n,0)+1
   if candidate:
    (OUT/'candidate.json').write_text(json.dumps(candidate,indent=2)+'\n')
    print(json.dumps(dict(status='CANDIDATE',graphs=counts,seconds=time.monotonic()-start,selected=candidate['selected'],edges=candidate['edges'])));return
  print(json.dumps(dict(status='stage_done',order=n,graphs=counts,seconds=time.monotonic()-start)),flush=True)
 print(json.dumps(dict(status='NO_CANDIDATE_IN_WINDOW',graphs=counts,seconds=time.monotonic()-start)))
if __name__=='__main__':main()
