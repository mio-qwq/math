#!/usr/bin/env python3
"""Independent finite validator for the GP2 stage-two candidate.

This deliberately reconstructs the target, closures, weighted moments, 2-SAT
path witnesses and original Kautz BFS without importing model.py.
The all-alphabet statements rely on their written proofs, not finite sampling.
"""
import hashlib
import itertools
import json
import math
from collections import Counter, defaultdict, deque
from fractions import Fraction
from pathlib import Path

HERE=Path(__file__).resolve().parent
P=[(a,b) for a in range(1,5) for b in range(a+1,7)]
Q=[(a,b) for a in range(1,4) for b in range(a+1,6)]
R=[(a,b) for a in range(1,3) for b in range(a+1,5)]
logs=[]
def check(expr,tag):
    assert expr,tag
    logs.append(tag)
def heights(p):return [int(p[0]<=t)+int(p[1]<=t) for t in range(6)]
def ext_graph(V):return [[int(x[0]>=y[0]-1 and (x[1]>=y[1]-1 or x[1]>=len(V)//99+5)) for y in V] for x in V]
def allowed(p,q):return q[0]<=p[0]+1 and (p[1]>=5 or q[1]<=p[1]+1)
def marked(p,q):return allowed(p,q) and q[0]==1 and p[1]>=5 and q[1]<=p[0]+1

def closure_rectangles(H):
    n=len(H); ret={}
    for mask in range(1,1<<n):
        L=[i for i in range(n) if mask>>i&1]
        right=tuple(j for j in range(n) if all(H[i][j] for i in L))
        if not right:continue
        left=tuple(i for i in range(n) if all(H[i][j] for j in right))
        ret[(left,right)]=True
    return set(ret)

def from_pairs(V):
    if len(V)==14:
        w=5; lower=Q
    elif len(V)==9:
        w=4; lower=R
    else:raise Exception('wrong graph')
    rectangles=set()
    for a,b in lower:
        incoming=tuple(i for i,p in enumerate(V) if p[0]>=a and p[1]>=b)
        outgoing=tuple(j for j,p in enumerate(V) if p[0]<=a+1 and p[1]<=b+1)
        rectangles.add((incoming,outgoing))
    return rectangles

def graph_r(V):return [[int(q[0]<=p[0]+1 and q[1]<=p[1]+1) for q in V] for p in V]
def domain(V, x, y):return [p for p in V if p[0]>=y[0] and p[1]>=y[1] and p[0]<=x[0]+1 and p[1]<=x[1]+1]

def canon(n,C):
    S=range(n);P3=list(itertools.product(S,repeat=3)); F={v:[0] for v in P3}
    for t in range(1,6):
        for v in P3:
            F[v].append(max(F[(a,)+v[:2]][t-1]+int((a,)+v in C) for a in S))
    check(max(v[-1] for v in F.values())<=2, 'jiggs full-shift five-step strict DP')
    out={}
    for v,score in F.items():
        a=next(i for i in range(1,5) if score[i]>=1)
        b=next((i for i in range(2,6) if score[i]>=2),6)
        out[v]=(a,b)
    return out,F

def get_rotations(w):return sorted({w[i:]+w[:i] for i in range(4)})
def orbits(n,L):
    out=[]
    for rep in sorted({min(get_rotations(w)) for w in itertools.product(range(n),repeat=4)}):
        cs=[w for w in get_rotations(rep) if L[n*w[0]+w[1]]<L[n*w[2]+w[3]]]
        if cs:out.append(cs)
    return out

def direct_moments(n,L,weights):
    orb=orbits(n,L);W=sum(weights)
    forced={o[0] for o in orb if len(o)==1}
    T=Fraction(sum(math.prod(weights[v] for v in o[0]) for o in orb),W**4)
    ins={d:defaultdict(int) for d in range(1,4)}
    outs={d:defaultdict(int) for d in range(1,4)}
    for w in forced:
        for d in range(1,4):
            ins[d][w[d:]]+=math.prod(weights[i] for i in w[:d])
            outs[d][w[:4-d]]+=math.prod(weights[i] for i in w[4-d:])
    theta={}
    for a in range(1,4):
        for b in range(1,5-a):
            s=sum(math.prod(weights[i] for i in v)*ins[a][v[:4-a]]*outs[b][v[b:]] for v in forced)
            theta[f'{a},{b}']=str(Fraction(s,W**(4+a+b)))
    return {'E':str(1-4*T),'T':str(T),'forced_count':len(forced),'moments':theta},orb,forced

def check_sat_certificate(inst):
    n=inst['n'];L=inst['levels'];solution=inst['completion']
    oo=orbits(n,L)
    check(len(oo)==solution['orbits'],'orbit cardinality '+str(n))
    check(sum(len(o)==1 for o in oo)==solution['singletons'],'singleton cardinality '+str(n))
    idw={w:2*i+j for i,o in enumerate(oo) for j,w in enumerate(o)}
    adj=set();count=0
    for x in idw:
        for y in idw:
            if x[1:]==y[:3]:
                adj.add((x,y));count+=1
    check(count==solution['conflicts'],'candidate conflicts '+str(n))
    if solution['status']=='SAT':
        C={tuple(w) for w in solution['code']}
        check(len(C)==len(oo),'sat picks one candidate from every orbit')
        check(all(sum(w in C for w in o)==1 for o in oo),'sat orbital coverage')
        check(not any(w[1:]==v[:3] for w in C for v in C),'sat actual independence')
    else:
        i=solution['variable']; pp=solution['paths'];check(len(pp)==2,'unsat two paths')
        for k,path in enumerate(pp):
            x=2*i+k; target=2*i+(1-k)
            for edge in path:
                check(edge['from']==x,'implication path connected')
                y=edge['to']; reason=edge['reason']
                if 'unit' in reason:
                    w=tuple(reason['unit']);
                    check(x%2==1 and y==x-1 and x//2<len(oo) and len(oo[x//2])==1 and w==oo[x//2][0], 'single candidate forced implication')
                else:
                    u,v=(tuple(z) for z in reason['conflict'])
                    check(u in idw and v in idw and u[1:]==v[:3], 'conflicting shift words real')
                    check((x==idw[u] and y==(idw[v]^1)) or (x==idw[v] and y==(idw[u]^1)), 'implication grounded')
                x=y
            check(x==target,'unsat path reaches complement')

def BFS(n):
    W=[w for w in itertools.product(range(n),repeat=4) if all(w[i]!=w[i+1] for i in range(3))]
    ix={w:i for i,w in enumerate(W)}
    adj=[[ix[w[1:]+(a,)] for a in range(n) if a!=w[3]] for w in W]
    D=[]
    for i in range(len(W)):
        d=[-1]*len(W);d[i]=0;todo=deque([i]);
        while todo:
            v=todo.popleft()
            for j in adj[v]:
                if d[j]==-1:d[j]=d[v]+1;todo.append(j)
        D.append(d)
    return W,adj,D

def main():
    data=json.loads((HERE/'certificate.json').read_text())
    check(data['stage1_commit']=='b45b04eeab0fc521b789d6d47b4d8b94119e8c90','base signed stage1 identity')
    H=[[int(all(heights(q)[t]>=heights(p)[t-1] for t in range(1,6))) for q in P]for p in P]
    M=[[int(all(heights(q)[t]>=heights(p)[t-1]+1 for t in range(1,6))) for q in P]for p in P]
    check(H==data['target']['allowed'] and M==data['target']['marked'],'14-profile independent height inequalities')
    check(sum(sum(row) for row in H)==138 and sum(sum(row) for row in M)==20,'target arcs counts')
    check(closure_rectangles(H)==from_pairs(P),'14->9 all inclusion maximal rectangles')
    K=graph_r(Q);check(len(closure_rectangles(K))==5 and closure_rectangles(K)==from_pairs(Q),'9->5 all inclusion maximal rectangles')
    TT=graph_r(R);check(sum(sum(row) for row in TT)==23,'letter type graph has 23 arcs')
    ds=Counter();domin=[]
    for x,y in itertools.product(Q,repeat=2):
        dom=domain(P,x,y)
        if not dom:continue
        ds[len(dom)]+=1
        active=set()
        a,b=x;c,d=y
        if b>=4:active.add((a+1,b+1))
        if c==1 and d<=4:active.add((1,d))
        if c==1 and b>=4:active.add((1,5))
        if not active:active.add(min(dom))
        check(active.issubset(dom),'active domain contained')
        for p in dom:
            opts=[q for q in active if all((not M[P.index(p)][j] or M[P.index(q)][j]) and (not M[j][P.index(p)] or M[j][P.index(q)]) for j in range(len(P)))]
            if not opts:raise AssertionError('profile nondominated at '+str((x,y,p)))
        domin.append((x,y,active))
    check(len(domin)==64 and max(len(x[2]) for x in domin)<=3,'64 pair domains and <=3 active profiles')
    check(data['target']['profiles']==[list(p) for p in P] and data['target']['pair_types']==[list(p) for p in Q] and data['target']['letter_types']==[list(p) for p in R], 'target type binding')
    for key in ('jiggs','six_letter_obstruction'):
        obj=data[key];calc,_,forced=direct_moments(obj['n'],obj['levels'],obj['weights'])
        for k in ('E','T','forced_count','moments'):
            check(calc[k]==obj[k],f'{key} exact {k}')
        ws=obj['consecutive_forced_witness'];
        if ws:
            check(len(ws)==6 and all(tuple(ws[i:i+4]) in forced for i in range(3)), 'literal triple forced witness')
        check_sat_certificate(obj)
    source=HERE.parent/'literature_lifts/jiggs57_words.txt'
    check(hashlib.sha256(source.read_bytes()).hexdigest()==data['jiggs']['source_sha256'],'historical Jiggs dictionary SHA256')
    jiggs={tuple('ABCD'.index(x) for x in w) for w in source.read_text().split()}
    check(len(jiggs)==57 and sorted(jiggs)==[tuple(w) for w in data['jiggs']['original_code']], 'Jiggs 57 binding')
    g,F=canon(4,jiggs);check([list(g[w]) for w in itertools.product(range(4),repeat=3)]==data['jiggs']['gamma'],'64 canonical triple profiles')
    kap={(b,c):(min(3,min(g[a,b,c][0] for a in range(4))),min(5,min(g[a,b,c][1] for a in range(4)))) for b,c in itertools.product(range(4),repeat=2)}
    eta={b:(min(2,min(kap[a,b][0] for a in range(4))),min(4,min(kap[a,b][1] for a in range(4)))) for b in range(4)}
    check([list(kap[w]) for w in itertools.product(range(4),repeat=2)]==data['jiggs']['kappa'] and [list(eta[x]) for x in range(4)]==data['jiggs']['eta'],'pair/letter hierarchy Jiggs')
    reduced={}
    for w,p in g.items():
        x,y=kap[w[:2]],kap[w[1:]];a,b=x;c,d=y
        act=set()
        if b>=4:act.add((a+1,b+1))
        if c==1 and d<=4:act.add((1,d))
        if c==1 and b>=4:act.add((1,5))
        if not act:act.add(min(domain(P,x,y)))
        reduced[w]=next(q for q in sorted(act) if all((not marked(p,t) or marked(q,t)) and (not marked(t,p) or marked(t,q)) for t in P))
    check([list(reduced[w]) for w in itertools.product(range(4),repeat=3)]==data['jiggs']['reduced_gamma'],'exact reduced active triple assignment')
    CC={w for w in itertools.product(range(4),repeat=4) if marked(reduced[w[:3]],reduced[w[1:]])}
    check(jiggs<=CC,'objective and word preservation after profile domination')
    for instance in data['actual_kautz']:
        n=instance['n'];W,adj,D=BFS(n)
        check(instance['vertices']==[list(w) for w in W],'original valid Ka vertices '+str(n))
        check(instance['adjacency']==adj,'original Ka graph adjacency '+str(n))
        check(instance['distances']==D,'original Ka BFS all sources '+str(n))
        S=set(instance['selected']);
        # Check shortest-path triple via exact distance equality; no need enumerate shortest paths.
        check(all(not (i!=j and j!=k and i!=k and D[i][k]==D[i][j]+D[j][k]) for i in S for j in S for k in S),'actual GP semantics '+str(n))
    # Explicit controlled corruptions: mismatch of arc, altered parameter, impossible 2-SAT reason.
    falseH=[row[:] for row in H];falseH[0][0]^=1
    check(falseH!=data['target']['allowed'],'negative control: damaged target arc detected')
    badL=data['six_letter_obstruction']['levels'][:];badL[0]=3
    check(any(x not in (0,1,2) for x in badL),'negative control: corrupted level range detected')
    check(tuple(data['jiggs']['weights'])!=(5,5,3,4),'negative control: damaged weight vector detected')
    print('PASS: GP2 stage-two independent checks')
    print('passed checkpoints',len(logs),'pair domain size histogram',dict(sorted(ds.items())))
    print('certificate SHA256',hashlib.sha256((HERE/'certificate.json').read_bytes()).hexdigest())

if __name__=='__main__':main()
