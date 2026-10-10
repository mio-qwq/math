#!/usr/bin/env python3
"""Construct global sequence-distinguishing edge order for any d>=3 proper d-coloured simple d-regular graph.
Independent original-definition validator and negative tests; stdlib only.
"""
from collections import deque, defaultdict
from random import Random
from itertools import combinations


def validate(vs, ed, order, d):
    if len(ed)!=len(order) or len(ed)!=len(set(ed)) or set(ed)!=set(order): return False
    seq={v: [] for v in vs}
    for u,v,c in order:
        if u == v or c<0 or c>=d or u not in vs or v not in vs:return False
        seq[u].append(c);seq[v].append(c)
    if any(len(seq[v])!=d or len(set(seq[v]))!=d for v in vs):return False
    return all(seq[u]!=seq[v] for u,v,c in ed)


def orient_edges_no_sink(Tv,Te,danger):
    """Orient multigraph T edges (a,b) so every 'dangerous' node has some outgoing edge.
    Dangerous vertices have >=2 incident edges. Other vertices can be sinks.
    Return edges oriented from tail to head.
    """
    adj={v:[] for v in Tv}
    for i,(a,b) in enumerate(Te):adj[a].append((b,i));adj[b].append((a,i))
    assert all(len(adj[v])>=2 for v in danger)
    orient={}
    seen=set()
    for source in Tv:
        if source in seen:continue
        component=set(); q=[source];seen.add(source)
        while q:
            u=q.pop();component.add(u)
            for v,i in adj[u]:
                if v not in seen:seen.add(v);q.append(v)
        safes=component-danger
        if safes:
            roots={min(safes)}
        else:
            # All vertices are dangerous: min degree >=2; find an undirected cycle
            stack=[];pos={}; parent_edge={}; cyclic=None
            def search(u,pedge):
                nonlocal cyclic
                pos[u]=len(stack);stack.append(u)
                for v,e in adj[u]:
                    if cyclic is not None:break
                    if e==pedge:continue
                    if v in pos:
                        # stack positions pos[v]..pos[u] plus (u,v)
                        j=pos[v]
                        cycle_vertices=stack[j:]
                        pairs=[]
                        for z in cycle_vertices[1:]:
                            pe=parent_edge[z]
                            pairs.append((pe,stack[pos[z]-1],z))
                        pairs.append((e,u,v))
                        cyclic=pairs
                        break
                    if v not in parent_edge and v!=source:
                        parent_edge[v]=e
                        search(v,e)
                stack.pop();pos.pop(u)
            search(source,-1)
            if cyclic is None:raise AssertionError('min-degree-2 graph lacked cycle')
            for e,a,b in cyclic:
                assert e not in orient
                orient[e]=(a,b)
            roots={a for e,a,b in cyclic}|{b for e,a,b in cyclic}
        todo=deque(sorted(roots));visited=set(roots)
        while todo:
            u=todo.popleft()
            for v,e in adj[u]:
                if v not in visited:
                    visited.add(v)
                    orient[e]=(v,u)
                    todo.append(v)
        assert visited==component
    for i,(a,b) in enumerate(Te):orient.setdefault(i,(a,b))
    for v in danger:
        assert any(tail==v for tail,head in orient.values()),('sink',v)
    return orient


def choose_nonsaturated_roots(cycles,Q, V):
    """Proof-constructive two-candidate method via orientation on Q-components."""
    adj={v:[] for v in V}
    for u,v,c in Q:adj[u].append(v);adj[v].append(u)
    assert all(len(adj[v])>=1 for v in V)
    comp={};members=[]
    for v in sorted(V):
        if v in comp:continue
        k=len(members);q=[v];comp[v]=k;mem=[]
        while q:
            x=q.pop();mem.append(x)
            for y in adj[x]:
                if y not in comp:comp[y]=k;q.append(y)
        members.append(set(mem))
    # Candidate roots: two different vertices of every 0/1 cycle.
    cand=[(C[0],C[1]) for C in cycles]
    pool={v for pair in cand for v in pair}
    # Dangerous Q-components all vertices are candidates from distinct cycles
    danger=set()
    cyc_of={v:i for i,C in enumerate(cycles) for v in C}
    for k,mem in enumerate(members):
        if mem<=pool and len({cyc_of[x] for x in mem})==len(mem):danger.add(k)
    Te=[(comp[a],comp[b]) for a,b in cand]
    orient=orient_edges_no_sink(set(range(len(members))),Te,danger)
    roots=[]
    for i,(a,b) in enumerate(cand):
        ta,he=orient[i]
        roots.append(a if comp[a]==he else b)
    assert len(roots)==len(cycles)
    R=set(roots)
    assert len(R)==len(roots)
    assert all(not mem<=R for mem in members),('bad Qcomponent',members,R)
    return roots,comp,members


def make_order(V,E,d):
    E=[(min(a,b),max(a,b),c) for a,b,c in E]
    assert len(set(E))==len(E) and len({(u,v) for u,v,c in E})==len(E)
    adj={v:{} for v in V}
    for a,b,c in E:
        assert c not in adj[a] and c not in adj[b]
        adj[a][c]=b;adj[b][c]=a
    assert all(set(adj[v])==set(range(d)) for v in V)
    # independent even 0/1 cycles via alternation
    cycles=[];unused=set(V)
    while unused:
        s=min(unused);C=[];x=s;c=0
        while x not in C:
            C.append(x);unused.remove(x)
            x=adj[x][c];c^=1
        assert x==s and len(C)>=4 and len(C)%2==0
        cycles.append(C)
    Q=[e for e in E if e[2]>=2]
    roots,comp,members=choose_nonsaturated_roots(cycles,Q,V)
    rootset=set(roots)
    # Root graph consists of induced Q-edges among chosen roots.
    root_adj={r:[] for r in roots};boundary=set()
    for u,v,c in Q:
        if u in rootset and v in rootset:
            root_adj[u].append(v);root_adj[v].append(u)
        elif u in rootset:boundary.add(u)
        elif v in rootset:boundary.add(v)
    # Each root-component has some boundary vertex because no full Q-component is roots.
    seen=set();sorted_roots=[]
    for r in roots:
        if r in seen:continue
        sub=set();q=[r];seen.add(r)
        while q:
            x=q.pop();sub.add(x)
            for y in root_adj[x]:
                if y not in seen:seen.add(y);q.append(y)
        candidates=sub & boundary
        assert candidates,('component entirely saturated',sub)
        anchor=min(candidates)
        distance={anchor:0};q=deque([anchor])
        while q:
            x=q.popleft()
            for y in root_adj[x]:
                if y not in distance:distance[y]=distance[x]+1;q.append(y)
        assert set(distance)==sub
        sorted_roots += sorted(sub,key=lambda v:(-distance[v],v))
    assert set(sorted_roots)==rootset
    cyc_idx={r:i for i,r in enumerate(roots)}
    oriented=[];positions={}
    for cid,r in enumerate(sorted_roots):
        D=[];x=r;c=0
        while x not in D:
            D.append(x);x=adj[x][c];c^=1
        assert x==r and len(D)==len(cycles[cyc_idx[r]])
        oriented.append(D)
        for j,v in enumerate(D):positions[v]=(cid,j)
    # Everyone has an outgoing assigned Q edge at selected root.
    slots={v:[] for v in V}
    for a,b,c in Q:
        if a in rootset and b in rootset:owner=min((a,b),key=positions.get)
        elif a in rootset:owner=a
        elif b in rootset:owner=b
        else:owner=min((a,b),key=positions.get)
        slots[owner].append((a,b,c))
    assert all(slots[r] for r in rootset),('no root-owned extra edge',[(r,slots[r]) for r in roots])
    out=[]
    for D in oriented:
        for j,v in enumerate(D):
            a,b=v,D[(j+1)%len(D)]
            out.append((min(a,b),max(a,b),j%2))
            out+=sorted(slots[v],key=lambda e:e[2])
    assert validate(V,E,out,d)
    return out,len(cycles)


def random_matching(n,banned,rng,rounds=150):
    for trial in range(rounds):
        L=list(range(n));rng.shuffle(L)
        M=[(min(L[i],L[i+1]),max(L[i],L[i+1])) for i in range(0,n,2)]
        if all(tuple(pair) not in banned for pair in M):return M
    return None


def run():
    rng=Random(164010)
    tally=defaultdict(int)
    # For each d and cyclic 0/1 factor type, 3+ positive colours, random all graph-colouring constraints.
    for d in (3,4,5,6,7,9):
        for partition in ((4,4),(6,6),(4,4,4),(4,4,4,4),(4,4,4,4,4),(8,8),(6,10),(4,6,8)):
            n=sum(partition)
            if n<=d:continue
            cycles=[];k=0;E=[];banned=set()
            for size in partition:
                C=list(range(k,k+size));k+=size;cycles.append(C)
                for i,v in enumerate(C):
                    q=C[(i+1)%size];a,b=sorted((v,q))
                    E.append((a,b,i%2));banned.add((a,b))
            good=0
            for t in range(100):
                edges=E[:];S=set(banned)
                for col in range(2,d):
                    M=random_matching(n,S,rng)
                    if M is None:break
                    edges.extend((a,b,col) for a,b in M)
                    S.update(M)
                if len(edges)!=n*d//2:continue
                make_order(set(range(n)),edges,d)
                good+=1
            tally[(d,partition)]=good
    # Explicit all odd factor? K6 and K8 complete graphs via circle method
    for n in (6,8,10):
        d=n-1
        edges=[]
        for c in range(n-1):
            pairs=[(n-1,c)]+[((c+j)%(n-1),(c-j)%(n-1)) for j in range(1,n//2)]
            for a,b in pairs:edges.append((min(a,b),max(a,b),c))
        make_order(set(range(n)),edges,d)
        tally[('complete',n)]=1
    assert all(cnt>0 for cnt in tally.values()),{k:v for k,v in tally.items() if v==0}
    print('PASS all-degree independent-original-definition ordering, sample total',sum(tally.values()),'cases',len(tally),'mincase',min(tally.values()))
    # invalid/missing edge must be rejected
    E=[(0,1,0),(2,3,0),(0,2,1),(1,3,1),(0,3,2),(1,2,2)]
    order,_=make_order(set(range(4)),E,3)
    assert not validate(set(range(4)),E,order[:-1],3)
    print('PASS missing-edge negative test')

if __name__=='__main__':run()