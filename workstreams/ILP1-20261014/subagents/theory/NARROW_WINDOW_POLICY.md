# Oldest-inclusive normalization and the three-entry online gap

Date: 14 October 2026. ILP1-20261014 theory subagent A.
Status: written proofs; historical novelty unconfirmed; no Lean claim.
Use the exact eager unit-latency ROB model from `STRUCTURAL_RESULTS.md`.

## 1. Normalization when the window has one more slot than issue width

**Theorem 1.** Let `W≥1` and `B=W+1`. For every finite forward-dependence
program, there is a makespan-optimal schedule which is non-delay and which
issues the oldest unfinished instruction in every nonterminal cycle.
The same statement holds for optimal continuations from any reachable
completed state.

Here non-delay means issuing as many currently ready jobs as capacity
allows. The result is an existence/normalization theorem for offline
optima, not a claim that every online policy making this choice is optimal.

**Proof.** Fix a reachable completed state, let the optimal remaining
makespan be `T`, and select the lexicographically least vector of issue
times among **all** legal makespan-`T` continuations. Use increasing
program index for the vector coordinates of the unfinished jobs. This
minimum exists because there are finitely many maps into `{1,...,T}`.

First, the selected continuation is non-delay. If a cycle has an unused
issue slot and an unissued ready job, move that job from its later cycle
into this cycle. Every predecessor was already complete, and every
successor remains after the job; augmented precedence and issue capacity
are therefore preserved. The makespan does not increase and cannot drop
below the optimum `T`. The new vector is lexicographically smaller, a
contradiction.

Suppose the selected continuation omits its oldest unfinished job `h` in
some cycle. This job is ready because every true predecessor has smaller
index and is already complete. By non-delay, the cycle issues `W` other
jobs. Capacity `B=W+1` implies that the window contains exactly these
`W` jobs and `h`, all uncompleted and ready. Write the issued set as `A`.
Because `h` remains incomplete, no instruction retires after that cycle;
no new instruction can be admitted. In the next cycle the only unfinished
window job is `h`, so non-delay issues exactly `{h}`.

Choose any `x∈A`. Replace the first action by `(A\{x})∪{h}`, and the
second action by `{x}`. Every job in the new first action was already
ready. Job `x` is still ready in the second cycle; after the new first
action it is the oldest unfinished window job. The two cycles obey issue
capacity, and after them the completed set is exactly the same as in the
original continuation. Retiring/refilling therefore produces the same
state, so all later cycles can be copied without change. The resulting
schedule has makespan `T`, but its first changed program-index coordinate
is `h`, which issues one cycle earlier; `x>h` issues one cycle later.
This contradicts lexicographic minimality.

The swapped second cycle may leave additional newly visible jobs idle.
That is harmless: lexicographic minimality was over **all** optimal
continuations, not just non-delay ones. This distinction avoids an
incorrect iterative-normalization argument. ∎

The oldest job is always ready only because true edges point forward and
the state is interpreted after maximal in-order retirement. Finite
retirement bandwidth, side effects, and multi-cycle operations would
require separate arguments.

## 2. A scalar exact recurrence for `B=3,W=2`

Let `F_i` be the optimal remaining cycle count from the state in which
exactly jobs `1,...,i−1` have completed. Set `F_i=0` for `i>N`. For a
valid current index `i`, write `a=i`, `b=i+1`, `c=i+2`, `d=i+3`, omitting
letters whose indices exceed `N`.

Define `b_ready` to mean that `b` exists and `(a,b)∉E`. Define `c_ready`
to mean that `c` exists and neither `(a,c)` nor `(b,c)` lies in `E`.
When `c_ready` is true, define

`Q_i=2+F_(i+4)` if `d` exists and `(b,d)∉E`,

and `Q_i=2+F_(i+3)` otherwise.

**Theorem 2.** The exact recurrence is

| Ready younger jobs | `F_i` |
| --- | --- |
| neither `b` nor `c` | `1+F_(i+1)` |
| only `b` | `1+F_(i+2)` |
| only `c` | `Q_i` |
| both | `min(1+F_(i+2),Q_i)` |

Thus the exact offline optimum for `B=3,W=2` can be computed in
`O(N+|E|)` time, with a scalar backward dynamic program. Edges whose
index gap is at least three are already artificial ROB edges; only
true edges of gaps one and two affect the recurrence.

**Proof.** By Theorem 1, choose an optimal non-delay continuation issuing
oldest job `a`. If neither younger job is ready, issue `a` alone and
return to the clear-prefix state `i+1`. If only `b` is ready, issue
`a,b` and return to state `i+2`. These give the first two lines.

If `a,c` issue together, only `a` retires: `b` is still incomplete,
while `c` remains completed in the ROB. The next window is `b,c,d`,
with `d` omitted at the program boundary. Job `b` is now ready. If `d`
exists, its only possible uncompleted true predecessor is `b`: all
earlier jobs except `b` have completed, and it has no later predecessors.
Its artificial predecessors have indices at most `a` and are complete.
Therefore `d` is ready exactly when `(b,d)∉E`. Non-delay executes
`b,d` in that case and returns to clear-prefix state `i+4`; otherwise
it executes `b` alone and returns to state `i+3`. This is `Q_i`.
When both younger jobs are ready, Theorem 1 leaves exactly the two
first actions `a,b` and `a,c`, so take their minimum. All four cases
return to a clear-prefix state after at most two cycles and obey the
stated boundary conventions. Backward induction proves the recurrence. ∎

This is a simplified constant-window exact recurrence, not an improvement
to the complexity of arbitrary-width precedence scheduling. In particular,
the `O(poly(B)N3^B)` baseline already becomes linear in `N` at fixed `B`.

## 3. Randomized question under investigation

At `B=3,W=2`, the known global randomized interval in this project is
`[5/4,3/2]`. The lower endpoint comes from the four-job indistinguishability
pair; the upper endpoint comes from classical non-delay list scheduling.
Neither endpoint is assumed to be the exact randomized value.

A specific candidate policy issues the oldest job, and, whenever all
three current entries are ready, chooses each of the two younger jobs
with probability one half. In other states it issues all ready jobs.
Its expected remaining time from a clear-prefix state satisfies the
same recurrence as Theorem 2, with the `min` in the final line replaced
by the arithmetic mean. The `a,c` branch has a forced second action,
so this recurrence does not hide another randomized choice.

The next experiment will compare this exact rational expected-time
recurrence with the unrestricted exact ROB solver and search for a
program whose expected ratio exceeds `5/4`. Finding such a program
would refute the candidate policy's bound, not the existence of some
other `5/4`-competitive randomized policy.
