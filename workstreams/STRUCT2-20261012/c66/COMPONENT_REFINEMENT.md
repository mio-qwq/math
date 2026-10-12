# Constraint-component refinement at the `K=4` boundary

Date: 2026-10-13 UTC. Proved analytic lemma and exact finite regression;
the full `K=4` expectation limit remains a candidate problem. Independent
written acceptance and universal Lean verification are pending.

## 1. The penalty discarded by the previous bound

Put

\[
q=p^2+(1-p)^2,
\qquad
z=\frac{\min\{p^2,(1-p)^2\}}q.
\]

Consider any system of equality constraints among independent Bernoulli-`p`
edge variables, with an optional ground variable fixed to zero. After taking
connected components, let the ungrounded nontrivial component sizes be
`k_1,...,k_c`, each at least two, and let `g` be the number of ordinary
variables in the grounded component. Define

\[
N=g+\sum_i k_i,
\qquad
D=g+\sum_i(k_i-2).
\tag{1}
\]

Here `N` counts constrained ordinary variables, while `D` is the
**component excess**: a grounded variable is charged once and an ungrounded
component is charged only for its size beyond two.

**Lemma (refined component bound).** The probability `P` that all constraints
hold satisfies

\[
\boxed{P\le q^{N/2}(1-z)^{D/2}
       \le q^{N/2}\exp(-zD/2).}
\tag{2}
\]

This strictly strengthens the earlier `q^(N/2)` estimate exactly when the
constraint system contains a grounded variable or an ungrounded component of
size at least three. Size-two ungrounded components show that no positive
uniform penalty can be inserted without a structural statistic such as `D`.

## 2. Proof

Write `u=min(p,1-p)`, `v=max(p,1-p)`. Then

\[
x=\frac{u^2}{q}=z,
\qquad y=\frac{v^2}{q}=1-z,
\qquad 0\le x\le y.
\]

For an ungrounded component of size `k>=2`, its exact probability is
`p^k+(1-p)^k`. With `r=k/2>=1`,

\[
\frac{p^k+(1-p)^k}{q^{k/2}}
=x^r+y^r
\le x y^{r-1}+y y^{r-1}
=y^{r-1}.
\tag{3}
\]

The inequality uses `x^r<=x y^(r-1)`, valid because `x<=y`. Thus this
component contributes at most
`q^(k/2)(1-z)^((k-2)/2)`. A grounded component has exact probability
`(1-p)^g`, which is at most `v^g=q^(g/2)y^(g/2)`. Multiplying the independent
component probabilities proves the first inequality in (2). The second is
`1-z<=exp(-z)`.

The proof is valid for every `0<p<1`; it does not assume that `p<=1/2`.

## 3. Why this is the missing scale at `K=4`

At

\[
p=\frac{4\log n-4}{n},
\]

we have `z=(1+o(1))p^2`. Hence a structural estimate `D>=epsilon*n^2`
would add the factor

\[
\exp\bigl(-(8\epsilon+o(1))(\log n)^2\bigr).
\tag{4}

This is precisely the logarithmic-square penalty discarded by the earlier
power-mean bound. For the empty graph all edge variables are grounded, so
`D=binom(n,2)` and (4) reproduces the negative `Theta((log n)^2)` correction
in its exact probability. Conversely, systems dominated by size-two
ungrounded components have small `D` and must be counted by their much more
restricted permutation structure rather than charged a nonexistent
probability penalty.

Thus the unresolved boundary is reduced to a concrete entropy-versus-excess
statement: split permutation pairs according to `D`; use (2) for large
excess, and prove a sharper count for pairs whose selected constraint system
has small excess. No claim that this final structural estimate has already
been proved is made here.

## 4. Exact regression and status

`check_component_refinement.py` constructs both the full ordered-equation
constraint system and the selected functional constraint system used in
`SPARSE_THRESHOLD.md`. For every nonidentity permutation pair at `n=4,5` and
`p=1/10,1/2,9/10`, it checks the squared rational form

\[
P^2\le q^N(1-z)^D.
\]

This keeps all arithmetic exact even when `N` or `D` is odd. The run performs
89,844 exact bounds and detects a damage control that falsely charges a
size-two component one unit of excess. The receipt is
`verification/20261013-c66-component-refinement/checks.json`.

Status separation:

* **proved in writing and regression-checked:** the component lemma (2);
* **identified reduction:** large-excess versus low-excess permutation pairs;
* **still open here:** the required uniform low-excess counting theorem and
  therefore the final value of `E|T|-1` at `K=4`.
