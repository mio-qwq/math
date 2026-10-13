# The sparse boundary and its logarithmic-square correction

Date: 2026-10-13 UTC. Complete written proof with definition-level structural
regression. Independent written acceptance and universal Lean verification
are pending. All logarithms are natural.

Subsequent result: `EXACT_WINDOW.md` proves the matching upper bound and
the exact limiting function in the finer window left open by this note.
The historical scope and derivation below are retained; the new written
result has separate regression and Lean structural receipts.

Let

\[
T(G)=\{(\alpha,\beta)\in S_n^2:
 A_{ij}=A_{\alpha(i),\beta(j)}\text{ for every }i,j\}.
\]

For a fixed real number `c`, write `L=log n` and, for sufficiently large `n`,

\[
p_n=\frac{4L-4-cL^2/n}{n}.
\tag{1}
\]

**Theorem.** For the full ordered-pair group,

\[
\boxed{
\begin{cases}
\mathbb E|T(G(n,p_n))|\longrightarrow1,&c<8,\\
\mathbb E|T(G(n,p_n))|\longrightarrow\infty,&c\ge8.
\end{cases}}
\tag{2}
\]

In particular, `c=0` resolves the previously untreated boundary
`p=(4 log n-4)/n`: the full-group expectation tends to one. The next downward
correction in `np` has sharp leading size `8(log n)^2/n`. Equation (2) does
not determine the finer window obtained by adding terms of size `log n/n`
or `1/n` to `np`. It is an expectation theorem, not a high-probability
rigidity threshold or a statement about the projection/reduced-conditional
random variable.

## 1. Full constraints and component invariance

For a fixed permutation pair impose every ordered adjacency equation,
including diagonal equations. There is one independent variable for each
unordered edge and one ground representing every diagonal entry. Equality
closure partitions the edge variables into grounded and ungrounded
components. Let `g` be the number grounded; let `k_1,...,k_t` be the sizes
of the ungrounded components with size at least two. Put

\[
N=g+\sum_i k_i,
\qquad D=g+\sum_i(k_i-2).
\tag{3}
\]

The exact prescribed-pair probability is

\[
P_{\alpha,\beta}=(1-p)^g
 \prod_{C\text{ ungrounded}}\bigl(p^{|C|}+(1-p)^{|C|}\bigr).
\tag{4}
\]

Singleton factors are one. With `q=p^2+(1-p)^2` and
`z=min(p^2,(1-p)^2)/q`, the already proved component lemma gives

\[
P_{\alpha,\beta}\le q^{N/2}e^{-zD/2}.
\tag{5}
\]

**Component invariance lemma.** If an ungrounded component `C` contains
`k` edge variables, every cycle of `alpha` or `beta` through an endpoint of
one of its edges has length at most `2k`.

**Proof.** Make the symmetric zero-diagonal matrix `B_C` whose edge set is
exactly `C`. By full equality closure,

\[
(B_C)_{ij}=(B_C)_{\alpha(i),\beta(j)}
\qquad\text{for all }i,j.
\tag{6}
\]

The ground is outside `C`, so (6) also handles diagonal entries. Summing
rows and permuting the column indices by `beta` proves
`deg_C(i)=deg_C(alpha(i))`. Summing columns gives the analogous equality
for `beta`. Thus both permutations preserve the set of positive-degree
vertices of `B_C`. This set has at most `2k` vertices and contains every
endpoint of an edge of `C`, proving the cycle-length bound. This is a
statement about the **full** constraint system; selected components need
not have this invariance. ∎

Fix an integer `K>=4`. Put

\[
r=\lfloor K/2\rfloor+1,\qquad \theta=1-2/r>0,
\]

and let `U` consist of the vertices in `alpha`-cycles of length greater
than `K`. Any ungrounded component touching an edge incident with `U` has
size at least `r`. Its excess is at least `theta` times its size. Grounded
variables also satisfy this inequality. Consequently,

\[
\boxed{D\ge\theta\left(\binom n2-\binom{n-|U|}2\right).}
\tag{7}
\]

The same bound holds using the long cycles of `beta`.

## 2. Counting permutations with many short-cycle vertices

Let `A_n(K,epsilon)` count permutations with at least `epsilon*n` vertices
in cycles of length at most `K`, where `0<epsilon<=1/2` is fixed. Put
`gamma=epsilon/K` and `m_0=ceil(gamma*n)`.

If `c_j` is the number of cycles of length `j`, `1<=j<=K`, their total
number `m=sum c_j` is at least `m_0`. For each specified short-cycle vector,
choosing these cycles and allowing an arbitrary permutation on the
remaining vertices gives the upper bound

\[
\frac{n!}{\prod_{j=1}^K j^{c_j}c_j!}.
\]

There are at most `(n+1)^K` vectors. The multinomial identity gives
`prod c_j! >= m!/K^m`. Hence

\[
\boxed{A_n(K,\epsilon)\le
 (n+1)^K n!\,\frac{K^n}{m_0!}.}
\tag{8}
\]

Using `log(m!)>=m log m-m` and `log(n!)<=n log n`, this implies

\[
\log A_n(K,\epsilon)
\le(1-\gamma)nL+O_{K,\epsilon}(n).
\tag{9}
\]

The fixed point cycles are included. The bound concerns actual permutations,
not an assumed random-permutation cycle distribution.

## 3. Uniform support estimates with the quadratic term retained

Let `a=max(|supp alpha|,|supp beta|)` and

\[
F(a)=a(2n-a-3).
\]

The moved-first edge selection from `SPARSE_THRESHOLD.md` has at least
`F(a)/2` distinct nontrivial source variables. Each lies in a nontrivial
or grounded full component, so `N>=F(a)/2`. Thus (5) gives

\[
P_{\alpha,\beta}\le q^{F(a)/4}e^{-zD/2}.
\tag{10}
\]

There are at most `2(a+1)(n)_a^2` pairs of maximum support `a`.

An essential sharper estimate is

\[
\boxed{\log q\le-2p+\frac83p^3\quad(0\le p\le1/2).}
\tag{11}
\]

Indeed, the derivative of `log(1-2p+2p^2)+2p` is `4p^2/q<=8p^2`.
Integrating proves (11). In particular, there is **no** quadratic term in
`log q`. At (1), the error after multiplying (11) by `F(a)/4` is `o(1)`
uniformly in `a`, since `p^3 n^2=O(L^3/n)`.

Write `C=max(c,0)`. Fix `0<delta<=1/8`.

For `2<=a<=(1-delta)n`, the estimate `(n)_a<=n^a` and (11) give

\[
\begin{split}
\log\bigl((n)_a^2q^{F(a)/4}\bigr)
&\le-2\delta aL+4a+6aL/n+C aL^2/n+O_c(aL^3/n^2)\\
&\le-\delta aL
\end{split}
\tag{12}
\]

for sufficiently large `n`, uniformly throughout this range.

For `a>(1-delta)n`, put `d=n-a`, so `0<=d<n/8`. The elementary factorial
upper bound `log(n!)<=nL-n+L+1` gives

\[
\log\bigl((n)_a^2q^{F(a)/4}\bigr)
\le\frac C2L^2+8L-4-2\log(d!)+2d^2L/n+o(1).
\tag{13}
\]

Here `F(a)=n^2-3n-d^2+3d`. If `d<=sqrt(n)`, the last positive term is at
most `2L`. If `sqrt(n)<d<n/8`, use
`log(d!)>=d log d-d >= (d/2)L-d`, which makes
`-2 log(d!)+2d^2L/n <= -3dL/4+2d <=0` for sufficiently large `n`.
Therefore the uniform estimate is

\[
\boxed{\log\bigl((n)_a^2q^{F(a)/4}\bigr)
\le\frac C2L^2+10L}
\tag{14}
\]

for all sufficiently large `n`. This removes the old unspecified
`O(L^2)` error at the boundary.

## 4. Convergence for c less than eight

Suppose `c<8`, hence `0<=C<8`. Choose fixed `K>=4` and
`0<epsilon<=1/2` so that

\[
4\theta(1-\epsilon^2)>C/2.
\tag{15}
\]

This is possible because `theta ->1` as `K ->infinity`. For example, put
`Delta=1-C/8>0`, choose `K=2 ceil(8/Delta)`, and take
`epsilon=Delta/2`. Then `theta>1-Delta/4` and
`theta*(1-epsilon^2)>1-Delta=C/8`, proving (15). Put
`gamma=epsilon/K` and choose fixed `0<delta<=1/8` with
`2delta^2<gamma`.

**Small maximum support.** By (12), its total contribution above the
identity is at most

\[
2\sum_{a\ge2}(a+1)n^{-\delta a}
=\frac{2t^2(3-2t)}{(1-t)^2}\longrightarrow0,
\qquad t=n^{-\delta}.
\tag{16}
\]

**Near-full support, few short-cycle vertices in alpha.** If fewer than
`epsilon*n` vertices belong to short cycles, (7) gives

\[
D\ge\frac\theta2\bigl((1-\epsilon^2)n^2-n\bigr).
\]

Since `p<1/2`, `z=p^2/q>=p^2`; at (1),

\[
zD/2\ge4\theta(1-\epsilon^2)L^2-O_c(L).
\]

Combining (10), (14) and the maximum-support counts bounds this whole
family by

\[
2n(n+1)\exp\left(
-\left[4\theta(1-\epsilon^2)-C/2\right]L^2+O_c(L)\right)
\longrightarrow0.
\tag{17}
\]

**Near-full support, many short-cycle vertices in alpha.** There are at
most `A_n(K,epsilon)*n!` such pairs, including an arbitrary `beta`. By
(9), their log count is at most `(2-gamma)nL+O(n)`. For
`a>(1-delta)n`,

\[
F(a)\ge(1-\delta^2)n^2-3n.
\]

Dropping the excess penalty and using (11) shows their total is at most

\[
\exp\left(-[\gamma-2\delta^2]nL+O_c(n+L^2)\right)
\longrightarrow0.
\tag{18}
\]

These three disjoint support/cycle cases exhaust every nonidentity pair.
Linearity of expectation proves the convergence branch of (2).

## 5. Divergence and the endpoint c=8

The empty graph has full group order `(n!)^2`. Its contribution is

\[
B_n=(n!)^2(1-p_n)^{\binom n2}.
\]

Stirling's formula and Taylor's formula, with error
`O(p_n^3 n^2)=o(1)`, give the more precise identity

\[
\boxed{\log B_n=(c/2-4)L^2+11L+\log(2\pi)-6+o(1).}
\tag{19}
\]

The terms arise as follows: `2 log(n!)=2nL-2n+log(2pi*n)+o(1)`;
`-binom(n,2)*p_n=-2nL+2n+2L-2+(c/2)L^2+o(1)`;
`-binom(n,2)*p_n^2/2=-4(L-1)^2+o(1)`.

For `c>8`, (19) tends to infinity quadratically in `L`. At `c=8`,

\[
B_n\sim2\pi e^{-6}n^{11}\longrightarrow\infty.
\tag{20}
\]

Since `E|T|>=B_n`, the divergence branch follows, including the endpoint.

There is also a rigorous obstruction in the finer window. For fixed real
`h,s`, put

\[
np_n=4L-4-\frac{8L^2}{n}+\frac{hL+s}{n}.
\tag{21}
\]

The same expansion gives

\[
\log B_n=(11-h/2)L+\log(2\pi)-6-s/2+o(1).
\tag{22}
\]

Thus `h<22` already forces divergence. At `h=22`, linearity of expectation
over the nonidentity pairs supplies the sharper bound

\[
\mathbb E|T|\ge1+\bigl((n!)^2-1\bigr)
 (1-p_n)^{\binom n2},
\]

and therefore

\[
\boxed{\liminf\mathbb E|T|
 \ge1+2\pi e^{-6-s/2}>1.}
\tag{23}
\]

When `h>22`, this empty-graph contribution tends to zero; no matching upper
bound or exact limiting function in (21) is proved here.

The empty graph is an all-zero assignment; it does **not** imply that the
constraint system of every prescribed permutation pair is fully grounded.
This corrects that explanatory sentence in the preceding component note.
The component inequality itself is unchanged.

## 6. Verification, attribution and remaining scope

`check_critical_structure.py` builds full labelled constraint components by
graph traversal, separately compares them with the earlier DSU construction,
and checks endpoint invariance, the `2k` cycle bound, (7), and `N>=F(a)/2`.
It also compares exact short-cycle vector counts with direct permutation
counts, checks the rational component bound on selected cases, and uses
high-precision arithmetic to check the transcription of (19). A four-cycle
acting on a size-two edge component rejects the damaged bound `k` in place
of `2k`. The finite checks support transcription; Sections 1--5 are the
proof for all parameters, independent of finite extrapolation.

Reproduce the regression with Python 3 and `mpmath==1.3.0`:

```sh
python3 check_critical_structure.py --output /chosen/receipt/checks.json
```

The central component interface is additionally compiled in
`lean/ComponentSupport.lean`: it defines the actual original unordered
variables and full equation closure, constructs the canonical component
edge list, and proves endpoint transport and the distinct cycle-prefix bound.
Its 12 named audits pass official Lean 4.34.1 with no errors, warnings or
`sorryAx`; the axiom union is `propext`, `Classical.choice` and `Quot.sound`.
This verifies the structural interface; it does not formalize Sections 2--5.

The full-group definition and the distinction from the reduced projection
in Bychawski arXiv:2406.06267v1 are retained. The publicly posted MathDB proof
of the fixed-p limit uses a coarser equality-component bound; it remains
prior overlapping work. Source searches and access limits are separately
recorded in `PRIOR_ART_2026-10-13.md`. No historical-firstness claim is made.

This stage is a complete **written proof with structural regression** and a
separately kernel-verified component interface. Independent written acceptance
and universal Lean verification of the full expectation limit are pending. The next
smallest gap is a matching upper bound in the finer window
`np=4 log n-4-8(log n)^2/n+(22 log n+s)/n`. The empty-graph lower bound is
already proved, while an exact limiting function remains unproved. Further
formalization/review of the excess and short-cycle counts is also useful.
