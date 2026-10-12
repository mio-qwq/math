# Sparse random graphs: a sharp leading constant for full TF expectation

Date: 2026-10-12 UTC. Written theorem and exact finite regression;
independent written acceptance pending. All logarithms below are natural.

## 1. The result and what it measures

Let `T(G)` be the full ordered-pair group defined in `SECOND_ORDER.md`.
Write `q=p^2+(1-p)^2`. For `n >= 4`, put

\[
r_n=n^2q^{(n-3)/4}.
\]

**Theorem 1 (effective expectation bound).** If `0<p<1` and `r_n<1`,

\[
\boxed{0\le\mathbb E|T(G(n,p))|-1
\le\frac{2r_n^2(3-2r_n)}{(1-r_n)^2}.}
\tag{1}
\]

Consequently, for `p_n=c log(n)/n` with fixed `c>0`,

\[
\boxed{
\begin{cases}
\mathbb E|T(G(n,p_n))|\longrightarrow1,&c>4,\\
\mathbb E|T(G(n,p_n))|\longrightarrow\infty,&0<c<4.
\end{cases}}
\tag{2}
\]

This determines the leading sparse constant **4** for the full-group
expectation. No behavior at `c=4`, critical window, projection threshold,
conditional-reduced expectation threshold, or dense-end sharp constant is
asserted. The measure is an expectation: rare graphs with enormous groups
must be retained even if their probability tends to zero.

## 2. A selection bound for a prescribed permutation pair

Let `a=max(|supp alpha|,|supp beta|) >= 2`. The adjacency equation is
unchanged after exchanging the components, since the matrix is symmetric.
Thus assume `alpha` moves `a` vertices. Order these first, followed by the
fixed vertices. Select one orientation `(u,v)` of every unordered source
edge whose first vertex is moved. There are exactly

\[
M=a(n-a)+\binom a2=\frac{a(2n-a-1)}2
\tag{3}
\]

selected source variables, each occurring exactly once. Its equation is
an equality with the target edge variable, or with the fixed zero if the
image is diagonal. A tautological equality can only have
`alpha(u)=v, beta(v)=u`: the other way to preserve the unordered source
edge would require `alpha(u)=u`. For each moved `u`, at most one `v`
satisfies the first equality. Hence at least

\[
M-a=\frac{a(2n-a-3)}2
\tag{4}
\]

selected equalities are nontrivial.

Direct every such constraint from its source variable to its target
variable or ground. Each ordinary vertex has outdegree at most one and
ground has outdegree zero. Every weak component is a tree or has one
directed cycle. Tautological self-loops were removed. An ungrounded
component containing `k` ordinary variables and at least one constraint
has `k >= 2` and at most `k` constraints. A grounded component also has
at most `k` constraints. The components involve disjoint independent
original edge bits.

An ungrounded component has probability

\[
p^k+(1-p)^k\le(p^2+(1-p)^2)^{k/2}=q^{k/2}
\quad(k\ge2).
\tag{5}
\]

This is the monotonicity of the two-coordinate power mean, or directly
`x^r+y^r <= (x+y)^r` for `x,y>=0,r>=1` applied to `x=p^2`,
`y=(1-p)^2`, `r=k/2`. Grounded components have probability
`(1-p)^k <= q^(k/2)`. Their total number of ordinary variables is at
least the number of selected nontrivial constraints. Dropping all
unselected equations only increases probability, so

\[
\boxed{\Pr[(\alpha,\beta)\in T(G(n,p))]
\le q^{a(2n-a-3)/4}.}
\tag{6}
\]

The proof includes forced diagonal zeros; it does not use a random
rigidity theorem or independent ordered matrix entries.

## 3. Summation and the sharp leading constant

There are at most `n^a` permutations with support `a`. The number of
pairs with maximum support `a` is at most `2(a+1)n^(2a)`. Since
`2n-a-3 >= n-3`, linearity of expectation and (6) give

\[
\mathbb E|T|-1\le 2\sum_{a=2}^n(a+1)
 \left(n^2q^{(n-3)/4}\right)^a.
\tag{7}
\]

For `r_n<1`, completing this to an infinite geometric series gives (1).
If `p_n=c log(n)/n`, then

\[
\log r_n=\left(2-\frac c2\right)\log n+o(1).
\tag{8}
\]

Thus `c>4` implies `r_n -> 0` and proves the upper branch of (2).

For the lower branch retain just the empty graph. Its full TF group has
order `(n!)^2`, and its probability is `(1-p_n)^binom(n,2)`. Therefore

\[
\begin{aligned}
\log\mathbb E|T|
&\ge2\log(n!)+\binom n2\log(1-p_n)\\
&=\left(2-\frac c2\right)n\log n-2n+O((\log n)^2).
\end{aligned}\tag{9}
\]

For every fixed `0<c<4`, this tends to infinity. This proof identifies
the rare-event obstruction explicitly. It also prevents replacing
high-probability symmetry estimates by expectation estimates.

For the first-coordinate projection `P(G)`, the same empty graph gives
`E|P| >= n! (1-p)^binom(n,2)`, proving divergence for `c<2`.
Equation (1) supplies convergence for `c>4` because `|P|<=|T|`.
The interval `2<=c<=4` for the projection is left unresolved here.

## 4. A separate twin-free threshold and its critical window

Let `R_n` be the event of pairwise distinct **open** neighborhoods.
Two specified vertices are open twins with exact probability

\[
(1-p)q^{n-2}. \tag{10}
\]

For `p_n=c log(n)/n`, a union bound gives `Pr(R_n^c)->0` when `c>1`.
When `0<c<1`, let `I_n` count isolated vertices. Its mean is
`n(1-p)^(n-1)=n^(1-c+o(1)) -> infinity`. For two distinct vertices,
the joint isolation probability is `(1-p)^(2n-3)`, so

\[
\frac{\operatorname{Var}(I_n)}{(\mathbb E I_n)^2}
\le\frac1{\mathbb E I_n}+\frac p{1-p}\longrightarrow0.
\tag{11}
\]

At least two isolated vertices are then present with probability tending
to one, implying open twins and `Pr(R_n)->0`. The leading constant for
twin-freeness is therefore **1**, a different problem from (2).

More precisely, if `p_n=(log n+t)/n` with fixed real `t`, then

\[
\boxed{\Pr(R_n)\longrightarrow
e^{-e^{-t}}(1+e^{-t}).}\tag{12}
\]

Here is a self-contained deduction from the classical isolated-vertex
calculation. For each fixed integer `k>=1`,

\[
\mathbb E(I_n)_k=(n)_k
(1-p_n)^{kn-k(k+1)/2}\longrightarrow e^{-kt}.
\tag{13}
\]

The factorial moment criterion yields the Poisson limit with mean
`e^(-t)`. Its standard convergence implication can also be obtained by
the factorial-moment version of the method of moments; the Poisson law
is moment-determinate.

Let `X_n` count open-twin pairs. Every pair of isolated vertices is an
open-twin pair, so `Y_n=X_n-binom(I_n,2)>=0`. Its exact mean is

\[
\mathbb EY_n=\binom n2(1-p_n)^{2n-3}
\left[\left(1+\frac{p_n^2}{(1-p_n)^2}\right)^{n-2}-1\right].
\tag{14}
\]

The prefactor tends to `e^(-2t)/2`, while the bracket tends to zero
because `np_n^2 -> 0`. Thus `Pr(Y_n>0)->0`. With probability tending
to one, all open-twin pairs are pairs of isolated vertices. Consequently
`R_n` is equivalent to `I_n<=1` up to an event of probability `o(1)`,
which proves (12). Adjacent external-neighborhood twins also have expected
number `binom(n,2)p_n q^(n-2)->0` in this window.

The isolated-vertex Poisson mechanism and connectivity scale are classical;
they are not proposed as a new random-graph phenomenon. This note spells
out their implication for the reduced-graph domain of C66. Twin-freeness
does not establish absence of every nontrivial TF automorphism.

## Verification boundaries

`check_quantitative.py` verifies the selected constraints, component
edge/vertex inequality, and (6) on every permutation pair for `n=4,5`
at `p=1/10,1/2,9/10`, using exact rational fourth powers. It checks
the edge count in (13) directly. There are 44,922 rational probability
checks. These finite checks detect transcription and forced-zero mistakes;
the proofs in Sections 2-4 establish the parameter claims.

No universal Lean proof, independent AI written review, human review,
publication acceptance, or historical firstness is asserted for this new
quantitative package. Literature comparison is recorded separately.
