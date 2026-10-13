"""Independent augmented-precedence audit; no author search/replay imports."""
from pathlib import Path
import hashlib,json,time
HERE=Path(__file__).resolve().parent

def family(w,q):
    n=q*w*w;b=w+1;parents=[set() for _ in range(n)]
    optimal=[None]*n
    for block in range(q):
        start=block*w*w
        parents[start+w*w-1].add(start+w*w-w)
        if block:
            tail=set(range(start-w+1,start))
            for j in range(start,start+w+1):parents[j].update(tail)
        for j in range(w*w):optimal[start+j]=block*w+j//w
        # Swap the last job of penultimate nominal batch with the first
        # job of the last batch, keeping the latter a true predecessor.
        optimal[start+w*w-w-1],optimal[start+w*w-w]=optimal[start+w*w-w],optimal[start+w*w-w-1]
    # Independent static graph encoding: every older index at distance >=B.
    augmented=[parents[j]|set(range(max(0,j-b+1))) for j in range(n)]
    return parents,augmented,optimal

def main():
    begin=time.monotonic();cases=barrier_pairs=steps=0;maximum_n=0
    for w in range(2,15):
        for q in (1,2,3,5):
            parents,augmented,optimal=family(w,q);n=len(parents);b=w+1
            assert max(map(len,parents))<=w-1
            # Direct strict-time check of every true and augmented edge.
            assert all(optimal[i]<optimal[j] for j in range(n) for i in augmented[j])
            assert all(sum(t==c for t in optimal)<=w for c in range(q*w))
            assert max(optimal)+1==q*w==n//w
            # Reachability, not just successful witnesses, verifies block
            # separation: every old-block node is an ancestor of every next.
            ancestors=[]
            for j in range(n):
                old=set(augmented[j])
                for i in augmented[j]:old.update(ancestors[i])
                ancestors.append(old)
            for block in range(1,q):
                s=block*w*w;previous=set(range(s-w*w,s))
                for j in range(s,s+w*w):
                    assert previous<=ancestors[j]
                    barrier_pairs+=len(previous)
            # Simulate the actual named policy using only augmented readiness.
            done=set();trace=[]
            while len(done)<n:
                ready=sorted((j for j in range(n) if j not in done and augmented[j]<=done),reverse=True)
                issue=ready[:w];assert issue
                trace.append(issue);done.update(issue)
            assert len(trace)==q*(2*w-1)
            # Independently compute expected lists from the block arithmetic.
            expected=[]
            for block in range(q):
                s=block*w*w
                for k in range(w-1):
                    a=s+k*(w+1)
                    expected.extend([list(range(a+w,a,-1)),[a]])
                expected.append([s+w*w-1])
            assert trace==expected
            cases+=1;steps+=len(trace);maximum_n=max(n,maximum_n)
    result={'status':'PASS','widths':[2,14],'blocks':[1,2,3,5],'cases':cases,
            'youngest_cycles':steps,'barrier_ancestor_pairs':barrier_pairs,'maximum_n':maximum_n,
            'elapsed_seconds':time.monotonic()-begin,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'scope':'arbitrary-W/family proof separately reviewed; finite static augmented graph checks only; no exhaustive minimality rerun'}
    (HERE/'evidence/ratio-independent.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
