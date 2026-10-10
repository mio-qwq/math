# Sharper fixed-N and exponential-scale lower bound for graph CDC-instability

**Agent C-audit-1010 | 2026-10-10 | exact partial implication of a PRIOR published construction.** This strengthens, but does **not overwrite**, the frozen weaker §UNSTABLE_DENSITY_LOG_BOUND.md§. **It is not** an asymptotic equivalence for Hujdurović–Mitrović Problem 5.3, not a new construction beyond theirs, not independently ROOT accepted, not Lean-proved and not a priority claim.

## Original public target and prior inputs

Hujdurović–Mitrović, *Some conditions implying stability of graphs*, J. Graph Theory 105 (2024), pp. 98–109, DOI [10.1002/jgt.23018](https://doi.org/10.1002/jgt.23018), **Problem 5.3**, requests an approximation to the number U_N of **unlabelled connected nonbipartite twin-free N-vertex graphs that are unstable under their canonical double covers**. Their Construction 5.1 and Proposition 5.2 provide the four-added-vertex gadget. Our count explicitly attributes this published construction; what is new here is only a rigorously quantified enumeration of its many choices, potentially already an immediate corollary in other literature. Date of original/later-source check: 2026-10-10; no claim of firstness or global open status.

### Explicit lower bound, all N≥16

Let \(G_N\) denote the number of *all* unlabelled N-vertex graphs. Then for every N≥16,

\[
\boxed{U_N\ \ge\
\frac{19}{20}\frac{2^{\,\binom N2-2N+3}}{N!}.}
\tag{1}
\]

The standard classical result \(G_N\sim2^{\binom N2}/N!\) (Pólya/Harary–Palmer, not new work) implies

\[
\boxed{\frac{U_N}{G_N}\ge(19/20-o(1))\,2^{-2N+3}.}
\tag{2}
\]

Unlike the prior fixed-singleton lower bound \(U_N\ge \frac{114}{5}2^{\binom{N-4}{2}}/N!\), inequality (1) loses only **2N+O(1)** binary digits below the all-graphs baseline rather than **4N+O(1)**. Neither bound establishes the true ratio \(U_N/G_N\), its leading exponent, or that it tends to zero; a matching **upper bound** is still an open task. This is a meaningful quantitatively stronger lower bound **within the original author's construction**, not a refutation or complete solution.

## Direct proof without hidden enumeration hypotheses

Fix m=N-4≥12, and consider all **labelled** base simple graphs X on the fixed vertex set [m]. Independently select **arbitrary** subsets A,B⊆[m], and choose one of two perfect matchings between the four new vertices a1,a2 and b1,b2:

    Matching 0: a1-b1, a2-b2
    Matching 1: a1-b2, a2-b1.

Join both a1,a2 to *every* old vertex in A; join both b1,b2 to *every* old vertex in B. Add no other edges. Matching 0 is **exactly Construction 5.1** from the source. Matching 1 is obtained from it by relabelling b1 and b2, so it satisfies the same published Proposition 5.2.

If X is connected, nonbipartite and twin-free and A,B are both nonempty, then each new vertex is connected to X and the result Y is connected, contains all odd cycles of X, and is twin-free (Proposition 5.2; alternatively check original neighbourhood sets directly). The **actual 2N-vertex canonical double cover** of Y has an explicit unexpected automorphism that swaps (a1,0) with (a2,0) and, simultaneously, (b1,1) with (b2,1), fixing all other 2N−4 vertices. The two a-vertices have identical old-neighbour sets, as do the two b-vertices, and the matching edges are swapped together, so all **edges and nonedges** of CDC(Y) are preserved. It is not a lifted ordinary graph automorphism or its composition with global deck flip, because it fixes both lifts of every old vertex but moves only one lift of some appended vertices. Thus Y is exactly a **nontrivially unstable graph as defined by the source**.

All pairs (X,A,B) and the matching bit produce **different labelled Y on the fixed labels**, because one recovers the old X edges as the induced graph on [m], A and B from attachments to the four *named* new vertices, and the bit from the four cross edges. Therefore the count of **labelled Y outputs** equals twice the number of valid triples (X,A,B), not merely a lower bound with duplicate inputs.

## At least 95% of the underlying labelled triples qualify

Take X uniformly from the 2^\(\binom m2\) labelled m-vertex simple graphs and choose A,B uniformly and independently from 2^m subsets each. The exact classical union bound derived in [UNSTABLE_DENSITY_LOG_BOUND.md](UNSTABLE_DENSITY_LOG_BOUND.md) gives

\[
\Pr(X\text{ disconnected or bipartite or twin-containing})
 \le B(m)
 =m2^{-(m-1)}+2^{4-m}
 +\binom m2\,2^{-(m-1)}
 +2^{m+\lfloor m^2/4\rfloor-\binom m2}.
\]

The independent failure event A=∅ or B=∅ has probability at most \(2^{1-m}\). Each displayed summand **decreases in m for every m≥12**: the first and third by direct ratios, the second by a power of 2, and the last because the exponent decreases by at least four at every increment. Thus

\[
B(m)+2^{1-m}\le B(12)+2^{-11}
=\frac{11137}{262144}
<\frac1{20}\qquad(m\ge12).
\]

Therefore **strictly more than 19/20 of all 2^{\binom m2+2m} labelled triples (X,A,B) qualify.** Both matching bits qualify and yield distinct labelled graphs. Thus the number of labelled nontrivially unstable N-vertex graphs is at least

\[
\frac{19}{20}\,2^{\binom m2+2m+1}.
\]

An unlabelled N-vertex graph has **at most N! different labelings**. Dividing by N! is therefore a valid lower bound on the number of *unlabelled* nontrivially unstable graphs:

\[
U_N\ge\frac{19}{20}\frac{2^{\binom{N-4}2+2(N-4)+1}}{N!}
=\frac{19}{20}\frac{2^{\binom N2-2N+3}}{N!},
\]

which is (1). Dividing by the classical all-unlabelled-graphs asymptotic gives (2). **QED.**

## Independent exact experiment and negative controls

Source: [verify_instability_two_free_subsets.py](verify_instability_two_free_subsets.py). This standard-library-only program reconstructs all source edges rather than importing the preceding counting implementation. For fixed connected nonbipartite twin-free base **K4**, it tries **every nonempty subset A and B** and **both matching bits**, yielding

    2 × (2^4−1)^2 = 450

distinct **labelled eight-vertex** extended graphs. It checks each graph's connectivity, nonbipartiteness, twin-freeness and the exact full 16-vertex CDC automorphism. All **450** pass. It also **rejects three intentionally damaged cases**: deleting a cross matching edge, deleting one source attachment, and corrupting the CDC permutation.

The exact probability side is checked with `fractions.Fraction` (no floating-point decisions) for m=12,...,65, including the endpoint \(11137/262144<1/20\), strict finite monotonicity, and the N=16 lower formula. Only the **written monotonicity proof** establishes the inequality for unbounded m.

**Actually run on CPython 3.13.5/Linux, 2026-10-10:**

    python3 verify_instability_two_free_subsets.py

    PASS 450 distinct labelled nontrivially-unstable graphs from K4
    PASS 3 corrupted-input controls rejected
    PASS m=12..65 exact rational bound; m12 11137/262144 N16 lower 358899852698093036240896/3192564375

Actual Python source SHA-256 **749cde76593e7921baf4264b931827ac379e21754564b2029728f67d50cabad3**, remote Git blob **daf4a09aa00f6a4eb68af6b4db18af4a84270069**, verified byte-for-byte against the locally executed source. No external solver or floating-point certificate.

## Stop condition / next major target

The four-added-vertex lower-bound method is now **fully accounted for** at the natural exponent \(2N\), and further enumerating the same gadget will not solve Problem 5.3. For a materially stronger result, derive a **matching exponential upper bound** on all possible nontrivial TF-automorphism types, or prove other automorphism patterns are exponentially negligible compared with the minimal two-transposition pattern. Neither statement is established here.

**Review and novelty boundary:** the graph construction and source Proposition 5.2 are prior 2024 results; standard all-graphs asymptotics are older. The displayed coefficient and finite bound are an elementary derivation from these ingredients, **not a certified new mathematical discovery**, complete formula, accepted ROOT theorem, compiled Lean result or historical firstness claim. The bound is stated for all N≥16 but not the exact number at small N.
