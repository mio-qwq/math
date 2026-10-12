#!/usr/bin/env python3
"""Independent exact acceptance tests; no candidate checker is imported.

Rational tensor sums implement probability; rational weighted kernel operators
implement traces. Formal trace-word maps check dimension-independent identities.
Finite tests corroborate semantics, not the universal proof in REVIEW.md.
"""
from fractions import Fraction as Q
from itertools import product, combinations
from collections import Counter
from pathlib import Path
import hashlib
import json
import random
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
COUNTS = Counter()
NEGATIVE = []

def require(ok, tag):
    if not ok:
        raise AssertionError(tag)
    COUNTS[tag] += 1

def reject(tag, condition):
    require(not condition, 'negative_control')
    NEGATIVE.append(tag)

def transpose(a):
    return [list(x) for x in zip(*a)]

def matmul(a, b):
    n = len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(n))
             for j in range(n)] for i in range(n)]

def plus(a, b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def trace_word(*args):
    a = args[0]
    for b in args[1:]:
        a = matmul(a,b)
    return sum(a[i][i] for i in range(len(a)))

def operator(k, mu):
    # G=K diag(mu).  H=K^t diag(mu) is its weighted adjoint, NOT G^t.
    return [[Q(k[i][j])*mu[j] for j in range(len(mu))]
            for i in range(len(mu))]

def frob_kernel(a,b,mu):
    return sum(mu[i]*mu[j]*a[i][j]*b[i][j]
               for i in range(len(mu)) for j in range(len(mu)))

def weighted_composition(a,b,mu):
    return [[sum(a[i][k]*mu[k]*b[k][j] for k in range(len(mu)))
             for j in range(len(mu))] for i in range(len(mu))]

def moments(k,mu):
    g,h=operator(k,mu),operator(transpose(k),mu)
    return (trace_word(g,h,g,h),trace_word(g,g,g,g),
            trace_word(g,g,h,h),trace_word(g,g,g,h),
            trace_word(plus(g,h),plus(g,h),plus(g,h),plus(g,h)))

def tensor(k,mu,cycle=False):
    ans=Q(0)
    for a,b,c,d in product(range(len(mu)),repeat=4):
        w=mu[a]*mu[b]*mu[c]*mu[d]
        val=(k[a][b]*k[b][c]*k[c][d]*k[d][a] if cycle else
             k[a][b]*k[a][d]*k[c][b]*k[c][d])
        ans+=w*val
    return ans

def check_matrix(k,mu):
    t,l,y,x,r4=moments(k,mu)
    require(t==tensor(k,mu) and l==tensor(k,mu,True),'tensor_trace_binding')
    u=weighted_composition(k,transpose(k),mu)
    v=weighted_composition(transpose(k),k,mu)
    b=plus(weighted_composition(k,k,mu),
           weighted_composition(transpose(k),transpose(k),mu))
    d=plus(u,v)
    require(frob_kernel(u,u,mu)==t and frob_kernel(v,v,mu)==t
            and frob_kernel(u,v,mu)==y,'weighted_gram_UV')
    require(frob_kernel(b,d,mu)==4*x and
            frob_kernel(b,b,mu)==2*(y+l) and
            frob_kernel(d,d,mu)==2*(t+y),'weighted_gram_BD')
    require(r4==2*l+8*x+4*y+2*t,'R4_expansion')
    require(min(t,l,y,x)>=0 and y<=t,'positivity_Y_le_T')
    require(4*x*x<=(y+l)*(t+y),'Gram_Cauchy')
    require(2*x*x<=(t+l)**2,'simplified_Cauchy')
    require(x<=Q(177,250)*(t+l),'rational_X_bound')
    require(2*(t+l)>=Q(125,729)*r4,'rational_matrix_bound')
    mean=sum(mu[i]*mu[j]*k[i][j] for i in range(len(mu)) for j in range(len(mu)))
    require(t>=mean**4,'C4_mean_bound')
    return t,l,y,x,r4

def trace_key(word):
    # Trace is invariant under cyclic rotation and transposition/reversal.
    variants=[]
    for w in (word, tuple(1-i for i in reversed(word))):
        variants += [w[i:]+w[:i] for i in range(len(w))]
    return min(variants)

def word_map(words):
    out=Counter()
    for coef,w in words:
        out[trace_key(tuple(w))]+=coef
    return {w:c for w,c in out.items() if c}

def universal_trace_checks():
    rhs=[(2,(0,0,0,0)),(8,(0,0,0,1)),(4,(0,0,1,1)),(2,(0,1,0,1))]
    lhs=[(1,w) for w in product((0,1),repeat=4)]
    require(word_map(lhs)==word_map(rhs),'universal_trace_word_R4')
    bd=[(1,a+b) for a in ((0,0),(1,1)) for b in ((0,1),(1,0))]
    require(word_map(bd)==word_map([(4,(0,0,0,1))]),'universal_trace_word_BD')
    bb=[(1,a+b) for a in ((0,0),(1,1)) for b in ((0,0),(1,1))]
    require(word_map(bb)==word_map([(2,(0,0,1,1)),(2,(0,0,0,0))]),'universal_trace_word_BB')
    dd=[(1,a+b) for a in ((0,1),(1,0)) for b in ((0,1),(1,0))]
    require(word_map(dd)==word_map([(2,(0,1,0,1)),(2,(0,0,1,1))]),'universal_trace_word_DD')
    damaged=[(2,(0,0,0,0)),(4,(0,0,0,1)),(4,(0,0,1,1)),(2,(0,1,0,1))]
    reject('trace coefficient 8X changed to 4X',word_map(lhs)==word_map(damaged))
    # Algebraic identity for exact finite-sum Cauchy, checked by coefficients.
    for n in range(1,6):
        # The coefficients in (sum ui^2)(sum vi^2)-(sum ui vi)^2.
        lhs=Counter()
        rhs=Counter()
        for i,j in product(range(n),repeat=2):
            lhs[tuple(sorted((('u',i),('u',i),('v',j),('v',j))))]+=1
            lhs[tuple(sorted((('u',i),('v',i),('u',j),('v',j))))]-=1
        for i,j in combinations(range(n),2):
            rhs[tuple(sorted((('u',i),('u',i),('v',j),('v',j))))]+=1
            rhs[tuple(sorted((('u',j),('u',j),('v',i),('v',i))))]+=1
            rhs[tuple(sorted((('u',i),('v',j),('u',j),('v',i))))]-=2
        require({a:b for a,b in lhs.items() if b}=={a:b for a,b in rhs.items() if b},'Cauchy_square_identity')

def check_levels(ell,mu):
    n=len(mu)
    r=Counter()
    e=Q(0)
    contribution=Q(0)
    for a,b in product(range(n),repeat=2):
        r[tuple(sorted((ell[a][b],ell[b][a])))]+=mu[a]*mu[b]
    require(sum(r.values())==1,'six_class_mass_sum')
    patterns=Counter()
    for a,b,c,d in product(range(n),repeat=4):
        w=mu[a]*mu[b]*mu[c]*mu[d]
        empty=ell[a][b]==ell[c][d] and ell[b][c]==ell[d][a]
        if empty:
            e+=w
        pairs=((a,b),(a,d),(c,b),(c,d))
        classes=[tuple(sorted((ell[s][t],ell[t][s]))) for s,t in pairs]
        if all(z==classes[0] for z in classes):
            i,j=classes[0]
            bits=tuple(ell[s][t]==i for s,t in pairs)
            # The ordering makes the eligible masks 1111,0000,1001,0110.
            eligible=i==j or bits in ((1,1,1,1),(0,0,0,0),(1,0,0,1),(0,1,1,0))
            require(eligible==empty,'event_pattern_iff')
            if eligible:
                contribution+=w
                patterns[(i,j,bits)]+=w
    from_moments=Q(0)
    relaxed=Q(0)
    for i in range(3):
        k=[[int(ell[a][b]==i and ell[b][a]==i) for b in range(n)] for a in range(n)]
        t,l,y,x,r4=check_matrix(k,mu)
        from_moments+=t
        relaxed+=r[(i,i)]**4
    for i,j in combinations(range(3),2):
        k=[[int(ell[a][b]==i and ell[b][a]==j) for b in range(n)] for a in range(n)]
        t,l,y,x,r4=check_matrix(k,mu)
        kt=transpose(k)
        s=plus(k,kt)
        require(tensor(kt,mu)==t and tensor(kt,mu,True)==l,'transpose_T_L_equality')
        require(tensor(s,mu)==r4 and r4>=r[(i,j)]**4,'symmetric_union_binding')
        first=patterns[(i,j,(True,True,True,True))]
        second=patterns[(i,j,(False,False,False,False))]
        third=patterns[(i,j,(True,False,False,True))]
        fourth=patterns[(i,j,(False,True,True,False))]
        require((first,second,third,fourth)==(t,t,l,l),'four_disjoint_pattern_counts')
        from_moments+=2*(t+l)
        relaxed+=Q(125,729)*r[(i,j)]**4
    require(contribution==from_moments and e>=contribution>=relaxed>=Q(125,74088),'all_rational_empty_bounds')

def rational_certificate():
    require(Q(177,250)**2-Q(1,2)==Q(79,62500),'177_250_square')
    # kappa >= 125/729 iff sqrt(2) <= 1031/729.
    require(Q(1031,729)**2-Q(2)==Q(79,531441),'kappa_comparison')
    require(Q(2)/(6+8*Q(177,250))==Q(125,729),'matrix_constant')
    c=[Q(1)]*3+[Q(125,729)]*3
    t=[Q(5,42)]*3+[Q(3,14)]*3
    d=Q(125,74088)
    require(sum(t)==1 and all(ci*ti**3==d for ci,ti in zip(c,t)),'tangent_stationarity')
    require(sum(ci*ti**4 for ci,ti in zip(c,t))==d,'rational_minimizer')
    # Identity coefficients in x, t: x^4+3t^4-4xt^3.
    expected={(4,0):Q(1),(0,4):Q(3),(1,3):Q(-4)}
    actual=Counter()
    for ax,at,ca in ((2,0,1),(1,1,-2),(0,2,1)):
        for bx,bt,cb in ((2,0,1),(1,1,2),(0,2,3)):
            actual[(ax+bx,at+bt)]+=ca*cb
    require({a:b for a,b in actual.items() if b}==expected,'quartic_tangent_identity')
    require((1-d)/4==Q(73963,296352)<Q(182,729) and d>Q(1,729),'endpoint_comparisons')
    reject('larger rational mass lower bound 126/74088',sum(ci*ti**4 for ci,ti in zip(c,t))>=Q(126,74088))
    reject('arithmetic falsely upgrades derived coefficient to 1/4',Q(1,4)<=Q(2)/(6+8*Q(177,250)))

def strict_semantics():
    alphabet=range(2)
    words=list(product(alphabet,repeat=4))
    index={w:i for i,w in enumerate(words)}
    windows=[tuple(index[tuple(w[j:j+4])] for j in range(5)) for w in product(alphabet,repeat=8)]
    forbidden=set()
    for row in windows:
        for starts in combinations(range(5),3):
            forbidden.add(sum(1<<i for i in set(row[j] for j in starts)))
    strict=[]
    for mask in range(1<<16):
        if all(mask&bad!=bad for bad in forbidden):
            strict.append(mask)
    require(all(sum(bool(mask&(1<<i)) for i in row)<=2 for mask in strict for row in windows),'binary_strict_full_occurrence_check')
    for mask in strict:
        code=[w for i,w in enumerate(words) if mask&(1<<i)]
        pairs=list(product(alphabet,repeat=2))
        lev={p:0 for p in pairs}
        for _ in range(3):
            changed=False
            for w in code:
                a,b=w[:2],w[2:]
                if lev[b]<lev[a]+1:
                    lev[b]=lev[a]+1
                    changed=True
            if not changed:
                break
        require(max(lev.values())<=2 and all(lev[w[:2]]<lev[w[2:]] for w in code),'strict_canonical_pair_levels')
        for w in words:
            rots=[w[j:]+w[:j] for j in range(4)]
            hit=sum(z in code for z in rots)
            empty=lev[w[:2]]==lev[w[2:]] and lev[(w[1],w[2])]==lev[(w[3],w[0])]
            require(hit<=1-int(empty),'strict_rotation_pointwise')
        for mu in ((Q(1,2),Q(1,2)),(Q(1,3),Q(2,3)),(Q(0),Q(1))):
            p=sum(mu[w[0]]*mu[w[1]]*mu[w[2]]*mu[w[3]] for w in code)
            e=sum(mu[w[0]]*mu[w[1]]*mu[w[2]]*mu[w[3]] for w in words
                  if lev[w[:2]]==lev[w[2:]] and lev[(w[1],w[2])]==lev[(w[3],w[0])])
            require(4*p<=1-e and p<=Q(73963,296352),'strict_weighted_rotation_bridge')
    # A single period-two word is not strict: starts 0,2,4 count separately.
    w=(0,1,0,1,0,1,0,1)
    selected={(0,1,0,1)}
    row=[w[j:j+4] for j in range(5)]
    require(sum(z in selected for z in row)==3,'repeat_occurrence_witness')
    reject('replace occurrence count by distinct-word count',len({z for z in row if z in selected})>2)
    COUNTS['binary_strict_code_count']=len(strict)
    COUNTS['binary_forbidden_masks']=len(forbidden)
    # Repair theorem's symbolic union-bound coefficients.
    threshold={1:7,2:13,3:15}
    for a,b in ((1,1),(1,2),(1,3),(2,2)):
        first=max(a,b); second=min(a,b)
        require(4*first+first*(first-1)//2<=threshold[first] and
                (4+first)*second+second*(second-1)//2<=threshold[second],'repair_extension_table')
    require(3+2*sum(threshold.values())==73,'repair_loss_coefficient')
    reject('repair T3 incorrectly decreased to 14',4*3+3<=14)

def main():
    universal_trace_checks()
    rational_certificate()
    for bits in product((0,1),repeat=4):
        # With i=0,j=1, labels on reverse edges are complement bits.
        e=(bits[0]==bits[3] and bits[2]==bits[1])
        eligible=bits in ((1,1,1,1),(0,0,0,0),(1,0,0,1),(0,1,1,0))
        require(e==eligible,'sixteen_direction_truth_table')
    weights2=[(Q(1,2),Q(1,2)),(Q(1,3),Q(2,3)),(Q(0),Q(1)),(Q(9,25),Q(16,25))]
    for flat in product(range(3),repeat=4):
        ell=[list(flat[:2]),list(flat[2:])]
        for mu in weights2:
            check_levels(ell,mu)
    rng=random.Random(2026101301)
    for n,num in ((1,3),(3,60),(4,30)):
        for _ in range(num):
            ell=[[rng.randrange(3) for j in range(n)] for i in range(n)]
            integer=[rng.randrange(5) for i in range(n)]
            if sum(integer)==0:
                integer[0]=1
            mu=tuple(Q(x,sum(integer)) for x in integer)
            check_levels(ell,mu)
    # Non-indicator kernels, arbitrary zero weights, and non-symmetric operators.
    for n in range(1,6):
        for _ in range(30):
            k=[[Q(rng.randrange(5),rng.randrange(1,5)) for j in range(n)] for i in range(n)]
            integer=[rng.randrange(5) for i in range(n)]
            if sum(integer)==0:
                integer[0]=1
            mu=tuple(Q(x,sum(integer)) for x in integer)
            check_matrix(k,mu)
    mu=(Q(1,3),Q(2,3))
    k=[[0,1],[0,0]]
    g=operator(k,mu)
    reject('ordinary transpose of weighted KD used as adjoint',trace_word(g,transpose(g),g,transpose(g))==tensor(k,mu))
    cycle=[[int((j-i)%4==1) for j in range(4)] for i in range(4)]
    mu=(Q(1,4),)*4
    t,l,_,_,r4=check_matrix(cycle,mu)
    require(l>0,'directed_cycle_nonzero')
    reject('omit both alternating off-class patterns',2*(t+l)==2*t)
    reject('matrix coefficient incorrectly replaced by 1',2*(t+l)>=r4)
    check_matrix([[0]*3 for _ in range(3)],(Q(0),Q(0),Q(1)))
    negative_real=[[1,1],[-1,1]]
    require(trace_word(negative_real,negative_real,negative_real,negative_real)<0,'nonnegative_hypothesis_witness')
    strict_semantics()
    print('PASS: independent exact rational/tensor/trace review')
    print(json.dumps({'checks':dict(sorted(COUNTS.items())),'negative_controls':NEGATIVE},indent=2))
    print('Finite checks validate these instances; universal proof is independently reviewed in REVIEW.md.')

if __name__=='__main__':
    main()
