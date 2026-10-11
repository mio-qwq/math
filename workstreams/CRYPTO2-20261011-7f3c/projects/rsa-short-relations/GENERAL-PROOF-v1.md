# From one sufficiently short x-shift relation to a linear RSA relation

Proof candidate, CRYPTO2-20261011-7f3c, 2026-10-11 UTC.
**Awaiting independent review; historical originality unconfirmed.**
This extends the quadratic calculation in PROOF-v1.md to every degree,
with a stronger, explicit norm margin. It concerns the t=0 support only.
It does not prove an improved attack exponent, the existence of the input
relation, or recovery for the actual BD families with positive y shifts.

## Statement

Let e>=2, N be integers, f=1+x(N-y), I=(e,f). Let X,Y be positive integers
with X^2 Y>=e. Suppose positive coprime integers k,d and an integer s obey

    f(k,s)=ed,    0<k<=X,    |s|<=Y.

For m>=1 suppose a supplied nonzero H in Z[x,y] satisfies

1. support(H) is contained in S(m,0)={(i,j):0<=j<=i<=m};
2. H belongs to I^m;
3. gcd(content(H),e)=1;
4. 3^m M_X,Y(H)<e^m, where M_X,Y(H)=sum |h_ij|X^iY^j.

Then one can recover k,d in polynomial time from H,N,e,X,Y. More
specifically, the coefficient A(y)=[x^m]H contains a primitive linear
factor ry+t, with r>0, satisfying

    e | (rN+t),   3X max(rY,|t|)<e.                  (1)

For any such factor put u=(rN+t)/e. Then

    k=r/gcd(r,u),    d=u/gcd(r,u).

No primality or factorization of e is assumed. Rational polynomial
factorization of A, followed by integer tests of (1), is one algorithm.
The constant 3 is a sufficient margin, not an optimized threshold.

## Proof

**Leading coefficient and inherited order.** For every prime p|e,
H modulo p is a nonzero multiple of f^m. Since the support has x-degree
at most m and y-degree at most m in its top x-row, that multiple is a
nonzero constant. It follows that deg_x H=m, deg A=m, and the leading
coefficient of A is coprime to e.

In the localized coordinates y=N+(1-z)/x, ideal membership says that
the coefficient of z^j is divisible by e^(m-j) for j<m. Within that
Laurent coefficient, the coefficient of x^(m-j) is
(-1)^j A^(j)(N)/j!: lower x-rows cannot contribute to that exponent.
Therefore

    A belongs to (e,y-N)^m in Z[y].                 (2)

The same weight argument as Proposition A in PROOF-v1.md, now without
localizing any variable, has this consequence: if A=c product B_i^n_i
is its factorization into primitive irreducible integer polynomials,
with deg B_i=h_i, then

    B_i belongs to (e,y-N)^h_i for every i.         (3)

For completeness, at p|e with a=v_p(e), use the multiplicative weight
min_j(v_p(C_j)+a*j) in the Taylor expansion at N. For a polynomial nonzero
modulo p the weight is at most a times its degree. Equation (2) saturates
this bound for A. Multiplicativity and degree additivity force saturation
for every factor, at every p|e; that is (3).

**A small irreducible factor.** For a complex polynomial
P(z)=c product(z-alpha_i), let its Mahler measure be

    M(P)=|c| product max(1,|alpha_i|).

We use its multiplicativity and M(P)<=sum |coefficients(P)|. The latter
follows by averaging log|P(exp(it))| on the unit circle: the contribution
of z-alpha is log max(1,|alpha|), while |P(exp(it))| is bounded by the
coefficient l1 norm. This is a standard identity, not a new ingredient.

Our weighted height hypothesis yields

    M(A(Yz)) <= sum_j |h_mj|Y^j
              <= M_X,Y(H)/X^m < (e/(3X))^m.

As |c|>=1 and sum_i n_i h_i=m, at least one irreducible factor B of
degree h satisfies

    M(B(Yz)) < (e/(3X))^h.                         (4)

**A nonlinear factor would have an impossibly small discriminant.**
From (3), e^-h B(N+ez) is an integer polynomial. Discriminant scaling
therefore gives

    e^(h(h-1)) divides Disc(B).                    (5)

If h>=2, irreducibility over Q implies Disc(B)!=0. The elementary bound

    |Disc(P)| <= h^h M(P)^(2h-2)

follows from the Vandermonde determinant and Hadamard's inequality:
divide its i-th row by max(1,|alpha_i|)^(h-1); every resulting entry
has absolute value at most 1 and every row has norm at most sqrt(h).
Restoring the leading-coefficient factor gives the stated bound.

Applying it to B(Yz), using (4) and X^2Y>=e, gives

    |Disc(B)|
      <= h^h M(B(Yz))^(2h-2) / Y^(h(h-1))
       < [h^h / 3^(2h(h-1))] * e^(h(h-1))
       < e^(h(h-1)).

The last inequality holds for every h>=2. This contradicts (5).
Consequently h=1. Normalize B=ry+t with r>0. Equation (3) gives
e|(rN+t), and the linear Mahler measure is max(rY,|t|). Thus (4)
is exactly the strict inequality in (1).

**Lift and recover.** Set L=x(ry+t)-r=eux-rf. Then L in I and

    M_X,Y(L)=rXY+|t|X+r
             <= (2X+1/Y) max(rY,|t|)
              < (e/3)(2+1/(XY)) <= e.

At the stipulated root, L(k,s) is divisible by e and has absolute value
less than e, hence is zero. Thus uk=rd. Positivity and coprimality of
k,d give the recovery formula. Factoring N from the RSA value of phi(N)
is then checked exactly. Polynomial factorization over Q and all the
remaining integer operations have polynomial bit complexity. QED.

## Implication and limits

The mechanism is a reduction from a supplied, sufficiently short high-degree
relation to a linear relation. It explains why, in this specified t=0
class and with the stated margin, failure to obtain two independent
relations does not prevent recovery. It does not say the full .284 or
.292 attack satisfies these assumptions. In particular, a positive
y-shift changes the leading-row degree from m to as much as m+t; the
degree/order saturation step above then fails.

The factor 3^m is material in finite computations and must not be dropped.
For fixed m an exponent margin eventually absorbs it, but no such margin
or relation existence is promised here. The quadratic proposition has a
sharper bound and remains separately stated.

Synthetic fixtures of degrees 3 and 12 exercise the conditional extraction,
including a degree-12 leading row with two distinct rational roots. They
are constructed from a disclosed test key, not discovered attacks. The
finite checker checks the supplied linear witness, ideal membership, norm
and key recovery. It does not replace this proof of existence or certify
historical originality.

Next research boundary: positive y-shift support, where there is a genuine
degree/ideal-order deficit. Before extending this argument, compare the
small-inverse optimality literature and retain the exact deficit in the
discriminant estimate; do not assume all leading factors inherit their
full degree as ideal order.
