"""All-width Graham-tight c=1 family; independent explicit ROB replay."""
import json,time,hashlib
from pathlib import Path

def construct(W,q):
    assert W>=2 and q>=1
    n=W*W;edges=[];optimal=[];bad=[]
    for block in range(q):
        s=n*block;edges.append((s+n-W,s+n-1))
        if block:
            edges.extend((p,j) for j in range(s,s+W+1) for p in range(s-W+1,s))
        optimal.extend([list(range(s+t*W,s+(t+1)*W)) for t in range(W-2)])
        optimal.append(list(range(s+n-2*W,s+n-W-1))+[s+n-W])
        optimal.append([s+n-W-1]+list(range(s+n-W+1,s+n)))
        for k in range(W-1):
            a=s+k*(W+1);bad.extend([list(range(a+1,a+W+1)),[a]])
        bad.append([s+n-1])
    return n*q,edges,optimal,bad

def check(N,edges,trace,W,youngest):
    B=W+1;parents=[set() for _ in range(N)]
    for i,j in edges:parents[j].add(i)
    done=set();window=set();r=a=0
    for batch in trace:
        while a<N and len(window)<B:window.add(a);a+=1
        ready={j for j in window-done if parents[j]<=done}
        assert len(batch)==len(set(batch)) and set(batch)<=ready
        assert len(batch)==min(W,len(ready))
        if youngest:assert sorted(batch)==sorted(sorted(ready,reverse=True)[:W])
        done.update(batch)
        while r in done:window.remove(r);r+=1
    assert len(done)==N
    assert max(map(len,parents))<=W-1

def main():
    start=time.time();cases=0
    for W in range(2,21):
        for q in range(1,11):
            N,e,opt,bad=construct(W,q)
            check(N,e,opt,W,False);check(N,e,bad,W,True)
            assert len(opt)==N//W==q*W and len(bad)==q*(2*W-1)
            cases+=1
    print(json.dumps(dict(status='PASS',width_range=[2,20],q_range=[1,10],cases=cases,traces=2*cases,
          elapsed=time.time()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))
if __name__=='__main__':main()
