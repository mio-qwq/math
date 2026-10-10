"""Independent original-definition tests of FULL_PROOF.md.
Stdlib only. Does not import prior checkers, discovery, or Yang-Wu's proof.
Finite base color search is a test fixture, NOT a universal substitute for Yang-Wu.
"""
from itertools import combinations,product,permutations
from collections import deque,Counter
import json,platform
STATS=Counter()
P_EDGES=[(0,2),(0,3),(1,2),(1,3),(2,3)]
D_EDGES=[(0,1),(0,2),(1,2),(1,3),(2,4),(3,5),(3,6),(4,5),(4,6),(5,6)]
P_ROWS={(0,1):[0,1,2,3,1],(1,0):[1,0,2,3,0],(1,2):[1,0,3,4,2]}
D_ROWS={(0,1):[0,2,3,0,0,1,4,1],(1,0):[1,0,2,3,0,1,4,0],(1,2):[1,0,3,2,0,1,4,2]}

def graph(n,edges):
    a={u:set() for u in range(n)}
    for u,v in edges:
        assert u!=v and v not in a[u];a[u].add(v);a[v].add(u)
    return a

def induced(a,keep):return {u:a[u]&keep for u in keep}
def good(a):
    return all(len(ns)<=3 and all(y in a[x] or z in a[x] or z in a[y] for x,y,z in combinations(ns,3)) for ns in a.values())
def distances(a):
    D={}
    for s in a:
        d={s:0};q=deque([s])
        while q:
            u=q.popleft()
            for v in a[u]:
                if v not in d:d[v]=d[u]+1;q.append(v)
        D[s]=d
    return D

def valid(a,c):
    assert set(a)==set(c)
    D=distances(a)
    return all(c[u]!=c[v] or D[u].get(v,10**9)>(1 if c[u]==0 else 2) for u,v in combinations(a,2))

def components(a):
    unseen=set(a);out=[]
    while unseen:
        s=min(unseen);unseen.remove(s);co={s};q=[s]
        while q:
            for v in a[q.pop()]:
                if v in unseen:unseen.remove(v);co.add(v);q.append(v)
        out.append(co)
    return out

def root_check(a):
    triangles=[set(t) for t in combinations(a,3) if all(v in a[u] for u,v in combinations(t,2))]
    assert all(not(x&y) for x,y in combinations(triangles,2))
    cliques=triangles+[set((u,v)) for u in a for v in a[u] if u<v and not any(u in t and v in t for t in triangles)]
    next_id=len(cliques);root_edges={}
    for u in a:
        ends=[i for i,C in enumerate(cliques) if u in C]
        assert len(ends)<=2
        while len(ends)<2:ends.append(next_id);next_id+=1
        root_edges[u]=tuple(ends)
    assert len(set(tuple(sorted(e)) for e in root_edges.values()))==len(a)
    degree=Counter(x for e in root_edges.values() for x in e)
    assert all(u!=v and degree[u]+degree[v]<=5 for u,v in root_edges.values())
    reconstructed={u:{v for v in a if v!=u and set(root_edges[u])&set(root_edges[v])} for u in a}
    assert reconstructed==a
    assert distances(reconstructed)==distances(a)
    STATS['root_graphs']+=1

def exact_base(a):
    D=distances(a);c={}
    def rec():
        if len(c)==len(a):return dict(c)
        choices={u:[x for x in range(5) if all(x!=y or D[u].get(v,10**9)>(1 if x==0 else 2) for v,y in c.items())] for u in a if u not in c}
        u=min(choices,key=lambda v:(len(choices[v]),-len(a[v])))
        for x in choices[u]:
            c[u]=x;ans=rec()
            if ans is not None:return ans
            del c[u]
        return None
    ans=rec();assert ans is not None
    return ans

def leaf(a,c,r,u):
    if c[u]:c[r]=0
    else:c[r]=next(x for x in (1,2,3,4) if all(c[v]!=x for v in a[u]))

def cap_colors(rows,root_color,out_color):
    typ=(0,1) if root_color==0 else ((1,0) if out_color==0 else (1,2))
    for perm in permutations((1,2,3,4)):
        m=(0,)+perm
        if m[typ[0]]==root_color and m[typ[1]]==out_color:
            return [m[x] for x in rows[typ]]
    raise AssertionError('boundary not proper')

def solve(a):
    assert good(a)
    cs=components(a)
    if len(cs)!=1:
        out={}
        for co in cs:out.update(solve(induced(a,co)))
        return out
    if len(a)==4 and all(len(ns)==3 for ns in a.values()):
        STATS['K4']+=1;return dict(zip(sorted(a),range(4)))
    diamond=None
    for C in combinations(a,4):
        degrees={u:len(a[u]&set(C)) for u in C}
        if sorted(degrees.values())==[2,2,3,3]:
            tips=[u for u in C if degrees[u]==2];centers=[u for u in C if degrees[u]==3]
            diamond=(set(C),tips,centers);break
    if diamond is None:
        root_check(a);return exact_base(a)
    C,(x,y),(p,q)=diamond
    extx=a[x]-C;exty=a[y]-C
    if not extx and not exty:
        STATS['isolated_diamond']+=1;c=dict(zip(sorted(a),range(4)))
    elif not extx or not exty:
        STATS['pendant_diamond']+=1
        if not extx:x,y=y,x;extx,exty=exty,extx
        u=next(iter(extx));old=induced(a,set(a)-C);c=solve(old);leaf(old,c,x,u)
        row=cap_colors(P_ROWS,c[x],c[u]);c.update(dict(zip((x,y,p,q),row[:-1])))
    else:
        u=next(iter(extx));v=next(iter(exty))
        if u==v:
            STATS['same_neighbor_five']+=1;assert len(a)==5
            c={x:0,y:0,p:1,q:2,u:3}
        elif v not in a[u]:
            STATS['edge_replacement']+=1;old=induced(a,set(a)-C);old[u].add(v);old[v].add(u)
            c=solve(old);A,B=c[u],c[v];pos=[z for z in (1,2,3,4) if z not in (A,B)]
            c.update({x:B,y:A,p:pos[0],q:pos[1]})
        elif len(a[u])==len(a[v])==2:
            STATS['adjacent_six']+=1;assert len(a)==6;c={x:0,y:0,p:1,q:2,u:3,v:4}
        else:
            w=next(iter(a[u]-{v,x}));assert a[v]-{u,y}=={w}
            cap=C|{u,v,w};outside=a[w]-cap
            if not outside:
                STATS['isolated_D']+=1;c=dict(zip((w,u,v,x,y,p,q),D_ROWS[(0,1)][:-1]))
            else:
                STATS['pendant_D']+=1;z=next(iter(outside));old=induced(a,set(a)-cap);c=solve(old);leaf(old,c,w,z)
                row=cap_colors(D_ROWS,c[w],c[z]);c.update(dict(zip((w,u,v,x,y,p,q),row[:-1])))
    assert valid(a,c)
    return c

def main():
    # Exact cap rows, independently from the frozen/discovery files.
    cap_pairs=0
    for E,rows,n in ((P_EDGES,P_ROWS,4),(D_EDGES,D_ROWS,7)):
        g=graph(n+1,E+[(0,n)])
        for typ,row in rows.items():
            assert (row[0],row[-1])==typ and valid(g,dict(enumerate(row)))
            cap_pairs+=(n+1)*n//2
    # Universal edge boundary: maximal double-star, all 5^6 assignments.
    old=graph(6,[(0,1),(0,2),(0,3),(1,4),(1,5)])
    expanded=graph(10,[(0,2),(0,3),(1,4),(1,5),(0,6),(1,7),(6,8),(6,9),(7,8),(7,9),(8,9)])
    boundary_count=0
    for row in product(range(5),repeat=6):
        c=dict(enumerate(row))
        if not valid(old,c):continue
        A,B=c[0],c[1];positive=[x for x in (1,2,3,4) if x not in (A,B)]
        c.update({6:B,7:A,8:positive[0],9:positive[1]});assert valid(expanded,c);boundary_count+=1
    # ALL labeled simple graphs on at most six vertices, filtering original hypotheses.
    tested=0;pairs=0
    for n in range(7):
        E=list(combinations(range(n),2))
        for mask in range(1<<len(E)):
            a=graph(n,[e for i,e in enumerate(E) if mask>>i&1])
            if not good(a):continue
            c=solve(a);assert valid(a,c);tested+=1;pairs+=n*(n-1)//2
    # Exercise the seven-vertex exceptional cap and its pendant restoration at larger sizes.
    fixtures=[graph(7,D_EDGES),graph(8,D_EDGES+[(0,7)]),graph(10,D_EDGES+[(0,7),(7,8),(7,9),(8,9)])]
    # Several diamond insertions on a cycle, with and without retained triangle structure.
    a=graph(6,[(i,(i+1)%6) for i in range(6)])
    for k in range(5):
        u=min(a);v=min(a[u]);start=max(a)+1;x,y,p,q=range(start,start+4)
        a[u].remove(v);a[v].remove(u)
        for w in (x,y,p,q):a[w]=set()
        for b,c in ((u,x),(v,y),(x,p),(x,q),(y,p),(y,q),(p,q)):a[b].add(c);a[c].add(b)
        fixtures.append({u:set(ns) for u,ns in a.items()})
    for a in fixtures:
        c=solve(a);assert valid(a,c);tested+=1;pairs+=len(a)*(len(a)-1)//2
    bad=solve(fixtures[0]);u=min(fixtures[0]);v=min(fixtures[0][u]);bad[v]=bad[u]
    assert not valid(fixtures[0],bad)
    # Root construction must reject a claw and the separately handled K4.
    for badroot in (graph(4,[(0,1),(0,2),(0,3)]),graph(4,list(combinations(range(4),2)))):
        try:root_check(badroot)
        except AssertionError:pass
        else:raise AssertionError('invalid root hypothesis accepted')
    assert all(STATS[k]>0 for k in ('K4','isolated_diamond','pendant_diamond','same_neighbor_five','edge_replacement','adjacent_six','isolated_D','pendant_D','root_graphs'))
    print(json.dumps(dict(status='PASS',python=platform.python_version(),original_graphs=tested,original_distance_pairs=pairs,cap_rows=6,cap_distance_pairs=cap_pairs,universal_edge_boundaries=boundary_count,reduction_calls=dict(STATS),negative_controls=3,scope='all labeled n<=6 plus eight explicit fixtures; imported Yang-Wu theorem not reverified'),sort_keys=True))
if __name__=='__main__':main()
