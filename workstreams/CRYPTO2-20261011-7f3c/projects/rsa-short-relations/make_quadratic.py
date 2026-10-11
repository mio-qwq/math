"""Synthetic theorem control using a disclosed test secret; not an attack."""
import argparse
import json
import math
from pathlib import Path

base=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--out',type=Path,required=True)
a=ap.parse_args()
record=json.loads((base/'evidence/control-96-m2-t0.json').read_text())
key={k:int(v) for k,v in record['key'].items()}
e,k,s,Y=key['e'],key['k'],key['s'],key['Y']
X=max(k+1,math.isqrt((e+Y-1)//Y)+1)
r,t=k,1-k*s
# Coefficients of [rxy+tx-r]*[rxy+tx-r+e], expanded directly.
coeff=[(2,2,r*r),(2,1,2*r*t),(2,0,t*t),
       (1,1,r*e-2*r*r),(1,0,t*e-2*r*t),(0,0,r*r-r*e)]
out=dict(schema='rsa-quadratic-synthetic-v1',
         purpose='Synthetic control built using disclosed k,s; no attack claim.',
         public={k:str(key[k]) for k in ('N','e')},X=str(X),Y=str(Y),
         terms=[[i,j,str(c)] for i,j,c in coeff],
         expected={k:str(key[k]) for k in ('p','q','k','d','s')})
a.out.parent.mkdir(parents=True,exist_ok=True)
a.out.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(result='written',certificate=a.out.name)))
