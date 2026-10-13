import random,json,time
from search import solve
rng=random.Random(2026101406);start=time.time();best=(0,1);record=None
for case in range(10000):
 n=rng.randint(9,100);p=rng.choice([.02,.05,.1,.2,.4,.7])
 e=[(i,j) for j in range(n) for i in range(max(0,j-3),j) if rng.random()<p]
 lo,hi,lp,hp=solve(n,e)
 if hi*best[1]>best[0]*lo:best=(hi,lo);record=dict(n=n,edges=e,lo=lo,hi=hi,optimal=lp,worst=hp)
 if 2*hi>3*lo:
  print(json.dumps(dict(status='REFUTED',case=case,elapsed=time.time()-start,example=record),indent=2));break
else:print(json.dumps(dict(status='COMPUTATIONALLY_SUPPORTED',cases=case+1,seed=2026101406,elapsed=time.time()-start,best=record),indent=2))
