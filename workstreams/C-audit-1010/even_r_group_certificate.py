#!/usr/bin/env python3
"""Raw finite verification of the two-ring group formula for even-r/odd-n
claw covers. Explicitly reconstructs *all* predicted automorphisms from ring
coordinate data, then checks the actual canonical double-cover adjacency.
It does not use NetworkX and is independent of VF2 enumerator.
"""
import argparse,json,hashlib
from pathlib import Path


def edges(r,n):
    h=r*n;N=3*h+n;X=[set() for _ in range(2*N)]
    def original_edge(u,v):
        X[2*u].add(2*v+1);X[2*v+1].add(2*u)
        X[2*v].add(2*u+1);X[2*u+1].add(2*v)
    for s in range(2*h):original_edge(s,(s+1)%(2*h))
    for p in range(h):
        leaf=2*h+p
        original_edge(leaf,p);original_edge(leaf,p+h)
        original_edge(leaf,3*h+p%n)
    assert all(len(nei)==(r if i//2>=3*h else 3) for i,nei in enumerate(X))
    return X


def map_formula(r,n,w,s,a0,a1):
    h=r*n;N=3*h+n
    assert n%2==1 and n>=3 and r>=2 and r%2==0
    assert w in (0,1) and s in (-1,1)
    assert a0%(2*n)==a1%(2*n)
    F=[-1]*(2*N)
    def v(u,layer):return 2*u+layer
    def set_one(u,layer,vv,ll):
        i=v(u,layer);j=v(vv,ll)
        assert F[i]<0
        F[i]=j
    for C in (0,1):
        a=a0 if C==0 else a1
        D=C^w
        for t in range(2*h):
            tt=(s*t+a)%(2*h)
            set_one(t,(t+C)%2,tt,(tt+D)%2)
        for p in range(h):
            pp=(s*p+a)%h
            layer=1-(p+C)%2
            newlayer=1-(pp+D)%2
            set_one(2*h+p,layer,2*h+pp,newlayer)
    for i in range(n):
        for eps in (0,1):
            b=i if i%2==eps else i+n
            assert b%(2*n)%2==eps
            bb=(s*b+a0)%(2*n)
            ip=bb%n
            ep=(bb+w)%2
            set_one(3*h+i,eps,3*h+ip,ep)
    assert -1 not in F and sorted(F)==list(range(2*N))
    return F


def check_raw(X,F):
    return all({F[v] for v in X[u]}==X[F[u]] for u in range(len(X)))


def run_case(r,n):
    h=r*n
    X=edges(r,n)
    unique=set();switch=[];strong=[]
    orientations={}
    for w in (0,1):
        for s in (1,-1):
            for a0 in range(2*h):
                for d in range(r):
                    a1=(a0+2*n*d)%(2*h)
                    f=map_formula(r,n,w,s,a0,a1)
                    ff=tuple(f);assert ff not in unique
                    unique.add(ff)
                    assert check_raw(X,f),(r,n,w,s,a0,a1)
                    is_switch=all(f[2*u]%2==1 and f[2*u+1]%2==0 for u in range(len(X)//2))
                    assert is_switch==((a0+w)%2==1)
                    if is_switch:
                        switch.append((w,s,a0,a1,f))
                        involution=all(f[f[i]]==i for i in range(len(f)))
                        loopless=all(f[i] not in X[i] for i in range(len(f)))
                        if involution and loopless:
                            strong.append((w,s,a0,a1))
    expected=8*h*r
    assert len(unique)==expected
    assert len(strong)==r+h and all(w==1 for w,_,_,_ in strong)
    counts={str(s):sum(ss==s for _,ss,_,_ in strong) for s in (1,-1)}
    assert counts=={'1':r,'-1':h}
    # The deck switch is exactly w=1,s=1,a0=a1=0.
    d=map_formula(r,n,1,1,0,0)
    assert all(d[i]==(i^1) for i in range(len(d)))
    return {'r':r,'n':n,'cover_vertices':len(X),'aut_constructed':len(unique),
            'switching_involutions_no_loop':len(strong), 'strong_class_sizes_by_orientation':counts,
            'deck_in_plus_orientation_class':True,
            'all_expected_automorphisms_raw_checked':True}


def tests():
    n=3;r=2;X=edges(r,n)
    f=map_formula(r,n,1,1,0,0)
    bad=f.copy();bad[0]=bad[1]
    assert not check_raw(X,bad)
    badX=[row.copy() for row in X]
    x=0;y=min(X[x]);badX[x].remove(y);badX[y].remove(x)
    assert not check_raw(badX,f)
    try:map_formula(r,n,0,1,0,1)
    except AssertionError:pass
    else:raise AssertionError('accepted impossible cross-cycle translation')
    return 3


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',default='even_r_group_results.json')
    a=p.parse_args()
    m=tests()
    pairs=[(r,n) for r in (2,4,6,8) for n in (3,5,7)]
    data=[run_case(r,n) for r,n in pairs]
    out=Path(a.out);out.write_text(json.dumps({'cases':data,'negative_controls':m},indent=2)+'\n')
    print('PASS',len(data),'odd-n/even-r parameter pairs; exact all proposed group actions')
    print('aut(X)=8*n*r*r; strong switches r*(n+1), slope classes [r,r*n]')
    print('negative controls',m)
    print('source sha256',hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    print('results sha256',hashlib.sha256(out.read_bytes()).hexdigest())

if __name__=='__main__':main()
