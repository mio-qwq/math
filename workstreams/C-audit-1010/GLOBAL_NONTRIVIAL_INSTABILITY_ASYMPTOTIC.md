# Asymptotic enumeration of nontrivially unstable graphs — full proof candidate

**Agent C-audit-1010 | 10 October 2026 | independent-discovery manuscript, NOT ROOT accepted, Lean compiled, historically certified novel, peer-reviewed or submitted.** This supersedes only the *bound*, not the frozen bytes, of the two earlier Problem 5.3 lower-bound notes. The proof below has been independently checked against finite raw-TF diagnostics **within this same research instance**; a genuinely uninvolved mathematical review is still needed.

## Original public question

Hujdurović and Mitrović, *Some conditions implying stability of graphs*, Journal of Graph Theory **105** (2024), 98–109, DOI 10.1002/jgt.23018, **Problem 5.3**: find an approximation formula for the number of nontrivially unstable graphs on n vertices. Paper source: https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.23018 ; original preprint arXiv:2210.15249. A graph is **nontrivially unstable** precisely when it is finite simple, connected, nonbipartite, open-neighbourhood-twin-free, and its canonical double cover has automorphisms outside Aut(G)×C2. The authors' **Construction 5.1 / Proposition 5.2**, adding two pairs of vertices, is **prior work**. Our counting reuses it; no new construction priority is asserted. Literature search 2026-10-10 (journal, author followups, 2024–2026 random graph/TF literature) found no confirmed same-scope asymptotic equivalent; unindexed papers and historical priority remain unresolved.

Let L_n be the **labelled** count on [n], U_n the **unlabelled graph-isomorphism class** count in this exact class. Let g_n be the number of all unlabelled simple graphs, and (n)_4=n(n-1)(n-2)(n-3).

## Candidate full answer to the original asymptotic question

As n→∞:

\[
\boxed{ L_n \sim 3\binom n4\,2^{\binom{n-4}{2}+2(n-4)+1}. }\tag{A}
\]

\[
\boxed{ U_n \sim \frac{2^{\binom{n-4}{2}+2(n-4)-1}}{(n-4)!}. }\tag{B}
\]

Consequently, using g_n∼2^{\binom n2}/n!,

\[
\boxed{\frac{U_n}{g_n}\sim\frac{2(n)_4}{4^n}.}\tag{C}
\]

Thus the proportion of all unlabelled graphs that are nontrivially unstable tends to zero at an **explicit leading exponential rate**. Almost all nontrivially unstable graphs are, **uniquely up to interchanging the two appended pairs**, members of the authors' four-vertex Construction 5.1. This theorem would answer their Problem 5.3 **if independently validated**; neither the paper nor the small tests supply an acceptance receipt.

## 1. Canonical double cover and exact TF symmetry

For a connected nonbipartite simple graph G, CDC(G) is a connected bipartite graph, so every cover automorphism either preserves or interchanges the two bipartition classes. Compose a class-swapping automorphism with the natural deck flip to make it class-preserving. It then acts as (u,0)↦(α(u),0), (u,1)↦(β(u),1) and preserves every cover edge **and nonedge** exactly when

\[
\forall u,v,\qquad A_{uv}=A_{\alpha(u),\beta(v)}.\tag{TF}
\]

The expected factor automorphisms correspond exactly to **diagonal** pairs α=β. Hence a graph in the original source class is unstable iff some **non-diagonal** (α,β) satisfies (TF).

For such a pair let S=supp(α)∪supp(β), s=|S|, W=[n]\S, m=n-s. Let Γ=⟨α,β⟩ acting on S, and t be its number of vertex orbits. Every orbit has at least two vertices, since S contains no common fixed point. Thus t≤⌊s/2⌋.

For each w∈W, (TF) and its transposed equality force the neighbourhood indicators A_{uw}, u∈S, to be constant on each Γ-orbit. Therefore **at least**

\[
(s-t)(n-s)\tag{1}
\]

of the \(\binom n2\) independent possible edge bits are lost. In particular the total number of labelled graphs satisfying one fixed pair is at most \(2^{\binom n2-(s-t)(n-s)}\). This is only a safe upper bound; the internal edges of S may impose more constraints and forbid some pairs altogether.

## 2. Exact four-vertex leading pattern and its finite-support uniqueness

First suppose α=(a_1 a_2), β=(b_1 b_2) are two **disjoint transpositions**, and put m=n−4. Then (TF) is equivalent to the following **entire** original edge list:

- G[W] arbitrary;
- both a-vertices join the same arbitrary subset A⊆W, and both b-vertices the same arbitrary subset B⊆W;
- a_1a_2 and b_1b_2 are absent;
- the 2×2 cross adjacency between the a-pair and b-pair is \(\begin{pmatrix}p&q\\q&p\end{pmatrix}\).

This is checked by substituting all ordered pairs into (TF). Since G is twin-free, p≠q (otherwise the a-pair are twins). Hence the cross edges are **exactly one of two perfect matchings**; this is precisely the source's Construction 5.1 up to relabelling the b-pair. For this **fixed unordered pair of disjoint two-vertex supports** the number of *potential* twin-free graphs before any other graph condition is imposed is at most, and up to events with vanishing probability exactly,

\[
M_n=2^{\binom m2+2m+1}=2^{\binom n2-2n+3}.\tag{2}
\]

There are \(K_n=3\binom n4\) unordered partitions of four vertices into two pairs. Switching α and β gives the *same* condition by symmetry of G.

**Small-support structural lemma.** If a non-diagonal TF pair acts on s≤3 vertices, G cannot be twin-free. If s=4 and t=2, then among twin-free graphs the only possible non-diagonal TF pair has the two disjoint transpositions above (up to swapping α,β).

Here is a complete finite-case proof, not a random search:
- If α or β is identity while the other is not, (TF) makes two rows/columns identical, yielding twins.
- For s=2 the other possibility is diagonal α=β, excluded.
- For s=3 with both nontrivial, Γ is transitive. With two **different transpositions**, images of the three forbidden diagonal entries force all three S-internal edges absent. With a 3-cycle and an unequal 3-cycle, the pair is (γ,γ^{-1}); all S-internal edges are forbidden by iterating the odd-orbit TF relation. With a 3-cycle and a transposition, iterating a diagonal entry along the 6-element directed TF orbit forces all three internal edges absent. In each case all three S vertices share their external neighbours because Γ is transitive, so they are twins.
- For s=4,t=2, Γ has precisely two size-two orbits A_0,B_0. Both α and β restrict to either swap or identity on each. If one permutation is identity, twins result. Otherwise, if α,β are not the opposite **single swaps**, then on one orbit both swap and on the other orbit only one swaps. The latter orbit's two vertices have no internal edge and have identical adjacency to every outside vertex **including** the both-swapped orbit (use the full four TF cross equations); they are twins. The only surviving pattern is the disjoint pair of single transpositions.

**Caution:** the nonminimal four-support pair α=(a_1 a_2)(b_1 b_2), β=(a_1 a_2) can have the **same raw number of free edge bits** as the leading pair. It is excluded ONLY by the original twin-free requirement. A naive entropy-only exclusion is **false**, as caught by the exact checker. Four-support t=1 cases are not excluded, but (1) loses ≥3(n−4) bits and they are asymptotically negligible.

## 3. All other TF symmetries are negligible: full-support union bound

We give the missing **global upper bound**, without assuming that a random graph automatically has no other cover automorphism.

### 3a. Support 5≤s≤n/4

For a fixed s and a fixed pair, (1) loses at least \(\lceil s/2\rceil(n-s)\) bits. There are no more than \(\binom ns(s!)^2\le n^{2s}\) choices of a pair with support S of size s. Therefore the number of **labelled** graphs with at least one such pair is bounded by

\[
\sum_{s=5}^{\lfloor n/4\rfloor}
n^{2s}2^{\binom n2-\lceil s/2\rceil(n-s)}.
\tag{3}
\]

This is \(o(2^{\binom n2-2n})\): the individual s=5,6 terms lose \(3n-O(1)\) bits and have only polynomially many choices; for s≥7, use n−s≥3n/4 to obtain loss≥3sn/8, which outruns 2s log₂n+2n uniformly in that range. The s=4,t=1 exceptional family likewise loses 3(n−4) bits and is negligible.

### 3b. Support s>n/4: independent equalities give a quadratic entropy deficit

At least one of α,β moves at least n/8 vertices. By interchanging α,β if needed, suppose α moves a≥n/8. Relabel the vertices so these a come first. Choose each unordered edge {u,v} with u moved by α and u earlier than v. There are

\[
M=a(n-a)+\binom a2 \ge a(n-1)/2
\]

such edges. The TF equation associates to it either a forced zero (if α(u)=β(v)) or an equality between the source edge bit and the edge bit {α(u),β(v)}. The latter is tautological only if α(u)=v and β(v)=u, which holds for at most **a** selected edges. Hence at least \(M-a\ge a(n-3)/2\) constraints are nontrivial.

Every unordered edge bit occurs as a selected source in at most one constraint, and can occur as target in **at most two** constraints (invert the ordered bijections α,β). Thus its total incidence is at most three. Greedily keep a set of pairwise variable-disjoint constraints: one chosen constraint involves at most two variables and deletes at most six constraints. We keep at least \((M-a)/6\ge n(n-3)/96\) **independent** equalities or zero-bit constraints. Each halves the number of assignments. Therefore for **every** such permutation pair,

\[
\#\{G\text{ satisfying (TF)}\}
\le2^{\binom n2-n(n-3)/96}.
\]

There are at most (n!)² permutation pairs, so the total number of these graphs is
\(2^{\binom n2-\Omega(n^2)}\), negligible even relative to the **unlabelled** main term after dividing by no factorial at all.

### 3c. Unlabelled upper bound for all small-support unwanted pairs

Let \(g_m\) be the number of unlabelled m-vertex graphs. Fix s, α,β on an **abstract marked s-set**, and an unlabelled graph X on W (size m=n−s). The internal S graph has at most \(2^{\binom s2}\) possibilities and each w∈W has only 2^t allowed adjacency signatures to S. Thus the number of unlabelled graphs *marked with at least one such symmetry* is at most

\[
(s!)^2\,g_{n-s}\,2^{\,t(n-s)+\binom s2}.\tag{4}
\]

This counts every target graph at least once, so it is a valid **upper bound** even though different markings can identify the same underlying graph. The classical all-graphs asymptotic \(g_m\sim2^{\binom m2}/m!\) makes the sum of (4) over s=5,...,⌊n/4⌋, plus s=4,t=1, equal to

\[
o\!\left(\frac{2^{\binom{n-4}{2}+2(n-4)-1}}{(n-4)!}\right).\tag{5}
\]

For example, when s=5 or 6, the ratio to the proposed main term is \(n^{O(1)}2^{-n+O(1)}\); for s≥7 the entropy loss rises at least linearly with s. Together with §3b, **every qualifying graph without a minimal disjoint-transposition TF pair is negligible in the unlabelled count.**

## 4. Distinct minimal patterns almost never overlap

Take two *different unordered* partitions of four marked vertices into a-pair and b-pair, and let S be the union of their supports, 4≤s≤8. If s=4, the partitions differ, and their four constituent transpositions generate a **transitive** action on S: t=1. If s≥5, the combined group has no common fixed point, so t≤⌊s/2⌋. Hence in every case

\[
s-t\ge3.
\]

External adjacency constraints to W=[n]\S lose at least \(3(n-s)\ge3(n-8)\) free bits. Counting the at most \((s!)^4\) ways to mark the two patterns, and using the unlabelled X∈\(\mathcal G_{n-s}\) bound just as in (4), proves that the number of unlabelled graphs admitting **two distinct minimal patterns** is

\[
o\!\left(\frac{2^{\binom{n-4}{2}+2(n-4)-1}}{(n-4)!}\right).\tag{6}
\]

The corresponding **labelled** two-pattern overlap also is \(O(n^8 2^{\binom n2-3(n-8)})=o(K_n M_n)\). Thus the K_n leading patterns are asymptotically disjoint. **They can overlap at small n**; we have not incorrectly assumed literal disjointness.

## 5. Pass from a canonical minimal pattern to unlabelled graphs

The following classical facts about G(m,1/2) are standard; for completeness they follow from the same sparse/dense permutation-support bounds above for *ordinary* pairs α=β and Burnside's lemma: (i) \(g_m\sim 2^{\binom m2}/m!\); (ii) all but o(g_m) unlabelled m-vertex graphs are **asymmetric**, connected, nonbipartite and twin-free. Connectivity/bipartiteness/twin-freeness themselves have elementary vanishing-probability union bounds (see the previous lower-bound note); the nontrivial-automorphism sum is \(o(2^{\binom m2})\).

Now let m=n−4. For almost all unlabelled old graphs X, Aut(X)=1 and X satisfies the original source conditions. Choose any two **distinct nonempty** subsets A,B⊆V(X); there are

\[
\binom{2^m-1}{2}=(1+o(1))\,2^{2m-1}
\]

unordered choices. Attach the published four-vertex matching gadget with the two pairs assigned to A and B. The result is connected, nonbipartite, twin-free and unstable by Proposition 5.2 (or by the exact CDC automorphism). As shown in §4, only a negligible number of these outputs have more than one minimal pattern. For those with a **unique** minimal unordered TF pattern, its support and the two unordered 2-vertex blocks are intrinsic. An isomorphism of two such augmented graphs restricts to an isomorphism of their old induced X, and can only interchange A,B; the matching orientation is eliminated by relabelling one appended pair. Since X is asymmetric, **two different unordered {A,B} produce nonisomorphic outputs**.

This gives the lower bound \(U_n\ge(1-o(1))\,g_m\,2^{2m-1}\). Conversely, every qualifying graph with exactly one minimal pattern is isomorphic to a graph produced by some old X and unordered A,B, hence contributes at most \(g_m\binom{2^m+1}{2}=(1+o(1))g_m2^{2m-1}\) possibilities. By (5) and (6), graphs with no minimal pattern or multiple minimal patterns are negligible. Therefore

\[
U_n\sim g_m2^{2m-1}
\sim \frac{2^{\binom m2+2m-1}}{m!},
\]

proving **(B)**. For the **labelled** form, each of the K_n support partitions has \((1-o(1))M_n\) valid labelled graphs and overlaps are negligible by §4. This proves **(A)**.

Finally \(g_n\sim2^{\binom n2}/n!\) and

\[
\binom n2-\Big(\binom{n-4}{2}+2(n-4)-1\Big)=2n-1
\]

give \(U_n/g_n\sim(n)_4/2^{2n-1}=2(n)_4/4^n\). This proves **(C)**.

## 6. Falsification diagnostics and comparison with the original published table

The independently implemented **original-definition** Python program \`verify_global_support.py\` checks every TF permutation pair on 2,3,4 moving vertices against *every possible induced S-edge pattern*, testing exactly whether a pair of vertices forced to have equal outside adjacency must be twins:

| | Exact local survivors with no **forced** twins | Interpretation |
|---|---:|---|
| s=2 | 0 | all non-diagonal cases impossible in twin-free graphs |
| s=3 | 0 | same |
| s=4,t=2 | 12 ordered-pair/internal-mask cases | precisely the two disjoint transpositions |
| s=4,t=1 | 36 ordered-pair/internal-mask cases | genuine nonminimal alternatives, exponentially rarer |

The program also builds the **full ordered-pair TF equivalence relation** using union-find on all graph edge variables, rather than reusing the analytic edge-count formula, and verifies for n=5,6,7,8,10,12 that the minimal pair has exactly \(\binom{n-4}2+2(n-4)+2\) unrestricted bits, with exactly one bit removed by the twin-free p≠q restriction.

Another separate exhaustive six-vertex program \`finite_overlap.py\` enumerates all \(3\binom64\cdot64=2880\) marked minimal-pair occurrences; they represent 2370 **distinct labelled** graphs, with multiplicities 1,2,3,6 (as opposed to an unfounded uniqueness claim at small n). It finds 1035 labelled graphs both in the union and connected/nonbipartite/twin-free, 135 with more than one leading support pattern. These tests are consistency checks, not a universal proof.

**Sanity comparison, not fit to data:** the exact table in Hujdurović–Mitrović gives U_7=43, U_8=395, U_9=5113, U_10=105919. Formula (B) predicts respectively 42.67, 341.33, 4369.07, 93206.76. These values were NOT used to choose the proof's constants. Source: Section 5 Table 1, https://onlinelibrary.wiley.com/doi/full/10.1002/jgt.23018 .

## 7. Independent-review requests and limits

This would resolve the **original unlabelled asymptotic enumeration Problem 5.3** if all steps are accepted. Reviewers should challenge:
1. the exact TF↔unexpected cover equivalence for connected nonbipartite graphs and all original twin-free quantifiers;
2. s≤3 exclusions and the *genuinely necessary* twin-free check in the s=4,t=2 exceptional pair;
3. the sparse orbit count and the dense-support independent-constraint extraction, especially the *at most two targets per variable* claim;
4. the **unlabelled** marking upper bound (4), not merely the labelled union bound;
5. two-pattern overlap when both support sets are the **same four vertices** but pair partitions differ;
6. the canonical reconstruction of the unordered attachment sets and the original-old-graph isomorphism from a unique minimal pattern;
7. uniform random-graph asymmetry / Burnside normalizer and whether a later article already obtains this formula.

The manuscript intentionally **does not** claim a human peer review, a second independent Agent's acceptance, any Lean theorem, historical world firstness or arXiv/journal publication. The authors' 2024 graph construction, classical random-graph asymmetry and graph enumeration are explicitly treated as **prior results**. The result concerns original connected nonbipartite twin-free graphs only; no disconnected or bipartite unstable graph count is asserted. Keep this as a newly frozen C-audit branch object until ROOT reviews it; do not overwrite or merge earlier works.
