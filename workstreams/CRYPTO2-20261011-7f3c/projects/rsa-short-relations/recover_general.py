"""Conditional extraction using supplied H and public inputs only.

The fixture's expected secret and linear witness are deliberately not read.
Uses Sympy for polynomial arithmetic/factorization; check.py uses integers.
"""
import argparse
import json
import math
from pathlib import Path
import sympy as sp

x,y,z=sp.symbols('x y z')


def recover(c):
    N,e=int(c['public']['N']),int(c['public']['e'])
    X,Y,m=int(c['X']),int(c['Y']),c['m']
    h=sp.Poly(sum(int(a)*x**i*y**j for i,j,a in c['terms']),x,y)
    assert all(0<=j<=i<=m for (i,j),a in h.terms())
    M=sum(abs(int(a))*X**i*Y**j for (i,j),a in h.terms())
    assert math.gcd(int(h.content()),e)==1 and 3**m*M<e**m and X*X*Y>=e
    # Multiplication by x^m clears all Laurent powers.
    transformed=sp.Poly(sp.expand(sum(a*x**(m+i-j)*(1+N*x-z)**j for (i,j),a in h.terms())),x,z)
    assert all(int(a)%e**max(m-j,0)==0 for (i,j),a in transformed.terms())
    A=sp.Poly(sum(a*y**j for (i,j),a in h.terms() if i==m),y)
    for B,multiplicity in sp.factor_list(A)[1]:
        if B.degree()!=1:
            continue
        r,t=map(int,B.all_coeffs())
        if r<0:r,t=-r,-t
        if 3*X*max(r*Y,abs(t))>=e or (r*N+t)%e:
            continue
        u=(r*N+t)//e;g=math.gcd(r,u)
        k,d=r//g,u//g
        if k<=0 or d<=0 or (e*d-1)%k:continue
        s=N-(e*d-1)//k;disc=(s+1)**2-4*N
        if disc<0:continue
        qdisc=math.isqrt(disc)
        if qdisc*qdisc!=disc or (s+1+qdisc)%2:continue
        p,q=(s+1+qdisc)//2,(s+1-qdisc)//2
        if p*q==N and p>q>1:
            return {a:str(b) for a,b in dict(k=k,d=d,p=p,q=q,s=s).items()}
    raise ValueError('No verified RSA recovery from the supplied relation')


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('certificate',type=Path)
    a=ap.parse_args()
    record=json.loads(a.certificate.read_text())
    print(json.dumps([dict(m=c['m'],recovered=recover(c)) for c in record['cases']],indent=2))
