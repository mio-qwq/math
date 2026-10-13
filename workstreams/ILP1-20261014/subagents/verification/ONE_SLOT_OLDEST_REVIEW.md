# Independent review: one-slot approximation effect and oldest inclusion

Date: 14 October 2026, Singapore. Verifier: subagent C.
Both conclusions below have independent written proof acceptance. The new
finite checks are small; earlier large audits were not repeated. No Lean or
historical novelty claim is made.

## One added issue slot changes a linear approximate window to a constant

Use the chain-prefix/independent-suffix program `P_K` with `N=2K` and the
relative approximate threshold from `APPROXIMATE_SATURATION_REVIEW.md`.
Fix an integer `W>=2` and a real constant

`1/(W+1) <= epsilon < 1/W`.

Then

`B_epsilon(P_K,W) >= (1-W*epsilon)K+1`,

while

`B_epsilon(P_K,W+1) <= W+1`.

Consequently their ratio is at least
`((1-W*epsilon)K+1)/(W+1)` and tends to infinity with `K`. The additive
difference is also unbounded. The approximation factor stays fixed and
positive throughout this comparison.

**Proof including the left endpoint.** Set `q=floor(epsilon*K)`. The first
inequality follows from the exact threshold formula and `q<=epsilon*K`.
For the second, the assumed lower endpoint gives
`q>=floor(K/(W+1))`. Integer division therefore yields

`K+1 <= (W+1)(floor(K/(W+1))+1) <= (W+1)(q+1)`.

At window `B=W+1` and issue width `W+1`, this is exactly the threshold
condition `K+1<=B+q*min(B,W+1)`. If this window exceeds the program length,
use the equivalent capped window `2K`; it is still at most `W+1`. Thus the
bound remains valid for small `K` as well as asymptotically. At the left
endpoint the coefficient of `K` in the first bound is `1/(W+1)>0`, so
linear growth persists. The right endpoint must be excluded.

The statement does not concern every positive `epsilon` at a fixed `W`.
Equivalently, for any chosen fixed `0<epsilon<1/2`, selecting
`W=ceil(1/epsilon)-1` puts it in the displayed interval and gives the same
unbounded ratio phenomenon. No such extension to `epsilon>=1/2` is asserted
for this family.

Independent exact-rational boundary checks cover `W=2..8`, `K=1..20`, and
three fixed tolerances per width: the included left endpoint, the midpoint,
and a point close to the excluded right endpoint. All 420 checks passed.

## An optimal schedule can include the oldest job every cycle at B=W+1

Assume positive integer `W`, set `B=W+1`, and use any finite forward-DAG
program in the eager ROB model. There exists an optimal complete schedule
which is non-delay and issues the oldest unfinished job in every unfinished
cycle. The same argument applies to an optimal continuation from a fixed
reachable state.

**Independent proof.** Among all optimal complete schedules, choose one
whose execution-time vector in program-index order is lexicographically
least. This minimum exists: at the optimal finite horizon there are only
finitely many time assignments.

This chosen schedule is non-delay. Otherwise some ready job scheduled later
could be moved into a vacant current issue slot. Its predecessors already
completed; moving it earlier preserves successor constraints. By the augmented
precedence characterization, it cannot worsen ROB legality. The makespan does
not increase, and the time vector strictly decreases in exactly that one
coordinate, contradicting minimality. If the move shortened the makespan,
it would instead directly contradict optimality.

Suppose the chosen schedule omits the oldest unfinished job `h` in some cycle.
Job `h` is ready because all its predecessors have smaller indices and have
already completed. Non-delay implies that the issue action has size `W`.
Since the entire window has at most `W+1` entries, those `W` issued jobs and
`h` exhaust the window. In particular, all window entries are unfinished and
ready at this cycle's beginning. The full action is every entry except `h`.

At the next cycle, retirement has not advanced because `h` is incomplete;
all other window entries are complete. The only unfinished admitted job is
therefore `h`, and non-delay issues it alone. Choose any job `x` from the
previous full action. Replace these two actions by

`(first_action minus {x}) union {h}`, followed by `{x}`.

All first-action jobs were initially ready. After that action, `x` remains
admitted and ready; it is also the oldest unfinished job because all other
entries preceding it completed. Thus the replacement is legal. After two
cycles its completed set, retired prefix and eagerly admitted prefix are
exactly the original ones, so every later cycle can be kept unchanged.

The replacement may leave additional ready future jobs idle in its second
cycle. This is harmless: the lexicographic minimum was chosen among **all**
optimal legal schedules, not only the non-delay schedules. The first changed
program-index coordinate is `h`, whose time moved earlier; `x>h` moves later.
The unchanged makespan and lexicographically smaller vector contradict the
choice. Therefore the chosen schedule never omits the oldest job.

For a fixed reachable initial state, completed jobs remain fixed and the
same finite minimization is applied only to unfinished jobs. The two-cycle
replacement preserves the completed set after its second cycle, so its
argument is unaffected by the already completed history.

This is an existence/optimal-search restriction. It does not say that every
arbitrary oldest-inclusive choice is optimal, or remove the need to decide
which other ready jobs to issue. Nor does it hold at every larger window:
with `N=4,B=4,W=2` and edges `(1,3),(2,3)`, optimum two requires first action
`{1,2}`, omitting oldest job `0`.

## Fresh finite audit

The independent time-assignment CSP was augmented with the following exact
description of oldest inclusion: `t[0]=0`, and each new maximum of the prefix
of the time vector is at most one above the preceding prefix maximum. If a
record jumps over cycle `c`, the earliest program job still unfinished at `c`
does not issue then; conversely the first job with time at least `c` has time
exactly `c` when no such jump occurs. Direct schedule inspection checks the
property again after construction.

At `B=W+1`, the restricted CSP attained the unrestricted exact optimum for
all 225 tested resource instances from every forward DAG with `1<=N<=4` and
`W=1..3`, and 200 seeded random instances with `5<=N<=10,W=1..4`, indegree at
most two. Every witness passed direct ROB replay and oldest-inclusion checks.
The outside-domain four-job counterexample above was correctly rejected at
horizon two. Source, seed and exact run metadata are recorded in
`one_slot_oldest_audit.py` and `one_slot_oldest_results.json`.
