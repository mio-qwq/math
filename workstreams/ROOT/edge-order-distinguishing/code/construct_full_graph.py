#!/usr/bin/env python3
"""Construct/verify a global edge order for a properly edge-coloured simple graph.

Given {"n":n,"edges":[[u,v,color],...]}, return a correct single global edge
order, or reject a K2 or bicoloured-even-cycle connected component. All colours
are fixed and never changed. Strings/integers are supported. Standard library.
For the uniform-palette regular case import frozen verify_all_regular.py.
The differing-palette routine implements Theorem 5 of Gorzkowska--Kwasny.
"""
import argparse
from collections import deque
import json
import sys
from verify_all_regular import make_order as regular_make_order


def parse_graph(data):
    n=data['n']
    if type(n) is not int or n<0:
        raise ValueError('n must be nonnegative integer')
    edges=[]; pairs=set(); at={i:[] for i in range(n)}
    for item in data['edges']:
        if not isinstance(item,(list,tuple)) or len(item)!=3:
            raise ValueError('edge must be triple')
        a,b,c=item
        if type(a) is not int or type(b) is not int or not 0<=a<n or not 0<=b<n or a==b:
            raise ValueError('invalid endpoints')
        if type(c) not in (int,str):
            raise ValueError('bad colour type')
        a,b=sorted((a,b))
        if (a,b) in pairs:raise ValueError('duplicate edge')
        pairs.add((a,b)); e=(a,b,c); edges.append(e)
        at[a].append(e);at[b].append(e)
    if any(len({e[2] for e in es})!=len(es) for es in at.values()):
        raise ValueError('improper fixed colouring')
    return set(range(n)),edges


def independent_validate(V,E,order):
    if len(order)!=len(E) or len(set(E))!=len(E) or set(E)!=set(order):
        return False
    seq={v:[] for v in V}
    for a,b,c in order:
        if a not in seq or b not in seq or a==b:return False
        seq[a].append(c);seq[b].append(c)
    return all(seq[a]!=seq[b] for a,b,c in E)


def components(V,E):
    adj={v:[] for v in V}
    for a,b,c in E:adj[a].append(b);adj[b].append(a)
    seen=set();result=[]
    for root in sorted(V):
        if root in seen:continue
        Q={root};seen.add(root);todo=deque([root])
        while todo:
            x=todo.popleft()
            for y in adj[x]:
                if y not in seen:seen.add(y);Q.add(y);todo.append(y)
        result.append(Q)
    return result


def seq(local,v):
    return tuple(c for a,b,c in local if v in (a,b))


def order_distinct_palettes(V,E,palettes):
    """Faithful constructive proof of the original authors' Theorem 5."""
    P=palettes[min(V)]
    A={v for v in V if palettes[v]==P}
    assert A and A!=V
    M=sorted(e for e in E if ((e[0] in A)!=(e[1] in A)))
    assert M
    position={e:i for i,e in enumerate(M)}
    Mset=set(M);Qedges=[e for e in E if e not in Mset]
    Qs=components(V,Qedges)
    qidx={v:i for i,Q in enumerate(Qs) for v in Q}
    local_orders=[]
    for Q in Qs:
        inside=[e for e in Qedges if e[0] in Q]
        border=[e for e in M if (e[0] in Q or e[1] in Q)]
        assert border
        first=border[0];suffix=border[1:]
        root=first[0] if first[0] in Q else first[1]
        inc={v:[] for v in Q};adj={v:set() for v in Q}
        for e in inside:
            a,b,c=e
            inc[a].append(e);inc[b].append(e)
            adj[a].add(b);adj[b].add(a)
        parent={root:None};BFS=[root];todo=deque([root])
        while todo:
            u=todo.popleft()
            for v in sorted(adj[u]):
                if v not in parent:
                    parent[v]=u;BFS.append(v);todo.append(v)
        assert len(parent)==len(Q)
        prefix=[];processed=set()
        for v in reversed(BFS[1:]):
            pe=next(e for e in inc[v] if parent[v] in e[:2])
            prefix.extend(sorted(e for e in inc[v] if e not in prefix and e!=pe))
            indices=[i for i,e in enumerate(prefix) if v in e[:2]]
            slots=[indices[0] if indices else len(prefix)]+[i+1 for i in indices]
            assert len(slots)==len(inc[v])
            chosen=None
            for i in slots:
                candidate=prefix[:i]+[pe]+prefix[i:]
                if all(seq(candidate+suffix,v)!=seq(candidate+suffix,u)
                       for u in processed & adj[v]):
                    chosen=candidate;break
            if chosen is None:raise AssertionError('nonroot greedy choice impossible')
            prefix=chosen;processed.add(v)
        indices=[i for i,e in enumerate(prefix) if root in e[:2]]
        slots=[indices[0] if indices else len(prefix)]+[i+1 for i in indices]
        assert len(slots)==len(inc[root])+1
        chosen=None
        for i in slots:
            candidate=prefix[:i]+[first]+prefix[i:]
            if all(seq(candidate+suffix,root)!=seq(candidate+suffix,u)
                   for u in adj[root]):
                chosen=candidate;break
        if chosen is None:raise AssertionError('root greedy choice impossible')
        local=chosen+suffix
        assert set(local)==set(inside)|set(border)
        assert [e for e in local if e in Mset]==border
        assert all(seq(local,a)!=seq(local,b) for a,b,c in inside)
        local_orders.append(local)
    gaps=[[] for _ in range(len(M)+1)]
    for local in local_orders:
        gap=0
        for e in local:
            if e in Mset:
                assert position[e]>=gap-1
                gap=position[e]+1
            else:gaps[gap].append(e)
    global_order=[]
    for i in range(len(M)+1):
        global_order.extend(gaps[i])
        if i<len(M):global_order.append(M[i])
    assert independent_validate(V,E,global_order)
    return global_order


def order_connected(V,E):
    if not E:
        assert len(V)==1
        return [],'isolated_vertex'
    at={v:[] for v in V}
    for e in E:at[e[0]].append(e);at[e[1]].append(e)
    palette={v:frozenset(e[2] for e in at[v]) for v in V}
    if any(palette[a]!=palette[b] for a,b,c in E):
        return order_distinct_palettes(V,E,palette),'source_distinct_palette'
    P=palette[min(V)];d=len(P)
    assert all(palette[v]==P and len(at[v])==d for v in V)
    if d<3:
        if d==1:raise ValueError('obstruction: isolated K2 component')
        raise ValueError('obstruction: two-coloured even-cycle component')
    labels=sorted(P,key=lambda x:(type(x).__name__,repr(x)))
    encoding={v:i for i,v in enumerate(labels)}
    norm=[(a,b,encoding[c]) for a,b,c in E]
    result,ncycles=regular_make_order(V,norm,d)
    output=[(a,b,labels[c]) for a,b,c in result]
    assert independent_validate(V,E,output)
    return output,'uniform_palette_regular'


def construct(data):
    V,E=parse_graph(data);whole=[];methods=[]
    for part in components(V,E):
        internal=[e for e in E if e[0] in part]
        ordered,mode=order_connected(part,internal)
        whole.extend(ordered)
        methods.append({'size':len(part),'method':mode})
    if not independent_validate(V,E,whole):
        raise AssertionError('independent original-definition validator failed')
    return {'order':[list(e) for e in whole],'verified':True,'components':methods}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('file',nargs='?',help='JSON file, defaults to stdin')
    args=p.parse_args()
    with (open(args.file,encoding='utf8') if args.file else sys.stdin) as f:
        data=json.load(f)
    print(json.dumps(construct(data),ensure_ascii=False,separators=(',',':')))


if __name__=='__main__':main()
