"""Independent static-DAG simulation of the oldest-inclusive tightness family."""
import json,time,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent

def graph(q):
    n=9*q;true=[set() for _ in range(n)]
    for s in range(0,n,9):
        for i,j in ((1,4),(2,4),(2,5),(5,8)):true[s+j].add(s+i)
        if s:
            for j in range(s,s+4):true[j].add(s-1)
    assert max(map(len,true))<=2
    return [true[j]|set(range(max(0,j-3))) for j in range(n)]

def ready(graph,done):
    return sorted(j for j,ps in enumerate(graph) if j not in done and ps<=done)

def main():
    start=time.monotonic();cycles=0
    qs=list(range(1,21))+[50]
    for q in qs:
        g=graph(q);done=set();trace=[]
        while len(done)<len(g):
            r=ready(g,done);oldest=min(set(range(len(g)))-done)
            assert r[0]==oldest
            a=[r[0]]+sorted(r[1:],reverse=True)[:2]
            assert len(a)==min(3,len(r))
            trace.append(sorted(a));done.update(a)
        expected=[[s+i for i in a] for s in range(0,9*q,9) for a in ((0,2,3),(1,),(4,6,7),(5,),(8,))]
        assert trace==expected and len(trace)==5*q
        cycles+=len(trace)
        done=set()
        for s in range(0,9*q,3):
            a=set(range(s,s+3));r=ready(g,done)
            assert a<=set(r) and len(a)==min(3,len(r)) and min(set(range(len(g)))-done) in a
            done.update(a)
        assert len(done)==9*q
    # Refute the stronger barrier explicitly: next-block job9 can run before
    # old-block jobs6 and7. Each action below is a legitimate partial trace.
    g=graph(2);done=set();partial=[(0,1,2),(3,4,5),(8,),(9,)]
    for a in partial:
        assert set(a)<=set(ready(g,done)) and len(a)<=3
        done.update(a)
    assert 9 in done and 6 not in done and 7 not in done
    result={'status':'PASS','q_values':qs,'cases':len(qs),'youngest_after_oldest_cycles':cycles,
        'full_traces':2*len(qs),'maximum_n':450,'strong_barrier_counterexample_partial_trace':partial,
        'elapsed_seconds':time.monotonic()-start,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'evidence/oldest-independent.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
