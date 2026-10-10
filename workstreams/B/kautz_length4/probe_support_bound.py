"""New upper-bound mechanism: partition arbitrary GP sets by exact letter support.
Exact finite search, not a rank/block-uniform restriction on the original set.
"""
from itertools import product,combinations,permutations
from functools import lru_cache
from pathlib import Path
import json,time

def dist(u,v):
    if u==v:return 0
    return next((s for s in range(1,4) if u[s:]==v[:-s]),4)

def main():
    packets=[]
    for t in (2,3,4):
        words=[w for w in product(range(t),repeat=4) if len(set(w))==t and all(w[i]!=w[i+1] for i in range(3))]
        bad=[]
        for triple in combinations(range(len(words)),3):
            if any(dist(words[a],words[b])+dist(words[b],words[c])==dist(words[a],words[c]) for a,b,c in permutations(triple)):
                bad.append(sum(1<<i for i in triple))
        start=time.monotonic();nodes=0
        @lru_cache(None)
        def opt(mask):
            nonlocal nodes
            nodes+=1
            if nodes%4096==0 and time.monotonic()-start>20:raise TimeoutError
            candidates=[tri for tri in bad if mask&tri==tri]
            if not candidates:return mask
            degrees=[sum(bool(tri>>i&1) for tri in candidates) for i in range(len(words))]
            tri=max(candidates,key=lambda tri:sum(degrees[i] for i in range(len(words)) if tri>>i&1))
            best=0
            for i in sorted((i for i in range(len(words)) if tri>>i&1),key=lambda i:-degrees[i]):
                reduced=mask^(1<<i)
                if reduced.bit_count()<=best.bit_count():continue
                ans=opt(reduced)
                if ans.bit_count()>best.bit_count():best=ans
            return best
        try:
            witness=opt((1<<len(words))-1)
            out=dict(support=t,vertices=len(words),forbidden_triples=len(bad),maximum=witness.bit_count(),witness=[words[i] for i in range(len(words)) if witness>>i&1],nodes=nodes,seconds=round(time.monotonic()-start,3))
        except TimeoutError:out=dict(support=t,vertices=len(words),status='UNKNOWN',nodes=nodes,seconds=round(time.monotonic()-start,3))
        print(json.dumps(out),flush=True);packets.append(out)
    Path(__file__).with_name('support_bound_probe.json').write_text(json.dumps(packets,indent=2)+'\n')
if __name__=='__main__':main()
