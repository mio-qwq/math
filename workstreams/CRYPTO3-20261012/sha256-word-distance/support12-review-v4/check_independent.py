#!/usr/bin/env python3
"""Independent exact carry/GF(2) exhaustion; imports no author code.

Three actual +D input pairs are a,a+D; b,b+D; c,c+D.  The third
pair is reversed from the support's negative-D pair.  Necessary core:
Fa=Fb=-Fc, Gb-Ga=2D, Gb+Gc=D (all modulo 2^32).
"""
import argparse
import collections
import datetime
import hashlib
import itertools
import json
import pathlib
import time

N=1<<32
M=N-1
ROOT=pathlib.Path(__file__).resolve().parent

def rotr(x,n):
    return ((x>>n)|(x<<(32-n)))&M

def sigma0(x):
    return rotr(x,7)^rotr(x,18)^(x>>3)

def sigma1(x):
    return rotr(x,17)^rotr(x,19)^(x>>10)

def output_rows(fn):
    return [sum(1<<i for i in range(32) if (fn(1<<i)>>j)&1)
            for j in range(32)]

FR=output_rows(sigma0)
GR=output_rows(sigma1)

def masks(k):
    """Enumerate every high-13-bit word.  Check each fibre is exactly affine.

    The mask fixes a_i=carry_{i+1} for each flipped input i<31;
    unflipped bits and the final input bit31 remain free.
    """
    fibres=collections.defaultdict(list)
    for a in range(1<<13):
        fibres[a^((a+k)&8191)].append(a)
    ans=[]
    for m,values in sorted(fibres.items()):
        fixed=m&4095
        value=values[0]&fixed
        expected=[a for a in range(8192) if a&fixed==value]
        assert values==expected, ('mask fibre not exact',k,m)
        alpha=m<<19
        ans.append((alpha,fixed<<19,value<<19,
                    sigma0(alpha),sigma1(alpha)))
    return ans

def insert(basis,row,rhs):
    """Rows use 96 variables plus constant bit 96. Returns False iff 0=1."""
    w=row|((rhs&1)<<96)
    while w&((1<<96)-1):
        pivot=(w&((1<<96)-1)).bit_length()-1
        if pivot in basis:
            w^=basis[pivot]
        else:
            basis[pivot]=w
            return True
    return not (w>>96)

def fixed_input_basis(cases):
    basis={}
    for word,case in enumerate(cases):
        _,mask,value,_,_=case
        for bit in range(19,31):
            if mask>>bit&1:
                assert insert(basis,1<<(32*word+bit),value>>bit&1)
    return basis

def equation_templates(mask1,mask2,target,op,rows1,rows2):
    """Truth-table every exact masked add/subtract bit and its signed carry.

    An arithmetic equation is A1 op A2 = target modulo 2^31. Output
    masks f(alpha),g(alpha) have no bits >=29, so this is equivalent
    here to the original derivative equality modulo 2^32.
    Each carry transition's allowed 0/1 tuples form a singleton or a
    two-point affine line. Nothing is relaxed: both kinds are retained.
    """
    templates=[]
    for j in range(31):
        groups={}
        p=mask1>>j&1
        q=mask2>>j&1
        t=target>>j&1
        for carry in (-1,0,1):
            bynext=collections.defaultdict(list)
            for u in range(2) if p else (0,):
                for v in range(2) if q else (0,):
                    value=carry+u+op*v-t
                    if value%2==0:
                        bynext[value//2].append((u,v))
            branches=[]
            for nxt,pairs in sorted(bynext.items()):
                if len(pairs)==2:
                    assert p and q
                    assert pairs[0][0]^pairs[0][1]==pairs[1][0]^pairs[1][1]
                    constraints=[(rows1[j]^rows2[j],pairs[0][0]^pairs[0][1])]
                else:
                    assert len(pairs)==1
                    u,v=pairs[0]
                    constraints=[]
                    if p:constraints.append((rows1[j],u))
                    if q:constraints.append((rows2[j],v))
                branches.append((nxt,constraints))
            groups[carry]=branches
        templates.append(groups)
    return templates

def core_possible(k,cases,counters):
    a,b,c=cases
    fa,fb,fc=a[3],b[3],c[3]
    ga,gb,gc=a[4],b[4],c[4]
    D=k<<19
    # Exact unsigned-mask bound on ordinary output derivatives.
    if ga+gb<2*D or gb+gc<D:
        counters['output_width_cuts']+=1
        return False
    specs=[(fa,fb,fa-fb,-1,FR,FR,0,1),
           (fa,fc,fa+fc,+1,FR,FR,0,2),
           (gb,ga,gb-ga-2*D,-1,GR,GR,1,0),
           (gb,gc,gb+gc-D,+1,GR,GR,1,2)]
    eqs=[]
    for m1,m2,twiceT,op,r1,r2,i,j in specs:
        if twiceT&1:
            counters['parity_cuts']+=1
            return False
        eqs.append(equation_templates(m1,m2,(twiceT//2)&((1<<31)-1),op,
                                     [x<<(i*32) for x in r1],
                                     [x<<(j*32) for x in r2]))
    stack=[(0,(0,0,0,0),fixed_input_basis(cases))]
    while stack:
        step,cs,basis=stack.pop()
        counters['nodes']+=1
        if step==124:
            counters['satisfiable_leaves']+=1
            return True
        bit,which=divmod(step,4)
        for nxt,constraints in eqs[which][bit][cs[which]]:
            nb=basis.copy()
            if not all(insert(nb,row,rhs) for row,rhs in constraints):
                counters['linear_contradictions']+=1
                continue
            ncs=list(cs)
            ncs[which]=nxt
            stack.append((step+1,tuple(ncs),nb))
    counters['exhausted_triples']+=1
    return False

def recurrence_check():
    src=ROOT.parent/'supports-v2.json'
    supports=json.loads(src.read_text())['supports']
    # Explicit independently selected originals; each row is d_t - RHS = 0.
    expected={18:{'d18':1,'d11':-1},27:{'d20':-1,'d11':-1},
              34:{'d34':1,'d18':-1},20:{'d20':1,'G18':-1,'d13':-1},
              29:{'d29':1,'d13':-1},36:{'G34':-1,'d29':-1,'d20':-1},
              45:{'G43':-1,'d29':-1},50:{'d43':-1,'d34':-1},
              33:{'d26':-1,'F18':-1},42:{'d42':1,'d26':-1},
              49:{'d42':-1,'F34':-1},58:{'F43':-1,'d42':-1}}
    out={}
    for index,shift in ((12,0),(6,1),(7,3),(13,2)):
        support=set(supports[index])
        rows=[]
        for t,template in expected.items():
            tt=t+shift
            derived=collections.Counter()
            for name,i,coefficient in (('d',tt,1),('G',tt-2,-1),
                                      ('d',tt-7,-1),('F',tt-15,-1),
                                      ('d',tt-16,-1)):
                if i in support:derived[name+str(i)]+=coefficient
            derived={s:v for s,v in derived.items() if v}
            shifted={s[0]+str(int(s[1:])+shift):v for s,v in template.items()}
            assert derived==shifted,(index,tt,derived,shifted)
            rows.append({'t':tt,'row':derived})
        assert 18+shift in support and 34+shift in support and 43+shift in support
        out[str(index)]=rows
    return {'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'rows':out}

def run(ks):
    report={'schema':'support12-review-v4-independent-carry-exhaustion',
            'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'source_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
            'bridge_check':recurrence_check(),'results':[]}
    for k in ks:
        start=time.monotonic()
        cases=masks(k)
        counters=collections.Counter()
        ok=False
        witness=None
        for triple in itertools.product(cases,repeat=3):
            counters['triples']+=1
            if core_possible(k,triple,counters):
                ok=True
                witness=[list(t) for t in triple]
                break
        result={'k':k,'D':k<<19,'mask_count':len(cases),
                'mask_fibres_exhaustively_verified':8192,
                'counts':dict(counters),'core_satisfiable':ok,
                'satisfiable_masks':witness,'elapsed_seconds':time.monotonic()-start}
        report['results'].append(result)
        print(json.dumps(result),flush=True)
    report['all_unsat']=not any(r['core_satisfiable'] for r in report['results'])
    report['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    return report

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--k',type=int,nargs='+',default=list(range(1,8)))
    parser.add_argument('--out',type=pathlib.Path,default=ROOT/'INDEPENDENT_RUN.json')
    args=parser.parse_args()
    assert all(1<=k<=7 for k in args.k)
    args.out.write_text(json.dumps(run(args.k),indent=2)+'\n')
