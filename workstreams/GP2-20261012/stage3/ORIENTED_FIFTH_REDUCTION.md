# Exact reduction for the candidate oriented coefficient 1/5

GP2-20261012, 2026-10-13. This note isolates a potentially useful next
inequality and an exact obstruction to the simplest pointwise proof. **The
candidate inequality is not proved here, and the certified Ka4 bound is not
changed.**

## 1. Candidate and conditional consequence

For a nonnegative real square matrix `M` with zero diagonal and no digons,

    M_xy M_yx=0,

retain

    T=tr((MM^t)^2), L=tr(M^4),
    Y=tr(M^2(M^t)^2), X=tr(M^3M^t).

The remaining candidate is

    2X <= T+L.                                           (C)

If (C) holds, then, using `Y<=T` and the accepted sixteen-term identity,

    tr((M+M^t)^4)=2L+8X+4Y+2T <= 6L+10T <= 10(T+L),

so `2(T+L)>=tr((M+M^t)^4)/5`. In the six reciprocal-mass argument this
would replace the off-diagonal coefficient `3-2sqrt(2)` by `1/5` and give
the *conditional* empty-orbit constant

    1/[27(1+5^(1/3))^3].

None of these conditional improvements is used in the current theorem.

## 2. Two exact equivalent forms

Put `R=M+M^t` and `S=M-M^t`. Direct expansion gives, for every real square
matrix `M` (the orientation hypothesis is not needed for the identities),

    T+L-2X = tr((MM^t-M^2)^2)
             = [tr(S^4)+tr(RSRS)]/4.                    (1)

The odd cross term vanishes because `R` is symmetric and `S^3` is
skew-symmetric. Thus (C) is exactly the assertion that either expression in
(1) is nonnegative for oriented nonnegative `M`. The first expression is the
trace of a square, not a Frobenius norm; it is not automatically nonnegative.

There is also an exact two-letter-interface form. For every ordered pair
`i,k`, set

    x=(M^2)_ik, y=(M^2)_ki,
    z=(MM^t)_ik, w=(M^tM)_ik.

Transpose and cyclic trace identities give

    T+L-2X
      = sum_(i,k) (z-x)(z-y)
      = sum_(i,k) (w-x)(w-y)
      = (1/2) sum_(i,k) [(z-x)(z-y)+(w-x)(w-y)].        (2)

For an oriented kernel, `x,y,z,w` are the four weighted two-step orientation
types at the pair interface. Formula (2) is the desired bridge to the pair
state hierarchy, but its summands need not be nonnegative.

## 3. Exact failure of pointwise positivity

The five-vertex orientation in `oriented_fifth_reduction.json` has rows

    00011
    00010
    00010
    00000
    01100.

At the pair `(3,4)` it gives `(x,y,z,w)=(0,2,0,1)`, hence the bracket in
(2) is

    (0-0)(0-2)+(1-0)(1-2)=-1.

Globally the same matrix has

    (T,L,X,Y)=(16,0,2,6),  T+L-2X=12>0.

Therefore a proof of (C) cannot declare each pair-interface contribution
nonnegative. It must use cancellation between interfaces, a genuine
sum-of-squares/flag certificate, or extra canonical-level structure.

Nor can one repair pointwise positivity by splitting according to whether
the endpoints are nonadjacent, joined as `i->k`, or joined as `k->i`.
The direct endpoint arc occurs in none of `x,y,z,w`. Starting from the
displayed witness, inserting either `3->4` or `4->3` therefore preserves
`(x,y,z,w)=(0,2,0,1)` and the value `-1`. Exact exhaustion shows that order
five is minimal for this phenomenon: for every zero-one orientation through
four vertices the minimum bracket is zero in each of the three endpoint
classes, while at order five it is `-1` in all three classes.

Thus any local-to-global proof based on (2) must see at least five vertices.
In particular, the next useful certificate basis is a two-labelled,
three-unlabelled flag (or an equivalent five-letter charging rule); endpoint
adjacency alone carries no correcting information.

## 4. Exact computation and status

The standard-library checker reconstructs every matrix product with integer
arithmetic, verifies both forms of (1), verifies the five-vertex local
obstruction, and exhausts all

    sum_(n=1)^5 3^(n choose 2) = 59809

zero-one orientations through five vertices. It finds `T+L-2X>=0` in every
case and independently verifies the endpoint-class minima just stated. Two
altered certificates are rejected. Run:

```sh
python workstreams/GP2-20261012/stage3/verify_oriented_fifth_reduction.py
python -O workstreams/GP2-20261012/stage3/verify_oriented_fifth_reduction.py
```

The finite exhaustion is evidence only: it neither proves (C) for all orders
and weights nor supplies a new Ka4 bound. No independent AI review, Lean
formalization, optimality, or historical-priority claim is made. The next
step is an exact global square/flag decomposition of (1), or a counterexample;
if neither emerges, return to mixed reciprocal classes rather than enlarging
the same search.
