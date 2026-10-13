# Finite actual execution to the global schedule model

Status: LEAN_VERIFIED, 16 audited declarations. Independent review is pending
for this new increment at the time of this record. This is a foundational
representation and normalization result, not an originality claim.

`ROBRepresentation.lean` imports the already compiled Std-only chain through
`ROBNonDelay.lean`. The fixed compiler is Lean 4.34.1, commit
`5045d0056413266e57c625dcd7c365b10e377c52`; Mathlib is not used.

## Exact statements

`Profile dep b w condition s actions final` is a finite list of **actual
ROBStep transitions** from `s` to `final`. Each step carries the additional
predicate `condition` on its actual start state and its actual action.
`Fires actions c i` reads action `c`; all cycles after the list are empty.

For every such profile, coherent start state, and `final.retired = n`,
`profile_realization` constructs a residual time assignment `t` satisfying:

* `Fires actions c i ↔ ¬s.completed i ∧ t i = c`, for every job and every
  natural cycle, including cycles beyond the profile length.
* Every initially unfinished job has `t i < actions.length`.
* Dependencies between initially unfinished jobs have strictly increasing
  times; so do the window edges `i.val + b ≤ j.val`.
* There is a lane assignment below `w` for initially unfinished jobs,
  injective among equal-time jobs.

Thus every initially unfinished job is issued exactly once. Times of
initially completed jobs are immaterial and deliberately have no width or
horizon obligations. `residual_unique_issue` states the uniqueness explicitly.

At `initialState n b`, no job is complete, retired is zero, and admitted is
`min n b`. `initial_profile_realization` removes the residual restriction
and proves the original `Legal dep b w t` together with the **same action
list's** exact issue-time correspondence. This uses the previously proved
window-edge/canonical-ROB equivalence.

For arbitrary `n`, `b`, `w`, `k`, and dependency relation, including zero
resources or the empty program, the following equivalences hold without
extra forwardness or positivity assumptions:

```
Feasible dep b w k ↔ FinishesFrom dep b w (initialState n b) k
Optimal dep b w k  ↔ OptimalFrom dep b w (initialState n b) k
```

The forward direction uses the existing `legalTrace`, `trace_segment`, and
`trace_finished_iff`; the reverse direction extracts actual issue times and
lanes from a finite completing chain. These assumptions are equivalences,
not existence claims for zero resources.

`global_optimal_nonDelay` states that every existing global optimum `k` has
a completing actual non-delay profile of length `k`, with a legal time
assignment that issues exactly its labelled batches. It uses the previously
proved actual-continuation non-delay normalization.

`global_optimal_nonDelay_exists` adds `Forward dep`, `0 < b`, `0 < w` and
proves existence of such a global optimum with `k ≤ n`. This includes
`n = 0`, where the result forces `k = 0` and the action list to be empty.

## Proof mechanism and audit concerns

The central induction extracts a residual time assignment from the tail.
Jobs issued in the head get time zero and the head's actual lane; every
remaining job gets its tail time plus one and its tail lane. A job already
completed at the start is never issued because actual eligibility prohibits
reissue. The step's completion union establishes exactly which jobs remain.

A first-cycle issued target cannot have an initially unfinished dependency:
its actual ready predicate requires that predecessor already complete.
Likewise a first-cycle target cannot be behind an unfinished window-edge
predecessor: coherence places that predecessor at or after retirement,
while the target is strictly below retirement plus `b`. Equal-time lane
collisions reduce to the head or tail injection; a head/tail collision is
impossible because tail times were shifted by one.

The non-delay endpoint retains `NonDelay dep w` in `Profile` itself, rather
than merely presenting an unrelated non-delay continuation with the same
duration. Exact issue correspondence therefore refers to the same actual
execution throughout the theorem.

No step assumes the desired feasibility equivalence, global optimality,
or final non-delay property. No `sorry`, `admit`, or custom axiom is added.
The audit permits only the standard Lean logical axioms `propext`,
`Classical.choice`, and `Quot.sound`.

## Reproduction and scope

Run from this directory or the worktree root:

```
python workstreams/ILP1-20261014/formal/verify_representation.py \
  --lean /path/to/lean-4.34.1-linux/bin/lean --proc-self-compat
```

The compatibility switch is only needed in this sandbox's documented
`/proc/<pid>/exe` restriction. The runner builds every import into a new
temporary directory, records source SHA256 hashes, real compiler output,
audit sets, times, and the compiler version. Evidence is in
`subagents/lean/evidence/rob-representation/`.

This increment closes the finite-continuation/time-assignment/global-optimum
gap. It does not prove that every non-delay strategy is optimal. It does not
formalize first-clear-prefix macro decomposition, the prefix dynamic
program, randomized policies, or a hardware implementation. It proves a
finite non-delay actual profile with an exactly matching global time
assignment; a separate uniqueness theorem identifying every intermediate
profile state with a particular infinite canonical trace is unnecessary
for this statement and is not asserted here.
