"""Small, exact diagnostic of the established full BD shift lattice.

This is discovery code, not an independent checker or a new attack.
Dependencies are isolated outside the repository; no shared requirements changed.
"""
import argparse
import json
import math
import time
from pathlib import Path

import sympy as sp
from flint import fmpz_mat

x, y = sp.symbols('x y')


def project(poly, N):
    """Clear exactly the negative Laurent powers after y=N+1/x."""
    p = sp.Poly(poly, x, y)
    beta = max(j-i for (i, j), c in p.terms())
    out = 0
    for (i, j), c in p.terms():
        out += c*x**(beta+i-j)*(N*x+1)**j
    return sp.Poly(sp.expand(out), x), beta


def run(bits, m, t, num, den, factor=True):
    # Reproducible test keys, not an RSA key-generation recommendation.
    p = int(sp.nextprime(2**(bits//2-1) + 2**(bits//2-3) + 101))
    q = int(sp.nextprime(2**(bits//2-1) + 2**(bits//2-4) + 1009))
    N, phi = p*q, (p-1)*(q-1)
    d = int(sp.integer_nthroot(N**num, den)[0]) | 1
    while math.gcd(d, phi) != 1:
        d += 2
    e = pow(d, -1, phi)
    k, s = (e*d-1)//phi, N-phi
    X = int(sp.integer_nthroot(N**num, den)[0])+3
    Y = 3*(math.isqrt(N)+1)
    assert k < X and s < Y and e*d == 1+k*(N-s)
    f = 1+x*(N-y)
    shifts = [sp.Poly(x**i*f**ell*e**(m-ell), x, y)
              for ell in range(m+1) for i in range(m-ell+1)]
    shifts += [sp.Poly(y**j*f**ell*e**(m-ell), x, y)
               for j in range(1, t+1) for ell in range(m+1)]
    support = [(i,j) for i in range(m+1) for j in range(i+t+1)]
    weights = [X**i*Y**j for i,j in support]
    rows = [[int(g.coeff_monomial(x**i*y**j))*w
             for (i,j),w in zip(support,weights)] for g in shifts]
    B = fmpz_mat(rows)
    print(json.dumps(dict(stage='basis-built', dimension=len(support))), flush=True)
    tick = time.monotonic()
    L, T = B.lll(transform=True, delta=0.99, eta=0.51)
    assert T*B == L and abs(int(T.det())) == 1
    print(json.dumps(dict(stage='lll-and-transform-checked',seconds=time.monotonic()-tick)),flush=True)
    records, good = [], []
    for idx in range(L.nrows()):
        row = [int(L[idx,j]) for j in range(L.ncols())]
        assert all(a % w == 0 for a,w in zip(row,weights))
        coeff = [a//w for a,w in zip(row,weights)]
        g = sp.Poly(sum(a*x**i*y**j for a,(i,j) in zip(coeff,support)), x,y)
        norm2, width = sum(a*a for a in row), sum(a!=0 for a in row)
        hg = width*norm2 < e**(2*m)
        vanishes = int(g.eval({x:k,y:s})) == 0
        assert not hg or vanishes
        if hg:
            good.append(g)
        records.append(dict(index=idx,hg=hg,vanishes=vanishes,
                            terms=[[i,j,str(a)] for (i,j),a in g.terms()]))
    common = good[0] if good else sp.Poly(0,x,y)
    print(json.dumps(dict(stage='norms-checked',certified_short=len(good))),flush=True)
    if factor:
        for g in good[1:]:
            common = sp.gcd(common,g)
    factors = []
    if good and factor:
        for h,multiplicity in sp.factor_list(common)[1]:
            R,beta = project(h,N)
            factors.append(dict(terms=[[i,j,str(a)] for (i,j),a in h.terms()],
                                multiplicity=multiplicity,
                                at_root=str(h.eval({x:k,y:s})),
                                beta=beta,projection_degree=int(R.degree()),
                                projection_zero_mod_e=all(int(c)%e==0 for c in R.all_coeffs())))
    return dict(schema='rsa-bd-diagnostic-v1', parameters=dict(bits=bits,m=m,t=t,num=num,den=den),
                key={a:str(b) for a,b in dict(p=p,q=q,N=N,e=e,d=d,k=k,s=s,X=X,Y=Y).items()},
                dimension=len(support),seconds=time.monotonic()-tick,
                certified_short=len(good),vanishing=sum(z['vanishes'] for z in records),
                common_factors=factors,factorization_checked=factor,rows=records,
                transform=[[str(T[i,j]) for j in range(T.ncols())] for i in range(T.nrows())])


if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--bits',type=int,default=96)
    ap.add_argument('--m',type=int,default=4)
    ap.add_argument('--t',type=int,default=2)
    ap.add_argument('--num',type=int,default=13)
    ap.add_argument('--den',type=int,default=50)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--skip-factor',action='store_true')
    a=ap.parse_args()
    result=run(a.bits,a.m,a.t,a.num,a.den,not a.skip_factor)
    elapsed=result.pop('seconds')
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(stage='certificate-written',elapsed_seconds=elapsed)),flush=True)
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','transform','key')},indent=2))
