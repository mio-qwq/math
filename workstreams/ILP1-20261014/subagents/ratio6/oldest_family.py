"""Oldest-inclusive fixed-priority 5/3 family: standalone ROB replay."""
import json,time,hashlib
from pathlib import Path

def construct(q):
    e=[];good=[];bad=[]
    for b in range(q):
        s=9*b;e.extend((s+i,s+j) for i,j in [(1,4),(2,4),(2,5),(5,8)])
        if b:e.extend((s-1,j) for j in range(s,s+4))
        good.extend([[s+i for i in A] for A in [[0,1,2],[3,4,5],[6,7,8]]])
        bad.extend([[s+i for i in A] for A in [[0,2,3],[1],[4,6,7],[5],[8]]])
    return 9*q,e,good,bad

def replay(N,e,trace,policy):
    pred=[set() for _ in range(N)]
    for i,j in e:pred[j].add(i)
    assert max(map(len,pred))<=2
    completed=set();window=set();r=a=0
    for batch in trace:
        while a<N and len(window)<4:window.add(a);a+=1
        ready={j for j in window-completed if pred[j]<=completed}
        assert set(batch)<=ready and len(batch)==len(set(batch))==min(3,len(ready))
        assert r in batch
        if policy:assert set(batch)=={r}|set(sorted(ready-{r},reverse=True)[:2])
        completed.update(batch)
        while r in completed:window.remove(r);r+=1
    assert len(completed)==N

def main():
    start=time.time()
    for q in range(1,101):
        n,e,good,bad=construct(q)
        replay(n,e,good,False);replay(n,e,bad,True)
        assert len(good)==n//3==3*q and len(bad)==5*q
    print(json.dumps(dict(status='PASS',q_range=[1,100],traces=200,largest_n=900,elapsed=time.time()-start,
          source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))
if __name__=='__main__':main()
