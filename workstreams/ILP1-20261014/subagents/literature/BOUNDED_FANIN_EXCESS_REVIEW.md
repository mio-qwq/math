# Two-input scheduling and window excess: targeted literature audit

Reviewer: ILP1 literature subagent D. Date: 2026-10-13 UTC.
Scope: the supplied-order R1 model, true fan-in at most two, and parameter
`c=B-W>0`. This is a finite follow-up to `EXCESS_HARDNESS_NOVELTY.md`, not
another general scheduling survey.

## Finding and exact unresolved question

This pass did not verify a published FPT(c) algorithm or parameterized
hardness theorem for the exact combination

`explicit unit jobs + supplied program order + occupied ROB window B
 + issue width W + true fan-in <= 2 + parameter B-W`.

That leaves a project research question unresolved; it is not evidence that
the question is a recognized open problem, nor a historical priority claim.
In particular, the project's arbitrary-fan-in biclique reduction does not
settle the two-input case. Ordinary poset width minus processor count is
insufficient because it omits the supplied distance-B order property.

Let the true DAG be G=([0,N),E), with all edges forward in program order.
Fan-in bounds apply to E, before adding the R1 precedences

`A_B = {(i,j): 0 <= i < j < N and j-i >= B}`.

The static equivalent scheduling instance is G_B=([0,N),E union A_B).
Its direct degree, cover degree, height, and other structural parameters can
be much larger than those of G. All sources below concern ordinary
precedence scheduling unless stated otherwise.

## Closest primary results checked

### Global predecessor count is not maximum fan-in

Christina Büsing, Maurice Draeger, Corinna Mathwieser, *Parameterized
Complexity of Scheduling Unit-Time Jobs with Generalized Precedence
Constraints*, IPEC 2025, Article 7, pp.7:1-7:16.
DOI: <https://doi.org/10.4230/LIPIcs.IPEC.2025.7>.
Full primary PDF read, especially Sections 2, 3 and 6:
<https://drops.dagstuhl.de/storage/00lipics/lipics-vol358-ipec2025/LIPIcs.IPEC.2025.7/LIPIcs.IPEC.2025.7.pdf>.

Their parameter k_p counts all distinct jobs occurring as a predecessor
anywhere, not the maximum number of predecessors of one job. Theorem 2
gives O(k_p^(k_p) m n^2) for makespan and total completion time. Their
k_s counts all jobs having a nontrivial predecessor constraint; Theorem 8
gives FPT(k_s) for AND+OR constraints. Section 6 proposes maximum in/out
degree as possible further structural parameters. Its two-machine hardness
uses mixed AND+OR constraints, not the ordinary all-inputs-required model.

Neither k_p nor k_s is bounded by c or by true fan-in; see the explicit
separation below. Applying an ordinary scheduling algorithm to G alone
would discard the ROB restriction; applying it to G_B need not preserve
the small parameter. The discussion of future work does not certify the
status of the exact R1 question.

### Fixed processors with graph degree and path-length restrictions

Isto Aho and Erkki Mäkinen, *On a parallel machine scheduling problem with
precedence constraints*, Journal of Scheduling 9, 493-495 (2006).
Primary publisher abstract read:
<https://link.springer.com/article/10.1007/s10951-006-8499-4>.

The abstract describes a polynomial special case involving fixed machine
count, bounded maximum path length and maximum degree. Its argument
distinguishes small instances from instances admitting a dense schedule.
The full proof was not obtained, so no theorem number or more precise
degree convention is asserted here.

Small c does not bound W. True fan-in two does not bound true outdegree or
height; even height-two true graphs can have arbitrarily large fan-out.
The additional graph restrictions also need not survive ROB augmentation.
Consequently the verified abstract does not establish FPT(c) for R1.

### Leveled, locally two-input graphs with substantial layer width

Kostas Politopoulos, George F. Georgakopoulos and Panagiotis Tsanakas,
*Precedence Constrained Scheduling: A Case in P*, The Computer Journal
44(3), 163-173 (2001), DOI <https://doi.org/10.1093/comjnl/44.3.163>.
Primary publisher abstract read earlier in this pass:
<https://academic.oup.com/comjnl/article-abstract/44/3/163/415517>.

The abstract describes a polynomial algorithm for leveled graphs with
locally bounded indegree two and a level-width condition exceeding 1.55
times the processor count, with an additional constant. It explicitly uses
limited lookahead. The appendix reportedly gives hardness results when
restrictions are relaxed, but its proofs and exact parameter conventions
were not accessible; no hardness theorem is imported from that statement.

This is close historical context for two-input instruction graphs. It
does not supply the occupied-window order or preservation of B-W, and its
extra layer-width hypothesis is not implied by c being small. Layer width
must not be identified with ROB capacity. A later attempt to reopen the
abstract failed; that access failure does not change the earlier reading.

### Height two, stars, and the input-encoding distinction

André Berger, Alexander Grigoriev, Pinar Heggernes and G.R.J. van der Zwaan,
*Scheduling unit-length jobs with precedence constraints of small height*,
Operations Research Letters 42(2), 166-172 (2014).
DOI: <https://doi.org/10.1016/j.orl.2014.01.008>.
Primary institutional abstract read:
<https://cris.maastrichtuniversity.nl/en/publications/scheduling-unit-length-jobs-with-precedence-constraints-of-small-/>.

For collections of stars, the abstract distinguishes NP-hardness with
compact encoding from polynomial solvability with explicit adjacency lists.
It also describes tractable collections of complete bipartite graphs.
The full proof was not obtained. R1 here explicitly lists its jobs, so
quoting the compact-encoding hardness without its qualification would be
incorrect. General height-two graphs of indegree two need not be star
collections, and augmentation can join formerly disjoint components.

## Elementary separations and a reduction obstruction

The following are direct graph observations, not claimed original theorems.
Their purpose is to prevent incorrect use of the preceding results.

### True fan-in zero can produce unbounded augmented cover indegree

For B>=2, take N=2B, W=B-1 and E empty. Thus c=1 and the true graph
has no dependencies. In G_B the final job 2B-1 has predecessors
0,...,B-1. They are pairwise incomparable. Every such predecessor edge is
a cover: a two-edge path using A_B would span at least 2B indices, which
is impossible within [0,2B). Hence even the transitive reduction of G_B
has maximum indegree at least B.

Similarly, E empty does not bound augmented height: the indices
0,B,2B,... form a chain in G_B. Algorithms whose input parameter is
augmented graph degree or height therefore cannot automatically be called
FPT(c) algorithms for true two-input programs.

### Global predecessor/successor counts remain unbounded

For q>=2, take q roots followed by q children, with only the true edges
i -> q+i for 0<=i<q. Set B=q+1 and W=q. Then c=1, true height is two,
true maximum in/outdegree is one, and both global counts k_p and k_s
equal q. Since these true edges remain after augmentation, both augmented
counts are at least q. No bound on these counts follows from c=1.

### Redundant artificial edges restrict bounded-height binary reductions

Suppose N>=1, B>=1, d>=0 and H>=1 are integers. Assume that the true DAG
has maximum indegree at most d and height at most H, where height counts
vertices on a longest directed path. Suppose every artificial edge in
A_B is already implied by true reachability E^+; the edge need not be
present directly in E. Then

`max(0,N-B) <= sum_{j=1}^{H-1} d^j`.

Proof: the final job has each of the max(0,N-B) indices i<=N-1-B as a
distinct true ancestor. Any true ancestor reaches it by a path of at most
H-1 edges. There are at most d^j backward paths of length j, and every
ancestor appears as the initial vertex of at least one such path. Counting
paths may count one ancestor several times, so summing these bounds is
still an upper bound. This proves the inequality. When H=1 the sum is
empty; when d=0 every summand is zero. Both boundary cases are valid.

In particular, true height at most two and fan-in at most two force
N<=B+2 whenever all window edges are redundant. Thus the existing
N=2B, height-two hardness embedding cannot retain both true fan-in two
and its redundancy property for B>2. A different two-input reduction may
use essential window edges or greater true height; this observation rules
out neither possibility and proves no FPT result. Replacing a large AND
by a binary tree adds jobs and unit-cycle latency, and changes admission
positions, so it does not automatically preserve the hardness parameter.

This last obstruction was sent to the primary agent and accepted for the
research record. It has a written proof; it has not been Lean-verified here.

## Safe next question and claim boundary

The project's general XP(c) algorithm and polynomial c=1 algorithm apply
also to two-input programs. Its arbitrary-fan-in W[1]-hardness result does
not specialize to them. A useful next target is therefore either an
FPT(c) algorithm exploiting only true fan-in two, or a parameter-preserving
two-input reduction in which window edges genuinely participate. Height-two
true DAGs are a sensible initial special case, with the explicit warning
that the augmented DAG can have larger height and degree.

Do not describe the finite search as proving novelty, assert that bounded
indegree makes classical DAG scheduling easy, import OR-precedence results
for AND dependencies, or replace a missing supplied-order construction by
a poset-width argument. No new complexity classification is established
by this review.

## Search and access record

Date: 2026-10-13, approximately 20:35-20:45 UTC. Representative exact queries:

- `"precedence" "at most two predecessors" "scheduling"`
- `"scheduling" "indegree at most two"`
- `"scheduling" "in-degree at most 2"`
- `"unit" "scheduling" "bounded indegree"`
- `"precedence" "bounded" "in-degree" scheduling parameterized`
- `"bounded window" "scheduling" "indegree"`
- `"scheduling" "height two" "degree" unit`
- `unit time scheduling indegree bounded fixed parameter`
- `precedence scheduling discrepancy constraints bounded fanin`
- `"Parameterized Complexity of Scheduling Unit-Time Jobs with Generalized Precedence Constraints"`
- `"Aho" "Mäkinen" scheduling maximum degree height`
- `"Precedence constrained scheduling: A case in P"`
- `"precedence" "1.55" scheduling`
- `"Scheduling unit-length jobs with precedence constraints of small height" pdf`

Both search engines were tried. Irrelevant results ignoring the academic
query were discarded. The IPEC paper was read in full in the relevant
sections; the other three entries are deliberately limited to primary
abstracts. A CiteSeer candidate for the 2001 paper returned an access error.
No unavailable proof is represented as read, and no access wall was
bypassed. No source PDF or extensive copied text is committed.

Repository checkpoint before writing: clean branch
`partner/ilp1-literature-20261014`, parent commit
`3bc46ccdc6ad815f1433d301f6e45d82b76a5ce1`. Actual `git fetch origin`
completed at 2026-10-13T20:42:16Z; `origin/main` remained
`bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
