"""Independent completed-set min/all-action and max/non-delay search."""
from functools import lru_cache
from itertools import combinations
import json,time,argparse

def solve(n,edges,B=4,W=3):
    parents=[0]*n
    for i,j in edges: parents[j]|=1<<i
    full=(1<<n)-1
    @lru_cache(None)
    def go(d):
        if d==full:return 0,0,(),()
        r=next(i for i in range(n) if not(d>>i&1))
        ready=[j for j in range(r,min(n,r+B)) if not(d>>j&1) and parents[j]&d==parents[j]]
        lo=n+1;hi=-1;lp=hp=()
        for k in range(1,min(W,len(ready))+1):
            for action in combinations(ready,k):
                nxt=d|sum(1<<j for j in action)
                a,b,ap,bp=go(nxt)
                if a+1<lo:lo=a+1;lp=(action,)+ap
                if k==min(W,len(ready)) and b+1>hi:hi=b+1;hp=(action,)+bp
        return lo,hi,lp,hp
    return go(0)

def main():
    p=argparse.ArgumentParser();p.add_argument('--max-n',type=int,default=7);args=p.parse_args()
    start=time.time();counts=[];best=(0,1);examples=[]
    for n in range(1,args.max_n+1):
        pairs=[(i,j) for j in range(n) for i in range(max(0,j-3),j)]
        for bits in range(1<<len(pairs)):
            e=[edge for k,edge in enumerate(pairs) if bits>>k&1]
            lo,hi,lp,hp=solve(n,e)
            if hi*best[1]>best[0]*lo:
                best=(hi,lo);examples.append(dict(n=n,edges=e,optimum=lo,worst_nd=hi,optimal_trace=lp,worst_trace=hp))
            if 2*hi>3*lo:
                out=dict(status='REFUTED',checked_smaller=counts,checked_at_n=bits+1,elapsed=time.time()-start,counterexample=examples[-1]);print(json.dumps(out,indent=2));return
        counts.append(dict(n=n,graphs=1<<len(pairs)));print(json.dumps(dict(progress=counts[-1],best=best)),flush=True)
    print(json.dumps(dict(status='COMPUTATIONALLY_SUPPORTED',counts=counts,elapsed=time.time()-start,record_examples=examples),indent=2))
if __name__=='__main__': main()
