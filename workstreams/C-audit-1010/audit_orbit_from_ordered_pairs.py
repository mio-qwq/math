#!/usr/bin/env python3
"""C-audit-1010: raw ordered-edge orbit adversarial audit of Mizzi v3/7.

Generate ALL symmetric q-compatible 0-1 relations without presupposing
orbit independence or CRT gcd classes.  Disallow source/target loops using
both original diagonal conditions.  Check every original graph assumption,
CDC isomorphism, pair nonisomorphism and the ORIGINAL cycle conclusion
by independently enumerating cycles of required lengths.

The finite computation cannot prove or refute the universal theorem unless
it finds a fully certified witness. No code imported from C's discovery suite.
"""
import argparse
import hashlib
import itertools
import json
import platform
from collections import deque
from pathlib import Path
import networkx as nx

CASES = [(1,1,4,4), (6,2,2), (8,4), (6,6), (2,2,4,4),
         (1,2,3,6), (2,2,2,2,4), (4,4,4), (2,4,6), (2,2,2,2,2)]


def permutation(sizes):
    q = []; orbit_id=[]; indices=[]; base=0
    for i,m in enumerate(sizes):
        for j in range(m):
            q.append(base + ((j+1)%m))
            orbit_id.append(i)
        indices.append(tuple(range(base,base+m)))
        base+=m
    return q,orbit_id,indices


def ordered_pair_orbits(q):
    n=len(q)
    visited=set(); valid=[]; forbidden=[]
    for a in range(n):
        for b in range(n):
            if (a,b) in visited:
                continue
            seen={(a,b)};front=[(a,b)]
            # Build equivalence under symmetry + TF generator DIRECTLY.
            for u,v in front:
                for x,y in [(v,u), (q[u],inv[v])]:
                    if (x,y) not in seen:
                        seen.add((x,y)); front.append((x,y))
            visited.update(seen)
            undirected=set((min(u,v),max(u,v)) for u,v in seen)
            # A(u,u)=0 AND B(u,u)=A(u,q(u))=0.
            invalid=any(u==v or (v==q[u]) for u,v in seen)
            if invalid:
                forbidden.append(undirected)
            else:
                valid.append(tuple(sorted(undirected)))
    assert len(visited)==n*n
    assert not any(any(u==v for u,v in cls) for cls in valid)
    return valid,forbidden


def from_selected_orbits(n,classes,mask):
    adj=[0]*n
    for i,cls in enumerate(classes):
        if (mask >> i) & 1:
            for u,v in cls:
                adj[u] |= 1<<v
                adj[v] |= 1<<u
    return adj


def twist(a,q):
    n=len(a)
    out=[0]*n
    for u in range(n):
        row=0
        for v in range(n):
            if (a[u] >> q[v]) & 1:
                row |= 1<<v
        out[u]=row
    return out


def raw_compatible(a,b,q):
    n=len(q)
    if sorted(q)!=list(range(n)):return False
    if any((a[u]>>u)&1 or (b[u]>>u)&1 for u in range(n)):return False
    for u in range(n):
        for v in range(n):
            if (a[u]>>v)&1 != (a[v]>>u)&1:return False
            if (b[u]>>v)&1 != (b[v]>>u)&1:return False
            if (b[u]>>v)&1 != (a[u]>>q[v])&1:return False
    return True


def source_graph(a):
    n=len(a)
    if len(set(a))!=n:return False # twin-free
    visited=1;queue=deque([0]);parity=[-1]*n;parity[0]=0;odd=False
    while queue:
        u=queue.popleft()
        mask=a[u]
        while mask:
            bit=mask & -mask;mask^=bit;v=bit.bit_length()-1
            if parity[v]<0:
                parity[v]=1-parity[u]
                visited |= bit
                queue.append(v)
            elif parity[v]==parity[u]:odd=True
    return visited==(1<<n)-1 and odd


def invariant(a):
    n=len(a)
    deg=sorted(row.bit_count() for row in a)
    tri=[]
    for i in range(n):
        t=0
        for j in range(n):
            if (a[i]>>j)&1:
                t += (a[i]&a[j]).bit_count()
        tri.append(t//2)
    return (tuple(deg),tuple(sorted(tri)))


def iso(a,b):
    if invariant(a)!=invariant(b):return False
    g=nx.Graph();h=nx.Graph();n=len(a)
    g.add_nodes_from(range(n));h.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1,n):
            if (a[i]>>j)&1:g.add_edge(i,j)
            if (b[i]>>j)&1:h.add_edge(i,j)
    return nx.is_isomorphic(g,h)


def cycle_sets(a,k):
    n=len(a);out=set()
    for root in range(n):
        def dfs(cur,path,used):
            if len(path)==k:
                if (a[cur]>>root)&1:
                    out.add(used)
                return
            neigh=a[cur]
            while neigh:
                bit=neigh & -neigh;neigh^=bit
                v=bit.bit_length()-1
                if v>root and not (used&bit):
                    dfs(v,path+[v],used|bit)
        dfs(root,[root],1<<root)
    return out


def has_disjoint_pair(masks):
    return any(a&b==0 for a,b in itertools.combinations(masks,2))


def cycle_claim(a,b):
    n=len(a)
    for k in range(3,n//2+1,2):
        for one,two in ((a,b),(b,a)):
            cs=cycle_sets(one,k)
            if len(cs)>=2 and has_disjoint_pair(cs) and cycle_sets(two,2*k):
                return True,k
    return False,None


def direct_cdc_iso(a,b,q):
    n=len(q);inv=[0]*n
    for i,j in enumerate(q):inv[j]=i
    phi=[2*u if layer==0 else 2*inv[u]+1 for u in range(n) for layer in range(2)]
    for i in range(2*n):
        for j in range(2*n):
            u,layer=i//2,i%2;v,other=j//2,j%2
            p,l2=phi[i]//2,phi[i]%2;r,m2=phi[j]//2,phi[j]%2
            source=(layer!=other) and bool((a[u]>>v)&1)
            dest=(l2!=m2) and bool((b[p]>>r)&1)
            if source!=dest:return False
    return True


def negative_tests(q,classes):
    n=len(q);a=from_selected_orbits(n,classes,1);b=twist(a,q)
    assert raw_compatible(a,b,q)
    assert not raw_compatible(a,b,q[:-1]+[q[0]])
    fake_b=b.copy();fake_b[0]^=1<<0
    assert not raw_compatible(a,fake_b,q)
    p=next((u,v) for u in range(n) for v in range(u+1,n) if (a[u]>>v)&1)
    bad_a=a.copy();u,v=p;bad_a[u]^=1<<v;bad_a[v]^=1<<u
    assert not raw_compatible(bad_a,b,q)
    return 3


def run(max_models=16384):
    global inv
    cases=[];total=0;cousins=0;bad=0
    for sizes in CASES:
        q,orbit_id,indices=permutation(sizes)
        inv=[0]*len(q)
        for i,j in enumerate(q):inv[j]=i
        cls,forb=ordered_pair_orbits(q)
        assert all(orbit_id[u]!=orbit_id[v] for block in cls for u,v in block),\
          'proof says intra-orbit edges violate at least one loop condition'
        count=1<<len(cls)
        if count>max_models:
            cases.append({'orbit_lengths':sizes,'allowed_classes':len(cls),'status':'SKIPPED_MASK_BUDGET','total_masks':count})
            continue
        assert cls
        negatives=negative_tests(q,cls)
        qualified=0;pass_claim=0;src=0;twinfree=0
        for mask in range(count):
            a=from_selected_orbits(len(q),cls,mask)
            b=twist(a,q)
            assert raw_compatible(a,b,q)
            if not (source_graph(a) and source_graph(b)):continue
            src+=1
            if iso(a,b):continue
            qualified+=1
            assert direct_cdc_iso(a,b,q)
            success,k=cycle_claim(a,b)
            if success:pass_claim+=1
            else:
                bad+=1
                print('CANDIDATE CONTRADICTION',sizes,mask)
        total+=count;cousins+=qualified
        cases.append({'orbit_lengths':sizes,'allowed_classes':len(cls),'forbidden_classes':len(forb),
          'all_admissible_masks':count,'source_constrained_pairs':src,
          'nonisomorphic_TF_cousins':qualified,'cycle_claim_verified':pass_claim,
          'exceptions':qualified-pass_claim,'negative_tests':negatives})
        print('CASE',sizes,'masks',count,'qualified',qualified,'exceptions',qualified-pass_claim,flush=True)
    result={'source':'Mizzi 2603.27559v3 Section 7 first TF-cousin conjecture',
      'algorithm':'direct ordered-pair group orbits (NOT gcd-sum construction)',
      'python':platform.python_version(),'networkx':nx.__version__,
      'masks_checked':total,'cousins_verified':cousins,'exceptions':bad,
      'per_profile':cases}
    file=Path(__file__).with_name('adversarial_result.json')
    file.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('RESULT',total,cousins,bad,'SHA256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    assert bad==0


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--max-models',type=int,default=16384)
    args=p.parse_args();run(max_models=args.max_models)
