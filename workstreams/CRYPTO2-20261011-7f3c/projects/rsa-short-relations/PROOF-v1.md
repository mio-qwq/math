# RSA common components: two route obstructions

CRYPTO2-20261011-7f3c, 2026-10-11 UTC. **Proof candidate; awaiting
independent review. No improved RSA attack or exponent is established.**

These results concern the actual polynomial used in small-private-exponent
RSA attacks. The first is a structural constraint on its auxiliary
polynomials; the second closes a deliberately specified, weak proof route.
Neither resolves Miller–Narayanan–Venkatesan Q2. Historical originality is
unconfirmed. The underlying valuation, resultant and lattice facts are
standard; their use here must not be sold as a new general technique.

## 1. Fixed object and recovery gap

Let e >= 2, N be integers, f=1+x(N-y), R=Z[x,y], and I=(e,f).
For RSA, N=pq, ed=1+k phi(N), and (k,s)=(k,N-phi(N)) is the
small root: f(k,s)=ed. We fix the phi(N) model, not an unspecified
lambda(N) convention. Balanced RSA and e of order N are used only for
the exponent comparison in section 4.

The full, established BD shift lattice at integers m>=1,t>=0 has generators

    e^(m-l) x^i f^l, 0<=l<=m, 0<=i<=m-l;
    e^(m-l) y^j f^l, 0<=l<=m, 1<=j<=t.

Every member lies in I^m and has x-degree at most m. With coefficient
weights X^i Y^j, the exact HG sufficient test is
`number_of_nonzero_terms * squared_norm < e^(2*m)`.
It implies vanishing at every modular root in the box |x|<=X,|y|<=Y.
Several linearly independent such polynomials can still have a common
curve. A shared curve can also contain efficiently recoverable integer
points. Thus neither a zero resultant nor a positive-dimensional ideal
alone refutes the RSA attack.

## 2. Factor inheritance at the degree limit

**Proposition A.** Let 0 != P in I^m satisfy deg_x(P)<=m and
gcd(content(P),e)=1, where content is the positive gcd of all integer
coefficients. Then deg_x(P)=m. For every integer factorization P=HG,

    H in I^(deg_x H),   G in I^(deg_x G).

No RSA balance, root, shortness, primality of e, irreducibility or lattice
reduction assumption is needed.

**Proof.** Invert x and replace y by N+(1-f)/x. This identifies
R[x^-1] with Z[x,x^-1,f]. Fix a prime p dividing e and put a=v_p(e).
For a nonzero Laurent polynomial C(x), v_p(C) is the minimum valuation
of its coefficients. For U=sum_j C_j(x) f^j, put

    w_p(U)=min_j (v_p(C_j)+a*j).

This weight is multiplicative. Indeed the terms of least weight form a
nonzero initial polynomial over F_p[x,x^-1] in two symbols of weights
1 and a. Products of these initial polynomials are nonzero because that
polynomial ring is a domain. It also obeys the usual minimum inequality
under addition. Consequently U in I^r implies w_p(U)>=a*r.

If U has at least one coefficient not divisible by p, write alpha=deg_x U.
The multiplicity of f in its reduction modulo p, even after inverting x,
is at most alpha. To see this, f has x-degree one and is coprime to x;
divisibility by f^j after localization is therefore divisibility before
localization. A nonzero polynomial of x-degree <=alpha cannot contain
f^(alpha+1). If j is this multiplicity, C_j is nonzero modulo p, so

    w_p(U) <= a*j <= a*alpha.                         (1)

Since the content of P is coprime to e, P,H,G are all nonzero modulo p.
Using x-degree additivity and weight multiplicativity,

    a*m <= w_p(P)=w_p(H)+w_p(G)
          <= a*(deg_x H+deg_x G)=a*deg_x P <= a*m.

All inequalities are equalities. In particular deg_x P=m and
w_p(H)=a*deg_x H for every p|e. If alpha=deg_x H, each Laurent
coefficient C_j of H is divisible by e^(alpha-j) whenever j<alpha.
This is exactly membership in (e,f)^alpha in the localized ring.

Finally localization loses no membership information: x is a unit in
R/I^alpha. For alpha>0, its inverse there is

    (y-N)*(1+f+...+f^(alpha-1)),

because x(y-N)=1-f and f^alpha=0 in that quotient. Thus I^alpha is
saturated with respect to powers of x. Contracting the localized
membership gives H in I^alpha. The same proof applies to G; alpha=0
is immediate. QED.

**Corollary A1 (direct projection obstruction).** For an integer
polynomial H define psi(H)=H(x,N+1/x). Under Proposition A,

    psi(H) belongs to e^(deg_x H) Z[x,x^-1].

For every factor with positive x-degree, clearing its Laurent denominator
and reducing modulo e therefore gives the zero polynomial. Factoring a
primitive-at-e relation cannot make this direct elimination provide a
nonzero modular equation. This is a method obstruction, not a root-recovery
impossibility theorem. Factors depending only on y are excluded from the
obstruction and can be solved as integer univariate polynomials.

**Corollary A2 (content defect).** Drop the coprime-content assumption.
Let c=content(P), d_x=deg_x P<=m, and P/c=product H_i^n_i be a
factorization into primitive integer factors. For every p|e, a=v_p(e),

    0 <= sum_i n_i*(a*deg_x H_i - w_p(H_i))
       = a*d_x - w_p(P/c) <= v_p(c)+a*(d_x-m) <= v_p(c).       (2)

This follows from the same multiplicativity and (1). For every primitive
divisor H of P/c of x-degree alpha, (2) gives

    psi(H) in [e^alpha/gcd(e^alpha,c)] Z[x,x^-1].               (3)

In particular, a projected factor can have a coefficient invertible
modulo e only if e^alpha divides c. This is necessary, not sufficient.

Both qualifications are essential. P=e(x-1) at m=1 has content e and
factor x-1 not in I. P=f(x-1) at m=1 is primitive, but has x-degree 2
and the same escaping factor. More generally e^r f^(m-r)(x^r-1), for
1<=r<=m, realizes the content cost e^r for an escaping degree-r factor.
These algebraic examples do not satisfy or refute a claimed HG norm bound.

## 3. The baseline projection identity, and its limit

For a primitive non-axis irreducible H let alpha=max i and
beta=max(j-i) over its monomials x^i y^j. Then beta>=0, since H is
not divisible by x. The polynomial

    R_H(x)=x^beta H(x,N+1/x)

has degree <=alpha+beta. Each term becomes
`h_ij x^(beta+i-j)(Nx+1)^j`. Since gcd(k,e)=1, H(k,s)=0 implies
R_H(k)=0 modulo e. If R_H is nonzero modulo e, has invertible leading
coefficient and degree D, the *existing* univariate Coppersmith theorem
can recover roots |k|<e^(1/D-epsilon). If e is prime, ordinary finite-field
factorization instead lists all residue roots, with no such size restriction;
the interval k<e then identifies integer candidates. Neither observation
is new cryptanalysis. Proposition A explains why the hoped-for nonzero
projection is automatically absent in an important part of this lattice.

## 4. A precisely limited count-and-volume route cannot exceed 1/4

The support is S(m,t)={(i,j):0<=i<=m,0<=j<=i+t}, of size

    D=(m+1)(m+2*t+2)/2.

The determinant of the weighted full BD basis is exactly
`e^A X^A Y^C`, where

    A=m(m+1)(2*m+3*t+4)/6,
    C=(m+1)*(m*m+3*m*t+2*m+3*t*(t+1))/6.

Indeed the x-shift leading monomial is x^(i+l)y^l and the y-shift
leading monomial is x^l y^(l+j), with coefficient +/-e^(m-l).
They biject with S; ordering by y-degree and then x-degree makes the
matrix triangular. Summing the exponents gives these formulas.

Consider only this proposed sufficient proof strategy:
(i) use the full determinant and the lower bound 1 on prefix integer
covolumes to bound the r-th LLL vector;
(ii) require enough independent short polynomials to force every common
non-axis irreducible factor to have alpha+beta<=3;
(iii) try the section 3 projection. Part (iii) has an additional obstruction
from section 2; even granting it, (i)-(ii) already fail beyond 1/4.

Newton-polytope additivity says the space of multiples HQ supported in S
has dimension at most

    D(m-alpha,t-beta),
    D(u,v)=sum_(i=0)^u max(i+v+1,0), with D(u,v)=0 for u<0.

For alpha>=1,beta>=0,alpha+beta>=4, the maximum is
B=D(m-1,t-3). For fixed alpha+beta, change variable l=i+t-beta:
the upper endpoint is m+t-alpha-beta and increasing alpha only removes
nonnegative summands at the lower endpoint. The maximum is attained at
alpha=1,beta=3. When m+t<4 it is zero. Thus this dimension-only strategy
requires r=B+1 short independent vectors.

An r-th-vector determinant guarantee of this specified kind has exponent
`(A*(1+delta)+C/2)/(D-r+1)` when e=N^(1+o(1)), X=N^delta,
Y=N^(1/2+o(1)). LLL constants and HG square-root factors only worsen it.
To certify shortness it needs

    A*(1+delta)+C/2 < m*(D-B).                        (4)

But at delta=1/4 the left side minus the right side is

    K=t*(m+1)*(-m+2*t+2)/8 + m*B >= 0.               (5)

Here is a proof for all m>=1,t>=0, not an inference from a finite scan.
For m+t<=3, B=0 and the displayed first term is nonnegative. Otherwise:

* t=0: K=m(m-3)(m-2)/2, for m>=4.
* t=1: writing m=u+3, 8K=4u^3+23u^2+41u+28.
* t=2: writing m=u+2, 4K=2u^3+9u^2+17u+20.
* t>=3: writing m=u+1,t=v+3,
  8K=4u^3+7u^2v+13u^2+2uv^2+27uv+35u+4v^2+34v+50.

Every coefficient is nonnegative. Since A>0, (4) is impossible for
delta>=1/4. This does **not** rule out sharper prefix-volume estimates,
structured sublattices, different norm arguments, direct arithmetic on a
common curve, or actual RSA key recovery. It closes only our specified
count-and-volume sufficient-criterion route.

## 5. Research decision after the first two routes

Stop treating either bare dimension counting or direct modular projection
of primitive-at-e factors as an independence proof. The next unresolved
step is to control common irreducible components using **both** the HG
height condition and the content/ideal-order allocation (2). No inequality
yet forces two independent integer equations or a recoverable low-degree
curve beyond Wiener. Generic discriminant-size estimates lose too much:
the basic y-degree-r estimate leaves a positive exponent proportional to
(1/2-delta)r(r-1), not the negative exponent needed for a contradiction.
That crude discriminant estimate is not an impossibility theorem. The
quadratic calculation below improves it by retaining the x-weights.

## 6. Exact recovery from a certified quadratic relation

This is a **conditional recovery theorem**, not an existence theorem for
the relation and not a new RSA exponent. The quadratic relation can itself
already encode an ordinary rational approximation.

**Proposition B.** Suppose positive coprime integers k,d and an integer s
satisfy f(k,s)=ed, 0<k<=X, |s|<=Y, where X,Y are positive integers.
Suppose H is a nonzero integer polynomial supported on S(2,0), H in I^2,
gcd(content(H),e)=1, and

    M(H)=sum |h_ij| X^i Y^j < e^2,
    X^2 Y >= e,     XY >= 3.                         (6)

Then k,d can be recovered from H,N,e,X,Y by integer arithmetic and gcds,
without a second relation, factoring e, or assuming algebraic independence.
For an RSA instance, verifying phi=(ed-1)/k then yields p,q by a quadratic
equation. The running time is polynomial in the supplied integers' bit
lengths. Finding H is expressly outside this theorem.

**Proof.** Write

    H=a x^2 y^2+B x^2 y+A x^2+E xy+D x+F.

For each p|e, H modulo p is a nonzero multiple of f^2. Its support forces
that multiple to be a nonzero constant. Thus gcd(a,e)=1 and a!=0.
Substituting y=N+(1-z)/x, ideal membership gives

    e | (2aN+B),    e | (2a+E),
    e^2 | (aN^2+BN+A),
    e^2 | [N(2a+E)+B+D],    e^2 | (a+E+F).

The last quantity has absolute value <=M(H)<e^2, so a+E+F=0.
Moreover Delta=B^2-4aA is divisible by e^2. Put
U=|B|X^2Y, V=|a|X^2Y^2, W=|A|X^2. Then

    |Delta| X^4Y^2 <= U^2+4VW <= (U+V+W)^2 < e^4.

By X^2Y>=e, |Delta|<e^2 and hence Delta=0. Express the integral binary
quadratic form as

    a=σ r^2,   B=2σ rt,   A=σ t^2,

where r>0, gcd(r,t)=1 and σ is a nonzero integer. This representation is
obtained by reducing t/r=B/(2a); its integrality follows from
B^2=4aA (or the primitive-square Gauss lemma). Since gcd(a,e)=1, both
σ and r are coprime to e. The divisibility of aN^2+BN+A then implies
e | (rN+t), including when e has prime-power factors. Set u=(rN+t)/e
and L=x(ry+t)-r=eux-rf. Thus L in I.

The displayed divisibilities and a+E+F=0 now give the exact decomposition

    H=σ L^2 + e J,
    J=b xy+c x-b in I,
    b=(E+2a)/e,    c=(D+B)/e.

To prove J vanishes at the desired root, its shortness must be checked;
dividing an equation by a vanishing factor would not suffice. Let M_high
be the three x-degree-2 terms' contribution to M(H), and M_low the rest.
The contribution of σL^2 below x-degree 2 is

    T=|σ|[2r^2 XY+2|rt|X+r^2],
    M_high=|σ|X^2(rY+|t|)^2.

Writing z=X(Y+|t|/r)>=XY>=3 gives T<=M_high because 2z+1<=z^2.
Consequently e M(J)<=M_low+T<=M(H)<e^2. At (k,s), H is divisible
by e^2 and J by e, whereas their absolute values are strictly smaller
than these moduli. Thus H(k,s)=J(k,s)=0, and H=σL^2+eJ gives L(k,s)=0.
Using f(k,s)=ed, this says uk=rd. Positivity and gcd(k,d)=1 yield

    k=r/gcd(r,u),    d=u/gcd(r,u).

All quantities on the right are computed from the public inputs and H.
This proves the claim. In fact J is a rational multiple of L, so the
relation H is reducible over Q whenever the stipulated RSA root exists.
QED.

For the usual e comparable with N and Y comparable with sqrt(N), the
condition X^2Y>=e covers the exponent regime X=N^delta with delta>1/4
for sufficiently large N. This does **not** guarantee H in that regime.
The original m=2,t=0 determinant condition does not provide it. The theorem
therefore closes the irreducible quadratic case of this proposed route,
without extending Wiener's guaranteed attack range.

The saved quadratic fixture is deliberately constructed using the disclosed
test secret key, as H=L(L+e), to test every hypothesis and recovery step.
It is not an experiment finding such a relation for an unknown key.
The degree-three question led to the separate GENERAL-PROOF-v1.md:
retaining weighted Mahler measure yields a result for every degree with
a stronger explicit norm margin. The next unresolved boundary is positive
y-shift support, not an unchecked assertion that this exact quadratic
bound extends unchanged to higher degree.
