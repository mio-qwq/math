# Independent review: finite ROB executions and global schedule equivalence

Reviewer: formal-dp, not the proof author. Date: 2026-10-13 UTC.
Pinned author commit: `0b4e56b3fe5e9dbf2d7e3132d991886a0b88a4f7`.
Reviewed source: `formal/ROBRepresentation.lean`, exact imports,
`verify_representation.py`, and `ROB_REPRESENTATION.md`.

**Verdict:** accept the residual extraction theorem, initial-state feasibility
and optimality equivalences, and globally optimal non-delay execution endpoints.
Independent fresh compilation and semantic review found no blocking issue,
circular equivalence assumption, reissue loophole, or same-cycle dependency
bypass. The initial-state representation gap identified by the two previous
reviews is now genuinely closed.

This does not verify a scalar prefix recurrence, an executable macro simulator,
or a Python solver. A literal infinite canonical-trace state-equality/splicing
theorem is not among the new endpoints; it is not needed for the stated coupled
finite-profile/global-time-assignment result.

## Independent build and pinned evidence

After a real `git fetch origin`, the reviewer inspected the runner and executed
it afresh with Lean 4.34.1, compiler commit
`5045d0056413266e57c625dcd7c365b10e377c52`, bundled Std, and no Mathlib.
The runner created a fresh temporary import directory and rebuilt Model,
Operational, WorkBounds, Ready, Continuation, NonDelay, and Representation.
The documented executable-path compatibility shim was compiled afresh; neither
compiler nor kernel was modified and no author `.olean` was reused.

All seven compilations returned zero. Primary audits were respectively
22+11+16+25+12+11+16. Only the final 16 are new endpoints; the 97 import audits
are repeated verification. Total actual compilation time was 3.944470 seconds.
Every transitive axiom audit uses only standard `propext`, `Classical.choice`,
and `Quot.sound`. No `sorry`, proof `admit`, custom axiom, unsafe proof, or
`native_decide` shortcut appears in the new source.

Complete logs and the receipt are in `evidence/representation-independent/`.
`evidence/representation-provenance.json` records the pinned commit, actual UTC
times, source/runner/document/shim hashes, fetched branch SHA, and byte-for-byte
comparison with the pinned commit for all reviewed inputs. No foreign file was
modified.

```sh
python workstreams/ILP1-20261014/formal/verify_representation.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /absolute/path/to/representation-independent
```

## 1. The action profile preserves actual choices

`Profile dep B W condition s actions final` records each original `ROBStep`
and the supplied condition on that step's actual initial state and action.
Its constructors are an empty chain and one actual transition followed by a
tail. Extraction from `Continuation` or `NonDelayContinuation` preserves the
length and original transition labels. The non-delay version carries the real
`NonDelay dep W` predicate, not an unrelated witness of the same duration.

`Fires` reads a list entry by a zero-based cycle index and uses the false
predicate outside the list. The nil, head, and successor lemmas match that exact
definition. Consequently the final correspondence quantifies over all natural
cycles, including after the finite profile ends.

## 2. Residual realization is proved without treating completed jobs as new

For a coherent starting state and a profile ending with `retired=N`,
`profile_realization` constructs a time assignment for all `Fin N` jobs but
imposes meaningful residual scheduling obligations only on jobs initially
unfinished. Its exact-issue field is

    Fires(actions,c,i) iff (not s.completed(i) and t(i)=c).

Thus it both excludes reissue of initially completed jobs and ensures every
initially unfinished job is issued exactly once before the profile horizon.
`residual_unique_issue` derives that existence/uniqueness explicitly. Times
assigned to initially completed jobs need not satisfy width or horizon bounds;
the theorem correctly does not call this arbitrary-state residual assignment a
global `Legal` assignment for all N jobs.

The induction uses the actual completion union. Jobs in the head action get
time zero; all other jobs get the extracted tail time plus one. A job initially
unfinished and absent from the head is precisely still unfinished in the
intermediate state. Initially completed jobs remain complete, and actual head
eligibility excludes issuing one of them. These facts justify each case of the
all-cycle exact-issue equivalence, rather than merely bounding a duration.

For a true edge between initially unfinished jobs, the target cannot be issued
in the head because that would require the source already complete. If only the
source is in the head, zero is strictly less than the positive shifted target
time. Otherwise the tail's strict inequality shifts by one. This preserves the
one-cycle latency with no same-cycle chain execution.

The same argument for a window edge `i+B<=j` uses the actual eager window: an
initially unfinished i has `retired<=i`, while an issued head job j satisfies
`j<retired+B`. These contradict the window edge if j is in the head. Remaining
cases again use zero versus positive time or the tail's strict inequality.
The proof establishes all such window edges before invoking the previously
verified canonical-ROB equivalence; it does not assume the desired equivalence
for the newly extracted schedule.

The combined lane map uses the head batch's actual lane for head jobs and the
tail lane otherwise. Equal-time collisions cannot mix the two cases, because
the times are zero and positive respectively. Within a case, the original head
or tail injectivity theorem applies. Lane reuse in different cycles is allowed
by the original `WidthBound` definition and does not create a missing constraint.

## 3. The initial-state bridge quantifies over the same horizons

`initialState N B` has no completed jobs, retired zero, and eager admitted
frontier min(N,B). Its coherence is proved for arbitrary N and B. The extensional
state equality lemma uses predicate equivalence plus matching retirement and
admission, so `trace_initial_eq` identifies the actual trace's initial state
with this canonical structure, rather than identifying just its completed set.

At this state every job is initially unfinished. `initial_profile_realization`
therefore removes the residual guards from dependency, window, lane, horizon,
and exact-issue obligations and obtains the original `Legal` predicate together
with exactly the original profile's issue batches.

The two directions of `feasible_iff_finishesFrom` are substantive:

* A finite finishing chain is labelled, realized, and converted to `Feasible`
  with the same k. List length equals k, and all extracted job times are below k.
* A global feasible assignment produces the existing actual `legalTrace`.
  Its first k transitions give a finite chain, its horizon bound implies full
  retirement at k, and actual initial-state equality gives the correct start.

Empty padding cycles are permitted on both sides. Neither side requires that
the last nonempty issue batch occur at k-1; both feasibility predicates mean
completion by horizon k. `optimal_iff_optimalFrom` then transfers the minimum
over **all** natural horizons using this same equivalence in both directions.
There is no horizon restriction, omitted shorter schedule, or postulated lower
bound in that transfer.

## 4. The global non-delay endpoint preserves the execution it certifies

`global_optimal_nonDelay` starts from an existing original `Optimal dep B W k`,
transfers it to the standard initial-state finite optimum, uses the earlier
non-delay normalization theorem, and labels that same non-delay execution.
The final legal time assignment is extracted from that profile. Its statement
retains the actual non-delay profile, endpoint retirement, length k, and exact
all-cycle correspondence with the extracted time assignment together.

It would be insufficient to return a non-delay execution and an unrelated legal
time assignment merely sharing a horizon; this code avoids that issue.
`global_optimal_nonDelay_exists` supplies an optimum for arbitrary forward
finite programs and positive B,W from the previously proved bounded finite
optimum, transfers it to the original `Optimal` predicate, and returns the
coupled profile/assignment witness with k<=N. These hypotheses are sufficient;
an optimum or finite finishing witness is not an extra premise of the existence
endpoint.

The statement certifies a finite actual non-delay execution and an exactly
matching globally legal time assignment. It does not literally quantify over
an infinite `ROBTrace` and identify every one of its states with every profile
state. Such a uniqueness/splicing endpoint remains separate and is not needed
to call the stated global feasibility and optimality equivalences proved.

## 5. Boundaries, residual scope and next gate

The representation equivalences need no forwardness or positive-resource
assumption. They are equivalences conditional on their left/right witnesses,
not existence assertions for an impossible nonempty zero-resource program.
N=0 admits empty assignments and idle finite profiles; its global optimum is
zero. Under the existence theorem, k<=N forces k=0 and the action list empty.
The zero-width and zero-window cases create no bogus residual job: their
obligations are vacuous only when every such job is already complete.

Arbitrary coherent residual starts are covered by residual realization; full
`Legal`/`Optimal` equivalence is asserted specifically at the standard initial
state. No claim about a history-spliced arbitrary-state global assignment is
smuggled through the residual theorem. W>B and truncated program-end windows
use the original predicates unchanged.

Accepted status: **LEAN_VERIFIED** and **INDEPENDENTLY_REVIEWED** for the 16 new
audited endpoints. Historical novelty is not established or claimed. The next
substantive gap is first-clear-prefix macro extraction and its exact scalar
recurrence, followed by first-action enumeration and implementation correctness.
`FIRST_CLEAR_PREFIX_INTERFACE.md` is a separate unverified interface proposal
for that next step, not an addition to the accepted proof count.
