"""Small independent exact checks; no imports from discoverer artifacts."""
from itertools import product, combinations
from random import Random
import json

class Field:
    def __init__(self, degree, modulus):
        self.q = 1 << degree
        self.modulus = modulus
    def mul(self, a, b):
        s = 0
        while b:
            if b & 1: s ^= a
            a <<= 1
            if a & self.q: a ^= self.modulus
            b >>= 1
        return s
    def inv(self, a):
        assert a
        for b in range(1, self.q):
            if self.mul(a,b) == 1: return b
        raise AssertionError('not a field')
    def dot(self, x, y):
        s = 0
        for a,b in zip(x,y): s ^= self.mul(a,b)
        return s

def rref(A, F):
    A = [r[:] for r in A]
    piv=[]
    row=0
    for col in range(len(A[0])):
        hit=next((i for i in range(row,len(A)) if A[i][col]),None)
        if hit is None: continue
        A[row],A[hit]=A[hit],A[row]
        t=F.inv(A[row][col]); A[row]=[F.mul(t,x) for x in A[row]]
        for i in range(len(A)):
            if i != row and A[i][col]:
                t=A[i][col]
                A[i]=[x ^ F.mul(t,y) for x,y in zip(A[i],A[row])]
        piv.append(col); row+=1
        if row==len(A): break
    return A,piv

def kernel(A,F):
    R,p=rref(A,F); n=len(A[0])
    free=next((j for j in range(n) if j not in p),None)
    if free is None: return None
    x=[0]*n; x[free]=1
    for i,j in enumerate(p): x[j]=R[i][free]
    return x

def solve(A,b,F):
    R,p=rref([row+[z] for row,z in zip(A,b)],F)
    assert p==list(range(len(A)))
    return [row[-1] for row in R]

def mv(A,u,F): return [F.dot(r,u) for r in A]
def sub(A,I,J): return [[A[i][j] for j in J] for i in I]
def rel(u,v): return all(x==0 or y==0 or x==y for x,y in zip(u,v))
def valid(A,u,v,F):
    assert any(u) and any(v) and u!=v
    p,q=mv(A,u,F),mv(A,v,F)
    assert any(p) and any(q) and p!=q
    assert rel(u,v) and rel(p,q)

def non_mds(A,F):
    n=len(A)
    for r in range(1,n):
        for I in combinations(range(n),r):
            for J in combinations(range(n),r):
                x=kernel(sub(A,I,J),F)
                if x is None: continue
                Ic=[i for i in range(n) if i not in I]
                Jc=[j for j in range(n) if j not in J]
                u=[0]*n
                for j,z in zip(J,x): u[j]=z
                D=sub(A,Ic,Jc); y=kernel(D,F)
                if y is None: y=solve(D,[mv(A,u,F)[i] for i in Ic],F)
                v=[0]*n
                for j,z in zip(Jc,y): v[j]=z
                valid(A,u,v,F)
                return u,v
    return None

def symmetric(A,F):
    assert all(A[i][j]==A[j][i] for i in range(len(A)) for j in range(len(A)))
    fallback=non_mds(A,F)
    if fallback is not None: return fallback
    n=len(A); k=n//2; L=list(range(k)); R=list(range(k+1,n))
    x=solve(sub(A,R,L),[A[i][k] for i in R],F)
    y=solve(sub(A,L,R),[A[i][k] for i in L],F)
    u=x+[1]+[0]*k; v=[0]*k+[1]+y
    valid(A,u,v,F); return u,v

def circ(a):
    n=len(a); return [[a[(j-i)%n] for j in range(n)] for i in range(n)]

def witness(a,F):
    n=len(a); A=circ(a)
    assert kernel(A,F) is None
    if n%2:
        S=[A[(-i)%n][:] for i in range(n)]
        u,v=symmetric(S,F)
    elif n==4:
        a,b,c,d=a
        if (a or c) and (b or d): u,v=[a,0,c,0],[0,d,0,b]
        else: u,v=[1,0,0,0],[0,1,0,0]
    else:
        d=4 if n%4==0 else n//2
        b=[0]*d
        for j,z in enumerate(a): b[j%d]^=z
        small=circ(b)
        assert kernel(small,F) is None
        u0,v0=witness(b,F)
        u=[u0[i%d] for i in range(n)]
        v=[v0[i%d] for i in range(n)]
        for j in range(d):
            e=[int(i%d==j) for i in range(n)]
            assert mv(A,e,F)==[small[i%d][j] for i in range(n)]
    valid(A,u,v,F)
    return u,v

F4=Field(2,0b111); F16=Field(4,0b10011)
report={'method':'Independent exact GF(4)/GF(16) arithmetic; no discoverer code imports','exhaustive_small':{},'sampled':{}}
for n in (3,4):
    count=0
    for a in product(range(4),repeat=n):
        if kernel(circ(a),F4) is None:
            witness(a,F4); count+=1
    report['exhaustive_small'][str(n)]={'all_coefficients':4**n,'invertible_passed':count}
rng=Random(721938)
for n in (6,8,10,14):
    count=0
    while count<24:
        a=[rng.randrange(4) for _ in range(n)]
        if kernel(circ(a),F4) is not None: continue
        witness(a,F4); count+=1
    report['sampled'][str(n)]={'invertible_passed':count}
report['symmetric_mds_GF16']={}
for n in (3,5):
    A=[[F16.inv(8^i^j) for j in range(n)] for i in range(n)]
    assert kernel(A,F16) is None
    assert non_mds(A,F16) is None
    u,v=symmetric(A,F16)
    report['symmetric_mds_GF16'][str(n)]={'u':u,'v':v,'passed':True}
print(json.dumps(report,indent=2))
