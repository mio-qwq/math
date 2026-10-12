# Full two-fold group expectation: the second exponential order

Date: 2026-10-12 UTC. Written derivation by the STRUCT2 continuation;
definition-level checks passed. Independent written acceptance is pending.
This note does not change the status of the earlier C-audit candidate.

## Statement and contribution boundary

For a labelled simple graph on `[n]`, with symmetric zero-diagonal
adjacency matrix `A`, define the full group

\[
T(G)=\{(\alpha,\beta)\in S_n^2:
 A_{ij}=A_{\alpha(i),\beta(j)}\text{ for all }i,j\}.
\]

For `G_n ~ G(n,1/2)` the following written theorem holds:

\[
\boxed{\mathbb E|T(G_n)|=1+
8\binom n2 2^{-n}+
\left(224\binom n3+528\binom n4\right)2^{-2n}
+R_n,}
\tag{1}
\]

where `R_n >= 0`, and, for every integer `n >= 1024`,

\[
\boxed{0\le R_n\le 200000000\,n^6 2^{-3n}.}
\tag{2}
\]

In particular the error after the second displayed order is
`O(n^6 2^(-3n))`. The earlier frozen candidate has only the first
exponential order and an `O(n^4 2^(-2n))` error. Equation (1) concerns
ordered permutation pairs. It is not an expansion for the first-coordinate
projection or the expectation conditioned on reduced graphs.

The fixed-probability limit already has a publicly posted MathDB proof
claim, examined in `PRIOR_ART_2026-10-12.md`. Neither that limit nor the
elementary constraint method is claimed as a first discovery here.

## 1. Exact decomposition by the union support

Fix a pair of permutations and let `S` be their union support, of size `s`.
Both permutations fix every vertex outside `S`, and preserve `S`. On `S`
let `Gamma=<alpha,beta>` have `t` orbits, and put `d=s-t`. Each orbit has
at least two vertices, so `d >= ceil(s/2)`.

For a vertex `w` outside `S`, the ordered equations with `(w,i)` and
`(i,w)` force all `s` incident bits to be constant on the `Gamma` orbits.
Conversely those orbit equalities imply every equation involving `w`.
Their exact probability at `p=1/2` is `2^(-d)`. Different external
vertices use disjoint bits. All external-external equations are identities.

Within `S`, make one Boolean variable for each undirected edge, and a
ground vertex representing the fixed diagonal zero. For every ordered
`(i,j)`, including `i=j`, identify the variable for `{i,j}` (or ground)
with the variable for `{alpha(i),beta(j)}` (or ground). If there are `f`
ungrounded components, exactly `2^f` internal assignments are allowed.
Put `r=binom(s,2)-f`. The prescribed pair has the exact probability

\[
2^{-d(n-s)-r}. \tag{3}
\]

Let `h_s(d,r)` count pairs on `[s]` with union support all of `[s]` and
these two deficits. Relabelling the support gives the finite identity

\[
\mathbb E|T(G_n)|=1+
\sum_{s=2}^n\binom ns\sum_{d,r}h_s(d,r)2^{-d(n-s)-r}.
\tag{4}
\]

No graph-rigidity assumption enters this identity. It is a sum of
indicators of every possible ordered permutation pair.

## 2. All contributions with external deficit at most two

The condition `d <= 2` forces `s <= 4`. The complete relevant table is

| `s` | `d` | `r` | Number of pairs |
|---:|---:|---:|---:|
| 2 | 1 | 0 | 1 |
| 2 | 1 | 1 | 2 |
| 3 | 2 | 2 | 2 |
| 3 | 2 | 3 | 24 |
| 4 | 2 | 2 | 3 |
| 4 | 2 | 4 | 18 |
| 4 | 2 | 5 | 6 |

Here is a direct small-support explanation. On two vertices the three
pairs are `(tau,tau)`, `(tau,id)`, and `(id,tau)`. The first leaves their
edge free; the others force it to zero.

On three vertices there are `6^2-1-3*3=26` pairs with full union support;
the generated action is necessarily transitive. The two equal oriented
three-cycles identify all three edge bits and leave the common bit free,
giving rank two. Every other pair forces all three bits to zero. This
last assertion can also be checked by the four types: an identity and a
three-cycle; a transposition and a three-cycle; two different
transpositions; and the two unequal three-cycles.

On four vertices, deficit two means two orbits of size two. There are
three partitions into such orbits. For each orbit, denote the three
possible nontrivial restrictions by `B=(tau,tau)`, `L=(tau,id)`, and
`R=(id,tau)`. For each partition there are nine patterns. Their internal
ranks are

| Orbit patterns | Internal rank | Patterns per partition |
|---|---:|---:|
| `BB` | 2 | 1 |
| `BL, BR, LB, RB, LR, RL` | 4 | 6 |
| `LL, RR` | 5 | 2 |

These ranks follow by equating the four cross-orbit bits and the two
within-orbit bits, retaining the forced diagonal zeros.

In (3), extracting `2^(-dn)` multiplies a table entry by `2^(ds-r)`.
Thus the coefficients are

\[
\begin{aligned}
c_{2,1}&=2^2+2\,2^1=8,\\
c_{3,2}&=2\,2^4+24\,2^3=224,\\
c_{4,2}&=3\,2^6+18\,2^4+6\,2^3=528.
\end{aligned}\tag{5}
\]

All terms not listed are nonnegative and have external deficit at least
three, proving (1) with `R_n >= 0`.

## 3. A summable tail valid for every remaining pair

For `s <= n/4`, (3) and `r >= 0` give

\[
\Pr[(\alpha,\beta)\in T]\le
2^{-\lceil s/2\rceil(n-s)},
\qquad
\#\{\text{pairs with union support }s\}\le\binom ns(s!)^2.
\tag{6}
\]

For larger supports use the selection lemma proved independently in
`SPARSE_THRESHOLD.md`. At `p=1/2` it gives, for
`a=max(|supp alpha|,|supp beta|)`,

\[
\Pr[(\alpha,\beta)\in T]\le
2^{-a(2n-a-3)/4}\le2^{-a(n-3)/4}.
\tag{7}
\]

If `s>n/4`, then `a >= s/2 > n/8`. Since there are at most `(n!)^2`
pairs altogether, their total contribution is at most

\[
(n!)^2 2^{-n(n-3)/32}.
\tag{8}
\]

For the transitive support-four pairs, the complete finite rank table is
`h_4(3,4)=12`, `h_4(3,5)=54`, `h_4(3,6)=360`. It gives the exact
contribution `33024*binom(n,4)*2^(-3n)`. These 426 pairs were exhaustively
checked by the original ordered adjacency equations and independently
matched by enumerating every four-vertex graph. Alternatively, replacing
this by the coarser bound `576*binom(n,4)*2^(-3(n-4))` also leaves (2)
valid, so the tail proof need not rely on that finer table.

Together these bounds give the explicit finite inequality

\[
\begin{split}
R_n\le {}&33024\binom n4 2^{-3n}\\
&+\sum_{s=5}^{\lfloor n/4\rfloor}
 \binom ns(s!)^2 2^{-\lceil s/2\rceil(n-s)}\\
&+(n!)^2 2^{-n(n-3)/32}.
\end{split}\tag{9}
\]

## 4. The effective constant

Assume `n >= 1024`. The first term of (9) is at most
`1376*n^4*2^(-3n)`. The `s=5,6` terms are at most, respectively,

\[
3932160\,n^5 2^{-3n},\qquad
188743680\,n^6 2^{-3n}.
\tag{10}
\]

For `7 <= s <= 10`, put `d=ceil(s/2)` and use
`binom(n,s)(s!)^2 <= s!*n^s`. Each contribution is at most
`n^6*2^(-3n)`, since

\[
s!2^{ds} n^{s-6}2^{-(d-3)n}\le1.
\tag{11}
\]

The checker verifies (11) at `n=1024` with exact integers. It also
verifies `(1+1/1024)^(s-6) <= 2^(d-3)` as an exact rational inequality.
The ratio at every larger integer `n` is no greater, which proves (11)
on the entire infinite range; this is an endpoint certificate, not a fit.

For `11 <= s <= n/4`, use `binom(n,s)(s!)^2 <= n^(2s)` and
`2*log_2(n) <= n/16` to get

\[
n^{2s}2^{-\lceil s/2\rceil(n-s)}\le2^{-5sn/16}.
\]

The sum is bounded by `2*2^(-55n/16) <= 2*n^6*2^(-3n)`.
Finally, `2*log_2(n)+4 <= (n-3)/32` implies (8) is at most `2^(-4n)`.
Both logarithmic inequalities hold at 1024 and their differences have
positive derivative afterwards. The endpoint checks use the even larger
integer upper bound `log_2(1024) <= bit_length(1024)`.

Adding the constants and using `n^4,n^5 <= n^6` gives

\[
1376+3932160+188743680+4+2+1
=192677223<200000000,
\]

which proves (2). If the coarser support-four tail is used, replace 1376
by 98304; the total is still less than 200000000.

## Reproduction and status

Run `python check_quantitative.py --output quantitative_checks.json`.
The actual run computes all support histograms through `s=5`, compares
the resulting full expectations with a separate graph/row enumerator for
every `2 <= n <= 5`, and checks the sparse selection bound at three
rational edge probabilities. The direct expectations agree exactly with
`3, 15/2, 141/8, 3375/128`.

The finite coefficient calculation, universal written tail argument,
independent written review, and full Lean formalization are separate
verification layers. Only the first two are supplied for this new theorem.
The new result is a second-order strengthening candidate for independent
acceptance, not a retrospective acceptance of the entire old C66 package.
