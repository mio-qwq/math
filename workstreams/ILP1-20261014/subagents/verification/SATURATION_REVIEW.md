# Independent review: unbounded resource-saturation drops

Date: 14 October 2026, Singapore. Reviewer: independent verification subagent C.
All indices below are zero-based. The conclusions are accepted as written
theorems for the eager unit-latency ROB model. Their universal statements are
not Lean-verified here, and historical novelty remains unconfirmed.

## Fixed issue widths: window demand drops from 2K to 3

For each `K>=2`, let `N=2K`. Job `0` is isolated. The other jobs consist of
`K-1` consecutive pair layers

`{1,2}, {3,4}, ..., {2K-3,2K-2}`

followed by singleton layer `{2K-1}`. Add every directed edge from one layer
to the next. Each original indegree and outdegree is at most two.

**Accepted conclusion:**

`B_sat(P_K,2)=2K`, and `B_sat(P_K,3)=3`.

The additive drop from one additional issue slot is `2K-3`, while the ratio
of required windows is `2K/3`. Both are unbounded as `K` grows, even though
the compared issue widths stay fixed at two and three.

**Independent proof.** The original dependency graph has height `K`. Every
nonisolated job lies on a path with exactly `K` vertices. Hence any schedule
of length `K` must issue every job in layer `ell` at cycle `ell-1`; along a
strictly increasing sequence of `K` natural issue times bounded by `K-1`,
there is no slack.

With unlimited window and width two, issue each pair layer in its forced
cycle, then issue the isolated job together with the final singleton. This
is a `K`-cycle schedule meeting both height and total-work lower bounds. In
every `K`-cycle width-two schedule the first `K-1` cycles are full, so isolated
job `0` necessarily issues in the final cycle alongside job `N-1`.

For any `B<N`, the ROB precedence condition includes the edge `0 -> N-1`,
because `(N-1)-0>=B`. It requires strict inequality of their issue times,
contradicting that forced common final cycle. Thus only `B=N` can attain the
unrestricted-window optimum at width two.

At width three, window three suffices: issue `{0,1,2}` first, each successive
pair layer next, and the singleton last. Each pair follows a completed initial
prefix and is admitted; the schedule takes `K` cycles and meets the height
lower bound. At `B<=2`, job `2` is not initially admitted, although its length-
`K` critical path requires it in cycle zero in every `K`-cycle schedule.
Therefore `B<3` cannot attain the optimum. This proves both threshold values.

**Finite checks.** All `2<=K<=10`, every window `1..2K`, and both widths two
and three were tested by the independent time-assignment solver: 216 horizon-
`K` feasibility decisions. Explicit attaining schedules were also replayed
directly, and exact optimum calls returned `K` at the asserted sufficient
resources. Every test agrees with the theorem.

## Depth-two family: exact issue-width saturation formula

Let `m>=2` and `1<=r<=floor(m/2)`. The first `r` jobs are isolated roots. The
next `m` jobs form the required-root set `A={r,...,r+m-1}`. The remaining
`m-r` jobs are sinks. Partition `A` into `r` pairs and `m-2r` singletons,
assigning one sink to each group with those roots as its parents. Thus
`N=2m`, original indegree is at most two, original outdegree is at most one,
and the true dependency height is two.

For `1<=B<=2m`, the independent exact characterization is:

`T*(P,B,W)<=2` if and only if
`B>=m+r` and `W>=m+min(r,2m-B)`.

**Independent proof.** No sink can execute initially, because its parents
are initially incomplete. A two-cycle completion therefore requires every
root in `A` in the first cycle. The last such root has index `m+r-1`, so
initial admission requires `B>=m+r`. Admission of the last job in the
second cycle also requires the prefix of length `2m-B` completed initially.
The union of this prefix and `A` has exactly `m+min(r,2m-B)` members.
They all must issue in the first cycle, giving the width requirement.

Conversely, under those two requirements issue exactly that union first.
Its members are initially admitted. The needed prefix retires, admitting
the entire program for the second cycle, and every sink operand is ready.
At most `m` jobs remain, no more than the permitted width. This gives the
required two-cycle schedule. A one-cycle schedule is excluded by any true
edge, so every attained value above is exactly two.

In particular, for `m+r<=B<=2m`, unrestricted issue attains two cycles, and

`W_sat(P,B)=m+min(r,2m-B)`.

As the window increases from `2m-r` to `2m`, the saturated width decreases
from `m+r` to `m`, an additive drop of `r`, which can grow arbitrarily large.

For `W>=m`, the unrestricted-window optimum is two, giving

`B_sat(P,m+s)=2m-s` for `0<=s<r`,

and `B_sat(P,W)=m+r` for `W>=m+r`.

The case `r=1` already gives `B_sat(P,m)=2m` and `B_sat(P,m+1)=m+1`.
The fixed-width layered family above is stronger for demonstrating an
unbounded window drop from one added issue slot; this depth-two family
additionally gives the exact issue-width saturation curve.

**Finite checks.** All `2<=m<=10` and every allowed `r` give 25 programs.
The independent solver checked all `1<=B,W<=2m`: 5,720 two-cycle feasibility
decisions. Both threshold formulas and additional exact optimum calls at
the predicted boundaries passed. The source and exact deterministic output
are `saturation_drop_audit.py` and `saturation_drop_results.json`.

## Scope

These threshold decreases do not contradict monotonicity of `T*` in either
resource. They ask how much of one resource is still necessary after the other
changes; this requirement may fall even when the target duration stays the
same, as it does in the layered family. Increasing resources never worsens
the optimum duration of a fixed program. The results
concern offline schedules under the specified idealized ROB rules and make no
claim about real processor speed, register pressure outside this model, or
whether the constructions are historically new.
