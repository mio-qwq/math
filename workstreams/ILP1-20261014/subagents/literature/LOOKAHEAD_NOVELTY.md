# Audit: hidden final operands and inverse-lookahead guarantees

Reviewer: literature subagent D. Retrieved **2026-10-13 UTC**.
This is an incremental review; earlier general online-scheduling references
are not reproduced. Verdict: written proofs accepted at the scope below;
**NOVELTY_UNCONFIRMED**, with a particularly close prior model and method.
No Lean or independently rerun solver evidence is claimed by this review.

## Exact results and independent model audit

R1 has `B=4,W=3`. At retired prefix `r`, an online policy sees incoming
operands only at indices below `min(N,r+4+L)`. It may know the total length
and retain arbitrary history; it has no oracle exposing future consumers.
This differs from knowing the entire outgoing dependency graph of each
visible job. Lookahead is a prefix of instruction **positions**, not elapsed
time, execution depth, or arbitrary future queries.

The theory note `LOOKAHEAD_BOUNDARY.md` at commit
`f9c74fc56e96a69772f7106519b3373df49c4ac6` was read. Its SHA-256 is
`395e9bc5e110825c3624a66b81ba3b0736971301d243f04d7e3a55cedddd56f2`.
For `M>=1`, the two interleaved chains, two isolated roots, optional
padding root, and final hidden operand have optimum `K=M+2`. The selected
chain must begin immediately to attain this critical-path bound. The A
case requires first action containing `{0,3}`; the B case requires exactly
`{0,1,2}` because admitting its second chain job requires both oldest roots
to retire. These requirements are incompatible even with underissue.
The displayed attaining schedules obey the four-entry window, including
`M=1` and the padding case. Thus the all-but-last observation claim holds
for every `N>=7`, and the single-block true indegree/outdegree bounds are one.

The verification note `REPEATED_LOOKAHEAD.md`, as read at its branch commit
`151ca5191e16bd65f7aec7a857c192e660143d29`, and its audit source were also
read. Connecting each next-block root to the preceding final job and the
unselected chain leaf enforces complete block separation: those parents
cover the last three preceding jobs, and ROB admission covers the earlier
prefix. The next block starts without an extra cycle. For `L<=2M`, neither
the current hidden operand nor the next-block edges encoding its choice
can have been observed before the current first decision. This holds over
the entire history, not only the current snapshot.

Consequently independent uniform hidden bits give expected cost at least
`q(K+1/2)` against offline value `qK`. Deterministic first-action failures
give a fixed recursively chosen bit vector costing at least `q(K+1)`.
Taking `q` arbitrarily large defeats an input-independent additive constant.
The repeated family preserves **true indegree at most two**; it does not
preserve outdegree one. Its exact one-bit-per-block advice requirement is
an elementary indistinguishability argument, not a new advice principle.

The candidate upper bound in theory's `LOOKAHEAD_UPPER_BOUND.md` was read
while uncommitted, SHA-256
`3c9508137e0d44fbaef67b503414c3c6600a8cf6f8590663cf4ed030fab71c61`.
This review accepts its general-R1 projection and cut-counting proof:

- Solve each fully visible consecutive `Q=B+L` block offline, then execute
  the blocks in order. Earlier-block true predecessors are already complete.
- Projection of a global schedule onto a consecutive block preserves true
  edges and augmented ROB edges; deleting empty projected cycles is legal.
- Each cycle crossing a cut consumes a distinct job among the last `B-1`
  positions before that cut, so a cut is crossed at most `B-1` times.

For nonempty programs this proves

`T_chunk <= T* + (B-1) floor((N-1)/(B+L))`

`<= [1+W(B-1)/(B+L)] T*`.

There is no claim that this coefficient is sharp. At `B=4,W=3`, taking
`M=max(1,ceil(L/2))` in the repeated lower family and combining it with
this upper bound gives deterministic and oblivious-randomized optimal
competitive excess `Theta(1/(L+1))`. This is an asymptotic order statement,
not exact ratios or leading constants. The general chunk planner need not
be computationally cheap; the separately proved `B=W+1` solver makes this
particular fixed-resource construction polynomial.

## Closest primary predecessor: the same positional reordering window

**Tomás Feder, Rajeev Motwani, Rina Panigrahy, Steve Seiden, Rob van Stee,
and An Zhu (2004)**, *Combining Request Scheduling with Web Caching*.
[CWI report SEN-E0402](https://ir.cwi.nl/pub/4063/04063D.pdf), Sections 1–3
read directly. The authors' [publication record](https://theory.stanford.edu/~tomas/)
also identifies Theoretical Computer Science 324, 201–218.

Section 1 uses a window of `r` positions beginning at the first unserved
request, counting already-served requests inside it; independent `l`
lookahead exposes a longer prefix. The objective is cache misses.
Theorem 3 proves deterministic `3/2` and randomized `5/4` lower bounds.
Theorem 4 uses partitioning, exact dynamic programming between boundaries,
and boundary costs to give `1+16r/l` when `l/(8r)` is integral.
Theorem 5 uses equal-length sequences `(01)^(3t+1)00` and
`(01)^(3t+1)01`: only the last request differs, lookahead sees all preceding
requests, and the correct first choice changes the optimum by one miss.
Repeating the patterns gives deterministic and randomized inverse-lookahead
lower bounds. Theorem 7 extends the partition method to metric costs.

This is direct prior art for the positional window, hidden-last-item
argument, and partition methodology. It is not a verified reduction to
precedence-constrained, width-limited parallel makespan.

## Earlier finite-lookahead makespan predecessor

**Rajeev Motwani, Vijay Saraswat, and Eric Torng (1998)**,
*Online Scheduling with Lookahead: Multipass Assembly Lines*, INFORMS
Journal on Computing 10(3), 331–340,
[DOI](https://doi.org/10.1287/ijoc.10.3.331).
The [author-hosted manuscript](https://theory.stanford.edu/~rajeev/postscripts/xerox.ps.gz)
was located through the author's publication list, downloaded, decompressed,
and converted with `ps2ascii`; Sections 2, 4, and 5 were inspected.
The model has a single processor, repeated passes, fixed return delay `k`,
FCFS output, and an orientation constraint. Theorems 5.1 and 5.2 give
deterministic and randomized finite-lookahead makespan lower bounds with
excess of order `k/L`; Section 5.2 gives approaching-one guarantees.
Corollary 4.2 explicitly repeats independently selected two-instance
patterns. These ideas therefore predate this project. Unit-latency R1
parallel issue is a different model. Extracted formulas were imperfect;
no exact numerical coefficient from the manuscript is reproduced here.

## Other checked model distinctions

**Leah Epstein (1998; journal note 2000)**,
*Lower bounds for on-line scheduling with precedence constraints on
identical machines*, APPROX 1998, 89–98,
[publisher](https://link.springer.com/chapter/10.1007/BFb0053966);
[author institution record](https://cris.haifa.ac.il/en/publications/lower-bounds-for-on-line-scheduling-with-precedence-constraints-o/).
The primary abstract explicitly reveals a job only after its predecessors
complete, and reports deterministic `2-1/m` and randomized
`2-2/(m+1)` makespan lower bounds, including unit jobs. This is important
precedence-discovery prior art. Its full proof was not retrieved, and the
model lacks the present all-but-last instruction-prefix revelation.

The full introduction of **Lassota, Lindermayr, Megow, and Schlöter (2023)**,
[*Minimalistic Predictions to Schedule Jobs with Online Precedence
Constraints*](https://arxiv.org/pdf/2301.12863), likewise reveals jobs when
predecessors finish. Its weighted-completion-time prediction results do
not directly imply the current makespan theorem. Previously audited
bounded-delay packet scheduling instead maximizes transmitted weight;
it is not the same problem merely because packets have unit sizes.

A search hit in Ulrich Michael Schwarz's 2010 dissertation,
[*Approximation Algorithms for Scheduling and Two-Dimensional Packing
Problems*](https://d-nb.info/102000150X/34), Section 2.3, was inspected and
excluded: its lookahead concerns the next machine-availability change.
Similarly, the 2019 non-clairvoyant precedence paper studies unknown
processing times and weighted completion/flow objectives. These were not
silently treated as matching impossibility theorems.

## Novelty decision and search limits

The new literature connection requires tightening the project's framing.
Neither the occupancy-based positional window, a hidden final datum
changing the best first choice, independent repetition, nor inverse-linear
lookahead excess is a new general idea. The particular parallel-issue ROB
theorems may still supply a useful specialization: unusually restrictive
true dependencies, exact resource constants, no extra separator jobs,
and an explicit projection bound with an executable information interface.
Their historical novelty remains unresolved; correctness does not settle it.

No cost-preserving translation from the cache-miss model to the present
unit-job makespan problem was established in this review. Numerical
coincidence of the older `5/4` lower bound also does not establish such a
translation or the current global randomized upper bound.

Representative actual queries, using both engines:

```text
online precedence constrained scheduling finite lookahead critical path unknown graph unit tasks
"online scheduling" "lookahead" "chains"
"online scheduling" "limited lookahead" precedence
"scheduling" "unknown" "chain lengths" "lookahead"
online unit task scheduling unknown precedence graph finite lookahead
"Online Scheduling with Lookahead" "Multipass" pdf
"A note on on-line scheduling with precedence constraints" pdf Epstein
"online scheduling" "lookahead" "partition" makespan
"bounded" "precedence" "lookahead" "batching"
"scheduling" "lookahead" "chunk"
"Combining Request Scheduling with Web Caching" "2004" theoretical computer
```

The stronger engine was also used with a recency filter; some queries
returned irrelevant material, which is not evidence of absence. The
finite pass stopped after the directly relevant cache/reordering source.
`git fetch origin` completed at `2026-10-13T20:25:47Z`; `origin/main` was
`bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`. Only the literature-owned
directory is modified. Raw copyrighted source documents are not committed.
