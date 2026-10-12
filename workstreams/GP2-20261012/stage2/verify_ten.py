#!/usr/bin/env python3
"""Additional definition-level checks for the full ten-state reduction."""
from __future__ import annotations
from itertools import product, combinations
import random
import model, ten_state


def need(x,msg):
    if not x:raise ValueError(msg)


def closures(H):
    n=len(H);out=set()
    for mask in range(1,1<<n):
        I=[i for i in range(n) if mask>>i&1]
        O=tuple(j for j in range(n) if all(H[i][j] for i in I))
        if O:out.add((tuple(i for i in range(n) if all(H[i][j] for j in O)),O))
    return out


def literal_strict(n,C):
    return all(sum(x[k:k+4] in C for k in range(5))<=2 for x in product(range(n),repeat=8))


def check(data):
    P=tuple((a,b)for a in range(1,5)for b in range(a+1,6))
    h={p:tuple(int(p[0]<=t)+int(p[1]<=t)for t in range(6))for p in P}
    H=[[all(h[q][t]>=h[p][t-1]for t in range(1,6))for q in P]for p in P]
    M=[[all(h[q][t]>=h[p][t-1]+1 for t in range(1,6))for q in P]for p in P]
    need(data['profiles']==[list(p)for p in P],'ten-profile list')
    need(data['allowed']==[[int(v)for v in row]for row in H],'ten allowed/height mismatch')
    need(data['marked']==[[int(v)for v in row]for row in M],'ten marked/height mismatch')
    Q=tuple((a,b)for a in range(1,4)for b in range(a+1,5))
    R=tuple((a,b)for a in range(1,3)for b in range(a+1,4))
    need(data['pair_types']==[list(q)for q in Q] and data['letter_types']==[list(r)for r in R],'six/three type lists')
    rectangles=[(tuple(i for i,(a,b)in enumerate(P)if a>=x and b>=y),
                 tuple(i for i,(a,b)in enumerate(P)if a<=x+1 and b<=y+1))for x,y in Q]
    need(set(rectangles)==closures(H),'ten-target six rectangles')
    K=[[bool(set(O)&set(II))for II,OO in rectangles]for I,O in rectangles]
    need(all(K[i][j]==(Q[j][0]<=Q[i][0]+1 and Q[j][1]<=Q[i][1]+1)for i,j in product(range(6),repeat=2)),'six-target threshold arcs')
    rrectangles=[(tuple(i for i,(a,b)in enumerate(Q)if a>=x and b>=y),
                  tuple(i for i,(a,b)in enumerate(Q)if a<=x+1 and b<=y+1))for x,y in R]
    need(set(rrectangles)==closures(K),'six-target three rectangles')
    B=[[bool(set(O)&set(II))for II,OO in rrectangles]for I,O in rrectangles]
    need(all(all(row)for row in B),'three-letter target must be complete')
    entries=0
    for i,j in product(range(6),repeat=2):
        D=tuple(P[k]for k in sorted(set(rectangles[i][1])&set(rectangles[j][0])))
        need(D==ten_state.domain(Q[i],Q[j]),'ten-model domain formula')
        if not D:continue
        active=ten_state.active(Q[i],Q[j]);need(1<=len(active)<=3 and set(active)<=set(D),'ten active domains')
        for p in D:
            ii=P.index(p)
            need(any(all((not M[ii][k]or M[P.index(q)][k])and(not M[k][ii]or M[k][P.index(q)])for k in range(10))for q in active),'ten active domination')
            entries+=1
    used=set()
    for x,y,z,t,u in product(range(3),range(3),range(3),range(2),range(2)):
        p=ten_state.five_profile(x,y,t);q=ten_state.five_profile(y,z,u);used.update((p,q))
        i,j=P.index(p),P.index(q)
        need(H[i][j],'five-profile local allowedness')
        need(M[i][j]==(t==1 and u==0 and x<z),'five-profile marked objective identity')
    need(used=={(3,5),(2,5),(1,4),(1,3),(2,4)},'five-profile image')
    return {'triple_profiles':10,'pair_types':6,'letter_types':3,
            'allowed_arcs':sum(map(sum,H)),'marked_arcs':sum(map(sum,M)),
            'pair_arcs':sum(map(sum,K)),'letter_arcs':sum(map(sum,B)),
            'local_independent_embedding_cases':108,'active_domain_entries':entries,
            'rectangle_subsets_checked':(1<<10)-1+(1<<6)-1}


def finite_examples(jiggs):
    W=list(product(range(2),repeat=4));idx={w:i for i,w in enumerate(W)};forb=set()
    for x in product(range(2),repeat=8):
        for starts in combinations(range(5),3):forb.add(sum(1<<k for k in {idx[x[s:s+4]]for s in starts}))
    minimal=[]
    for m in sorted(forb,key=int.bit_count):
        if not any(m&e==e for e in minimal):minimal.append(m)
    counts={True:0,False:0}
    for mask in range(1<<16):
        if any(mask&e==e for e in minimal):continue
        C={W[i]for i in range(16)if mask>>i&1}
        ind,eta,kappa,gamma=ten_state.from_code(2,C);counts[ind]+=1
        CC=model.marked_code(2,gamma);rr=ten_state.reduce_active(2,eta,kappa,gamma);CCC=model.marked_code(2,rr)
        need(C<=CC<=CCC and literal_strict(2,CCC),'binary ten-model completion')
        if not ind:need(all(p[1]<=5 for p in model.profile_from_code(2,C).values()),'canonical F5 adjacency implication')
    C={tuple(w)for w in jiggs['original_code']}
    ind,eta,kappa,gamma=ten_state.from_code(4,C)
    need(ind and set(eta.values())=={(1,3)},'Jiggs homogeneous letter-type embedding')
    need(model.marked_code(4,gamma)==C,'Jiggs five-profile equality')
    actual_profile_count=len(set(gamma.values()))
    old_sixes=sum(tuple(p)[1]==6 for p in jiggs['gamma'])
    need(actual_profile_count<=5 and old_sixes>0,'Jiggs distinction between canonical and new profiles')
    rng=random.Random(2026101210)
    for n in (3,4):
        for trial in range(12):
            eta={a:rng.choice(ten_state.R)for a in range(n)}
            kappa={(a,b):rng.choice(ten_state.pair_domain(eta[a],eta[b]))for a,b in product(range(n),repeat=2)}
            gamma={(a,b,c):rng.choice(ten_state.domain(kappa[a,b],kappa[b,c]))for a,b,c in product(range(n),repeat=3)}
            ten_state.validate(n,eta,kappa,gamma)
            CC=model.marked_code(n,gamma);rr=ten_state.reduce_active(n,eta,kappa,gamma);CCC=model.marked_code(n,rr)
            need(CC<=CCC,'random ten-model domination')
            if trial<2:need(literal_strict(n,CCC),'literal ten-model strictness')
            for u in CCC:
                for v in CCC:
                    if u[1:]==v[:3]:need(eta[u[0]]==(2,3) and eta[v[-1]]==(1,2),'ten-model adjacency endpoints')
            ind,ee,kk,gg=ten_state.from_code(n,CCC)
            need(CCC<=model.marked_code(n,gg),'ten-model case reconstruction')
    return {'binary_independent_codes':counts[True],'binary_nonindependent_codes':counts[False],
            'binary_total':sum(counts.values()),'jiggs_profiles_used':actual_profile_count,
            'jiggs_old_canonical_second_hit_six':old_sixes,
            'random_ten_hierarchies':24,'literal_random_ten_examples':4}
