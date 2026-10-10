"""Finite boundary exploration, not an original conjecture decision procedure."""
from itertools import product
from verify_subdivided import adjacency,check
import json
E=[(0,1),(0,2),(1,2),(3,4),(3,5),(4,5),(0,3)]
a=adjacency(6,E)
rows=[c for c in product(range(5),repeat=6) if check(c,a)[0]]
def extend(c,L):
    allowed=[]
    for i in range(1,L):
        good=[]
        for x in range(5):
            radius=1 if x==0 else 2
            d=[i,i+1,i+1,L-i,L-i+1,L-i+1]
            if all(x!=y or dist>radius for y,dist in zip(c,d)):good.append(x)
        allowed.append(good)
    states={(None,c[0]):[c[0]]}
    for choices in allowed+[[c[3]]]:
        new={}
        for (p,q),w in states.items():
            for x in choices:
                if x==q or (x!=0 and x==p):continue
                new[(q,x)]=w+[x]
        states=new
    return next(iter(states.values()),None)
for L in range(2,13):
    failed=[c for c in rows if extend(c,L) is None]
    print(json.dumps(dict(length=L,boundaries=len(rows),failed=len(failed),first=failed[:1])),flush=True)
