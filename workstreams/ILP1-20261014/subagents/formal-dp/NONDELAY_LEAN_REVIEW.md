# Independent review: optimal non-delay finite ROB continuations

Reviewer: formal-dp, not the proof author. Review date: 2026-10-13 UTC.
Pinned author commit: `daa73300afcbeb724be39077f42e97c746464895`.
Reviewed source: `formal/ROBNonDelay.lean`, its exact imports, runner, and
`formal/ROB_NONDELAY.md`.

**Verdict:** accept action extension, exact-horizon non-delay normalization,
bounded finishing-continuation existence, and existence of an optimal non-delay
finite continuation in the stated actual `ROBStep` model. Independent fresh
compilation and semantic review found no blocking issue or circular assumption.

This is a substantive closure of the finite-continuation gap identified in
`READY_CONTINUATION_LEAN_REVIEW.md`, not just a renamed optimum definition.
The remaining complete time-assignment/`ROBTrace` representation bridge and
prefix-DP correctness are outside this module. No claim that arbitrary
non-delay policies are optimal follows from its existence theorem.

## Reproduction and axiom audit

After an actual `git fetch origin`, the supplied runner was inspected and
executed afresh with Lean 4.34.1, compiler commit
`5045d0056413266e57c625dcd7c365b10e377c52`, bundled Std, and no Mathlib.
It rebuilt Model, Operational, WorkBounds, Ready, Continuation, and NonDelay
in a new temporary directory, including a fresh documented executable-path
compatibility shim. No author's `.olean` file was reused.

The six modules returned zero and produced, respectively, 22, 11, 16, 25, 12,
and 11 primary audits. The 11 NonDelay declarations are new; the 86 import
audits are repeated verification, not new results. Every transitive axiom
report uses only standard `propext`, `Classical.choice`, and `Quot.sound`.
The source contains no `sorry`, proof `admit`, additional axiom, unsafe proof,
or `native_decide` shortcut.

Full compilation logs, UTC timestamps, actual durations, version, hashes and
audited declarations are saved in `evidence/nondelay-independent/`.
`evidence/nondelay-provenance.json` verifies every reviewed source, import,
runner, explanatory document and shim is byte-identical to the pinned commit.
It records the fetched research-branch SHA and reviewer precommit state.
No files outside this reviewer's owned directory were changed.

```sh
python workstreams/ILP1-20261014/formal/verify_nondelay.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /absolute/path/to/nondelay-independent
```

## 1. Action extension has the required actual-model premises

`count_le_of_batchWidth` injects the duplicate-free selected action list into
the actual lane range. Thus the converse direction to the prior count-to-lanes
lemma is proved, rather than replacing width feasibility with an assumed count.

`nonDelay_extension` starts with an arbitrary actual-ready subset A and an actual
`BatchWidth A W` witness. It searches classically among predicates containing A,
contained in the actual ready predicate, and having count at most W. The original
A is an explicit feasible witness. Minimizing `W-count` uses the previously
proved least-natural-number lemma, not an optimal-schedule axiom.

If the selected extension has size different from `min(W,readyCount)`, its
proved upper bounds imply it is strictly below both bounds. A ready job missing
from it exists by finite predicate equality/count reasoning. Inserting that job
increases the count by exactly one, preserves containment and readiness, stays
within width, and strictly decreases unused slots. This contradicts the chosen
minimum. The natural subtraction is justified by the explicit count<=W premises
before and after insertion.

The conclusion is exactly a containing non-delay action. There is no forwardness,
positive-resource, coherence, or optimum premise hidden in this lemma. A width of
zero forces an empty action; an empty ready set is handled without a spurious
missing-job witness. The proof gives classical existence, not an executable
selection algorithm or online-optimal choice rule.

## 2. Normalization genuinely preserves an arbitrary finite horizon

`NonDelayContinuation` adds a non-delay proof to each constructor step of the
existing `ROBStep` relation. Its forgetful theorem produces the previously
reviewed actual `Continuation`. It does not replace eligibility, next-state
completion, retirement, or admission with abstract assumptions.

`nonDelay_normalization k` quantifies over every coherent initial state with a
finishing finite actual continuation of exactly k cycles. At k=0, the empty
constructor identifies the endpoint with the start and returns that actual state.
For k+1, it extends the original first action, constructs the actual canonical
successor, proves its completion set contains the old successor, and invokes the
separately verified finite-continuation dominance theorem for the remaining k
cycles. The induction normalizes this returned shorter chain, so it applies even
though dominance may have removed now-redundant jobs from subsequent actions.

The proof checks both successors coherent. Every newly issued job is ready in
the pre-step state, so there is no same-cycle dependency bypass. Terminal empty
actions are non-delay because completed states have no unfinished ready jobs;
keeping an exact horizon after an earlier finish is therefore legal. No positive
B,W or forwardness assumption is needed once a finishing continuation is given.

The returned endpoint need not be the same intensional state structure as the
original endpoint, but all N jobs are retired and its horizon is unchanged. This
is the required replacement property. It does not claim that an arbitrarily
chosen first non-delay action preserves the horizon: the new action specifically
contains the original first action of a supplied finishing witness.

## 3. Completion and optimum existence are not assumed

`nonDelay_finishes_bounded` removes the finishing-witness premise under
`Forward dep`, B>0, W>0, and `Coherent B s`. Its strong induction measure is the
genuine count `N-completedCountOfState(s)`, not an assumed progress function.

If `retired=N`, the zero-step actual chain is returned. Otherwise exact-prefix
coherence gives `retired<N`. Action extension applied to the empty legal batch
supplies a non-delay batch. The earlier oldest-ready/progress theorem, which
does require forward edges and positive resources, then proves that the actual
constructed successor completes at least one new job. Its count is at most N
by the finite-list count theorem. These two inequalities make natural subtraction
strictly decrease and prove the final length is at most the original remaining
count. The induction does not silently assume reachable-state or finishing-chain
existence.

This proof intentionally works for every coherent state, a potentially larger
class than reachable states. It does not assert that every such state is reachable
or that an arbitrary initial completion assignment represents a valid execution
history. In reachable states the earlier `trace_coherent` theorem supplies the
premise, so that generality does not weaken the actual-model endpoint.

`optimal_nonDelay_of_finishes` takes the least natural horizon among actual
finite finishing continuations, with its input continuation as the nonemptiness
witness, and normalizes the selected witness. `optimal_nonDelay_exists` first
constructs the bounded finishing chain above and then invokes this minimization.
Consequently its exact conclusion is justified:

    exists k, final:
      k <= N-completedCountOfState(s),
      OptimalFrom(dep,B,W,s,k),
      NonDelayContinuation(dep,B,W,s,k,final),
      final.retired = N.

`trace_state_optimal_nonDelay` applies this to every boundary of an actual trace
under the same forward/positive-resource assumptions. A separate segment endpoint
uses an already given finishing segment and needs no additional positive-resource
or forwardness premise. Neither endpoint treats the original trace's future
choices as the newly selected optimum.

## 4. Edge cases and exact coverage limit

N=0 and already-finished coherent states have a zero-cycle witness and zero
remaining count. Empty chains and exact-horizon terminal padding are covered.
W>B is allowed; actual ready jobs are still constrained by the ROB, while the
non-delay definition uses the minimum with W. B=0 or W=0 are allowed in the
conditional extension/normalization lemmas; they are explicitly excluded in the
unconditional nonterminal completion-existence theorem. No division or implicit
positive-size assumption occurs in the new proof.

`OptimalFrom` still minimizes the finite chain of actual `ROBStep` transitions
from a given state. This module does not construct a new infinite
time-assignment-indexed `ROBTrace` by attaching the chosen finite chain to a past,
nor prove an iff with the original `Legal`/`Feasible`/`Optimal` predicates. In
particular its optimum endpoint must not be renamed as that unproved bridge.

Also unproved here: complete forced-prefix macro extraction, the scalar suffix
DP recurrence, bounded branching enumeration, its complexity, or Python solver
correctness. The existential choice may depend on the entire dependency graph;
no online-information theorem or finite-hardware implementation is asserted.
The explanatory document accurately discloses these gaps.

Accepted status: **LEAN_VERIFIED** and **INDEPENDENTLY_REVIEWED** for the stated
finite operational results. Novelty is not established; classical normalization
and dominance foundations are not being represented as new discoveries.
