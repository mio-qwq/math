"""Set-based admission/retirement replay, independent of search.py."""
import json,time,hashlib
from pathlib import Path

def replay(n,edges,trace,non_delay):
    parents=[set() for _ in range(n)]
    for a,b in edges:parents[b].add(a)
    complete=set();window=set();retired=entered=0;boundaries=[]
    for action in trace:
        while entered<n and len(window)<4:
            window.add(entered);entered+=1
        ready={j for j in window-complete if parents[j]<=complete}
        issue=set(action)
        assert len(issue)==len(action) and issue<=ready and len(issue)<=3
        if non_delay:assert len(issue)==min(3,len(ready))
        boundaries.append(dict(retired=retired,window=sorted(window),ready=sorted(ready),issue=sorted(issue)))
        complete|=issue
        while retired in complete:
            window.remove(retired);retired+=1
    assert complete==set(range(n))
    return boundaries

def family(q):
    edges=[];optimal=[];bad=[]
    for b in range(q):
        s=9*b;edges.append((s+6,s+8))
        if b:
            for root in range(s,s+4):edges.extend([(s-2,root),(s-1,root)])
        optimal.extend([[s+i for i in act] for act in [[0,1,2],[3,4,6],[5,7,8]]])
        bad.extend([[s+i for i in act] for act in [[1,2,3],[0],[5,6,7],[4],[8]]])
    return 9*q,edges,optimal,bad

def main():
    start=time.time()
    minimal=replay(9,[],[[1,2,3],[0],[5,6,7],[4],[8]],True)
    replay(9,[],[[0,1,2],[3,4,5],[6,7,8]],False)
    for q in range(1,101):
        n,edges,opt,bad=family(q)
        good_states=replay(n,edges,opt,True);bad_states=replay(n,edges,bad,True)
        assert len(opt)==n//3 and len(bad)==5*q
        assert all(len([i for i,j in edges if j==v])<=2 for v in range(n))
        # Check youngest-ready implementation, not merely maximum cardinality.
        assert all(state['issue']==sorted(state['ready'],reverse=True)[:3][::-1] for state in bad_states)
    folder=Path(__file__).resolve().parent
    out=dict(status='PASS',q_range=[1,100],largest_n=900,checked_family_traces=200,
             minimal_counterexample_replay=minimal,elapsed=time.time()-start,
             sources_sha256={name:hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ['search.py','random_audit.py','replay.py']})
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
