# Readiness persistence, forced actions and progress

Status: the actual-state structural and termination results listed below
are **LEAN_VERIFIED**. They supply part of the proof infrastructure for
the forced-segment recurrence. They **do not** formalize optimal non-delay
continuation existence, the complete continuation-simulation argument,
the scalar prefix DP, its runtime, or the Python implementation.
Historical novelty remains **NOVELTY_UNCONFIRMED**.

New module: `ROBReady.lean`, using only Lean 4.34.1's bundled Std and the
unchanged `ROBWorkBounds` / `ROBOperational` / `ROBModel` imports.
The mathematical reference is the theory agent's `FORCED_SEGMENT_DP.md`
at commit `a9408865e844cd05ea7fefda10bf9139f671075c`.

## An actual-state invariant, not an assumed target inequality

`Coherent B s` records these structural facts:

* `s.retired` is the exact completed prefix, with its first missing index
  incomplete unless all jobs have retired.
* `s.admitted=min(N,s.retired+B)` is the eager exclusive admission frontier.
* Every completed job has index below that admission frontier.

`trace_coherent` proves all three for **every cycle of every actual
ROBTrace**. In particular, completed-but-unretired entries are still
inside the window. No capacity-count or readiness bound is included
as a premise of this invariant.

`canIssue_mono` proves that if two coherent states have completed sets
D subset D', then every job ready in D that is still incomplete in D'
is ready in D'. Its proof checks the retirement lower endpoint, eager
admission upper endpoint, uncompleted condition and all true predecessors.
`trace_canIssue_mono` instantiates this for arbitrary states of two actual
ROB traces with the same window and dependency predicate. The traces may
have different issue widths and may be examined at different cycles;
the only comparison assumption is the explicit completed-set inclusion.

This is the one-job readiness persistence needed for continuation dominance.
It is not by itself a proof that an entire arbitrary continuation can be
replayed, nor that its simulated state sequence is a complete ROBTrace.

## Exact finite counts and forced actions

All predicate counts are lengths of duplicate-free filtered `List.finRange N`
lists. `holeCount s` counts exactly the jobs satisfying
`s.completed(i)` and `s.retired<=i`. The module proves

    holeCount(s) + retired(s) = completedCountOfState(s).

Thus this definition agrees exactly with `|D|-r(D)`, including natural
subtraction and empty states. Ready jobs and holes are disjoint occupants
of the current ROB. Their concatenated no-duplicate list injects into
the B offsets starting at retirement, proving

    readyCount(dep,s) + holeCount(s) <= B.

`NonDelay dep W s A` means A contains only actually `CanIssue` jobs and
has size `min(W,readyCount(dep,s))`. It does not specify a priority rule
and does not assume optimality. `batchWidth_of_count_le` constructs real
lane numbers from the ranks of selected jobs; consequently every declared
NonDelay action satisfies the model's actual `BatchWidth` predicate.

Main closed endpoints:

| Theorem | Scope |
| --- | --- |
| `trace_ready_le_width_of_holes` | B=W+c and h>=c imply at most W ready jobs in an actual state. |
| `nonDelay_iff_all_ready` | Whenever readyCount<=W, non-delay holds exactly for the action containing every ready job. |
| `trace_nonDelay_unique_of_holes` | At h>=c any two non-delay actions agree on every job. |
| `trace_branching_requires_few_holes` | Two distinct non-delay actions imply h<c. |
| `zero_holes_iff_prefix` | h=0 exactly when the completed set equals the retired prefix. |
| `trace_nonprefix_forced` | At B=W+1 every non-prefix actual state forces the all-ready non-delay action. |

These theorems apply to arbitrary finite dependency predicates whenever
the stated trace/state exists. They require no oldest-job normalization.

## Progress and a quantitative termination theorem

Forward dependencies and positive B ensure that the oldest unretired job
is ready in every nonterminal coherent state. With positive W, every
non-delay action is therefore nonempty.

`nonDelay_step_progress` uses an actual `ROBStep`, including its completion
and eligibility fields, to prove that a nonterminal non-delay step increases
the completed count by at least one. The count bound is a genuine finite
set inclusion proof, not an assumed progress measure.

`nonDelay_trace_terminates` quantifies over an actual ROBTrace whose
cycle actions all satisfy NonDelay, a finite forward dependency predicate,
and positive B,W. It proves all N jobs have retired at cycle boundary N.
There is no given completion horizon. Empty programs are included.

This proves a bound for any such trace. Existence of a non-delay trace,
or of an **optimal** non-delay trace from an arbitrary reachable state,
is a separate theorem and is not asserted here. In particular the full
forced-macro recurrence is still outside this module's formal coverage.

## Reproduction and independent review boundary

```sh
python workstreams/ILP1-20261014/formal/verify_ready.py \
  --lean /absolute/path/to/lean-4.34.1/bin/lean
```

Add the previously documented sandbox-only `--proc-self-compat` flag when
needed. The runner freshly compiles the exact three imports and new module.
Twenty-five primary statements have real transitive axiom audits, containing
only `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorry`,
`admit`, new axiom, or trusted native proof shortcut. Logs, source hashes,
version and actual run durations are in `subagents/lean/evidence/rob-ready/`.

Independent parent/reviewer compilation and semantic review remain separate
from this author's successful compilation. Previous files and receipts are
unchanged; this increment can be integrated on its own.
