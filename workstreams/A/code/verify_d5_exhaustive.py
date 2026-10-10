from verify_all_regular import make_order, validate
from functools import lru_cache

@lru_cache(None)
def matchings(n,forbidden):
    bad=set(forbidden)
    def rec(V):
        if not V:
            yield ()
            return
        a=min(V)
        for b in sorted(V-{a}):
            if (a,b) in bad:continue
            for rest in rec(V-{a,b}):yield ((a,b),)+rest
    return tuple(rec(set(range(n))))

def test(parts):
    n=sum(parts);base=[];bad=set();k=0
    for size in parts:
        V=tuple(range(k,k+size));k+=size
        for j,u in enumerate(V):
            v=V[(j+1)%size];e=(min(u,v),max(u,v))
            base.append((*e,j%2));bad.add(e)
    count=0
    for M2 in matchings(n,tuple(sorted(bad))):
        bad2=bad|set(M2)
        for M3 in matchings(n,tuple(sorted(bad2))):
            bad3=bad2|set(M3)
            for M4 in matchings(n,tuple(sorted(bad3))):
                E=base+[(a,b,2) for a,b in M2]+[(a,b,3) for a,b in M3]+[(a,b,4) for a,b in M4]
                O,_=make_order(set(range(n)),E,5)
                assert validate(set(range(n)),E,O,5)
                count+=1
    print(parts,'PASS d5 complete edge-colouring enumeration',count)
    return count
if __name__=='__main__':
 for p in [(8,),(4,4)]:test(p)
