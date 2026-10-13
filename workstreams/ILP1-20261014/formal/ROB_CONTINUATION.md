# Completion dominance for finite actual ROB continuations

Status: **LEAN_VERIFIED** for finite continuations made from the existing
`ROBStep` relation. This closes the whole-continuation replay gap left by
`ROBReady.lean`; it does not prove non-delay optimum existence or the
forced-segment DP. The dominance principle is a foundation, not a claimed
original theorem. Historical priority of later algorithmic consequences is
outside this module.

Source: `ROBContinuation.lean`. Lean 4.34.1, bundled Std only. Existing
model, work-count and readiness files remain unchanged.

## Definitions use the actual transition relation

`Continuation dep B W s k final` is an inductive finite chain of exactly k
instances of the existing `ROBStep dep B W`. Its empty constructor has
identical start and end states; its nonempty constructor adds one actual
step. Each step retains the original width, eligibility, completion union,
contiguous retirement and eager admission conditions.

`afterAction B s A` constructs a successor with completed predicate
`s.completed OR A`, its exact first incomplete index, and eager admission.
`afterAction_step` proves that actual batch width and `CanIssue` eligibility
produce an actual ROBStep to this successor. The retirement prefix's
existence is proved for an arbitrary finite completion predicate, using the
already verified finite retirement-prefix construction.

`step_coherent` proves that every such actual step preserves the coherent
state invariant. No readiness-persistence conclusion, dominance conclusion,
or remaining-time inequality is assumed as part of that invariant.

## Closed simulation theorem

Write `Includes s s'` for completion inclusion. Given an actual step from
s, coherent states s,s', and `Includes s s'`, the simulated action is

    residualAction(s',A) = {i in A : i is not already complete in s'}.

`step_dominance` proves actual width and eligibility of that action,
constructs its successor, proves the successor coherent, and proves it
contains the original successor's completed set. Width cannot increase;
eligibility uses the previously verified admission/retirement/predecessor
readiness persistence theorem.

`continuation_dominance` inducts over the actual finite chain. It returns
a genuine chain of the **same** length from s', with a coherent final state
whose completed set contains the original final set. Empty actions and
terminal idle padding are allowed by the original processor semantics,
so matching the exact old length establishes a no-greater-time guarantee.

`FinishesFrom dep B W s k` means that such a finite chain ends with every
job retired. `finishesFrom_dominance` proves

    coherent(s), coherent(s'), Includes(s,s'), FinishesFrom(s,k)
      => FinishesFrom(s',k).

This covers every finite job count, including zero, and does not require
forward dependencies or positive resources as additional hypotheses once
the original finite continuation exists.

## Connection to existing actual traces

`trace_segment` extracts a finite continuation from cycles c through c+k
of every actual `ROBTrace`. This theorem requires no axioms.

`trace_finishing_segment_dominance` quantifies over two actual traces with
the same program/resources, two possibly different cycle boundaries, and
completion inclusion there. If the first trace finishes after k additional
cycles, the second state admits a finite actual ROBStep continuation that
finishes after the same k cycles. It need not follow the second trace's
original future choices.

The returned object is explicitly the finite transition chain. This module
does not reconstruct a new infinite time-assignment-indexed `ROBTrace` by
splicing that chain into its past; that representation conversion remains
a separate potential bridge. No illegal transition is hidden behind it.

`OptimalFrom` minimizes finite continuation length. The theorem
`optimalFrom_dominance` says that **when both state optima exist**, a
completion superset cannot have a larger optimal value. This theorem does
not supply existence of those optima or existence of a non-delay optimum.

## Audit and next gap

Twelve primary statements have actual transitive axiom audits; reports
contain only standard `propext`, `Classical.choice`, `Quot.sound`, with
`trace_segment` axiom-free. No `sorry`, `admit`, additional axiom, or trusted
native proof shortcut appears.

```sh
python workstreams/ILP1-20261014/formal/verify_continuation.py \
  --lean /absolute/path/to/lean-4.34.1/bin/lean
```

The runner rebuilds every exact local import in a fresh temporary directory.
Use the documented `--proc-self-compat` flag in the current sandbox. Actual
logs, hashes, version and durations are saved in
`subagents/lean/evidence/rob-continuation/`.

The next proof needs a finite action-extension theorem: every width-legal
ready subset can be enlarged to a NonDelay action. Replay dominance should
then support induction constructing a non-delay optimal continuation.
Neither this action-extension theorem nor the resulting macro recurrence
is assumed or claimed here.
