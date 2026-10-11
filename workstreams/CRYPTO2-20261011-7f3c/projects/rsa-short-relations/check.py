"""Definition-based integer checker; imports no discovery code or CAS.

Finite regression and certificates support, but do not replace, PROOF-v1.md.
No claim of an independent human review or verification of FLINT's LLL routine.
"""
import copy
import json
import math
from functools import lru_cache
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(*polys):
    out = {}
    for p in polys:
        for mon, c in p.items():
            out[mon] = out.get(mon, 0)+c
    return {k:v for k,v in out.items() if v}


def mul(p, q):
    out = {}
    for (i,j),a in p.items():
        for (k,l),b in q.items():
            mon=(i+k,j+l)
            out[mon]=out.get(mon,0)+a*b
    return {k:v for k,v in out.items() if v}


def power(p,n):
    out={(0,0):1}
    for _ in range(n):
        out=mul(out,p)
    return out


def scale(p,c,i=0,j=0):
    return {(a+i,b+j):c*v for (a,b),v in p.items() if c*v}


def terms(row):
    out={}
    for i,j,c in row['terms']:
        need((i,j) not in out and i>=0 and j>=0,'invalid or duplicate monomial')
        out[i,j]=int(c)
    need(out and all(out.values()),'zero coefficients must be omitted')
    return out


def evaluate(p,x,y):
    return sum(c*x**i*y**j for (i,j),c in p.items())


def f_coordinates(p,N):
    # y=(1+Nx-z)/x; second coordinate now denotes z=f, not y.
    base={(0,0):1,(1,0):N,(0,1):-1}
    return add(*(scale(power(base,j),c,i-j) for (i,j),c in p.items()))


def member(p,e,N,m):
    return all(c % e**max(m-j,0)==0 for (i,j),c in f_coordinates(p,N).items())


def projection(p,N):
    out={i:c for (i,j),c in f_coordinates(p,N).items() if j==0}
    return out


def content(p):
    return math.gcd(*p.values())


def degree_x(p):
    return max(i for i,j in p)


def det(a):
    # Exact Bareiss elimination, independent of FLINT.
    a=[r[:] for r in a]
    prev,sign=1,1
    for k in range(len(a)-1):
        if a[k][k]==0:
            j=next((j for j in range(k+1,len(a)) if a[j][k]),None)
            if j is None:
                return 0
            a[k],a[j]=a[j],a[k]
            sign=-sign
        pivot=a[k][k]
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                num=a[i][j]*pivot-a[i][k]*a[k][j]
                need(num%prev==0,'Bareiss exact division')
                a[i][j]=num//prev
            a[i][k]=0
        prev=pivot
    return sign*a[-1][-1]


@lru_cache(None)
def prime(n):
    # The saved fixtures have 48-bit or smaller primes. Trial division is
    # a deterministic proof here; no probable-prime oracle is used.
    need(n.bit_length()<=48,'fixture exceeds intended trial-division budget')
    return n>=2 and (n==2 or n%2 and all(n%d for d in range(3,math.isqrt(n)+1,2)))


def check_record(r):
    p,q,N,e,d,k,s,X,Y=(int(r['key'][v]) for v in ('p','q','N','e','d','k','s','X','Y'))
    need(prime(p) and prime(q) and q<p<2*q,'balanced distinct primes')
    need(N==p*q and s==p+q-1,'RSA modulus and phi deficit')
    need(e*d==1+k*(p-1)*(q-1) and 1<e<(p-1)*(q-1),'RSA equation')
    need(0<k<X and 0<s<Y,'root bounds')
    m,t=r['parameters']['m'],r['parameters']['t']
    f={(0,0):1,(1,0):N,(1,1):-1}
    basis=[scale(power(f,l),e**(m-l),i) for l in range(m+1) for i in range(m-l+1)]
    basis += [scale(power(f,l),e**(m-l),0,j) for j in range(1,t+1) for l in range(m+1)]
    support=[(i,j) for i in range(m+1) for j in range(i+t+1)]
    need(len(basis)==len(support)==r['dimension'],'dimension')
    T=[[int(c) for c in row] for row in r['transform']]
    need(len(T)==len(basis) and all(len(z)==len(basis) for z in T),'transform shape')
    need(abs(det(T))==1,'unimodular transform')
    need(len(r['rows'])==len(basis),'row count')
    good=[]
    vanishing=0
    for i,row in enumerate(r['rows']):
        g=terms(row)
        rebuilt=add(*(scale(b,c) for b,c in zip(basis,T[i])))
        need(g==rebuilt,'row differs from exact generator combination')
        need(set(g)<=set(support) and member(g,e,N,m),'support and ideal membership')
        norm2=sum((c*X**a*Y**b)**2 for (a,b),c in g.items())
        hg=len(g)*norm2<e**(2*m)
        zero=evaluate(g,k,s)==0
        need(row['index']==i and row['hg']==hg and row['vanishes']==zero,'row assertions')
        need(not hg or zero,'HG implication')
        vanishing+=zero
        if hg:
            good.append(g)
    need(len(good)==r['certified_short'] and vanishing==r['vanishing'],'counts')
    for fr in r['common_factors']:
        h=terms(fr)
        need(content(h)==1 and evaluate(h,k,s)==0,'primitive factor and root')
        proj=projection(h,N)
        beta=max(j-i for i,j in h)
        need(beta==fr['beta'] and max(proj)+beta==fr['projection_degree'],'projection degree')
        need(all(c%e==0 for c in proj.values())==fr['projection_zero_mod_e'],'projection assertion')
        # Saved control factor is a*x*y+b*x-a. Divide by it with x-degree
        # descending, using exact integer coefficients and lexicographic LT.
        for g in good:
            rem=g.copy()
            lt=max(h);lc=h[lt]
            while rem:
                top=max(rem)
                need(top[0]>=lt[0] and top[1]>=lt[1] and rem[top]%lc==0,'factor division')
                c=rem[top]//lc
                rem=add(rem,scale(h,-c,top[0]-lt[0],top[1]-lt[1]))
        for g in good:
            c=content(g);alpha=degree_x(h)
            guaranteed=e**alpha//math.gcd(e**alpha,c)
            need(all(z%guaranteed==0 for z in proj.values()),'content-defect projection divisibility')
        if set(h)=={(1,1),(1,0),(0,0)} and h[0,0]==-h[1,1]:
            a,b=h[1,1],h[1,0]
            need((a*N+b)%e==0,'bilinear recovery numerator')
            u=(a*N+b)//e
            divisor=math.gcd(a,u)
            need((a//divisor,u//divisor)==(k,d),'recover k,d from common curve')
    return dict(dimension=len(basis),hg=len(good),vanishing=vanishing)


def check_algebra():
    cases=0
    for e in (2,4,6,9,12,25):
        for N in (0,7):
            f={(0,0):1,(1,0):N,(1,1):-1}
            h=add(f,{(1,0):e})
            g=add(power(f,2),scale(f,e,1),{(0,1):e*e,(0,0):e*e})
            p=mul(h,g)
            need(math.gcd(content(p),e)==1 and degree_x(p)==3 and member(p,e,N,3),'inheritance premises')
            for factor in (h,g):
                alpha=degree_x(factor)
                need(member(factor,e,N,alpha),'inherited ideal membership')
                need(all(c%e**alpha==0 for c in projection(factor,N).values()),'inherited projection')
            # Sharp algebraic escape via content, and a missing degree bound.
            bad={(1,0):1,(0,0):-1}
            need(not member(bad,e,N,1),'escaping factor')
            need(member(scale(bad,e),e,N,1),'content counterexample premise')
            need(member(mul(f,bad),e,N,1),'degree counterexample premise')
            cases+=1
    return cases


def check_counts():
    count=0
    for m in range(1,61):
        for t in range(61):
            support=[(i,j) for i in range(m+1) for j in range(i+t+1)]
            D=len(support)
            A=sum((m-l)*(m-l+1+t) for l in range(m+1))
            C=sum(j for i,j in support)
            need(6*A==m*(m+1)*(2*m+3*t+4),'A formula')
            need(sum(i for i,j in support)==A,'x scaling exponent')
            need(6*C==(m+1)*(m*m+3*m*t+2*m+3*t*(t+1)),'C formula')
            B=sum(max(i+t-2,0) for i in range(m))
            K4=5*A+2*C-4*m*(D-B)
            need(K4>=0,'limited count-volume criterion must fail at 1/4')
            need(2*K4==t*(m+1)*(-m+2*t+2)+8*m*B,'K identity')
            count+=1
    return count


def recover_quadratic(N,e,h,X,Y):
    """Uses no secret key or fixture construction; verifies all conditions."""
    support={(i,j) for i in range(3) for j in range(i+1)}
    need(set(h)<=support and X>0 and Y>0,'quadratic support and bounds')
    need(member(h,e,N,2) and math.gcd(content(h),e)==1,'quadratic ideal/content')
    M=sum(abs(c)*X**i*Y**j for (i,j),c in h.items())
    need(M<e*e and X*X*Y>=e and X*Y>=3,'quadratic size assumptions')
    a,B,A,E,D,F=(h.get(ij,0) for ij in ((2,2),(2,1),(2,0),(1,1),(1,0),(0,0)))
    need(a!=0 and math.gcd(a,e)==1 and B*B==4*a*A,'forced discriminant')
    v=math.gcd(2*a,B)
    r=abs(2*a)//v;t=B*(1 if a>0 else -1)//v
    need(a%(r*r)==0,'integral primitive square')
    sigma=a//(r*r)
    need((sigma*r*r,2*sigma*r*t,sigma*t*t)==(a,B,A),'square reconstruction')
    need((r*N+t)%e==0,'linear modular relation')
    u=(r*N+t)//e
    L={(1,1):r,(1,0):t,(0,0):-r}
    residual=add(h,scale(power(L,2),-sigma))
    need(all(c%e==0 for c in residual.values()),'residual divisible by e')
    J={mon:c//e for mon,c in residual.items()}
    need(member(J,e,N,1),'residual ideal membership')
    need(sum(abs(c)*X**i*Y**j for (i,j),c in J.items())<e,'residual strict shortness')
    need(u>0,'positive candidate private exponent')
    common=math.gcd(r,u)
    k,d=r//common,u//common
    need((e*d-1)%k==0,'recovered phi is integral')
    phi=(e*d-1)//k;s=N-phi
    delta=(s+1)**2-4*N
    need(delta>=0,'factor discriminant nonnegative')
    root=math.isqrt(delta)
    need(root*root==delta and (s+1+root)%2==0,'factor discriminant square')
    p,q=(s+1+root)//2,(s+1-root)//2
    need(p*q==N and p>q>1 and 0<k<=X and abs(s)<=Y,'recovered RSA factors and box')
    need(evaluate(h,k,s)==evaluate(J,k,s)==evaluate(L,k,s)==0,'exact root implications')
    return dict(p=p,q=q,k=k,d=d,s=s)


def check_general(c):
    h=terms(c);m=c['m'];X,Y=int(c['X']),int(c['Y'])
    N,e=int(c['public']['N']),int(c['public']['e'])
    need(set(h)<={(i,j) for i in range(m+1) for j in range(i+1)},'general support')
    need(math.gcd(content(h),e)==1 and member(h,e,N,m),'general ideal/content')
    M=sum(abs(a)*X**i*Y**j for (i,j),a in h.items())
    need(3**m*M<e**m and X*X*Y>=e,'general norm and box')
    r,t=map(int,c['linear_witness'])
    need(r>0 and math.gcd(r,t)==1 and (r*N+t)%e==0,'general linear factor normalization')
    need(3*X*max(r*Y,abs(t))<e,'general linear witness bound')
    A=[h.get((m,j),0) for j in range(m+1)]
    for j in range(m,0,-1):
        need(A[j]%r==0,'leading-row factor exact division')
        q=A[j]//r;A[j]=0;A[j-1]-=q*t
    need(A[0]==0,'linear witness divides leading row')
    L={(1,1):r,(1,0):t,(0,0):-r}
    need(member(L,e,N,1) and sum(abs(a)*X**i*Y**j for (i,j),a in L.items())<e,'lift norm')
    u=(r*N+t)//e;divisor=math.gcd(r,u)
    k,d=r//divisor,u//divisor
    expected={a:int(b) for a,b in c['expected'].items()}
    p,q,s=(expected[a] for a in ('p','q','s'))
    need(prime(p) and prime(q) and p*q==N,'general fixture primes')
    need((k,d)==(expected['k'],expected['d']) and e*d==1+k*(p-1)*(q-1),'general recovery')
    need(0<k<=X and abs(s)<=Y and s==p+q-1,'general recovered box')
    need(evaluate(h,k,s)==evaluate(L,k,s)==0,'general exact root')
    return m


if __name__=='__main__':
    base=Path(__file__).resolve().parent
    records={p.name:json.loads(p.read_text()) for p in sorted((base/'evidence').glob('*.json'))}
    results={name:check_record(r) for name,r in records.items()}
    negative=0
    base_record=records['control-96-m2-t0.json']
    mutators=[
        lambda r:r['rows'][0]['terms'][0].__setitem__(2,str(int(r['rows'][0]['terms'][0][2])+1)),
        lambda r:r['transform'][0].__setitem__(0,str(int(r['transform'][0][0])+1)),
        lambda r:r.__setitem__('certified_short',r['certified_short']+1),
        lambda r:r['key'].__setitem__('s',str(int(r['key']['s'])+1)),
        lambda r:r['common_factors'][0].__setitem__('projection_zero_mod_e',False),
        lambda r:r['common_factors'][0].__setitem__('projection_degree',2),
    ]
    for change in mutators:
        damaged=copy.deepcopy(base_record);change(damaged)
        try:
            check_record(damaged)
        except ValueError:
            negative+=1
        else:
            raise AssertionError('damaged certificate accepted')
    qc=json.loads((base/'evidence/quadratic/synthetic.json').read_text())
    h=terms(qc);N,e=int(qc['public']['N']),int(qc['public']['e'])
    X,Y=int(qc['X']),int(qc['Y'])
    expected={k:int(v) for k,v in qc['expected'].items()}
    need(recover_quadratic(N,e,h,X,Y)==expected,'quadratic recovery')
    need(recover_quadratic(N,e,scale(h,-1),X,Y)==expected,'signed quadratic recovery')
    for hh,xx,yy in ((scale(h,e),X,Y),(add(h,{(0,0):1}),X,Y),(h,1,1),(h,X*e,Y)):
        try:
            recover_quadratic(N,e,hh,xx,yy)
        except ValueError:
            negative+=1
        else:
            raise AssertionError('invalid quadratic input accepted')
    gc=json.loads((base/'evidence/general/synthetic.json').read_text())
    general=[check_general(c) for c in gc['cases']]
    for c in gc['cases']:
        damaged=copy.deepcopy(c)
        damaged['linear_witness'][1]=str(int(damaged['linear_witness'][1])+1)
        try:
            check_general(damaged)
        except ValueError:
            negative+=1
        else:
            raise AssertionError('damaged general witness accepted')
    print(json.dumps(dict(result='PASS',fixtures=results,algebra_cases=check_algebra(),
                          count_regressions=check_counts(),quadratic_recovery='PASS (both signs)',
                          general_recovery_degrees=general,negative_controls=negative),indent=2))
