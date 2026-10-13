# Independent review: a chain followed by independent instructions

Reviewer: literature subagent D. Date: 2026-10-13 UTC.
Baseline worktree commit before this review: `5c2100fc87bc7bb6ca3d5588ce5eaded77edac29`.
`git fetch origin` succeeded during this review; `origin/main` remained
`bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.
This follow-up supplements the existing literature and threshold reviews.
It supplies an independent written proof and a targeted prior-art assessment.
The reviewer did not run Lean or a scheduling solver for this follow-up.

## Assessment and precise scope

The proposed exact makespan and width-two approximate-window formula are
correct under R1. Their proofs work for all positive window capacities and
all `K≥1`, with issue width at least two. The lower bound is a bound on every
offline schedule, not a limitation caused by an uninformed policy.

This family strengthens the approximation discussion in `THRESHOLD_REVIEW.md`:
for fixed width and a sufficiently small fixed relative makespan tolerance,
the minimum sufficient window grows linearly with program length. There is
also an unbounded *approximate* window reduction when the width increases by
one and the tolerance crosses the corresponding throughput threshold.

The mechanism of finite-window blocking, including distant independent work
being inaccessible while older instructions remain, is well established in
architecture literature. The new proof should be presented as an exact
extremal calculation for the stated model, with historical novelty unconfirmed.
It does not show that realistic workloads generally require such windows.

## Independently checked formula

Use zero-based instruction positions. Let `K≥1`, `N=2K`, and let
`0→1→⋯→K−1` be a chain. The remaining instructions `K,…,2K−1` have no true
dependencies. All instructions must execute: the independent instructions may
each compute an observable output. There is no dead-code elimination.
The true DAG has maximum indegree and outdegree one and height `K`.

The R1 hypotheses used here are eager in-order admission, capacity `B` counting
all admitted but unretired instructions, unit execution with results available
next cycle, issue bound `W`, unlimited end-of-cycle prefix retirement, and
refill before the following cycle. In particular, completed instructions
behind an unfinished chain instruction still occupy the window.

For integers `B≥1,W≥2`, write

`Q=max(0,K−B+1)` and `M=min(B,W)`.

Then the exact optimum is

`T*(P,B,W) = K + ceil(Q/M)`.                                      (1)

### Lower bound

Consider any legal schedule. Suppose the final chain instruction completes
at the end of the `τ`th cycle. Strict unit-time dependencies give `τ≥K`.
Before that cycle ends, the retired prefix contains at most the first `K−1`
instructions. Consequently the largest possibly admitted position is
`K+B−2`. At most `B−1` tail instructions can have executed by the time the
chain completes; if `B−1>K`, the weaker bound remains valid. Therefore at
least `Q` tail instructions remain unexecuted after those `τ` cycles.

Every subsequent cycle can execute at most `M` instructions: issue width
bounds this by `W` and window capacity by `B`. These remaining instructions
need at least `ceil(Q/M)` additional cycles. Thus every schedule takes at
least `τ+ceil(Q/M)≥K+ceil(Q/M)` cycles. Delaying the chain cannot invalidate
this bound or admit more than `B−1` tail instructions before it completes.

### Matching schedule

Execute chain instruction `c` in cycle `c`, for `0≤c<K`.
Let `h=min(K,B−1)`. In each of the last `h` chain cycles, also execute one
tail instruction, in increasing program order. Width two suffices.

For `B≤K`, the first tail instruction is admitted at cycle `K−B+1`;
each subsequent chain retirement admits the next one. For `B≥K+1`, a tail
instruction can accompany every chain instruction starting in cycle zero.
Thus every prescribed issue is inside the window. When the chain completes,
all `h` completed tail instructions retire with it. Execute the remaining
`Q=K−h` consecutive independent instructions in batches of `M`, with a
possibly smaller final batch. Each batch retires immediately and enables
the next refill. The total is (1).

### Edge cases and exact saturation

`B=1` gives `T*=2K`. For `W=1`, separately, `T*=2K` at every capacity.
`K=1` is included. Capacities exceeding `N` have the same behavior as `N`.
For every `W≥2`, the unrestricted-window benchmark is `K`, and

`B_sat(P,W)=K+1`.

Increasing width does not lower this family's *exact* saturation threshold.
It can lower the approximate threshold below.

## Approximate saturation and a width increment

Specify the objective precisely. Here

`B_ε(P,W)=min {B≥1 : T*(P,B,W)≤(1+ε) T*(P,N,W)}`

for real `0≤ε<1`. This is relative makespan tolerance. It is equivalent to
retaining at least the fraction `1/(1+ε)` of the unrestricted optimal IPC;
it is not the convention of retaining `1−ε` of that IPC.

Let `a=floor(εK)`, so `0≤a≤K−1`. By (1), feasibility is equivalent to

`max(0,K+1−B)≤a min(B,W)`.

Since the right side is nonnegative, this is equivalent to both
`K+1−B≤aB` and `K+1−B≤aW`. Therefore the exact integer inversion is

`B_ε(P,W)=max(ceil((K+1)/(a+1)), K+1−aW)`, for `W≥2`.             (2)

In particular,

`B_ε(P,2)=max(2,K+1−2 floor(εK))`.                              (3)

To check the simplification, capacity one is infeasible for `ε<1`.
For every `B≥2`, `min(B,2)=2`, so the remaining condition is exactly
`K+1−B≤2a`.

For fixed `W≥2` and `ε<1/W`, (2) implies

`B_ε(P,W)≥(1−εW)K+1=Ω(N)`.

For `ε≥1/W`, capacity `W` suffices, or capacity `N` if `N<W`.
Indeed write `K=qW+r`, `0≤r<W`. Then `floor(εK)≥q`, and
`K+1−W=qW+r+1−W≤qW`. This satisfies the condition at `B=W`.
Thus, when both resources are fixed, `1/W` is the sharp dividing tolerance
between the linear lower bound and a bounded sufficient window in this family.

### Robust unbounded window reduction

Fix `W≥2` and `1/(W+1)≤ε<1/W`. For the same programs as `K→∞`,

`B_ε(P,W)≥(1−εW)K+1`, whereas `B_ε(P,W+1)≤W+1`.

Their difference and ratio are unbounded. Both unrestricted-window optima
remain `K`. For `W=2`, the tolerance interval is `[1/3,1/2)`.
More generally, for every fixed `0<ε<1/2`, choose
`W=ceil(1/ε)−1≥2`; the interval condition holds. This gives an unbounded
approximate-window reduction from one additional issue slot, with the two
widths fixed independently of program length. The `ε=0` case is supplied
by the different layered family in `THRESHOLD_REVIEW.md`, not by this family.

The claim concerns required window capacities at a specified performance
target. The optimal makespan itself remains monotone in either resource.
For `ε<1/3`, this chain-tail family requires linear capacity at both widths
two and three; it does not establish the same fixed-width pair for every
positive tolerance.

## Program order is essential

The threshold is a property of the *ordered* dependency DAG. Interleave the
same chain vertices with the independent vertices in program order. Then
width two and window two execute one chain instruction and one independent
instruction each cycle, finishing in `K` cycles. The unlabeled true DAG is
unchanged, while its width-two exact saturation capacity changes from `K+1`
to two. This observation does not permit reordering in R1; it identifies why
ordinary precedence scheduling results do not determine ROB capacity without
the program-order information.

## Targeted primary-source comparison

The following sources were actually opened in this follow-up. Locations name
sections rather than theorem numbers because the relevant passages do not
state numbered theorems for this optimum or threshold.

1. **Dean M. Tullsen and Brad Calder, 1998.**
   [Computing Along the Critical Path](https://cseweb.ucsd.edu/~calder/papers/UCSD-CSE98-CPProfile.pdf),
   UCSD technical report, October 1998. Read §3 and §§4.1–4.3, printed
   pages 3–4 and 10–11. The profiler has in-order window entry/exit and adds
   window-edge dependencies for instructions prevented from entering a full
   window. Its model includes variable latencies, caches and prediction;
   its objective is critical-path profiling. This is direct prior art for
   representing window restrictions by additional dependencies, earlier than
   Fields et al. 2001. The inspected passages do not establish (1) or (2),
   nor a globally optimal finite-width scheduling theorem.

2. **Alvin R. Lebeck, Jinson Koppanalil, Tong Li, Jaidev Patwardhan and
   Eric Rotenberg, 2002.**
   [A Large, Fast Instruction Window for Tolerating Cache Misses](https://iscaconf.org/isca2002/FinalPapers/alvy-lebeck.pdf),
   ISCA 2002. Read §§2.1–2.2, printed pages 2–3. Their explanation explicitly
   retains completed instructions until in-order commit and describes a
   window blocked by a cache miss and its dependency chain. Larger windows
   expose independent future work. Their limit study is a simulation with
   multi-cycle operations and finite frontend/commit resources. The broad
   blocking mechanism is therefore prior art; the passages do not give an
   exact optimal makespan or relative-tolerance capacity theorem for unit jobs.

3. **Srikanth T. Srinivasan, Ravi Rajwar, Haitham Akkary, Amit Gandhi and
   Mike Upton, 2004.**
   [Continual Flow Pipelines](https://pages.cs.wisc.edu/~markhill/restricted/asplos2004_cfp.pdf),
   ASPLOS 2004, pp. 107–119. Read §§1, 3.1–3.3, 4.3 and the opening of §5.
   The paper separates ROB, scheduler and register limits, and uses resource
   reclamation and checkpoint mechanisms to reach distant independent work.
   Page 115 also discusses dependency chains whose total latency is long
   despite smaller individual latencies. These observations precede the
   chain-blocking interpretation. Its modified retirement/resource model
   cannot be substituted for R1 when asserting the formula above.

4. **Henry Wong, 2013.**
   [Measuring Reorder Buffer Capacity](https://blog.stuffedcow.net/2013/05/measuring-rob-capacity/),
   author research blog, 14 May 2013. Read the introduction and the sections
   on instruction-window and ROB capacity. Two cache misses separated by
   independent filler instructions overlap only while the later miss remains
   within the ROB. This is primary experimental evidence for the known
   distant-work blocking mechanism, not a peer-reviewed arbitrary-program
   theorem. Its long-latency loads and measured hardware differ from R1.

5. **Barbara Bluestein Simons and Vivek Sarkar, 2000.**
   [US6044222A: System, method, and program product for loop instruction
   scheduling hardware lookahead](https://patents.google.com/patent/US6044222A/en),
   published 28 March 2000, filed 23 June 1997. Read the abstracted definitions
   and lookahead model. It uses a contiguous fixed-size instruction window
   that advances when the first instruction is issued/dispatched, and
   optimizes compiler permutations within loop basic blocks. It gives
   lookahead-aware loop lower-bound reasoning. Issue-based release, latency
   assumptions, loop objectives and permitted compiler rearrangement require
   a separate equivalence proof before transferring any result to R1.
   No assertion about patent validity or comprehensive algorithm correctness
   is made here.

The detailed general literature audit remains in `LITERATURE_REVIEW.md`.
In particular, the unresolved full-text access to Dubey–Adams–Flynn 1994
remains a material gap for exhaustive novelty claims; this follow-up does
not close it. Generic buffer-reordering algorithms also require a careful
comparison of release rules before they count as the same problem.

## Search record and conclusion

Queries were executed on 2026-10-13 UTC, using the available two-engine web
search service. Exact queries in this follow-up included:

```text
"instruction window" "serial" "independent" "chain"
"reorder buffer" "head-of-line blocking" parallelism
bounded lookahead window precedence scheduling chain independent tasks
instruction level parallelism finite window critical path analytical model queue head blocking
Computing Along the Critical Path instruction window 1998 authors pdf
"reorder buffer" "chain" "independent" "window size" scheduling
"instruction-level parallelism" "lookahead" limits window theoretical
"instruction scheduling" "window" "approximation" "chain"
"precedence" "bounded" "lookahead" scheduling buffer
"reorder buffer" "optimal" "window" "theorem"
"instruction window" "chain" "independent instructions" limits
```

Some results concerned compiler scheduling, packet buffering, or unrelated
uses of lookahead. They were not treated as equivalent theorems. Search
snippets and upload/crawl dates were not used to infer publication priority.
The inspected primary sources establish strong conceptual prior art. This
bounded search neither finds an exact coverage theorem nor establishes its
absence. A suitable present classification is `WRITTEN_PROOF`,
`INDEPENDENTLY_REVIEWED` for the team's formula, and
`NOVELTY_UNCONFIRMED`. The general-width inversion and tolerance-crossing
corollary are reviewer-derived written consequences and need another reviewer
before receiving their own independent-review label. Lean coverage must be
reported separately by the formalization team.
