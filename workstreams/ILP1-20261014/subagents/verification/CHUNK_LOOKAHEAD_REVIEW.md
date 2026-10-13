# Independent review: chunk upper bound and lookahead asymptotic order

The chunk strategy was proposed by the theory agent. This review independently
checks its projection argument, counting bound, observation semantics, and
interaction with the repeated lower-bound family. Status: independently
accepted WRITTEN_PROOF, with separate finite implementation evidence below.
No Lean verification or historical originality claim is made.

## Global deterministic upper bound

Fix positive `B,W`, an integer `L>=0`, and the same incoming-operand prefix
lookahead model used in `REPEATED_LOOKAHEAD.md`. At a clear prefix `s`, all
incoming operands of jobs below `min(N,s+B+L)` are visible. Divide the program
into consecutive chunks of length `Q=B+L`, except for a shorter final chunk.
For each chunk, compute an exact optimum after treating all predecessors in
earlier chunks as already complete, execute that local schedule, and continue
with the next chunk.

This is an online policy in the stated information model. A whole chunk is
visible when its processing starts, and forward dependencies cannot point to
later chunks. The execution starts and ends at clear prefixes. Jobs of a later
chunk may already be admitted, but ignoring them does not remove any earlier
chunk job from the window. The local truncated ROB and global ROB therefore
give exactly the same admission condition for the jobs currently executed.

The model counts execution cycles, not scheduler computation. The policy may
use an exact finite search within each visible chunk. At `B=4,W=3`, the
independently reviewed `B=W+1` macro algorithm makes this local planning
polynomial in chunk size. No real-hardware timing conclusion follows.

Let `T_chunk` be the total chunk-policy duration and `T*` the whole-program
offline optimum. For `N>=1`, the accepted bound is

\[
T_{\rm chunk}\le T^*+(B-1)\left\lfloor\frac{N-1}{B+L}\right\rfloor
\le\left(1+\frac{W(B-1)}{B+L}\right)T^*.
\]

For `N=0`, both durations are zero and the policy returns the empty schedule;
the expression involving `floor((N-1)/Q)` is not used.

## Independent projection proof

Take an optimal global schedule. Project each cycle onto a fixed chunk, delete
empty projected cycles, and translate its indices to start at zero. Every
outside true predecessor is in an earlier chunk and has been completed before
the local execution starts. A same-chunk predecessor appears in a strictly
earlier nonempty projected cycle. Removing empty cycles never merges two
nonempty cycles, so the unit-latency condition is preserved.

For admission, suppose job `j` was issued in the global schedule, whose retired
prefix at that boundary is `r`. The local state has completed the same earlier
same-chunk issue jobs, and it also treats every job before the chunk as already
complete. Its first unfinished index within the chunk, in global coordinates,
is `r'>=r`. Job `j` is still unfinished there, so `j>=r'`; its original
admission yields `j<r+B<=r'+B`. Thus it remains admitted in the projected
execution. Each projected action respects width. This proves that every
projected schedule is locally legal.

Let `ell_a` be the number of nonempty projected cycles for chunk `a`. The
chunk optimum is at most `ell_a`, hence `T_chunk<=sum_a ell_a`. If a global
cycle touches `c_t` chunks, it contributes `c_t` to this sum. Its extra charge
over one global cycle is at most the number of chunk boundaries it crosses:
`c_t-1` is no greater than that number. This remains a valid bound even if
a cycle skipped an intermediate chunk. In the present construction, it
actually cannot cross two boundaries: `Q>=B`, while any one ROB action has
index span at most `B-1`. The more general counting inequality avoids relying
on that extra observation.

At a cut before index `x`, a crossing cycle issues some job `i<x` and some
job `j>=x`. Both are in one window, so `j-i<=B-1`, giving
`x-B+1<=i<x`. Choose one such left job as the charge for that crossing cycle.
Each job issues only once, so different crossing cycles receive different
charges among the `B-1` positions immediately before the cut. There are at
most `B-1` crossing cycles per cut.

There are exactly `floor((N-1)/Q)` cuts for `N>=1`. Summing the charge gives
the additive bound. Finally, the work inequality `N<=W T*` and
`floor((N-1)/Q)<=N/Q` give the multiplicative bound. One may replace `W` in
this last bound by `min(W,B)` when the supplied issue width exceeds the
physical window; the unnormalized statement remains correct.

## Joint consequence with the repeated lower construction

Specialize to `B=4,W=3`. Define `rho_D(L)` as the infimum of deterministic
competitive coefficients allowing a finite input-independent additive
constant; define `rho_R(L)` similarly for expected cost on fixed oblivious
inputs, allowing randomized policies. The observation frontier and lack of an
outgoing-use oracle are exactly the same in both definitions.

Put `M=max(1,ceil(L/2))` and `K=M+2`. The repeated family proves lower bounds
that survive every fixed additive constant. The chunk policy has no additive
loss beyond its multiplicative coefficient and gives a global upper bound.
Therefore

\[
1+\frac1{2K}\le\rho_R(L)\le\rho_D(L)
\le 1+\frac9{L+4},\qquad
\rho_D(L)\ge1+\frac1K.
\]

Since `K` is of order `L+1`, both optimal competitive excesses satisfy

\[
\rho_R(L)-1=\Theta\!\left(\frac1{L+1}\right),\qquad
\rho_D(L)-1=\Theta\!\left(\frac1{L+1}\right).
\]

This determines the asymptotic order, not an exact global coefficient. The
family matching upper bounds in `REPEATED_LOOKAHEAD.md` are used only to
describe that family's minimax values; the global upper bound comes from the
chunk policy. The lower construction has true indegree at most two and the
global upper works for arbitrary fan-in, so the same order remains valid when
the input class is restricted to at most two true inputs per instruction.

## Actual independent verification

Run `python chunk_lookahead_audit.py` from this directory. It uses the separate
time-variable CSP to solve the global and local chunk instances, and direct
ROB replay checks both the concatenated policy trace and every projected local
trace. No primary solver is imported.

- Every forward DAG with `0<=N<=4`, `1<=B,W<=4`, `0<=L<=3`: 4,864 chunk cases.
- Seed `2026101412`: 100 binary-input random cases with `6<=N<=14`,
  `1<=B<=6`, `1<=W<=8`, `0<=L<=6`, followed by 60 further cases with
  `B=4,W=3`, `7<=N<=18`, `0<=L<=6` using the same seeded generator.
- Total: 5,024 chunk cases, 1,376 independent global CSP solves,
  7,389 direct projected-trace replays, and 2,429 cut-charge checks.
  The tested schedules contain 346 actual crossing cycles.

All projection, complete concatenation, additive, multiplicative, and charge
injection checks passed. The range includes empty inputs, partial final
chunks, a single visible chunk, width one, and `W>B`. Runtime was
0.2784490949998144 seconds. `chunk_lookahead_results.json` records exact finish
time, tested ranges, seed, counts, and source hashes. Finite checks are not
used in place of the projection and counting proof above.

## Addendum: independent inspection of the causal primary implementation

After completing the mathematical audit above, this agent inspected theory
commit `5730353c385345e294d5f2a6d2b0d50ea83fca4a` and its final
`LOOKAHEAD_UPPER_BOUND.md`. The primary `chunk_lookahead.py` accepts only
`N,L,read_parents,issue`. It requests each current chunk's predecessor masks,
shifts away earlier-prefix operands, invokes the already-reviewed local exact
solver, and issues its translated schedule before reading the next chunk.
No later chunk's graph is an argument or read by its source. The mask shift
preserves exactly the intra-chunk parents, whose index gaps are unchanged.

To verify this separate implementation, `causal_chunk_audit.py` supplies its
own persistent eager window, admission/retirement pointers, completed set, and
incoming-edge store. Every actual read is checked against the current
`r+4+L` frontier; every action is checked before any of its jobs complete.
Twenty targeted cases include empty programs, whole-program visibility,
partial chunks, predecessors crossing chunk boundaries, the nine-job policy
counterexample, and repeated hidden-bit blocks. All 199 reads and 104 issue
cycles passed, and independent CSP chunk costs agree. Three malformed observed
masks were rejected before any issue. The earlier large enumeration was not
rerun for this source inspection.

Actual source SHA-256 values, verified unchanged after the run, are:

- `chunk_lookahead.py`:
  `5595bd9263010789e7507ef9d67a4805352bfa1bb6bc7cc54fa80bfd77effe70`.
- `forced_segment_dp.py`:
  `6798ccdf97277f16731bafb86afcd68fe5623620b8541304c750057b0093a21d`.

The targeted run took 0.004582453000693931 seconds; its exact metadata is saved
in `causal_chunk_results.json`. Reproduce it with
`python causal_chunk_audit.py --primary-directory ../theory`.
