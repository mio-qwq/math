# Effective unlabelled Problem 5.3 asymptotic: collision-free counting

**Agent C-audit-1010 / 10 October 2026 UTC.** This is a **separately frozen, complete mathematical proof candidate** strengthening the earlier global asymptotic manuscript by giving a concrete finite threshold and exponential error for the **unlabelled** count. ROOT's genuine independent acceptance, Lean formalization, human peer review and historical firstness remain pending. All previously frozen sources are preserved unchanged.

## Original source and exact scope

Hujdurović–Mitrović, *Some conditions implying stability of graphs*, *Journal of Graph Theory* 105 (2024), 98–109, DOI 10.1002/jgt.23018, **Problem 5.3**: approximate the number of nontrivially unstable finite simple graphs of order n. The original class is connected, nonbipartite, and **open-neighbourhood-twin-free**, with an unexpected automorphism of the canonical bipartite double cover. Its **Construction 5.1 / Proposition 5.2** is the source of the four-new-vertex gadget (a PRIOR construction, not new here). Source was checked directly on 2026-10-10: https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.23018 .

Let \(U_n\) be the number of **unlabelled isomorphism classes** in this exact class. Put

\[
m=n-4,\qquad
H_n=\frac{2^{\binom m2+2m-1}}{m!}.
\]

**Quantitative unlabelled theorem candidate:**

\[
\boxed{\quad
n\ge4096\quad\Longrightarrow\quad
\left|\frac{U_n}{H_n}-1\right|\le2^{-n/4}.
\quad}\tag{U}
\]

The earlier frozen full-asymptotic formula is the \(n\to\infty\) consequence \(U_n\sim H_n\). It also implies
\(U_n/g_n\sim2(n)_4/4^n\), where \(g_n\) is the number of all unlabelled graphs. The explicit threshold is deliberately conservative; it is **not estimated from finite graph samples**.

**Dependencies now proved within this isolated research packet:**

- [EFFECTIVE_INSTABILITY_ASYMPTOTIC_AUDIT.md](EFFECTIVE_INSTABILITY_ASYMPTOTIC_AUDIT.md): TF support≤4 *pure combinatorial classification*; full-support functional equality graph lemma with entropy deficit at least \(n(n-3)/32\).
- [BURNSIDE_UNLABELLED_SYMMETRY_AUDIT.md](BURNSIDE_UNLABELLED_SYMMETRY_AUDIT.md): for all q≥1024, \(2^{\binom q2}/q!\le g_q\le(1+2^{-q/2})2^{\binom q2}/q!\) and the fraction of unlabelled graphs with nontrivial ordinary automorphisms is at most \(2^{1-q/2}\).

Neither named audit has been independently accepted by ROOT. The next argument uses their **proved formulas**, not their finite regression tests.

## 1. Almost every **unlabelled** old graph X is admissible and asymmetric

Let \(m=n-4\ge4092\). We need X to be connected, nonbipartite, twin-free, and ordinarily asymmetric. Show their unlabelled failure fraction

\[
\varepsilon_m:=\frac{\#\{\text{unlabelled m-vertex X failing any condition}\}}{g_m}
\le 2^{-m/3}.
\tag{1}
\]

Here are four individually rigorous upper bounds:

**(a) Automorphisms:** From the separately proven Burnside estimate the symmetric fraction is at most \(2^{1-m/2}\).

**(b) Twins:** In a graph with open-neighbourhood twins, choose one unordered twin pair, delete it and keep the remaining unlabelled (m−2)-vertex graph, plus a common-neighbour subset of its vertices. Such a description has at most \(g_{m-2}2^{m-2}\) possibilities (the twin pair is nonadjacent, since adjacent vertices cannot have identical open neighbourhoods). For m−2≥1024, the Burnside upper and lower bounds give the fraction at most

\[
2m(m-1)2^{-(m-1)}.
\]

**(c) Bipartiteness:** A labelled bipartite graph is counted by some 0/1 vertex colouring, with at most \(\lfloor m^2/4\rfloor\) possible cross edges. Therefore the **unlabelled** number is at most the labelled bound \(2^{m+\lfloor m^2/4\rfloor}\), giving the fraction

\[
\le m!\,2^{m+\lfloor m^2/4\rfloor-\binom m2}
\le2^{-\frac15m^2}\quad(m\ge4092).
\]

**(d) Disconnectedness:** A disconnected graph has a component of order \(1\le k\le m/2\), so the unlabelled number is at most \(\sum_{k=1}^{\lfloor m/2\rfloor}g_k g_{m-k}\). Use the trivial \(g_k\le2^{\binom k2}\), the Burnside upper bound for \(m-k\ge m/2\ge1024\), and the lower bound for \(g_m\). The failure fraction is at most

\[
\sum_{k=1}^{\lfloor m/2\rfloor}
2\,\frac{m!}{(m-k)!}2^{-k(m-k)}
\le2m\,2^{-m/2+\log_2m}
\le2^{1-\frac{12}{25}m},
\tag{2}
\]

where \(\log_2m\le m/100\) for m≥1024.

These four contributions sum to at most \(2^{-m/3}\) throughout m≥4092 (the weakest exponent is still substantially stronger than −m/3). This proves (1). Unlike a bare assertion about “almost all random graphs,” this controls actual **unlabelled isomorphism classes**.

## 2. Actual number of unordered admissible attachment choices

For any unlabelled old graph X of order m whose ordinary automorphism group is trivial, choose two **distinct nonempty** subsets A,B of its m vertices, with their order disregarded. Their number is exactly

\[
P_m=\binom{2^m-1}{2}
=2^{2m-1}\bigl(1-3\cdot2^{-m}+2^{1-2m}\bigr).
\tag{3}
\]

Attach the four new vertices according to the authors' Construction 5.1 (either cross matching yields the *same unlabelled output* after swapping the names within one new pair). Because X is connected, nonbipartite and twin-free, each output Y satisfies the **full original nontrivial-instability definition** by the authors' published Proposition 5.2. Different unordered {A,B} can represent the same output only if an isomorphism changes its special four-vertex partition; if the output has a **unique minimal TF support partition**, no such collision occurs. In that case an isomorphism necessarily preserves the four-set, induces an isomorphism of the old X's, and sends {A,B} to itself; since X is asymmetric, different input pairs never collide.

The classification of minimal patterns is an **actual mathematical theorem** in the separate effective-audit note, not an assumption that all unexpected cover automorphisms come from the source gadget.

## 3. Nonminimal TF structures: negligible **unlabelled**, not merely labelled

The original global manuscript bounds the unlabelled graphs with a non-diagonal TF pair whose union support has size s, excluding the canonical s=4,t=2 case. For \(\Gamma=\langle\alpha,\beta\rangle\), t≤⌊s/2⌋, and for every unlabelled (n−s)-vertex graph X on the fixed complement there are at most \(2^{t(n-s)+\binom s2}\) possible induced/attachment patterns for one abstract pair (α,β). Summing over at most \((s!)^2\) abstract pairs yields

\[
V_{n,s}\le (s!)^2g_{n-s}\,
2^{\,t(n-s)+\binom s2}
\quad(5\le s\le n/4),
\tag{4}
\]

with t replaced by ⌊s/2⌋ for an upper bound. The s=4,t=1 exceptional TF pairs obey the same bound with t=1. The s≤3 and the other s=4,t=2 cases are impossible for twin-free graphs by the **direct structural proof** in the effective-audit note.

Because n−s≥3n/4≥3072, the Burnside bound gives \(g_{n-s}\le2^{\binom{n-s}2+1}/(n-s)!\). Dividing (4) by \(H_n=2^{\binom n2-2n+3}/(n-4)!\), using
\((n-4)!/(n-s)!\le n^{s-4}\), \((s!)^2\le n^{2s}\), yields

\[
\frac{V_{n,s}}{H_n}
\le2 n^{3s-4}
2^{-\lceil s/2\rceil(n-s)+2n-3}.
\tag{5}
\]

For s=5,6, the sum of these bounds is at most \(2^{-4n/5}\). For 7≤s≤n/4, using \(\log_2n\le n/100\) and n−s≥3n/4, their sum is at most \(2^{-2n/5}\) (the worst exponent is at s=7). The s=4,t=1 term is ≤\(2\cdot(4!)^2 2^{-n+9}\).

For s>n/4, the improved **labelled** full-support count from the functional graph lemma is also a valid upper bound on the **unlabelled** number. After dividing by H_n and bounding \((n!)^2(n-4)!\le n^{3n}\),

\[
\frac{V_{n,\mathrm{dense}}}{H_n}
\le2^{-n^2/800+(67/32)n}
\le2^{-n^2/2000}\quad(n\ge4096).
\tag{6}
\]

Combining (5),(6) and s=4,t=1, the number \(V_n\) of unlabelled qualifying graphs with **no canonical minimal TF pattern** obeys the conservative bound

\[
\boxed{V_n/H_n\le2^{-n/3}\qquad(n\ge4096).}
\tag{7}
\]

## 4. An upper bound on **unlabelled multiple-pattern collisions**

Let Q_n count unlabelled graphs with **at least two distinct minimal disjoint-transposition TF support partitions**. For a pair of patterns, their union S has size 4≤s≤8, and the four corresponding swaps generate a permutation group on S with at most t orbits satisfying **s−t≥3**. If s=4 and the partitions differ, the group is transitive; if s≥5, every orbit has size≥2. Thus their external adjacency has at least 3(n−s) lost independent binary bits.

There are at most \((s!)^4\) abstract ordered pairs of TF patterns on an abstract s-set. With \(g_{n-s}\) choices of the unlabelled graph on the complement, at most \(2^{\binom s2+t(n-s)}\) internal and external patterns, so

\[
Q_n\le \sum_{s=4}^8 (s!)^4
g_{n-s}\,2^{\binom s2+t(n-s)}
\]

with the actual t for each pair. After replacing \(g_{n-s}\le2^{\binom{n-s}2+1}/(n-s)!\), using s−t≥3 and \((n-4)!/(n-s)!\le n^4\),

\[
\frac{Q_n}{H_n}\le
10(8!)^4 n^4\,2^{-n+21}
\le2^{-n/2}\quad(n\ge4096).
\tag{8}
\]

This bound counts the **number of bad isomorphism classes**, not just labelled graphs. A single such graph has at most \(K_n=3\binom n4\le n^4\) possible minimal support partitions; for each fixed partition the complementary old graph and unordered attachments are determined up to isomorphism. Hence **at most K_n of our unlabelled (X,{A,B}) representations can be lost per bad graph**. Equations (8) and \(K_n\le n^4\) imply that the number of lost representations, divided by H_n, is at most \(2^{-2n/5}\) for n≥4096.

This is the precise point at which a naive appeal to random labelled graphs would be inadequate.

## 5. Upper and lower counts; explicit effective rate

**Lower bound.** Among the g_m unlabelled old graphs, a fraction at least \(1-\varepsilon_m\) is admissible and asymmetric. Each contributes the \(P_m\) unordered pairs of distinct nonempty subsets from (3). Outside the graphs with multiple patterns, each representation gives a different unlabelled Y. Thus

\[
U_n\ge g_m(1-\varepsilon_m)P_m-K_nQ_n.
\]

Use \(g_m\ge 2^{\binom m2}/m!\), (1), (3) and (8):

\[
\frac{U_n}{H_n}
\ge1-2^{-m/3}-3\cdot2^{-m}-2^{-2n/5}.
\tag{9}
\]

**Upper bound.** Every qualifying graph with a canonical minimal pattern is isomorphic to a four-vertex gadget over some **unlabelled** m-vertex old graph, with at most \(\binom{2^m+1}2=2^{2m-1}(1+2^{-m})\) choices of unordered attachment subsets **allowing repetitions**. Those with no minimal pattern are covered by \(V_n\). Therefore

\[
U_n\le g_m\,2^{2m-1}(1+2^{-m})+V_n.
\]

Use \(g_m\le (1+2^{-m/2})2^{\binom m2}/m!\) and (7):

\[
\frac{U_n}{H_n}
\le (1+2^{-m/2})(1+2^{-m})+2^{-n/3}.
\tag{10}
\]

For every n≥4096, both absolute deviations in (9),(10) are strictly less than \(2^{-n/4}\) (their largest term is of scale \(2^{-n/3}\), leaving a large exponential margin). This proves the effective unlabelled candidate theorem (U).

## 6. Independent arithmetic diagnostic; review obligations

[ audit_unlabelled_threshold.py ](audit_unlabelled_threshold.py) checks the **exact integer threshold inequalities** supporting (6),(8),(9),(10) for 28 chosen n≥4096, including the first 24 consecutive integers and n=16384. It is a falsification test; **the universal proof is the symbolic argument above**, not extrapolation from 28 cases.

Actual CPython 3.13.5/Linux run: PASS 28 threshold parameter values; source SHA256 `235a32f47cbc240c158c6c86278a0afd66f8aabcf336fa47712951a7fca3950c`, Git blob `3295b087bb0039ddd886c78b6b0d9a88377167d6`. Related independently executed sources: `audit_functional_entropy.py` (18,862 permutations), `verify_burnside_unlabelled.py` (all permutations for 1≤m≤7), and the three earlier original-definition finite TF/support checkers.

**Mandatory ROOT challenges:** check the exact source quantifiers; the support≤4 structural lemma; the functional-graph entropy proof for arbitrary overlapping α,β; the explicit *unlabelled* Burnside numerator rather than naive division of labelled rare graphs; the s-orbit marked upper bound (4); the treatment of two minimal support partitions with the same four vertices; and the claim of at most K representations per collided unlabelled graph. Source attribution and possible earlier equivalent asymptotics must be checked before any statement of historical originality. No universal Lean, independent ROOT acceptance, paper submission, merged main, signed release, or author contact is claimed.

**Deliverable:** strictly stronger **unlabelled error theorem candidate** with all explicit constants and a reproducible exact-arithmetic diagnostic. This is not an additional numbered 007/008 result. All previous frozen files are preserved.
