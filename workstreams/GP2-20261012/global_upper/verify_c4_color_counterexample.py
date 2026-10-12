#!/usr/bin/env python3
"""Exact rational checks for the generic pair-color counterexample."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json

N=3
I=[[F(int(i==j)) for j in range(N)] for i in range(N)]
P=[[F(int(j==(i+1)%N)) for j in range(N)] for i in range(N)]
A=[[F(1,3) for j in range(N)] for i in range(N)]
B=[[(I[i][j]-P[i][j])/9 for j in range(N)] for i in range(N)]
M=[[[A[i][j]/3+s*B[i][j] for j in range(N)] for i in range(N)] for s in (1,-1,0)]
K=[[[3*v for v in row] for row in m] for m in M]

def mul(X,Y):return [[sum(X[i][k]*Y[k][j] for k in range(N)) for j in range(N)]for i in range(N)]
def trace(X):return sum(X[i][i] for i in range(N))
def power(X,n):
    z=I
    for _ in range(n):z=mul(z,X)
    return z

def check_probabilities(L):
    assert all(0<=L[c][a][b]<=1 for c,a,b in product(range(3),repeat=3))
    assert all(sum(L[c][a][b]for c in range(3))==1 for a,b in product(range(3),repeat=2))

check_probabilities(K)
zero=[[F(0)]*N for _ in range(N)]
assert mul(A,A)==A and mul(A,B)==zero and mul(B,A)==zero
assert trace(power(B,4))==F(-1,729)
matrix_value=sum(trace(mul(mul(mul(M[i],M[j]),M[i]),M[j]))for i,j in product(range(3),repeat=2))
type_value=sum(K[i][a][b]*K[j][b][c]*K[i][c][d]*K[j][d][a]
               for a,b,c,d,i,j in product(range(3),repeat=6))/81
assert matrix_value==type_value==F(77,729)
assert matrix_value<F(1,9)
q=365
finite_bound=matrix_value+F(2,q)
assert finite_bound<F(1,9)

damaged=[[row[:]for row in x]for x in K];damaged[0][0][0]+=F(1,6)
try:check_probabilities(damaged)
except AssertionError:pass
else:raise AssertionError('damaged normalization accepted')
assert trace(power(B,4))!=F(1,729)
assert type_value!=F(1,9)

here=Path(__file__).resolve().parent
proof=here/'C4_DEFECT_AND_COLOR_COUNTEREXAMPLE.md'
report={'status':'exact rational checks passed',
        'color_probabilities':[[[str(v)for v in row]for row in m]for m in K],
        'trace_B4':str(trace(power(B,4))),
        'matrix_E':str(matrix_value),'independent_type_sum_E':str(type_value),
        'finite_q':q,'finite_alphabet_size':3*q,'expected_defect_upper':str(finite_bound),
        'negative_controls':['normalization','trace sign','false 1/9 value'],
        'proof_sha256':hashlib.sha256(proof.read_bytes()).hexdigest(),
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(here/'c4_color_counterexample_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
