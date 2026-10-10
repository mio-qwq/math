# Effective Burnside correction for unlabelled graph asymmetry

**Independent mathematical supplementary audit / C-audit-1010 / 2026-10-10 UTC.** This is a rigorous, elementary, **previously-known-in-spirit** random-graph enumeration estimate, presented as the missing detailed justification for the unlabelled step of the frozen [GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md](GLOBAL_NONTRIVIAL_INSTABILITY_ASYMPTOTIC.md). The source Problem 5.3 is Hujdurović–Mitrović, JGT 105 (2024), DOI 10.1002/jgt.23018. This is NOT itself a proof of the complete original asymptotic, a firstness claim, a ROOT independent approval, or a Lean theorem.

## Exact statement

Let \(g_m\) be the number of ordinary **unlabelled simple undirected** m-vertex graphs, and \(g_m^{\rm sym}\) the number of their isomorphism classes whose ordinary automorphism group is **nontrivial**. For every integer \(m\ge1024\),

\[
\boxed{
\frac{2^{\binom m2}}{m!}
\le g_m
\le \frac{2^{\binom m2}}{m!}\bigl(1+2^{-m/2}\bigr),
\qquad
\frac{g_m^{\rm sym}}{g_m}\le2^{1-m/2}.
}
\tag{B}
\]

This makes both the classical \(g_m\sim2^{\binom m2}/m!\) and the assertion that **almost all unlabelled graphs are asymmetric** quantitative, using only elementary permutation-support orbit counting plus the separately proved functional-entropy lemma. The threshold 1024 is intentionally conservative.

## 1. Burnside identity and fixed-edge orbits

Set \(E=\binom m2\). A vertex permutation \(\pi\in S_m\) acts on unordered possible graph edges. If \(e(\pi)\) is the number of its orbits on those E edges, then exactly \(2^{e(\pi)}\) labelled adjacency matrices are invariant under \(\pi\) (choose 0 or 1 per edge orbit). Burnside gives, **exactly**,

\[
g_m=\frac1{m!}\sum_{\pi\in S_m}2^{e(\pi)}
=\frac{2^{E}}{m!}(1+R_m),
\qquad R_m=\sum_{\pi\ne id}2^{e(\pi)-E}.
\]

The identity contributes precisely 1. It suffices to prove \(R_m\le2^{-m/2}\).

## 2. Small vertex-permutation support

Fix a nonidentity ordinary graph automorphism \(\pi\), with \(a=|\operatorname{supp}\pi|\), and suppose \(2\le a\le m/4\). Its a moved vertices break into \(c\) cycles, each length≥2, hence \(c\le a/2\). The m−a fixed vertices are individually invariant.

For each fixed old vertex w and each moved cycle C, the adjacency bits from w to C must be constant. The bipartite cut between moved and fixed vertices has \(a(m-a)\) potential edges but only \(c(m-a)\) freely chosen bits. Thus

\[
E-e(\pi)\ge(a-c)(m-a)\ge \frac{a(m-a)}{2}
\ge \frac{3am}{8}.
\]

At most \(\binom ma a!\le m^a\) permutations have support exactly a. The resulting contribution from all supports a≤m/4 is

\[
R_m^{\rm sparse}\le
\sum_{a=2}^{\lfloor m/4\rfloor}
m^a2^{-3am/8}.
\]

For m≥1024, \(\log_2m\le m/100\) (prove it at 1024, then note \(m^{100}/2^m\) decreases). Hence every summand is at most \(2^{-73am/200}\). With at most m summands and a≥2,

\[
R_m^{\rm sparse}\le m\,2^{-73m/100}
\le2^{-18m/25}.
\tag{S}
\]

## 3. Large vertex-permutation support

For \(a>m/4\), apply the **fully proved functional graph entropy lemma** from [EFFECTIVE_INSTABILITY_ASYMPTOTIC_AUDIT.md](EFFECTIVE_INSTABILITY_ASYMPTOTIC_AUDIT.md) to the ordinary automorphism TF pair \((\pi,\pi)\). It yields

\[
E-e(\pi)\ge \frac{a(m-3)}4
>\frac{m(m-3)}{16}.
\]

There are at most \(m!\le m^m\) such vertex permutations. Therefore

\[
R_m^{\rm dense}\le
m^m2^{-m(m-3)/16}
\le2^{-21m^2/400+3m/16}
\le2^{-m^2/20}
\tag{D}
\]

for m≥1024. The last inequality is elementary:
\((21/400-1/20)m^2=m^2/400\ge3m/16\) whenever m≥75.

Combining (S),(D),

\[
R_m\le2^{-18m/25}+2^{-m^2/20}\le2^{-m/2}
\quad(m\ge1024).
\]

This proves the first part of (B).

## 4. Convert the nonidentity Burnside weight to the **fraction of unlabelled symmetric graphs**

Let a graph-isomorphism class [G] have ordinary automorphism group of size \(k\). Its number of distinct labelings is \(m!/k\). Each such labelled representative contributes exactly k−1 nonidentity automorphism pairs. Consequently its contribution to the nonidentity Burnside sum divided by m! is

\[
\frac{(m!/k)(k-1)}{m!}=\frac{k-1}{k}.
\]

This is 0 for asymmetric classes, and at least 1/2 for each **symmetric** class (k≥2). Summing gives

\[
\frac{g_m^{\rm sym}}{2}
\le\frac{1}{m!}\sum_{\pi\ne id}2^{e(\pi)}
=\frac{2^E}{m!}R_m.
\]

Since \(g_m\ge 2^E/m!\), divide both sides by g_m and obtain

\[
\frac{g_m^{\rm sym}}{g_m}\le2R_m\le 2^{1-m/2}.
\]

This step is crucial: merely knowing that **labelled** symmetric graphs are rare does **not** immediately prove the same for **unlabelled** classes, because their label multiplicities differ. The weighted Burnside identity removes that gap exactly.

## 5. Independent finite original-definition audit

The separate standard-library-only checker [verify_burnside_unlabelled.py](verify_burnside_unlabelled.py) directly enumerates **every vertex permutation for each n=1,...,7**, computes its orbits on **unordered edge slots**, sums the exact integer \(2^{e(\pi)}\), and divides by n!. It reproduces the published all-unlabelled simple graph counts \(1,2,4,11,34,156,1044\) and verifies the nonidentity weight term. **Actual CPython 3.13.5/Linux run:** PASS for all permutations n=1..7, with zero third-party libraries. Executed source SHA-256 `5ef47dbcc54b59d751c5f708fb801ab602b2a8fadf817c9b362b6e361ce8ef7a`, Git blob `9c1dccfd59cd611681c7f3453e927d500c58f713`. The **symbolic proof above**, not finite enumeration, covers all m≥1024.

## Scope and next remaining gap

This completely fills the formerly brief “almost all unlabelled old graphs are asymmetric” input to the candidate Problem 5.3 proof, with a strong explicit error. It does NOT automatically turn the previous **unlabelled** asymptotic into a finite-threshold error bound, because other exceptional sources (unlabelled graph collisions, nonminimal TF pairs, and unusual old-graph conditions) must still be combined. The **labelled** formula, however, now has an independently written effective remainder in [EFFECTIVE_INSTABILITY_ASYMPTOTIC_AUDIT.md](EFFECTIVE_INSTABILITY_ASYMPTOTIC_AUDIT.md).

No ROOT acceptance, external peer review, Lean proof, signed main integration, historic originality claim, new project number, author contact, PR or manuscript submission is claimed. Keep all earlier frozen objects unchanged.
