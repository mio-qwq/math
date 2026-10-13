# Literature audit: perfect issue saturation with one extra ROB entry

Reviewer: literature subagent D. Retrieval date: **2026-10-13 UTC**.
This is a bounded follow-up to the earlier reviews, not an exhaustive survey.
Result status: **WRITTEN_PROOF**, independently checked below;
**NOVELTY_UNCONFIRMED**. No Lean verification is supplied by this review.

## Exact claim being assessed

Use R1, with a fixed forward program order, unit execution latency, eager
admission, unlimited in-order retirement, and completed but blocked jobs
occupying ROB slots. Let `W>=2`, `B=W+1`, and `N=kW`. Partition the program
into consecutive `W`-job blocks. The candidate characterizes `T*=k` using:

- `A`: one consecutive block in one cycle;
- `D`: two neighboring blocks in two cycles, swapping the last job of the
  first block with the first job of the second block.

Every `k`-cycle schedule has this decomposition. A macro is legal exactly
when all its internal true edges strictly advance its local cycle. Legal
macros tile the block path if and only if the work bound is attainable.
The resulting decision algorithm and explicit positive/negative certificates
take `O(N+|E|)` indexed-graph operations, **uniformly in the input width W**.
It does not compute the larger optimum when saturation fails, nor cover
`N` not divisible by `W`.

The reviewed sources are the theory worktree's `PERFECT_SATURATION.md` and
`perfect_saturation.py`. Their SHA-256 digests at 19:49:19 UTC were:

```text
c561ae338ed3b16872c3620132780cc9f0b1097eb2d9642e7e5ca2f51e9be296  PERFECT_SATURATION.md
2718784659ddb8aba84b8d0b5db200bacf518c4559f6a8cc80ee58aeafce125a  perfect_saturation.py
```

Verification commit `d566e057cf3cd7b2e9eaf597c5851cda5921b6df` was also
read. It independently accepts the tiling equivalence, component test, and
algorithm; its proof invokes oldest-inclusive normalization. This review
separately checked the stronger all-schedules claim: after a full issue
that omits the `r`-th window entry, only `r-1` earlier jobs retire, so the
next cycle has at most `r` unfinished admitted jobs. If two blocks remain,
full utilization forces `r>=W`. The two remaining cases give `D` and `A`.
No normalization is needed. Last-block and empty-program cases are separate.

## Closest prior terminology: discrepancy precedence constraints

**Egon Balas (1999)**, *New classes of efficiently solvable generalized
Traveling Salesman Problems*, Annals of Operations Research 86, 529–558.
[Publisher/DOI](https://link.springer.com/article/10.1023/A:1018939709890).
The publisher abstract explicitly requires original-order pair `i,j` to
retain their order whenever `j>=i+k`. Its layered-network algorithm has
linear dependence on the number of cities and exponential dependence on
`k`. The full paper was subscription-blocked; no theorem number or
independent verification of its full proof is asserted here.

**Egon Balas and Neil Simonetti (2001)**, *Linear Time Dynamic-Programming
Algorithms for New Classes of Restricted TSPs: A Computational Study*,
INFORMS Journal on Computing 13(1), 56–75.
[Publisher/DOI](https://pubsonline.informs.org/doi/abs/10.1287/ijoc.13.1.56.9748).
The primary abstract confirms the same ordered-pair condition, extends its
parameter to city-specific values, and describes a path representation of
feasible tours. The publication page gives February 1, 2001. The PDF link
returned the abstract page, so the full proof was not read.

**Andre A. Cire and Willem-Jan van Hoeve**, *Multivalued Decision Diagrams
for Sequencing Problems*, Operations Research 61(6), 1411–1428.
[Author manuscript](https://www.andrew.cmu.edu/user/vanhoeve/papers/mdd_sequencing.pdf);
[publisher](https://pubsonline.informs.org/doi/abs/10.1287/opre.2013.1221).
The issue and online date are 2013; the publisher's generated citation says
2014. Sections 3 and 9 of the May-2013-revised manuscript were read.
Section 9, PDF pp.18–19, explicitly calls the condition
`j_p << j_q whenever q>=p+k` **discrepancy precedence constraints**.
Lemma 8 and Theorem 3 count its decision-diagram states; the displayed
width bound grows exponentially with `k`. These are unary sequencing
problems, possibly with setups and time windows, rather than simultaneous
unit-job batches. Arbitrary additional true edges can restrict the feasible
orderings; the equality in the pure-constraint state count must not simply
be asserted for every such restriction.

**Consequences for this project (reviewer's comparison):** the added R1
precedences are exactly this established ordered-pair restriction with
`k=B`. Neither the constraint family nor finite-state dynamic programming
for constrained permutations should be presented as new. The reviewed
sources do not state the current A/D full-batch normal form or a linear
algorithm with `W=B-1` varying as part of the input. Their exponential
parameter factor does not itself imply the new uniform bound. Conversely,
different objectives and machine semantics prevent using this observation
as a proof that the new theorem is absent from the wider literature.

## A second precise connection: linear discrepancy of a poset

**Peter C. Fishburn, Paul J. Tanenbaum, and Ann N. Trenk (2001)**,
*Linear Discrepancy and Bandwidth*, Order 18, 237–245.
[Publisher/DOI](https://link.springer.com/article/10.1023/A:1012267732204).
The primary abstract was read; the full text was unavailable. It identifies
poset linear discrepancy with the bandwidth of its incomparability graph.
No theorem number from the unavailable body is claimed.

**Mitchel T. Keller, Noah Streib, and William T. Trotter (2010 manuscript)**,
*Online Linear Discrepancy of Partially Ordered Sets*.
[Author-hosted PDF](https://rellek.net/home/images/publications/online-ld.pdf),
dated June 1, 2010. Sections 2.2 and 3 were read. They distinguish
`ld(P,L)`, the maximum distance in a chosen linear extension of an
incomparable pair, from `ld(P)`, minimized over extensions. Their online
model inserts revealed elements into a growing linear order; it does not
execute batches or maintain ROB occupancy.

Our inference is immediate but useful for searching: in the augmented
R1 poset, the **given program order** has `ld(P,L)<=B-1=W`. Thus the
incomparability graph has a supplied bandwidth-`W` order. This is stronger
information than the consequence `width(P)<=W+1`; it is not an instruction
to optimize or change the program order. It supplies a precise bridge to
existing graph parameters, but no saturation algorithm by itself.

Also, arbitrary true edges do not preserve interval-order structure.
For example, with one-based indices, `N=4,B=3,W=2` and sole true edge
`2->3`, the augmented poset has exactly the two disjoint relations
`1<4` and `2<3`. It is `2+2`, hence not an interval order. Therefore
interval-order scheduling theorems cannot automatically cover R1.

## Broader results checked, without overextending them

**René van Bevern, Robert Bredereck, Laurent Bulteau, Christian Komusiewicz,
Nimrod Talmon, and Gerhard J. Woeginger (2016)**,
*Precedence-constrained scheduling problems parameterized by partial order
width*, DOOR 2016, LNCS 9869, 105–120.
[Primary preprint](https://arxiv.org/html/1605.00901v1).
The introduction and model were read. Its discussion notes that an earlier
unit-job scheduling hardness reduction has poset width `m+1`; this is an
attributed observation, not a fresh reading here of that earlier proof.
Its width-and-lag algorithm has parameter-dependent exponential factors.
Neither result implies hardness or the present linear criterion for
R1's more constrained, supplied-order instances. The paper's own
two-machine hardness theorem uses processing times 1 and 2, which cannot
be silently substituted for R1's unit jobs.

**Hans L. Bodlaender and Maher Mallem (2026 preprint)**,
*The Parameterized Complexity of Scheduling with Precedence Delays:
Shuffle Product and Directed Bandwidth*.
[Primary text](https://arxiv.org/html/2605.03727v1), May 5, 2026.
The introduction and directed-bandwidth definition were read. Directed
bandwidth controls distances of arcs in a selected topological ordering,
with a scheduling interpretation using maximum delays. Here we instead
bound distances of incomparable pairs in a supplied order. The shared
word “bandwidth” does not make those the same problem.

Other search leads included *Sequencing with limited flexibility*
(Lahmar–Benjaafar, 2007, DOI 10.1080/07408170701416665). The publisher
full-text retrieval failed; its indexed primary abstract concerns position
shifts and sequence-dependent costs. No unseen theorem from it is used.

## Novelty and significance verdict

The standard final step is matching on a path with allowed uncovered
vertices. Its parity criterion, a monomer/dimer recurrence, and its linear
scan are elementary; none should be promoted as an original matching
theorem. Likewise the work lower bound and its full-utilization consequence
are foundations.

The potentially useful result is the **R1-specific collapse of every
perfectly saturated schedule to these two local macros**, plus the fact
that each true edge invalidates at most three macro candidates. This
creates a structural, independently checkable impossibility certificate
without enumerating the ROB state space. The variable-width guarantee is
the substantive complexity distinction from a fixed-window exhaustive
algorithm. The result has deliberately narrow hypotheses and gives no
general polynomial algorithm for unit precedence scheduling.

No identical or immediately subsuming full-batch theorem was found in this
bounded retrieval. That is a search outcome, **not evidence of priority**.
Keep **NOVELTY_UNCONFIRMED**, cite the exact existing constraint family,
and describe the macro reduction as a candidate specialized contribution.
The strongest next search, if preparing publication, is forward citation
work from Balas and the discrepancy-constraint literature, specifically
parallel batches and exact work-bound feasibility; another broad generic
scheduling keyword sweep is lower value.

## Reproducible search scope

Both available web search engines were used. Representative actual queries:

```text
"scheduling" "bounded window" "unit"
"scheduling" "buffer" "unit jobs" "fixed order"
"precedence" "work bound" scheduling
"precedence" "scheduling" "n/m" "feasibility"
scheduling precedence poset "width" "m+1"
scheduling "incomparability graph" "bandwidth"
"linear discrepancy" scheduling unit time
"Linear Discrepancy and Bandwidth" pdf
"perfect schedule" "precedence" "unit"
"scheduling" "discrepancy precedence"
"discrepancy precedence constraints"
"discrepancy precedence constraints" "parallel"
"discrepancy precedence" "batch"
"Balas Simonetti" "parallel" scheduling
"New classes of efficiently solvable generalized traveling salesman problems" Balas pdf
```

Search snippets were used to locate sources, not to authenticate a theorem.
Unavailable full texts and manuscript/publication-date discrepancies are
recorded above. No Lean files were changed or compiled in this audit.
The independent worktree was clean before this increment; `git fetch origin`
completed successfully before its local commit.
