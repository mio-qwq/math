# Effective, finite-threshold error bounds for Bychawski Conjecture 6.6

**Agent C-audit-1010, 2026-10-10 UTC.** This is a supplementary **unaccepted mathematical proof candidate**. The exact original source and reduced-domain ambiguity are addressed in [BYCHAWSKI_C66_EXPECTED_TF_GROUP.md](BYCHAWSKI_C66_EXPECTED_TF_GROUP.md). Original: Bychawski arXiv:2406.06267v1, Conjecture 6.6, Definition 1.4 and Proposition 1.6. No universal Lean proof, external independent acceptance, journal peer review or historical-priority claim is implied.

Let `G_n` be uniformly random on labelled simple graphs with n vertices. Let `T(G)` be the **full TF group** of ordered permutation pairs, `P(G)` its first-coordinate projection (canonical extension to all graphs), and `R_n` the event that G is open-neighbourhood-twin-free. Put `b=binom(n,2)`.

**Theorem candidate, with EFFECTIVE constants:** for every integer **n>=1024**,

\[
0\le\mathbb E|T(G_n)|-1-b\,2^{-(n-3)}\le2^{13}n^4 2^{-2n},
\]
\[
0\le\mathbb E|P(G_n)|-1-b\,2^{-(n-2)}\le2^{13}n^4 2^{-2n},
\]
\[
\left|\mathbb E(|\operatorname{Aut}^{\pi}(G_n)|\mid R_n)-1-b\,2^{-(n-1)}\right|
\le 2^{16}n^4 2^{-2n}.
\]

All formulas are exact finite inequalities, unlike unspecified big-O error symbols. They give the **affirmative limit** asserted by original Conjecture 6.6 in all interpretations (defined only on reduced graphs, versus natural all-graph projection extension). They also show why full TF and projected TF expectation have **different first corrections**.

## 1. Sharpen the general support tail with explicit integer constants

The full proof's global support lemma says a fixed ordered TF pair with support union S of size s and t orbits under the generated group loses >=(s-t)(n-s)>=ceil(s/2)(n-s) independent graph-edge bits; t<=floor(s/2). Define Q as the total **expected contribution** of every TF pair with union support s>=3. We prove

\[
Q\le 2^{13}n^4 2^{-2n}\qquad(n\ge1024).\tag{T}
\]

For `3<=s<=n/4` bound the number of ordered pairs with exactly S by `binom(n,s)(s!)^2`. The s=3 contribution is at most

\[
\binom n3(3!)^2 2^{-2(n-3)}\le384n^3 2^{-2n}.
\]

The s=4 contribution is at most

\[
\binom n4(4!)^2 2^{-2(n-4)}\le6144n^4 2^{-2n}.
\]

The s=5,6 contributions are together bounded by `2*n^12*2^(-3n+18)<=2*n^4*2^(-2n)` for n>=1024. This is because `n^8*2^18<=2^n` for every integer n>=1024: it holds at n=1024, and the ratio `2^n/n^8` increases thereafter.

For 7<=s<=n/4, using `n-s>=3n/4`, `ceil(s/2)>=s/2`, and `2log_2 n<=n/16` for n>=1024, each contribution is bounded by

\[
n^{2s}2^{-\lceil s/2\rceil(n-s)}\le2^{-5sn/16}.
\]

The sum starts at s=7 with exponent <=−35n/16, hence its whole sum is at most `n*2^(-35n/16)<=n^4*2^(-2n)` (since `n<=2^(3n/16)` for n>=1024). This replaces any unverified extrapolation from finite support scans.

For s>n/4, at least one TF permutation moves `a>n/8` vertices. The direct functional-constraint graph argument in the primary proof gives at least `a(n-3)/4>n(n-3)/32` independent constraints. Over all <=(n!)^2 pairs the large-support expectation is at most

\[
(n!)^2 2^{-n(n-3)/32}
\le2^{-9n^2/800+3n/32}\le n^4 2^{-2n}
\quad(n\ge1024),
\]

where `log_2 n<=n/100` bounds `2nlog n<=n²/50` and the last comparison uses `(9/800)n>=67/32` for n>=1024.

Thus the sum of all terms is at most

\[
(384+6144+2+1+1)n^4 2^{-2n}=6532n^4 2^{-2n}<2^{13}n^4 2^{-2n},
\]

proving (T). The full ordered TF and natural projected expectation inequalities follow immediately from the exact support-two classifications; the larger-support correction to the latter can be no bigger than Q, since multiple TF pairs sharing the same projected α are counted only once in P.

## 2. Condition on reduced graphs with a quantitative error

The open-twin union bound gives `Pr(R_n^c)<=b*2^{-(n-1)}`. For n>=1024 this is <1/2.

Fix a transposition τ=(xy). Its diagonal ordinary-automorphism event with edge xy present has exact probability `p=2^{-(n-1)}`; it is the only **support-two TF mechanism** for τ on reduced graphs. Conditional on this true-twin event, x and y cannot have open twins involving any other vertex. The probability any two vertices z,w outside `{x,y}` are open twins is `2^{-(n-2)}`: their own mutual edge must be zero, their edges to n−4 other outside vertices must agree, and their common connections to x,y must agree. Hence

\[
0\le p-\Pr(R_n\wedge\tau\in\operatorname{Aut}(G_n))
\le p\binom{n-2}{2}2^{-(n-2)}.
\]

For all first-coordinate projected permutations beyond transpositions, and all non-diagonal TF representations of a transposition with union support>=3, the full expected contribution is <=Q even before restricting to R_n. Divide their joint expectation by `Pr(R_n)` and use

\[
1- b2^{-(n-1)}\le\Pr(R_n)\le1,
\quad b2^{-(n-1)}\le1/2.
\]

A direct upper and lower subtraction yields

\[
\left|\mathbb E(|Aut^\pi(G_n)|\mid R_n)-1-bp\right|
\le bp\binom{n-2}{2}2^{-(n-2)}
+\frac{(bp)^2+Q}{1-bp}.
\]

Use `b<=n²/2`, `p=2^{-(n-1)}` and (T). The first term is <=`2n^4*2^(-2n)`, the second <=`2(1+2^13)n^4*2^(-2n)`. Their sum is <`2^16*n^4*2^(-2n)`, as claimed. This finite inequality is the stated **conditional** version, not a silent assertion that the undefined original Aut^π exists on every graph.

## 3. Reproducibility and sign-off scope

Independent exact arithmetic implementation [audit_bychawski_tail_threshold.py](audit_bychawski_tail_threshold.py) verifies the finite arithmetic comparisons at 203 selected integers n>=1024 (n=1024..1223 and 2048,4096,8192). Actual run with CPython 3.13.5 on Linux, standard library only: PASS, SHA-256 `e36b6a4132e719b7ffa45a71a266455984e04d968da9e9b4c4e26666242b9b51`. This finite check is a **regression test**, not the universal mathematical proof: every inequality across the infinite range is justified by explicit symbolic comparisons above. The independent full ordered-edge DSU test for n=2..5 and separate n=4 complete graph enumeration lives in [bychawski_expectation_exact.py](bychawski_expectation_exact.py), SHA-256 `46f13488d3fa2302b226e8154af60d91767484ffebf96156742012c350791aca`.

**Review priorities:** (i) check source Definition1.4 domain / Conjecture6.6 quantifier mismatch; (ii) full probability for each of the three support-two TF pairs; (iii) the group-orbit loss across outside vertices; (iv) the functional-graph independent-rank lemma, including zero-target constraints; (v) the projected expectation count does not double count α; and (vi) reduced conditional true twins. Historical originality not certified, and no ROOT independent acceptance/Lean compilation claimed. Do not rewrite frozen discoveries or claim a numbered 007/008, merge, PR, submission or author contact.
