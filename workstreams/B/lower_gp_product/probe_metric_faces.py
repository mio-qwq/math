"""Discovery of arbitrary five-point metric equality types. No new theorem yet.
Uses prior MET5 ray description: 15 cuts and 10 K2,3 graph metrics.
"""
from itertools import combinations
from pathlib import Path
import json,time
start=time.monotonic();P=Path(__file__).parent
edges=list(combinations(range(5),2));triangles=[(a,b,c) for a,c in edges for b in range(5) if b!=a and b!=c]
def data(D):return [D[a][b] for a,b in edges]+[D[a][b]+D[b][c]-D[a][c] for a,b,c in triangles]
rays=[]
for mask in range(1,16):rays.append([[int(bool(mask>>a&1)!=bool(mask>>b&1)) for b in range(5)] for a in range(5)])
for side in combinations(range(5),2):rays.append([[0 if a==b else 1 if ((a in side)!=(b in side)) else 2 for b in range(5)] for a in range(5)])
faces={0}
for i,D in enumerate(rays):
 ds=data(D);assert min(ds)>=0;r=sum(1<<i for i,x in enumerate(ds) if x>0);faces|={f|r for f in faces}
 print(json.dumps(dict(stage=i+1,faces=len(faces),seconds=time.monotonic()-start)),flush=True)
(P/'metric_faces.json').write_text(json.dumps(dict(edges=edges,triangles=triangles,rays=rays,positive_masks=sorted(faces)),separators=(',',':'))+'\n')
