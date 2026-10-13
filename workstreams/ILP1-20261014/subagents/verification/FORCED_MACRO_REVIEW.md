# Independent review: exact optimization by forced segments

Reviewer: independent verification subagent C. Reviewed theory commit:
`a9408865e844cd05ea7fefda10bf9139f671075c`.
The arbitrary-size statements below have independently accepted written proofs.
The implementation evidence is recorded separately. No Lean verification,
confirmed historical novelty, or online-optimality claim is made here.

## Non-delay optimality does not fix a priority rule

For a reachable completed set `D`, let `r(D)` be its retired-prefix length and
let `R(D)` be the true-dependency-ready unfinished jobs in
`[r(D),min(N,r(D)+B))`. A non-delay action has exactly `min(W,|R(D)|)` jobs.
The oldest unfinished job is always ready, so such an action is nonempty.

There exists a non-delay optimal continuation from every reachable state.
Here is an independent operational proof of the needed monotonicity. Suppose
`D` is contained in a reachable completed set `D'`. Replay a continuation from
`D`, removing jobs already complete in the simulated state. At every boundary
the simulated completed set contains the old one, so its retired prefix `r'`
is at least `r`. A retained issue job `j` cannot be below `r'`, since it is
unfinished; its old admission gives `j<r+B<=r'+B`. It therefore remains in the
simulated window. Its true predecessors remain complete. The shortened action
respects width and results still become usable only next cycle. Induction
replays the entire continuation in at most its original time.

An optimal continuation exists within the finite sequential horizon. Extend
its first action to non-delay size. The resulting completed superset has a
continuation of no greater duration by the preceding argument. Induct on the
strictly smaller number of unfinished jobs to choose a non-delay continuation
from there. Its combined cost cannot beat the optimum and hence equals it.
This proves existence of a non-delay optimum; it does not assert that every
choice among ready jobs is optimal.

## Exact scalar recurrence when B=W+1

Put `h(D)=|D|-r(D)`. Every completed but unretired instruction remains inside
the current window: a job was admitted below an earlier prefix plus `B`, and
the prefix only increases. Thus the number of unfinished window entries is
`min(B,N-r(D))-h(D)`, at most `B-h(D)`.

When `B=W+1` and `h(D)>=1`, at most `W` jobs can be ready. There is exactly one
non-delay action: all ready jobs. A state can branch only when `h(D)=0`,
meaning `D=[0,i)`, and all `B` window entries are ready. That state has `B`
possible non-delay actions, each omitting one entry. If at most `W` entries
are ready, there is only one action. This argument needs no oldest-inclusive
normalization lemma.

From a clear prefix `i`, choose one first action and then use the unique
non-delay action until the completed set is a prefix again. Every cycle
finishes at least one new job, so this macro must end within `N-i` cycles.
Its endpoint is a clear prefix `j>i`; the terminal set is itself a clear
prefix. Denote its duration by `ell(i,A)`. If `F_i` is the optimum from a
clear prefix, then

\[
F_N=0,\qquad F_i=\min_A\bigl(\ell(i,A)+F_{j(i,A)}\bigr).
\]

For the lower inequality, take a non-delay optimum: its first action is listed
and all actions until the next clear prefix are forced, so it follows exactly
one listed macro. Its remainder costs at least `F_j`. For the opposite
inequality, concatenate any listed legal macro with an optimum at its
endpoint. Backward induction applies because endpoints strictly increase.
Executing the first `i` jobs sequentially makes every clear-prefix state
reachable, including those no whole-program optimum happens to visit.

This is an arbitrary-makespan theorem for every finite forward dependency DAG,
without an assumption that `N` is divisible by `W` or that the work lower
bound is attainable. Width one, an empty program, truncated terminal windows,
and `W>=N` cause no exception. It does not replace the sharper linear
perfect-saturation criterion and its short obstruction certificates.

## Implementation and complexity review

The primary theory implementation `forced_segment_dp.py` has SHA-256

`6798ccdf97277f16731bafb86afcd68fe5623620b8541304c750057b0093a21d`.

It initializes predecessor counters for each clear-prefix macro, fixes an
action before decrementing any counter, and updates retirement and admission
only after the action completes. Hence it implements the required one-cycle
latency without same-cycle dependent execution. An initially omitted ready job
is retained exactly once. An existing admitted successor is queued when its
counter reaches zero; newly admitted jobs are queued in the disjoint admission
interval. No ready job is duplicated or lost. Duplicate edge-list entries are
handled consistently on both predecessor and successor sides.

Each macro initializes `O(N+E)` data and subsequently processes each job and
edge at most once. The `N` nonterminal clear-prefix nodes have at most
`min(B,N)` choices each. Saving only the winning omission, endpoint, and cost,
then re-simulating winning macros, gives

\[
O\bigl(N\min(B,N)(N+E)\bigr)\text{ time},\qquad O(N+E)\text{ working space},
\]

in the usual indexed-array model, apart from the `O(N)` returned schedule.
The same bound contains initialization and final replays. Terminal truncation
means no iteration is proportional to an arbitrarily oversized numeric `W`.
No defect was found in the reviewed source.

The independent verifier's implementation deliberately uses Python sets and
repeated ready scans and keeps schedule tails. It is an exact reference
implementation, not evidence that this more efficient complexity bound holds
for that reference code. The complexity bound above was checked against the
separate predecessor-counter implementation.

## General window excess: an independently checked XP extension

For a nonempty program normalize resources to `B=min(B,N)` and
`W=min(W,B)` and put `c=B-W`. If `c=0`, all-ready actions are unique and
give an optimum directly. For `c>=1`, branching requires `h<c`. Apart from
its retired prefix `r`, a candidate state is determined by `h` completed
positions among at most `B-1` later window positions. Thus the nonterminal
candidate count is at most

\[
N\sum_{h=0}^{c-1}\binom{B-1}{h}.
\]

For a fixed `h`, the number of non-delay actions is at most
`binom(B-h,W)=binom(B-h,c-h)`. This also bounds the single action when
at most `W` jobs are ready. Compressing all forced segments produces an exact
acyclic macro graph, since each macro strictly increases the completed set.
Its arc bound is

\[
N\sum_{h=0}^{c-1}\binom{B-1}{h}\binom{B-h}{W}
\le N(2^c-1)\binom{B}{c}.
\]

Independently, the termwise identity is
`binom(B-1,h) binom(B-h,W) = ((B-h)/B) binom(B,c) binom(c,h)`.
Summing `binom(c,h)` for `h<c` gives `2^c-1`; dropping the factor at most
one proves the displayed bound. A forced segment is at most `N` cycles and
can be simulated with the same counter method. The resulting exact algorithm
is polynomial for each fixed `c`, hence XP in `c`; the exponent still depends
on `c`, so this argument does not prove FPT in `c` alone.

The independent prototype retains every reachable state with `h<c`, even if
its action is unique, and compresses only states with `h>=c`. This is a
possibly less compressed graph with the same candidate and arc bounds. Its
exactness and bounds were checked as well as the `c=1` scalar recurrence.
The theory's general-`c` statement remains a written algorithmic result;
its efficient primary implementation currently covers `c=1` only.

## Actual verification and reproducibility

From this directory:

```sh
python forced_macro_audit.py --primary-module ../theory/forced_segment_dp.py
```

The optional import is used only in the audit driver. Neither independent
macro solver calls the primary implementation or the time-variable CSP;
the latter remains the independent optimal-value oracle. Every returned
macro schedule is checked by direct operational ROB replay.

The recorded run checked:

- Every forward DAG, with unrestricted fan-in, on `0<=N<=5`, all
  `1<=W<=4`, and `0<=c<=2`: 13,200 general-excess optimum comparisons;
  the `c=1` slice gives 4,400 scalar-recurrence comparisons.
- Seed `2026101410`: 180 fresh indegree-at-most-two programs with
  `6<=N<=12`, `1<=W<=8`, and `1<=c<=3`.
- 15 separate resource-normalization cases with `W>B`, `B>N`, `W=1`,
  independent jobs, a serial chain, and a single job.
- In total, 4,472 scalar-recurrence/primary/CSP comparisons and direct primary
  trace replays; 26,746 primary prefix values agreed with the independent
  scalar recurrence. The general-excess prototype had 13,380 CSP comparisons,
  in addition to the 15 resource-boundary comparisons. All passed.

The largest observed macro in these runs lasted five cycles. The algorithms
and proof permit arbitrary lengths up to the number of remaining jobs; they
do not assume the one- or two-cycle full-throughput macro classification.

The exact run finished in 1.694372382000438 seconds. Finish time, seed, tested
ranges, counts, and immutable source hashes are in `forced_macro_results.json`.
The primary source hash was checked before and after the run. These finite
results audit implementations and boundary cases; arbitrary-size correctness
rests on the independent mathematical argument above.
