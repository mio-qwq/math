#!/usr/bin/env python3
"""Rebuild and verify a 52-vertex nonbipartite girth-6 cubic graph from Heawood gadget."""
from collections import deque

BY_U={1:(0,2,10),3:(2,4,12),5:(4,6,0),7:(6,8,2),
      9:(8,10,4),11:(10,12,6),13:(12,0,8)}
U_ORDER=(1,3,7,9,11,13,5)
ROOT_BY_COLOR={0:1,1:13,2:5}

def norm(u,v,c):
    return (u,v,c) if u<v else (v,u,c)

def verify_interface():
    edge_list=[norm(u,v,c) for u,ns in BY_U.items() for c,v in enumerate(ns)]
    assert len(edge_list)==21 and len({(u,v) for u,v,c in edge_list})==21
    seq={v:[] for v in range(14)}
    for u in U_ORDER:
        for c,v in enumerate(BY_U[u]):
            seq[u].append(c)
            seq[v].append(c)
    assert all(len(seq[v])==3 and len(set(seq[v]))==3 for v in seq)
    assert all(tuple(seq[u])==(0,1,2) for u in U_ORDER)
    assert tuple(seq[0])==(0,1,2)
    assert all(tuple(seq[v])!=(0,1,2) for v in range(2,14,2))
    assert [u for u in U_ORDER if 0 in BY_U[u]]==[1,13,5]
    assert all(seq[u]!=seq[v] for u,v,c in edge_list if 0 not in (u,v))

def independent_check(vertices,edges,ordered):
    assert len(ordered)==len(edges) and set(ordered)==set(edges)
    assert len({(u,v) for u,v,c in edges})==len(edges)
    seq={v:[] for v in vertices};adj={v:[] for v in vertices}
    for u,v,c in ordered:
        assert u!=v
        seq[u].append(c)
        seq[v].append(c)
        adj[u].append(v)
        adj[v].append(u)
    assert all(len(seq[v])==3 and len(set(seq[v]))==3 for v in vertices)
    assert all(tuple(seq[u])!=tuple(seq[v]) for u,v,c in edges)
    return adj

def replace(vertices,edges,ordered,z):
    ext=[edge for edge in ordered if z in edge[:2]]
    assert len(ext)==3
    neighbors=[v if u==z else u for u,v,c in ext]
    palette=[edge[2] for edge in ext]
    assert len(set(palette))==3
    nxt=max(vertices)+1
    ids={v:nxt+i for i,v in enumerate(range(1,14))}
    newext={i:norm(ids[ROOT_BY_COLOR[i]],neighbors[i],palette[i]) for i in range(3)}
    internal=[norm(ids[u],ids[v],palette[c]) for u,ns in BY_U.items()
              for c,v in enumerate(ns) if v!=0]
    assert len(internal)==18
    template=[]
    for u in U_ORDER:
        for c,v in enumerate(BY_U[u]):
            template.append(('ext',c) if v==0 else ('int',norm(ids[u],ids[v],palette[c])))
    assert [val for tag,val in template if tag=='ext']==[0,1,2]
    gaps=[[] for i in range(4)]
    phase=0
    for tag,item in template:
        if tag=='ext':
            assert item==phase
            phase+=1
        else:
            gaps[phase].append(item)
    replacement={ext[i]:newext[i] for i in range(3)}
    out=[]
    for edge in ordered:
        if edge in replacement:
            i=ext.index(edge)
            out.extend(gaps[i])
            out.append(replacement[edge])
            if i==2:
                out.extend(gaps[3])
        else:
            out.append(edge)
    newedges=[e for e in edges if z not in e[:2]]+internal+list(newext.values())
    newvertices=(set(vertices)-{z})|set(ids.values())
    independent_check(newvertices,newedges,out)
    return newvertices,newedges,out

def exact_girth(adj):
    best=len(adj)+1
    for start in adj:
        seen={start:0}
        parent={start:None}
        todo=deque([start])
        while todo:
            u=todo.popleft()
            for v in adj[u]:
                if v not in seen:
                    seen[v]=seen[u]+1
                    parent[v]=u
                    todo.append(v)
                elif parent[u]!=v:
                    best=min(best,seen[u]+seen[v]+1)
    return best

def is_bipartite(adj):
    labels={}
    for start in adj:
        if start in labels:continue
        labels[start]=0
        todo=deque([start])
        while todo:
            u=todo.popleft()
            for v in adj[u]:
                if v in labels:
                    if labels[v]==labels[u]:return False
                else:
                    labels[v]=1-labels[u]
                    todo.append(v)
    return True

def main():
    verify_interface()
    edges=[norm(0,1,0),norm(2,3,0),norm(0,2,1),
           norm(1,3,1),norm(0,3,2),norm(1,2,2)]
    ordered=sorted(edges,key=lambda e:(e[0]+e[1],e[0],e[1]))
    verts=set(range(4))
    independent_check(verts,edges,ordered)
    for root in (0,1,2,3):
        verts,edges,ordered=replace(verts,edges,ordered,root)
    adj=independent_check(verts,edges,ordered)
    assert (len(verts),len(edges))==(52,78)
    assert exact_girth(adj)==6
    assert not is_bipartite(adj)
    assert all(not (set(adj[u]) & set(adj[v])) for u,v,c in edges)
    try:
        independent_check(verts,edges,ordered[:-1])
    except AssertionError:
        pass
    else:
        raise AssertionError('incomplete edge order was accepted')
    print('PASS Heawood interface, 4 substitutions, 52 vertices / 78 edges, girth 6, nonbipartite, original edge sequences')

if __name__=='__main__':
    main()
