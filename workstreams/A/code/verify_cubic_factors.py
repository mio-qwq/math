#!/usr/bin/env python3
"""Independent exact checks for all-cubic edge-order construction (stdlib)."""
from collections import defaultdict,deque

def matchings(V,forbidden):
    if not V:
        yield ()
        return
    x=min(V)
    for y in sorted(V-{x}):
        if frozenset((x,y)) in forbidden:continue
        for tail in matchings(V-{x,y},forbidden):yield ((x,y),)+tail

def verify(V,edges,order):
    if len(edges)!=len(order) or len(set(edges))!=len(edges) or set(edges)!=set(order):return False
    seq={v:[] for v in V}
    for a,b,c in order:seq[a].append(c);seq[b].append(c)
    return all(len(seq[v])==3 and len(set(seq[v]))==3 for v in V) and all(seq[a]!=seq[b] for a,b,c in edges)

def build(cycles,M):
    V={x for C in cycles for x in C}
    assert sum(map(len,cycles))==len(V) and all(len(C)>=4 and len(C)%2==0 for C in cycles)
    colors={frozenset((C[i],C[(i+1)%len(C)])):i%2 for C in cycles for i in range(len(C))}
    E=[tuple(sorted(pair))+(col,) for pair,col in colors.items()]
    E += [tuple(sorted(pair))+(2,) for pair in M]
    assert len(M)*2==len(V) and {v for pair in M for v in pair}==V
    assert len({(a,b) for a,b,c in E})==len(E)
    # Select a root per cycle independent under third-colour matching.
    pairs=[(C[0],C[1]) for C in cycles]
    aux=defaultdict(set)
    for a,b in pairs:aux[a].add(b);aux[b].add(a)
    chosen={v for pair in pairs for v in pair}
    for a,b in M:
        if a in chosen and b in chosen:aux[a].add(b);aux[b].add(a)
    two={}
    for x in chosen:
        if x in two:continue
        two[x]=0;Q=deque([x])
        while Q:
            a=Q.popleft()
            for b in aux[a]:
                if b not in two:two[b]=1-two[a];Q.append(b)
                else:assert two[a]!=two[b]
    roots={a if two[a]==0 else b for a,b in pairs}
    assert all(not (a in roots and b in roots) for a,b in M)
    # Rotate each alternating cycle to root; orient with outgoing colour zero.
    oriented=[];positions={}
    for i,C in enumerate(cycles):
        root=next(v for v in C if v in roots);j=C.index(root)
        D=list(C[j:]+C[:j])
        if colors[frozenset((D[0],D[1]))]!=0:D=[D[0]]+D[:0:-1]
        assert all(colors[frozenset((D[j],D[(j+1)%len(D)]))]==j%2 for j in range(len(D)))
        oriented.append(D)
        for j,v in enumerate(D):positions[v]=(i,j)
    slots={}
    for a,b in M:
        owner=a if a in roots else b if b in roots else min((a,b),key=positions.get)
        assert owner not in slots
        slots[owner]=tuple(sorted((a,b)))+(2,)
    out=[]
    for D in oriented:
        for j,v in enumerate(D):
            out.append(tuple(sorted((v,D[(j+1)%len(D)])))+(j%2,))
            if v in slots:out.append(slots[v])
    assert verify(V,E,out)
    return E,out

def main():
    counts={}
    for partition in ((4,),(6,),(8,),(10,),(12,),(4,4),(4,6),(4,8),(6,6),(4,4,4)):
        cycles=[];k=0
        for n in partition:cycles.append(tuple(range(k,k+n)));k+=n
        forbid={frozenset((C[i],C[(i+1)%len(C)])) for C in cycles for i in range(len(C))}
        count=0
        for M in matchings(set(range(k)),forbid):
            build(cycles,M);count+=1
        counts[str(partition)]=count
    assert sum(counts.values())==13964
    edges,ordered=build([(0,1,2,3),(4,5,6,7)],((0,4),(1,5),(2,6),(3,7)))
    assert not verify(set(range(8)),edges,ordered[:-1])
    print('PASS 13964 all-cubic coloured instances:',counts,'negative test PASS')
if __name__=='__main__':main()
