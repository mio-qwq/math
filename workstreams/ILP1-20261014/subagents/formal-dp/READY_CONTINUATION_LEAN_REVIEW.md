# Independent review: readiness and finite ROB continuation dominance

Reviewer: formal-dp, not the proof author. Review date: 2026-10-13 UTC.

Reviewed author commits:

* `4b7334a571f2ee24ee84297774a243affa7b3814` (`ROBReady.lean`).
* `0ddd4ba34ad7554ea32e487c18aea92bc28e9cf9`
  (`ROBContinuation.lean`, retaining the identical readiness source).

**Verdict:** accept the stated actual-state and finite-transition results.
Both modules passed independent fresh compilation and semantic review. No
blocking mathematical error, circular target assumption, or nonstandard axiom
was found. The 25 readiness endpoints and 12 continuation endpoints are 37 new
primary audits. Rebuilt import audits are not additional new results.

The accepted statements do **not** establish existence of an optimal non-delay
continuation, equivalence of finite continuation optima with the existing
time-assignment optimum, a complete replacement `ROBTrace`, or the forced-segment
DP. The author's two explanatory documents state these boundaries accurately.

## 1. Independent reproduction and pinned inputs

Both supplied runners were inspected and then executed independently, sequentially,
using Lean 4.34.1, compiler commit
`5045d0056413266e57c625dcd7c365b10e377c52`, and bundled Std without Mathlib.
Each run creates a new temporary directory and rebuilds every local import;
neither run reused the author's `.olean` files. The documented own-process
`proc_self_compat.c` shim was freshly compiled and preloaded. Its source hash
is recorded; this changes executable-path discovery, not the kernel or proofs.

| Independent run | Rebuilt primary audit counts | Compilation time |
| --- | --- | --- |
| `ready-independent` | Model 22, Operational 11, WorkBounds 16, Ready 25 | 2.682011 s |
| `continuation-independent` | Model 22, Operational 11, WorkBounds 16, Ready 25, Continuation 12 | 2.935891 s |

All return codes were zero. Transitive audits contain only `propext`,
`Classical.choice`, and `Quot.sound`; `trace_segment` is axiom-free. The checked
sources contain no `sorry`, proof `admit`, new axiom, `native_decide`, or unsafe
proof shortcut. The token `admit` in this code is the pre-existing eager-admission
field of `ROBStep`, not a proof command.

Evidence, including complete logs, individual source hashes, compiler version,
audit declarations and UTC timestamps:

* `evidence/ready-independent/receipt.json` and its four module logs.
* `evidence/continuation-independent/receipt.json` and its five module logs.
* `evidence/ready-continuation-provenance.json` pins both author commits and
  verifies that all reviewed sources, runners, documents, imports and compatibility
  source are byte-identical to those commits.

The author started an untracked `ROBNonDelay.lean` during this review. It is not an
import of either audited module and is outside this review. No foreign files were
modified. `git fetch origin` was actually completed before this checkpoint;
the fetched research-branch SHA is in the provenance receipt.

Reproduction from a checkout containing the author commits:

```sh
python workstreams/ILP1-20261014/formal/verify_ready.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /absolute/path/to/ready-independent
python workstreams/ILP1-20261014/formal/verify_continuation.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /absolute/path/to/continuation-independent
```

## 2. The invariant and counts are connected to actual ROB states

`Coherent B s` records an exact retired prefix, eager admission
`admitted = min(N,retired+B)`, and that every completed job has already been
admitted. It does not assume readiness persistence, a capacity count, a potential
inequality, or a scheduling-optimality conclusion.

`trace_coherent` derives this invariant for every boundary of every existing
`ROBTrace`. Its less immediate component, completed jobs lying below the current
admission frontier, uses the already established actual-trace/window-edge
equivalence: an allegedly completed job beyond `retired+B` would have to follow
the still-incomplete first unretired job. Thus the source does not silently
replace ROB occupancy by a queue containing only unexecuted instructions.

The predicate counts really enumerate `Fin N` using a duplicate-free filtered
`List.finRange`. The proof of `hole_count_identity` partitions completed jobs
below/at-or-above retirement and obtains

    holeCount(s) + retired(s) = completedCountOfState(s).

The natural subtraction formula is a consequence of this exact identity; it does
not lose an unproved nonnegativity condition. `ready_plus_holes_le` proves the two
sets disjoint and injects their union into offsets `0,...,B-1`. The lower index
bound is used before cancelling natural subtraction, and the upper bound follows
from actual eligibility or completed-admitted coherence, as appropriate.

`canIssue_mono` checks every original `CanIssue` conjunct. Increasing the completed
set increases the exact retired prefix and hence the eager admitted prefix; an
unfinished job cannot lie below the new retirement frontier; all its true
predecessors remain complete. Its `still unfinished` hypothesis is essential and
present. The actual-trace version permits different widths and different cycle
boundaries, but keeps the dependency predicate and B fixed and requires explicit
completed-set inclusion. It does not infer inclusion merely from elapsed time.

## 3. What the non-delay theorems say

`NonDelay dep W s A` says that A is an actually ready subset of cardinality
`min(W,readyCount)`. It assumes neither a priority rule nor optimality. The
lane-ranking construction proves that this finite count gives the model's real
`BatchWidth`; capacity is not weakened to an unrelated numerical surrogate.

The accepted implications are:

* B = W+c and at least c completed-but-unretired holes imply readyCount <= W.
* In that case a non-delay action is exactly the set of all ready jobs, so two
  non-delay actions agree pointwise.
* Consequently branching between two non-delay actions requires fewer than c
  holes. In particular B=W+1 and a non-prefix completed set force the all-ready
  non-delay action.

These are local statements about non-delay actions. Delaying or omitting ready
jobs remains legal in the processor model, so the source correctly does not say
that every legal or optimal action is forced.

For progress, and only there, `Forward dep` and positive B,W are supplied.
The exact first missing job is then admitted and all its true predecessors lie
in the retired prefix, proving it ready. Every non-delay action is nonempty and
every actual nonterminal non-delay step strictly increases the completion count.
`nonDelay_trace_terminates` proves retirement of all N jobs at boundary N for an
already given actual trace satisfying non-delay at every cycle. This is a real
quantitative theorem; it neither constructs such a trace nor assumes a completion
horizon. Existence of a non-delay optimum is a separate missing theorem.

## 4. Finite continuation simulation is substantive and closed

`Continuation` is an inductive chain of exactly k existing `ROBStep` transitions.
Each step retains batch width, readiness using the old state, completion union,
exact contiguous retirement, and eager admission. It is not an abstract relation
with simulation or optimality built into its constructors.

`completedPrefix_exists` proves a retirement prefix exists for every finite
completion predicate, then `afterAction` uses that prefix to define the canonical
successor. `afterAction_step` requires actual `BatchWidth` and actual readiness.
`step_coherent` independently proves preservation of coherence, including that
newly completed jobs remain below the new eager frontier. Increasing retirement
is derived from completion inclusion, not posited.

Given coherent s,s' with completed(s) contained in completed(s'), the simulated
action removes exactly the jobs already completed in s'. Restricting the old
lane map preserves width. Readiness persistence proves each residual job eligible
before the new cycle; this does not allow executing a dependent pair via
same-cycle bypass. Constructing the successor then preserves completion inclusion.

`continuation_dominance` inducts on every original step and composes these real
successors. It returns a chain of the same length, a coherent endpoint, and
completion inclusion at that endpoint. Empty residual actions and idle steps
after completion are permitted by the original relation, so an earlier finish
does not invalidate the exact-length conclusion. `finishesFrom_dominance` uses
endpoint coherence to turn full retirement into all jobs complete, applies the
inclusion, and turns it back into full retirement in the simulated endpoint.

Thus this is a genuine finite operational replay theorem, not merely the
one-job readiness lemma. It requires no forward-edge or positive-resource
hypothesis once the original finite continuation exists.

## 5. Representation and optimality limits

`trace_segment` derives the finite chain from any actual `ROBTrace` segment.
`trace_finishing_segment_dominance` applies simulation to states of two actual
traces with the same program and resources. Its conclusion is that the second
state **admits an alternative finite continuation** of the given finishing
length. It does not assert that the second trace's preselected future actions
finish that quickly.

The converse bridge is not proved here: no theorem turns a newly returned finite
chain into a complete time-assignment-indexed trace spliced to the reachable
state's past. No equivalence with the old `Optimal` predicate follows merely
from the one-way extraction theorem.

`OptimalFrom` minimizes lengths of finite finishing continuations. Its monotonicity
endpoint takes both optima explicitly as premises and then applies the substantive
finishing-dominance theorem. It does not establish the existence of either optimum,
the existence of a non-delay optimum, an action-extension theorem, a scalar
macro recurrence, any runtime bound, or correctness of a Python implementation.

For an arbitrary incoherent structure, the raw predicate `FinishesFrom` tests
`final.retired=N` and need not by itself imply all jobs complete. Every accepted
dominance/actual-state use has coherent starts and proves coherent endpoints, so
this definitional distinction creates no loophole in the audited theorems.

## 6. Boundaries and disposition

The structural and finite-simulation proofs allow N=0, empty chains k=0, empty
actions, and zero resource parameters wherever an input state/continuation
satisfies the premises. At N=0 coherence forces retirement zero; the finite-chain
base case preserves the entire initial state. Full completion makes the
readiness set empty, so terminal idle padding remains an actual step. The progress
and N-cycle termination theorem explicitly requires B,W>0 and also covers N=0.

The completed-prefix coherence condition includes both `retired<=N` and the first
missing job, so no malformed retirement index or hidden finite-index omission
supports these proofs. The code does not infer arbitrary reachable-state
existence from coherence alone, nor does it need that inference for simulation.

Accepted status: **LEAN_VERIFIED** and **INDEPENDENTLY_REVIEWED** for the exact
statements above. Novelty is not established by this review. The next substantive
formal gap is finite action extension and existence of an optimal non-delay
continuation, followed by the representation and exact macro-DP bridges.
