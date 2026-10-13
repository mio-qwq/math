# Narrow-window randomized scheduling: targeted novelty increment

Independent literature role D; retrieval completed 2026-10-13 UTC
(2026-10-14 Asia/Singapore). This supplements, rather than repeats,
`LITERATURE_REVIEW.md` and `NOVELTY_REVIEW.md`.

## Scope and evidence status

Inspected main worktree commit
`cb972a2cc787248b1c902ed3b2701befad54f1a2` and the actual theory sources
`NARROW_WINDOW_POLICY.md` and `RANDOMIZED_FIVE_QUARTERS.md`.
The former contains oldest-inclusive non-delay normalization for
`B=W+1` and a scalar exact suffix recurrence for `B=3,W=2`.
The latter contains an arbitrary-size joint-induction proof of
`4 E[T_R] <= N+3 T* <= 5 T*`, with the matching four-job lower bound
against an oblivious adversary. At inspection it identifies itself as
**WRITTEN_PROOF**, awaiting the saved independent mathematical review.
This literature audit does not substitute for that review or claim Lean
verification. Its originality status remains **NOVELTY_UNCONFIRMED**.

The preceding exhaustive evidence covers 2,796,203 effective gap-one/two
DAGs through twelve jobs; it is evidence for the policy, not a proof over
all lengths or an enumeration of all randomized online algorithms.

The prospective contribution is the exact performance of this policy in
the specified ROB information model. Generic dynamic programming,
two-processor optimal scheduling, and the matching identity below are
classical. A linear algorithm at fixed `B=3` is not a new complexity
classification: the project's general finite-window DP is already linear
in program length when the window is fixed.

## 1. The direct classical connection: maximum matching

**M. Fujii, T. Kasami and K. Ninomiya, 1969.**
*Optimal Sequencing of Two Equivalent Processors*, SIAM Journal on
Applied Mathematics 17(4), 784–789.
[Publisher / DOI](https://epubs.siam.org/doi/10.1137/0117070).
There is a [1971 correction](https://epubs.siam.org/doi/10.1137/0120018),
20(1), 141. Publisher metadata and abstract were inspected; the original
and correction bodies were not accessible. Do not claim to have audited
their original proof or attach an unverified original theorem number.

A directly accessible primary later source is **Dexter Kozen, Umesh
Vazirani and Vijay Vazirani, 1985**, *NC Algorithms for Comparability
Graphs, Interval Graphs, and Unique Perfect Matching*,
FSTTCS, LNCS 206, 496–503.
[Author-hosted paper](https://www.cs.cornell.edu/~kozen/Papers/comp.pdf)
and [author publication record](https://www.cs.cornell.edu/~kozen/Papers/papers_by_year.htm).
The final scheduling section, PDF page 16, explicitly attributes the
two-processor unit-time scheduling/maximum-matching theorem to Fujii,
Kasami and Ninomiya. The scanned theorem numeral is not reliably
extractable. It yields `T*=N-nu(H)`, where `H` is the incomparability
graph of the precedence order. This is prior art, not an ILP1 discovery.

**Application and limits, derived here from that classical identity.**
Apply it to the ROB-augmented order, including transitive closure.
For `B=3`, every pair of indices at distance at least three is comparable,
so `H` is a subgraph of the square of the program-order path. Its bandwidth
is at most two. Thus the proposed stronger expected-time guarantee can be
written as an expected matching-size guarantee of `3 nu(H)/4`, since a
non-delay width-two schedule with `M` pairs takes `N-M` cycles.
This reformulation alone establishes no policy guarantee.

Important distinctions prevent automatic import of a generic matching
theorem:

- `H` is the incomparability graph of the transitive order, not simply
  the complement of the listed true edges.
- It can contain triangles and have degree four; it is not necessarily
  bipartite or of maximum degree two.
- Incomparability with the oldest job does not ensure readiness. With
  jobs `0,1,2` and sole edge `1->2`, `H` contains edge `0--2`, but the
  first ROB action cannot pair `0` with `2`. The proposed policy must
  pair `0` with `1`. An unrestricted random-neighbor matching step can
  therefore make a different, immediately unschedulable decision.
- ROB visibility changes after contiguous retirement, rather than after
  an externally fixed sequence of matching arrivals or deadlines.

## 2. Closely related randomized matching results

**Amey Bhangale, Arghya Chakraborty and Prahladh Harsha, 2025.**
*Optimal Online Bipartite Matching in Degree-2 Graphs*, ISAAC 2025,
LIPIcs 359, article 13.
[Full primary text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol359-isaac2025/html/LIPIcs.ISAAC.2025.13/LIPIcs.ISAAC.2025.13.html).
Inspected the model, Theorems 1–2, and the Half-Half algorithm/Theorem 6.
One vertex class is known in advance; vertices of the other class arrive
with at most two neighbors, and matching decisions are irrevocable.
Half-Half chooses uniformly when both neighbors remain available.
Its optimal randomized integral guarantee is
`eta=1-sum_(i>=1) 2^(-2^i-i+1) ~= 0.717772` (Theorems 1 and 6).
The `3/4` guarantee in Theorem 2 concerns fractional matching.
Consequently neither “two choices” nor this fractional theorem proves
the ROB policy's proposed `3/4` pairing guarantee. The online model and
graph restrictions differ. No implication in either direction has been
established by this audit.

**Mahsa Derakhshan and Tao Yu, 2026.**
*A Unified Framework for Analysis of Randomized Greedy Matching
Algorithms*, [arXiv:2604.00331v1](https://arxiv.org/html/2604.00331v1),
1 April 2026. Inspected the introduction and Appendix A definitions,
not every proof. The framework distinguishes adversarial or random vertex
orders and independent or shared random neighbor preferences. These
distinctions matter: independently choosing a ready younger job is not
the same random process as using one shared ranking. Its fully online
matching model also uses arrivals/deadlines, rather than dependency
readiness and retirement. The paper is a useful general comparison, but
no theorem inspected there directly covers the R1 policy. Only the
specified preprint version was inspected for this comparison.

## 3. Lookahead and buffer terminology can hide different models

**Marvin Mandelbaum and Dvir Shabtay, 2011.**
*Scheduling unit length jobs on parallel machines with lookahead
information*, Journal of Scheduling 14, 335–350.
[Publisher](https://link.springer.com/article/10.1007/s10951-010-0192-y).
Publisher abstract inspected; full text unavailable. Its lookahead concerns
online job assignment with machine-eligibility types, not precedence-ready
issue followed by in-order retirement. Abstract-level claims cannot
establish coverage of the present normalization or randomized guarantee.

**Koji M. Kobayashi, 2018 preprint / 2021 journal publication.**
*An optimal algorithm for 2-bounded delay buffer management with
lookahead*, [full preprint](https://arxiv.org/pdf/1807.00121),
[journal DOI](https://doi.org/10.1016/j.tcs.2021.10.005).
Inspected the preprint's model and introductory result comparisons;
publisher access failed. Packets have exogenous release times, weights
and deadlines; one is transmitted per time step. Its buffer is unlimited,
and the objective is transmitted weight. “2-bounded” refers to delay,
not two processors or three ROB entries. Bounds numerically involving
`5/4` in this literature do not establish the present makespan result.

## 4. Novelty assessment and claim boundaries

No identical or directly subsuming theorem was located in this targeted
pass. That is a bounded search outcome, not proof of historical novelty.
The strongest remaining candidate is the R1-specific sharp randomized
guarantee, particularly the auxiliary invariant that controls readiness
and contiguous-window progression. It should be presented as an exact
special-case online result, not a resolution of general precedence
scheduling or a guarantee for real CPUs.

The universal statement must retain these assumptions: fixed complete
input chosen independently of the policy's random bits; forward unit-time
dependencies; eager admission; completed-but-unretired jobs retaining
window slots; unlimited in-order retirement; no same-cycle dependency
bypass; knowledge restricted to admitted instructions and incoming
operands, without unseen successor lists. The four-job witness proves a
strict worst-instance expected ratio. Calling that alone an asymptotic
lower bound allowing arbitrary additive constants requires a further
repeatable construction.

The oldest-inclusive normalization is an offline existence theorem.
It neither says that every oldest-inclusive policy is optimal nor follows
merely from a bound on the width of an arbitrary poset. The exchange proof
uses the fact that omitting the oldest job blocks *all* admission. A prior
result about bounded-width posets needs this additional model comparison.

Next highest-value originality check: a verified reduction to an existing
randomized matching algorithm on ordered bandwidth-two incomparability
graphs, preserving both readiness and revelation. If that succeeds,
attribute the general theorem and state the ROB result as its corollary.

## Retrieval record and remaining access limits

Both available search engines were used. Representative exact queries:

```text
"online scheduling" "precedence" "5/4" randomized
"scheduling" "lookahead" "two processors"
"precedence" "buffer" "three" "randomized"
"instruction scheduling" "oldest" "optimal" window
"two processor scheduling" "maximum matching" unit
"online matching" "bandwidth two"
"online matching" "paths" "3/4"
random greedy matching "3/4" "degree" two
"online bipartite matching" "degree 2" "random"
"unit" "precedence" "oldest" "window" scheduling
"randomized" "bounded-window" scheduling
```

The original Fujii article/correction bodies and Mandelbaum–Shabtay full
text remain unread. Previously recorded Epstein precedence-online paper
links again failed to open; no new claim about its complete theorem scope
is made here. A search lead on online convex bipartite matching also failed
to open and is not counted as inspected evidence. Source unavailability
limits the audit; it must not be silently converted into an absence claim.
