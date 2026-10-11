"""Synthetic controls for the general proof, constructed with a test secret."""
import argparse
import json
import math
from pathlib import Path

base=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
args=ap.parse_args()
q=json.loads((base/'evidence/quadratic/synthetic.json').read_text())
r=int(q['expected']['k']);s=int(q['expected']['s']);e=int(q['public']['e'])
t=1-r*s
cases=[]
for m in (3,12):
    # L^m, or L^(m-1)(L+e*x), expanded by the binomial theorem.
    h={(i,j):math.comb(m,i)*math.comb(i,j)*(-r)**(m-i)*r**j*t**(i-j)
       for i in range(m+1) for j in range(i+1)}
    if m==12:
        n=m-1
        for i in range(n+1):
            for j in range(i+1):
                extra=e*math.comb(n,i)*math.comb(i,j)*(-r)**(n-i)*r**j*t**(i-j)
                h[i+1,j]=h.get((i+1,j),0)+extra
    cases.append(dict(m=m,public=q['public'],X=q['X'],Y=q['Y'],
                      terms=[[i,j,str(c)] for (i,j),c in sorted(h.items()) if c],
                      linear_witness=[str(r),str(t)],expected=q['expected']))
out=dict(schema='rsa-general-synthetic-v1',
         purpose='Synthetic inputs built with disclosed secret; no relation-search or attack claim.',cases=cases)
args.out.parent.mkdir(parents=True,exist_ok=True)
args.out.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(result='written',degrees=[3,12])))
