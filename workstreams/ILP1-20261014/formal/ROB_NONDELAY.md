# Existence of optimal non-delay finite ROB continuations

Status: **LEAN_VERIFIED** in the finite actual transition model. These are
classical dominance/normalization foundations, not claimed novel results.
The forced-segment prefix recurrence and its polynomial runtime remain
outside the formal coverage.

Source: `ROBNonDelay.lean`, using Lean 4.34.1 with bundled Std only and the
unchanged `ROBContinuation` / `ROBReady` / work/model sources.

## Action extension is proved

`count_le_of_batchWidth` maps the actual action jobs injectively to their
actual issue lanes, proving the cardinality bound from `BatchWidth`.
Together with the previously proved converse, cardinality and the lane
predicate are now connected in both directions.

`nonDelay_extension` quantifies over any state, dependency predicate,
width W, ready subset A and actual `BatchWidth A W`. It supplies A' with
A subset A', all jobs in A' actually `CanIssue`, and

    |A'| = min(W,readyCount).

The proof minimizes unused slots among all eligible extensions of A.
If the chosen size were below both W and readyCount, a missing ready job
would exist. Inserting it increases the genuine finite cardinality by one,
contradicting minimality of unused slots. The non-delay size equality is
therefore a proved consequence, not an interface assumption.

The proof is classical finite existence, not an extracted deterministic
implementation or an efficient algorithm for selecting a preferred action.

## Exact-horizon normalization

`NonDelayContinuation dep B W s k final` is a finite chain of existing
`ROBStep` transitions carrying a `NonDelay` proof at each step.
`toContinuation` forgets these extra proofs and yields the existing actual
finite continuation object.

`nonDelay_normalization` says that every coherent state with a finishing
finite actual continuation of k cycles also has a non-delay actual
continuation finishing in exactly k cycles. Its induction:

1. Extends the original first action to a proved non-delay action.
2. Constructs its actual ROB successor.
3. Shows the new successor's completed set contains the old successor's.
4. Uses the separately verified whole-continuation dominance theorem to
   preserve the remaining horizon.
5. Normalizes that shorter remaining continuation inductively.

Empty non-delay cycles after completion provide legal padding if extension
finishes the program earlier. This theorem needs no positive-resource or
forwardness assumption beyond existence of the original finishing chain.

## Closed optimum-existence result

`nonDelay_finishes_bounded` removes the assumed finishing chain when the
dependency predicate is forward and B,W are positive. From **any coherent
state**, it constructs a non-delay continuation finishing in at most the
actual number of unfinished jobs, `N-completedCountOfState(s)`.

This proof uses strong induction on that actual finite count. In a
nonterminal state, the previously proved oldest-ready theorem makes a
non-delay action nonempty. The actual constructed ROBStep increases the
completed count by at least one. No termination or horizon bound is an
additional premise.

`optimal_nonDelay_exists` then minimizes the natural finite continuation
horizon and normalizes its witness. Its exact quantified conclusion is:

```lean
Forward dep → 0 < B → 0 < W → Coherent B s →
  ∃ k final,
    k ≤ N - completedCountOfState s ∧
    OptimalFrom dep B W s k ∧
    NonDelayContinuation dep B W s k final ∧
    final.retired = N
```

`trace_state_optimal_nonDelay` applies this to every cycle of any actual
ROBTrace under the forward/positive-resource assumptions. Empty programs
and already-completed states are included and have a zero-cycle witness.

## Representation and coverage boundary

The minimized object here is explicitly the finite chain of the original
ROBStep relation, from an arbitrary current state. It is not an abstract
Bellman system or an assumed valid-state relation. The initial state's
coherence is proved for actual traces by the earlier `trace_coherent`.

This module does **not** yet reconstruct an infinite time-assignment-indexed
ROBTrace by splicing a chosen finite continuation into an earlier trace.
It also does not prove a representation iff between these state optima
and the original `Optimal dep B W K` predicate. That conversion is a
separate representational theorem if needed for a direct original-predicate
endpoint.

Also not formalized: forced-macro first-prefix endpoint extraction; the
exact scalar F_i recurrence; enumeration of all first omissions; the
polynomial/XP complexity arguments; or `forced_segment_dp.py` correctness.
No online observation or probability claim is made.

## Reproduction and audit

Eleven primary statements have actually compiled transitive axiom audits.
Their only dependencies are standard `propext`, `Classical.choice`, and
`Quot.sound`; no `sorry`, `admit`, added axiom or trusted native proof
shortcut appears.

```sh
python workstreams/ILP1-20261014/formal/verify_nondelay.py \
  --lean /absolute/path/to/lean-4.34.1/bin/lean
```

The runner freshly builds all exact local imports and the new module.
The documented `--proc-self-compat` flag handles the current sandbox.
Actual version, hashes, timing, logs and axiom reports are in
`subagents/lean/evidence/rob-nondelay/`. Independent review is a separate gate.
