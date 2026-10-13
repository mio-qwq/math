# Exact optimization with a window one slot wider than issue width

Status: **WRITTEN_PROOF**; independent review and implementation checks are
tracked separately below. Historical novelty is unconfirmed. No Lean
verification is asserted. This note uses the eager unit-latency ROB model
and zero-based job indices. It concerns arbitrary finite forward DAGs and
arbitrary makespans, without a perfect-saturation assumption.

## 1. Non-delay optimality and the source of branching

Let `D` be a reachable completed set, including retired jobs, and let
`r(D)` be its first uncompleted index, or `N` at completion. The eager
window is `[r(D),min(N,r(D)+B))`. Write `R(D)` for its uncompleted jobs
whose true predecessors all belong to `D`. Every nonterminal state has
`r(D) in R(D)`, since all predecessors have smaller indices.

A non-delay action has size `min(W,|R(D)|)`. This is a restriction on
the number issued, not a fixed priority order.

**Lemma 1 (completion dominance).** If reachable completed sets satisfy
`D subset D'`, every continuation from `D` can be simulated from `D'`
in no more cycles.

**Proof.** Replay each action after deleting jobs already completed in
the simulating state. Its completed set continues to contain the
original completed set. A retained job `j` admitted from the original
state remains admitted: retirement has advanced from `r` to `r'>=r`,
the fact that `j` is not complete gives `j>=r'`, and its original upper
admission bound gives `j<r+B<=r'+B`. True predecessors remain complete.
Deleting issued jobs cannot violate width. Induction simulates the
continuation, possibly completing earlier. ∎

**Corollary 2 (non-delay optimum).** Every reachable finite state has an optimal
non-delay continuation.

**Proof.** A legal sequential continuation exists. Among finitely many
issue-time assignments up to that sequential horizon, choose an optimum.
At any state, extend its first action by ready jobs until its size is
`min(W,|R|)`. The enlarged action leads to a completed superset, so Lemma 1
gives a continuation of no greater cost. The optimum cannot decrease
below itself. Repeat by induction on the number of unfinished jobs;
each enlarged action is nonempty in a nonterminal state. ∎

Let `h(D)=|D|-r(D)` count completed but unretired jobs. These entries
remain in the window. Its number of unfinished entries is
`min(B,N-r(D))-h(D)`, so

`|R(D)| <= B-h(D)`.

**Lemma 3.** For `B=W+1`, every state with `h(D)>=1` has a unique
non-delay action: issue all ready jobs. A state has more than one
non-delay action only if `D=[0,r(D))`, the window has all `B` entries,
and all of them are ready.

**Proof.** If `h>=1`, the displayed bound is at most `W`. If `h=0`,
the completed set is exactly the retired prefix. More than `W` ready
jobs then means exactly `B=W+1`, since no window has more entries.
There are exactly `B` non-delay choices, each omitting one ready job.
No oldest-job normalization is needed for this statement. ∎

## 2. A scalar macro graph for every finite program

Call `D=[0,i)` a clear-prefix state and let `F_i` be its optimal
remaining makespan. Set `F_N=0`. All clear-prefix states are reachable
by executing the prefix sequentially, regardless of whether an optimal
execution of the whole program visits them.

For each `i<N`, list the non-delay first actions from that state. There
is one action if at most `W` jobs are ready, and `B` actions otherwise.
For each first action `A`, execute it and then, while the completed set
is not a prefix, repeatedly execute all ready jobs. Lemma 3 makes this
continuation unique. Stop at the first subsequent clear-prefix state.
Record its index `j(i,A)` and the number `ell(i,A)` of executed cycles.

This construction is well defined. Every forced cycle has a ready oldest
job and is nonempty; the first action is nonempty too. Each cycle adds
at least one completed job, so a clear prefix or the terminal state is
reached in at most `N-i` cycles. The final index satisfies `j(i,A)>i`.
An omitted oldest job in the first action causes no difficulty: the
next state is nonclear and the next forced action contains that job.

**Theorem 4 (exact prefix recurrence).** For `B=W+1`,

`F_i = min_A (ell(i,A)+F_(j(i,A)))`.

The recurrence computes the exact offline optimum and an optimal
schedule for every finite forward DAG.

**Proof.** Corollary 2 gives a non-delay optimal continuation. Its first
action is one of the listed actions. Until the first later clear state,
all its actions are uniquely forced by Lemma 3, so its prefix equals
the corresponding macro. Its remaining cost is at least `F_j`. This
proves the lower inequality. Conversely, each macro is an actual legal
ROB execution; following it by an optimum from its endpoint realizes
`ell+F_j`. Strictly increasing endpoints permit backward induction
from `F_N=0`. ∎

There are `N+1` scalar nodes and at most `N min(B,N)` macro arcs. One
need not enumerate the exponentially many completed masks in a general
window. In particular, the recurrence's polynomial guarantee treats
`W` as an input, not as a fixed constant.

## 3. Implementation and cost

`forced_segment_dp.py` implements Theorem 4 from a forward edge list.
Each macro is simulated using uncompleted-predecessor counters,
completion flags, and admission and retirement pointers. Initialize
the counters from the clear prefix in `O(N+|E|)` time. During the macro,
each job is admitted and completed at most once, and each outgoing true
edge is processed at most once. Ready queues are taken in full during
forced cycles; sorting is unnecessary. Thus a macro costs
`O(N+|E|)` using ordinary indexed-array operations.

The resulting conservative bound is

`O(N min(B,N) (N+|E|))` time and `O(N+|E|)` working space,

apart from the returned `O(N)`-size schedule. The dynamic program saves
only the winning first omission (or the unique action), endpoint and
cost at each prefix; it does not retain every long macro trace. It
replays only winning macros to return the schedule. Reinitialization
on those replays stays within the same overall bound.

The empty program returns zero. Width one is permitted: the same
recurrence is valid at `B=2` and returns `N`. If `B>N`, truncation at
the end of the program applies, and there cannot be a full `B`-entry
branch. Arbitrarily large binary-encoded `W` therefore does not cause
an iteration over non-existent window positions.

This does not replace the linear perfect-saturation criterion in
`PERFECT_SATURATION.md`: that theorem gives a sharper linear decision
algorithm and local positive/negative certificates for `N=kW,T=k`.

## 4. General excess-window parameter: an XP extension

Normalize `W` to `min(W,B)` first, and let `c=B-W>=0`. For a nonempty
program one can also truncate `B` and `W` at `N`. When `c=0`, every
non-delay action is unique, so deterministic all-ready simulation is
optimal. Suppose henceforth `c>=1`.

A branching state has `|R(D)|>W`, which forces `h(D)<c`. Apart from its
retired prefix `r`, it is described by `h` completed holes among at
most `B-1` later window positions. Thus there are at most

`N sum_(h=0)^(c-1) binomial(B-1,h)`

branching states. From such a state enumerate all full-width ready
subsets. Compress every resulting run of unique non-delay actions
until the next branching state or completion. The completion set
strictly increases on every macro, so this is an acyclic exact state
graph. Include the initial forced run separately when it does not
begin at a branching state.

For a state with `h` holes there are at most
`binomial(B-h,W)=binomial(B-h,c-h)` possible actions: the function
`binomial(R,W)` is nondecreasing for `R>=W`, and `R<=B-h`.
Consequently the total number of arcs is at most

`N sum_(h=0)^(c-1) binomial(B-1,h) binomial(B-h,c-h)`

`<= N (2^c-1) binomial(B,c)`.

The last inequality follows term by term from
`binomial(B-1,h)<=binomial(B,h)` and the identity

`binomial(B,h) binomial(B-h,c-h)
 = binomial(B,c) binomial(c,h)`.

Summing `binomial(c,h)` for `0<=h<c` gives `2^c-1` exactly. This is
not an asymptotic cancellation that assumes fixed `W`.

A direct macro simulator can initialize counters for an arbitrary
completed set and then process each subsequent job and edge at most
once. Exactness follows from Corollary 2 and uniqueness of each
compressed segment, just as in Theorem 4. These bounds yield an
`N^(O(c))`-time exact algorithm: an **XP** result in `c`, not a claimed
fixed-parameter tractable algorithm in `c` alone. The bounded-total-idle
corridor instead gives a separate FPT result in `c+S`; neither statement
implies the other parameter dependence.

The current implementation covers the `c=1` prefix recurrence only.
The general XP extension is a written algorithm and counting proof.

## Evidence and remaining limits

The file `FORCED_SEGMENT_CHECK.json` records the actual implementation
check range, runtime, Python version and source hashes. The checker
uses the full completed-state optimum from `sanity_check.py`, which
enumerates all nonempty ready subsets, and independently replays every
returned schedule. Finite agreement is not the proof of Theorem 4.

The saved run covers all 1,100 forward DAGs through five jobs at widths
`1,...,N+2` (7,605 resource cases); 60 seeded binary-input random programs
up to 12 jobs also compare every suffix value. It checks a genuine
four-cycle forced macro, empty and one-job inputs, widths one and larger
than the program, independent/serial 200-job programs, duplicate edges,
and five invalid-input rejections. Every case passes; the recorded
Python 3.12.14 runtime is 0.895748 seconds.

The verification agent independently accepted the branching argument
and suggested the predecessor-counter implementation bound before
this implementation was written. Its saved independent report, once
available, determines the formal scope of INDEPENDENTLY_REVIEWED.
Neither historical novelty nor a general Lean bridge is asserted.
