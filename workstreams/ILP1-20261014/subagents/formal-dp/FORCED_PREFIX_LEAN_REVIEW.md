# Independent review: first-clear forced segments in actual ROB executions

Reviewer: formal-dp, not the proof author. Review date: 2026-10-13 UTC.
Pinned author commit: `f681f6a6ddc379ec683ba0e6c5d5803c1c9c4052`.
Reviewed source: `formal/ROBForcedPrefix.lean`, its exact imports, runner,
and `formal/ROB_FORCED_PREFIX.md`.

**Verdict:** accept the 18 audited endpoints. Fresh compilation and semantic
review found no blocking error. The source proves actual fixed-action successor
uniqueness, forced non-delay steps outside clear states at B=W+1, first-clear
forced-tail existence/uniqueness, and decomposition of the original finishing
non-delay action profile at its first clear state or first subsequent clear state.

The module does not yet prove strict macro endpoint advance, the macro N-r length
bound, the optimal-cost recurrence, action enumeration, or an executable DP. The
author's documentation correctly preserves those boundaries.

## Fresh compilation and provenance

The reviewer completed `git fetch origin`, inspected the runner, and executed
`verify_forced_prefix.py` with the pinned Lean 4.34.1 compiler, commit
`5045d0056413266e57c625dcd7c365b10e377c52`, bundled Std, and no Mathlib.
The complete import chain was rebuilt into a fresh temporary directory, with a
fresh documented executable-path compatibility shim and no reused author oleans.

Model, Operational, WorkBounds, Ready, Continuation, NonDelay, Representation,
and ForcedPrefix passed with 22+11+16+25+12+11+16+18 primary audits respectively.
The 18 final-module endpoints are new; the other 113 are repeated import audits.
All exit codes were zero. Actual compilation time totaled 4.406593 seconds.
The reports contain only standard `propext`, `Classical.choice`, and `Quot.sound`;
several declarations are axiom-free. No `sorry`, proof `admit`, new axiom,
`native_decide`, or unsafe proof shortcut appears. `step.admit` names the original
eager-admission field, not a proof command.

Logs and receipt: `evidence/forced-prefix-independent/`.
Pinned source, runner, document, import and shim hashes:
`evidence/forced-prefix-provenance.json`. Every inspected input was verified
byte-identical to the author commit. The provenance also records the fetched
research-branch SHA and UTC build times. The author's new untracked
`ROBMacroOptimality.lean` was neither imported nor reviewed here.

```sh
python workstreams/ILP1-20261014/formal/verify_forced_prefix.py \
  --lean /absolute/path/to/lean-4.34.1-linux/bin/lean \
  --proc-self-compat --output /absolute/path/to/forced-prefix-independent
```

## 1. Clear states and actual successor uniqueness

`Clear s` means `s.completed(i) iff i<s.retired`, not merely that every
retired job is complete. It therefore excludes completed-but-unretired holes.
`prefixState` also fixes the retired and eager admitted frontiers. Its coherence
theorem explicitly requires r<=N; the unguarded `prefixState_clear` statement
alone does not assert that an out-of-range r is a coherent processor state.

`clear_state_eq` proves equality of all fields for a coherent clear state.
`finished_clear` uses retirement=N and coherence, and `nonclear_nonterminal`
uses both this implication and the coherent bound retired<=N. Thus nonclear
states cannot be terminal under the hypotheses used for progress.

`step_unique` derives next-state completion equivalence from the original step
union equations and extensional equality of actions. Applying completed-prefix
monotonicity in both directions proves equal retirement frontiers, and eager
admission then agrees. It does not assume the start state coherent because all
constraints needed for uniqueness are already in the two actual successor steps.

This theorem proves extensional state equality, rather than a weaker coincidence
of costs or retirement indices. It also correctly allows action predicates with
different expressions but identical membership.

## 2. Outside a clear state, the actual non-delay step is forced

For coherent B=W+1 states, nonclear means at least one hole by the previously
proved hole-count/prefix equivalence. The actual ready+hole count bound then
gives readyCount<=W. `nonclear_all_ready` applies the existing non-delay count
equivalence to show every non-delay action is exactly `CanIssue dep s`.

`nonclear_step_unique` combines action equality with actual successor uniqueness.
It does not say all legal actions are forced: a delaying action may still be
legal. No oldest-first assumption, graph-shape restriction, or forwardness
hypothesis is smuggled into this conditional structural theorem.

## 3. ForcedTail really stops at the first clear state

Its stop constructor requires Clear and has no actions. Its continuation
constructor requires not Clear, uses the existing actual all-ready `ROBStep`,
and recursively continues from the resulting state. These opposite guards
exclude both premature stopping at a nonclear state and continuing through a
clear state. The endpoint is clear by induction.

`forcedTail_profile` proves that, from a coherent start, every recorded step is
non-delay and yields a profile with precisely the same list and endpoints. This
uses the ready-count theorem and propagates coherence via actual steps; non-delay
is not an assumed field in the forced-tail relation.

`forcedTail_unique` compares two tails by induction. Stop/continue mismatches
contradict the guards; when both continue, their first action predicates are
literally the same all-ready predicate, actual successor uniqueness identifies
their intermediate states, and the induction identifies the remaining list and
endpoint. No horizon or endpoint equality is assumed. Conditional uniqueness
does not need coherence, forwardness, or positive width once both tail objects
exist; those hypotheses are supplied separately for existence.

`forcedTail_exists` uses forward dependencies, W>0, and a coherent start at
B=W+1. A clear start returns the zero-length tail immediately, including a clear
but not yet finished prefix. At a nonclear start it constructs the all-ready
actual action, proves it non-delay, and applies actual nonterminal step progress.
The genuine count N-completedCount strictly decreases, with the successor count
bounded by N before natural subtraction is used. Strong induction yields a tail
of length at most the original remaining count and a coherent endpoint.

This is a first-clear return bound, not a claim that the tail alone finishes all
remaining jobs. The endpoint may be a nonterminal clear prefix. There is no
unproved fixed-width constant bound on tail length.

## 4. Decomposition preserves the original execution

`profile_first_clear` assumes a finishing non-delay actual `Profile`, coherent
start, and endpoint retirement=N. If the current state is already clear, it
splits off the empty list and retains the entire original profile as the suffix.
Otherwise the actual next action equals all-ready by the structural theorem;
the proof recurses on the original profile tail, after proving the successor
coherent, and prepends that same action to the extracted forced list.

The empty-profile case is justified because coherence and final retirement=N
make its only state clear. This ensures a first-clear endpoint exists somewhere
in the supplied finishing profile without assuming a separate termination bound.
No positive-resource or forwardness premise is needed for this conditional
decomposition.

The result states exact list equality `actions=first++rest`, an actual forced
tail for `first`, and the original profile suffix `rest` to the original final
state. It is stronger than replacing the remainder with some equally fast
schedule. Since the forced relation cannot pass a clear state, this cut is the
first clear one, including a possible cut at the starting boundary.

`profile_first_macro` additionally assumes a clear, nonterminal starting state.
The original finishing profile cannot be empty. The proof retains its original
first actual non-delay action, then applies first-clear decomposition to the
original remaining profile. Thus its macro ends at the first **subsequent** clear
state and is nonempty; a one-cycle macro is allowed when the first successor is
already clear. An omitted oldest job is covered without a separate case or
normalization rule.

## 5. Terminal idle macros and remaining proof obligations

`PrefixMacro` itself requires a clear start, one actual non-delay step, and a
forced tail. It does not require the start nonterminal. Consequently a completed
coherent state can have a one-cycle terminal idle macro returning to itself:
the empty action is non-delay, its actual successor is unchanged, and the tail
immediately stops. This is allowed by the definition and expressly documented;
it is not a counterexample to the guarded decomposition theorem.

Therefore `prefixMacro_nonempty` proves positive *list length*, not strict
endpoint-index progress. Any later strict-growth/acyclic macro theorem must
include the needed nonterminal and progress hypotheses. Likewise the N-|D|
bound proved for `ForcedTail` is not yet a bound for `PrefixMacro`, whose first
decision cycle is separate. A valid N-r macro bound must combine first-step
progress with the tail bound.

N=0 is handled by coherent clear/terminal states and an empty forced tail; the
nonterminal macro-decomposition premise is then impossible. The forced-tail
existence theorem excludes W=0, while structural uniqueness and conditional
decomposition do not need positivity. Program-end truncation, W=1, and B>N
remain inside the same actual model; no full-window premise is assumed.

Accepted status: **LEAN_VERIFIED** and **INDEPENDENTLY_REVIEWED** for these exact
18 endpoints. No novelty claim is made. The operational decomposition component
of `FIRST_CLEAR_PREFIX_INTERFACE.md` is now supplied by this author module;
strict macro advance, actual macro-cost optimality, complete first-action
enumeration and executable DP correctness remain separate gates.
