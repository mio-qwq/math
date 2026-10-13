# Independent review: exact work-bound attainment by one-/two-block tiling

Verification subagent C, 2026-10-13 UTC. The main/theory agents supplied the
structural claim; this review independently reconstructs its proof and compares
a separate implementation against the time-variable CSP. Verdict: accepted under
the stated model. No novelty or Lean claim is made here.

## Statement and complete macro definitions

Let `W>=2`, `B=W+1`, and `N=kW`, with `k>=0`. Partition the program into
consecutive blocks of `W` instructions. At a clear-prefix state beginning with
block `j`, there are two canonical macros:

- `A_j`: execute all `W` instructions of block `j` in one cycle.
- `B_j`: on blocks `j,j+1`, let `h` be the last instruction of block `j`
  and `x` the first instruction of block `j+1`. Execute block `j` without
  `h`, together with `x`; then execute `h` and block `j+1` without `x`.

The `B` macro is available only if `j+1<k`. Each macro is declared legal when
all true edges with both endpoints in it go strictly from an earlier cycle to
a later cycle. Edges from the preceding prefix are already satisfied, and
forward edges into the remaining suffix will be satisfied after the macro.

Then `T*=k` if and only if the block sequence can be tiled by legal `A`
and `B` macros. A tiling is a legal optimal schedule of exactly `k` cycles.
If no tiling exists, `T*>k`; this test alone does not compute the larger optimum.
The restriction `N=kW` is essential to the proof, and the statement does not
claim to characterize `T*=ceil(N/W)` when `W` does not divide `N`.

## Necessity of only these two shapes

By the separately reviewed oldest-inclusive normalization theorem for
`B=W+1`, a makespan-optimal schedule can always include the oldest unfinished
job each cycle. If `T*=k`, the `kW` jobs force every one of its `k` cycles
to issue exactly `W` jobs.

Consider a clear-prefix state. If only the final `W` jobs remain, they must
all issue together, giving `A`. Otherwise at least two blocks remain, and the
initial window has exactly `W+1` unfinished jobs. Its first action omits one
job, at zero-based offset `r` from the oldest. Oldest inclusion gives `r>=1`.
If `r=W`, the action is exactly the first block, giving `A` and an immediate
return to a clear-prefix state.

If `r<W`, precisely the preceding `r` jobs retire after this action. The
window admits precisely `r` replacements: enough jobs remain because at least
`2W` jobs were present before the action. The next window has one omitted
old job, `r` new jobs, and completed blocked entries. Thus at most `r+1`
jobs can issue in the next cycle. Full utilization forces `r+1>=W`.
Consequently `r=W-1`. Its first action is exactly block `j` except its last
job, plus the next block's first job. The next cycle has exactly `W`
unfinished entries and must issue them all. This is `B`, after which exactly
two complete blocks have finished and another clear-prefix state is reached.

Induction through these clear-prefix boundaries yields a tiling. This uses
the existence of an oldest-inclusive optimum; it does not assert every
work-bound schedule has this shape before normalization.

## Sufficiency and the artificial precedences

Inside `A`, the maximum index difference of two same-cycle jobs is `W-1`.
Inside either cycle of `B`, it is `W`. Both are smaller than `B=W+1`,
so no artificial ROB precedence has same-cycle endpoints. Every artificial
edge between the two cycles of `B` points from its first cycle to its second:
the only index-order inversion is `h,x`, whose index gap is one and therefore
is not artificial. All artificial edges between successive macros point from
the completed prefix into a later macro.

Hence the canonical macros automatically satisfy every artificial precedence.
Checking their true edges suffices for the exact ROB timing constraints.
Concatenating a legal tiling preserves all true and artificial precedences,
uses exactly `W` jobs each cycle, and takes `k` cycles. The work bound proves
its global optimality. This also handles the empty tiling at `N=0` and the
single-block case, where the effective window exceeds the program length.

## Linear algorithm and a component criterion

Let `A[j]` and `B[j]` be the legal-macro flags. For each true edge `(u,v)`,
let `p=floor(u/W)` and `q=floor(v/W)`. It can affect a single-block macro only
when `p=q`, in which case that macro is invalid. It can affect a two-block
macro only when both endpoints lie in its two blocks. There are at most two
such starts, namely `p-1` and `p`. Check the endpoint phases for each valid
start; the edge invalidates the macro if its source phase is greater than or
equal to its target phase. This is constant work per input edge.

The forward block DP has transitions `j -> j+1` when `A[j]` is legal and
`j -> j+2` when `B[j]` is legal. Flags and DP use `O(k)` space and
`O(k+|E|)` time; producing the schedule uses `O(N)` output time. Thus the
entire algorithm has `O(N+|E|)` time with arbitrary, variable `W`.
This complexity does not rely on checking every edge afresh at each macro.

There is also a direct criterion. Draw a path edge between blocks `j,j+1`
exactly when `B[j]` is legal. Its connected components are consecutive block
intervals. Every even-size component can be covered by its alternating legal
two-block macros. An odd-size component can be covered if and only if one
of its blocks at an **even zero-based offset from its left end** has legal
`A`. For necessity, the leftmost singleton in any tiling is preceded by only
two-block macros, placing it at even offset. For sufficiency, use such a
singleton; the two sides have even length and can each be paired internally.

This path-tiling observation is elementary; the substantive model-specific
step is the normalization from fully utilized ROB schedules to these macros.

## A short negative certificate

An infeasible odd component yields a negative certificate: its endpoints;
the illegality of the two macros crossing its boundaries, unless already at
a program endpoint; and the illegality of `A` at each even-offset block.
Each illegal `A` has a true edge internal to that block as a witness. Each
illegal boundary `B` has a true edge whose endpoints have equal or reversed
phases as a witness. At most `ceil(component_length/2)+2` edges suffice.

The verifier need not even establish that all interior `B` macros are legal.
An odd interval closed by illegal boundary macros and with all even-offset
singletons illegal is already impossible to tile: its first singleton, which
must exist, would have even offset. Thus interior legality and maximality of
the component are optional information for a negative certificate. The
component scan remains a simple way to find a certificate when one exists.

This is a proof of impossibility at exactly `k` cycles and, by the work bound,
at all shorter horizons. It does not need an enumerated ROB state space.

## Independent computation

`packed_tiling_audit.py` implements macro flags with a per-edge constant number
of tests, a block DP, the separate component scan, and a canonical schedule
constructor. It compares feasibility with the independent time-variable CSP
at horizon `N/W`; every returned schedule passes direct ROB replay.

The actual run checked 4,715 effective graphs across `(W,N)` equal to
`(2,0),(2,2),(2,4),(2,6),(3,3),(3,6),(4,4)`. At each pair it enumerates all
true edges whose gaps are below `W+1`; larger-gap true edges are redundant
with ROB precedences. It then checked 540 seeded indegree-at-most-two graphs
with `W=2,...,10` and one through six blocks, plus a forced-swap positive
construction for every `W=2,...,20`. The latter makes the first `A` invalid
using edge `0 -> W-1`, while leaving the two-block `B` legal.

Finally, 2,731 arbitrary Boolean `A/B` flag patterns with at most six blocks
were checked against both the DP and component criterion. All checks passed.
The empty case, final single block, and rejection of nonintegral `N/W` are
explicitly covered. Seed, source hashes, scope, and actual runtime are in
`packed_tiling_results.json`. These are finite implementation checks; the
general equivalence and component proof are given above.

Status: **WRITTEN_PROOF**, **INDEPENDENTLY_REVIEWED**;
**NOVELTY_UNCONFIRMED**; no Lean verification claimed by this subagent.
