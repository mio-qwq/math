# A constant-order refinement of the sparse full-group threshold

Date: 2026-10-12 UTC. Complete written candidate; independent written
acceptance and universal Lean verification are pending.

Let `T` be the full ordered-pair TF group and fix a real constant `K`.
For all sufficiently large integers `n`, put

\[
p_n=\frac{4\log n-K}{n}.
\]

**Theorem.** The following sharpened alternatives hold:

\[
\boxed{
\begin{cases}
\mathbb E|T(G(n,p_n))|\to1,&K<4,\\
\mathbb E|T(G(n,p_n))|\to\infty,&K>4.
\end{cases}}
\tag{1}
\]

Thus the leading location is refined to `(4 log n-4)/n`, with
one-sided conclusions at every fixed nonzero constant displacement in
`np`. No conclusion at `K=4`, finer window, projection threshold or
reduced-conditional threshold is claimed.

## 1. Retain falling factorials in the finite upper bound

The selection lemma in `SPARSE_THRESHOLD.md` bounds a pair with maximum
support `a` by

\[
q_n^{a(2n-a-3)/4},\qquad q_n=p_n^2+(1-p_n)^2.
\]

There are at most `(n)_a` permutations with support `a`. Since `(n)_b`
is nondecreasing in `0<=b<=n`, the number of pairs with maximum support
`a` is at most `2(a+1)(n)_a^2`. Therefore, at every `n>=4` and every
`0<p<1`, we have the finite inequality

\[
0\le\mathbb E|T|-1
\le2\sum_{a=2}^n(a+1)(n)_a^2
 q^{a(2n-a-3)/4}.
\tag{2}
\]

This is the same proved selection bound, with a sharper count; it does
not make a new probabilistic independence assumption.

## 2. Uniform factorial estimate near full support

For `x=a/n`, define

\[
f(x)=x+(1-x)\log(1-x),\quad0\le x\le1,
\qquad0\log0:=0.
\]

The elementary uniform estimate

\[
\log((n)_a)=a\log n-nf(x)+O(\log n)
\tag{3}
\]

holds for every `0<=a<=n`. Apply
`log(m!)=m log m-m+O(log(m+1))` to `m=n` and `m=n-a`, taking
`0!=1`. Both errors are bounded by a common constant times `log(n+1)`.
This proves (3), including `a=n`.

Also `log q_n=-2p_n+O(p_n^2)`. Its contribution to the logarithm of a
summand in (2) has uniform error `O((log n)^2)` when `a<=n`. Combined
with (3), apart from the factor `2(a+1)`, the logarithm is

\[
\begin{split}
\log\left((n)_a^2q_n^{a(2n-a-3)/4}\right)
={}&-2a(1-x)\log n\\
&+n\left(-2f(x)+\frac K2x(2-x)\right)
+O((\log n)^2).
\end{split}\tag{4}
\]

The error includes the `-3` in the exponent and is uniform in `a`.

## 3. Convergence when K is less than four

At `x=1`, the continuous function

\[
g_K(x)=-2f(x)+\frac K2x(2-x)
\]

has value `K/2-2<0`. Choose constants `delta>0` and `eta>0` such
that `g_K(x)<=-eta` for `1-delta<=x<=1`. For those supports, (4)
and the nonpositive first term give

\[
 (n)_a^2q_n^{a(2n-a-3)/4}\le e^{-\eta n/2}
\]

for sufficiently large `n`. Their total in (2) is bounded by
`2n(n+1)e^(-eta*n/2)`, which tends to zero.

For the remaining supports `a<=(1-delta)n`, avoid the uniform logarithmic
error in (3) at small `a`: simply use `(n)_a<=n^a`. Direct substitution
of `p_n` and `log q_n=-2p_n+O(p_n^2)` gives

\[
\begin{split}
\log\left((n)_a^2q_n^{a(2n-a-3)/4}\right)
&\le -2a(1-a/n)\log n+O_K(a)+O\left(\frac{a(\log n)^2}{n}\right)\\
&\le -\delta a\log n
\end{split}\tag{5}
\]

for sufficiently large `n`, uniformly on this range. Their total is at
most `2 sum_(a>=2)(a+1)n^(-delta*a) -> 0`. The two ranges exhaust
all supports and prove the upper branch of (1). In particular,
`p=4 log(n)/n` (here `K=0`) has expectation tending to one.

## 4. Divergence when K exceeds four

Retain only the empty graph, whose full group has order `(n!)^2`.
Taylor's formula and the factorial estimate give

\[
\begin{aligned}
\log\mathbb E|T|
&\ge2\log(n!)+\binom n2\log(1-p_n)\\
&=\left(\frac K2-2\right)n+O((\log n)^2).
\end{aligned}\tag{6}
\]

The linear term is positive for fixed `K>4`, proving divergence.
At `K=4`, the retained quadratic logarithmic correction is negative
and the upper estimate (4) loses its negative linear margin. These
arguments do not decide that boundary.

## Status and next smallest gap

This refinement is a written consequence of the earlier selection lemma
and exact permutation counting, not a fitted transition. That selection
lemma has the definition-level rational checks in
`quantitative_checks.json`; its universal written proof still awaits
independent acceptance. No extra finite experiment is used to assert (1).

The next gap is `K=4` and displacements smaller than a fixed constant in
`np`, where the current bound does not retain the `p^2 n^2` penalty
from the empty-graph probability. `COMPONENT_REFINEMENT.md` now proves the
exact missing penalty in terms of component excess. The remaining step is a
uniform count of permutation pairs whose selected constraint system has low
excess; the final boundary limit is still not claimed.
