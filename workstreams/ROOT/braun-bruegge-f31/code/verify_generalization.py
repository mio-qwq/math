#!/usr/bin/env python3
"""Exact finite regressions for t-row centered-binomial majorization; stdlib-only."""
from itertools import combinations_with_replacement, product
from math import comb
from collections import Counter

def B(m,x): return comb(m,(m+x)//2) if abs(x)<=m and (m+x)%2==0 else 0

def H(rows):
    return sum(__import__('math').prod(B(m,x) for m in rows)
               for x in range(-min(rows),min(rows)+1))

def words(rows):
    counters=[]
    for m in rows:
        d=Counter()
        for xs in product((0,1),repeat=m):d[2*sum(xs)-m]+=1
        counters.append(d)
    return sum(__import__('math').prod(d[x] for d in counters)
               for x in set.intersection(*(set(d) for d in counters)))

def test():
    comparisons=bounded_max=independent=0
    for t in range(3,7):
        for parity in [0,1]:
            d=2 if parity==0 else 1
            for rows in combinations_with_replacement(range(d,12,2),t):
                if sum(rows)>27:continue
                base=H(rows)
                if sum(rows)<=12:
                    assert base==words(rows)
                    independent+=1
                for qi in range(t):
                    for pi in range(t):
                        if pi==qi or rows[qi]<=d or rows[pi]<rows[qi]:continue
                        out=list(rows);out[pi]+=2;out[qi]-=2
                        assert H(out)>base,(rows,pi,qi)
                        comparisons+=1
                maxrows=(sum(rows)-(t-1)*d,)+(d,)*(t-1)
                assert base<=H(maxrows)
                assert (base==H(maxrows))==(sorted(rows,reverse=True)==list(maxrows))
                bounded_max+=1
    for p in range(3,20):
        for q in range(2,p+1):
            if (p-q)%2==0:
                assert H((p,q))==H((p+2,q-2)) if q>=3 else True
    print('PASS transfer=',comparisons,' fixed-parity-max=',bounded_max,'word-count=',independent,'two-row-Vandermonde=PASS')
if __name__=='__main__':test()
