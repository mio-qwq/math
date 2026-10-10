#!/usr/bin/env python3
"""All-colouring finite certificates for two rooted cubic gadgets; standard library."""
from itertools import permutations
from hashlib import sha256

GADGETS={
 'cube':{1:(0,3,5),2:(3,0,6),4:(5,6,0),7:(6,5,3)},
 'heawood':{1:(0,2,10),3:(2,4,12),5:(4,6,0),7:(6,8,2),9:(8,10,4),11:(10,12,6),13:(12,0,8)},
}

def proper(rows,cols):
    U=tuple(rows)
    W={v for ns in rows.values() for v in ns}
    if set(cols)!={(u,v) for u in U for v in rows[u]}:return False
    if any({cols[u,v] for v in rows[u]}!={0,1,2} for u in U):return False
    if any({cols[u,v] for u in U if v in rows[u]}!={0,1,2} for v in W):return False
    return True

def exhaustive_colours(rows):
    E=tuple((u,v) for u in rows for v in rows[u])
    used={('u',u):set() for u in rows}
    used.update({('v',v):set() for ns in rows.values() for v in ns})
    curr={}
    def rec(k):
        if k==len(E):
            assert proper(rows,curr)
            yield curr.copy()
            return
        u,v=E[k]
        for c in range(3):
            if c in used['u',u] or c in used['v',v]:continue
            used['u',u].add(c);used['v',v].add(c);curr[u,v]=c
            yield from rec(k+1)
            del curr[u,v];used['u',u].remove(c);used['v',v].remove(c)
    yield from rec(0)

def aligned(rows,cols,order):
    if not proper(rows,cols) or set(order)!=set(rows) or len(order)!=len(rows):return False
    interface={cols[u,0]:u for u in rows if 0 in rows[u]}
    if set(interface)!={0,1,2}:return False
    if [u for u in order if u in interface.values()]!=[interface[i] for i in range(3)]:return False
    ranks={u:i for i,u in enumerate(order)}
    W={v for ns in rows.values() for v in ns}
    for v in W-{0}:
        seq=tuple(cols[u,v] for u in sorted((u for u in rows if v in rows[u]),key=ranks.get))
        if seq==(0,1,2):return False
    return True

def independent_count(rows):
    """Second algorithm: choose colour-0 matching; complement's cycles alternate 1/2."""
    U=tuple(rows)
    E={(u,v) for u in rows for v in rows[u]}
    def matchings(i,used,chosen):
        if i==len(U):
            yield set(chosen)
            return
        u=U[i]
        for v in rows[u]:
            if v not in used:yield from matchings(i+1,used|{v},chosen+[(u,v)])
    total=0
    for matching in matchings(0,set(),[]):
        adj={}
        for u,v in E-matching:
            a=('u',u);b=('v',v)
            adj.setdefault(a,set()).add(b)
            adj.setdefault(b,set()).add(a)
        assert all(len(ns)==2 for ns in adj.values())
        unseen=set(adj);components=0
        while unseen:
            components+=1
            stack=[unseen.pop()]
            while stack:
                for y in adj[stack.pop()]:
                    if y in unseen:
                        unseen.remove(y)
                        stack.append(y)
        total+=1<<components
    return total

def main():
    for name,rows in GADGETS.items():
        U=tuple(rows)
        expected={'cube':24,'heawood':48}[name]
        total=0
        digest=sha256()
        worst=0
        for colors in exhaustive_colours(rows):
            total+=1
            candidate=None
            for tries,order in enumerate(permutations(U),start=1):
                if aligned(rows,colors,order):
                    candidate=order
                    worst=max(worst,tries)
                    break
            assert candidate is not None,(name,total)
            digest.update(repr(tuple(sorted(colors.items()))).encode())
            digest.update(repr(candidate).encode())
        assert total==expected
        assert independent_count(rows)==expected
        bad={(u,v):0 for u in rows for v in rows[u]}
        assert not proper(rows,bad) and not aligned(rows,bad,U)
        print('PASS',name,'all properly labelled 3-edge-colourings',total,
              'independent 1-factor count',expected,
              'max checked U orders',worst,
              'witness SHA256',digest.hexdigest()[:16])
    print('PASS negative colouring tests')

if __name__=='__main__':
    main()
