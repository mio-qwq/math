# Minimal interface for the first-clear-prefix macro theorem

Status: **PROOF PLAN / INTERFACE PROPOSAL**, not Lean verification and not an
independent acceptance of a new theorem. Prepared after reviewing actual-state
Ready, Continuation, and NonDelay modules. The mathematical target is the
already written `subagents/theory/FORCED_SEGMENT_DP.md`, Sections 1–3.

Use the existing finite actual `ROBStep` model. This interface avoids an
unnecessary suffix-renumbering or infinite-trace construction before proving the
macro recurrence. All proposed statements below still require implementation
and actual compiler evidence.

## Fixed assumptions and states

For the nonempty-state progress and recurrence results, fix a finite forward
dependency predicate on `Fin N`, W>0, and B=W+1. Keep initial/terminal indices
`0<=i<=N`; using `Fin (N+1)` is one convenient way to carry this bound.

Define `prefixState i` by completed(j) iff j<i, retired=i, and
admitted=min(N,i+B). Prove it coherent. Let `Clear s` mean that s.completed is
exactly the prefix below s.retired. Existing `zero_holes_iff_prefix` identifies
this with holeCount=0 for coherent states. For a coherent clear state, extensional
equality identifies it with `prefixState s.retired`.

For fixed s and an extensionally fixed action A, actual successor state is unique:
completion is the same union, exact completed prefixes are equal by applying
`completedPrefix_mono` both ways, and admission then agrees. Use extensional
state equality, since completion fields are predicates.

## A stopping relation, not an assumed recurrence

Introduce an inductive finite `ForcedTail s ell final` with these constructors:

* Stop only when `Clear s`, with ell=0 and final=s.
* If `not Clear s`, take an actual `ROBStep` whose action is exactly
  `CanIssue dep s`, and continue with `ForcedTail` from its successor.

Thus it cannot stop at a nonclear state or continue past its first clear state.
It consists of the existing actual transition relation. Do not put a Bellman
value, optimality condition, or target endpoint into its admissibility premises.

Define `PrefixMacro i A ell j` by one actual non-delay first step from
`prefixState i`, followed by a `ForcedTail`, ending at `prefixState j`.
If the tail length is k, use ell=k+1 directly, avoiding subtraction at ell=0.
The first action may omit the oldest job; no oldest-inclusive normalization is
required by the written theorem and none should be added to this interface.

The forced tail's stop case may apply immediately after the first action.
Terminal prefix N is clear, so reaching completion always stops.

## Small lemmas which close the operational gap

1. **All-ready is the unique non-delay choice outside Clear.** Derive this for
   arbitrary coherent states from `zero_holes_iff_prefix`,
   `ready_le_width_of_holes`, and `nonDelay_iff_all_ready`. The present
   `trace_nonprefix_forced` endpoint need not be strengthened by inventing a
   surrounding trace; its state-level ingredients already suffice.

2. **Forced-tail existence, bound and uniqueness.** Under the fixed positive
   forward assumptions, construct it by strong induction on N-completedCount.
   At a nonclear state, the actual all-ready action is non-delay, hence width
   legal, and `nonDelay_step_progress` strictly decreases that measure.
   The endpoint is clear and the length is at most the starting remaining count.
   Uniqueness uses successor uniqueness and the stop/nonstop guards, by induction
   on one of the finite forced tails. It gives endpoint and length uniqueness
   for a fixed first action, not that different first actions agree.

3. **Macro existence and strict advance.** For i<N and any non-delay first action,
   construct its macro and prove 1<=ell<=N-i and i<j<=N. The first-step progress
   gives at least i+1 completed jobs; the final clear state's completed count is
   exactly j. This proof handles an omitted oldest job without an extra rule.

4. **First-clear decomposition of any finishing non-delay chain.** After its
   first step, inspect the finite chain until the first clear state. Every
   intermediate nonclear state's non-delay action is forced by lemma 1, so this
   segment is the unique matching macro. The original finite length k decomposes
   as ell+rest, with an actual finishing continuation of length rest at j.
   Termination of this inspection follows from the finite finishing chain and
   its coherent all-retired endpoint; it does not assume a uniform short bound
   on macro length.

5. **Composition.** Prove finite continuation concatenation from actual
   constructors. A macro followed by any finishing continuation at its endpoint
   is a finishing continuation from its initial prefix of the sum length.

Macro length cannot be bounded solely by W: the written even-chain family at
B=4,W=3 has first-clear return length N/2. The N-i bound above is intentional.

## Optimality statement before an executable enumerator

Choose F(i) together with `OptimalFrom dep B W (prefixState i) (F i)`, using
the already proved coherent-state optimum-existence theorem. Prove F(N)=0.
For i<N, the two substantive endpoints are:

    every PrefixMacro(i,A,ell,j) satisfies F(i) <= ell + F(j);

    some PrefixMacro(i,A,ell,j) satisfies F(i) = ell + F(j).

For the first inequality, concatenate the actual macro with an optimal endpoint
continuation. For the attaining equality, take an optimal non-delay continuation,
apply first-clear decomposition, and bound its remaining length below by F(j).
Combine with the first inequality. This proves the minimization characterization
without assuming that the residual tail of an optimum is itself optimal.

These endpoints establish a mathematical minimum over actual macros, but do not
yet verify a computed finite list of choices or an executable DP.

## Separate enumeration and algorithm gate

To connect the recurrence to the claimed polynomial algorithm, additionally prove:

* A complete finite list of first actions: all-ready if readyCount<=W; otherwise
  exactly the B choices omitting one job from a full ready B-entry window.
* When readyCount>W, count equality really forces all B admitted positions to
  be ready, including the program-end truncation bound. Do not assume the window
  is full merely from `Coherent`.
* Every listed first action is non-delay and every non-delay first action is
  extensionally one of the listed choices, including W=1 and B>N boundaries.
* An executable forced-tail simulator agrees with the actual `ForcedTail`
  relation, and a backward recurrence over strictly increasing endpoints returns
  the value and an actual concatenated optimal witness.

Only after these semantic gates does an implementation-correctness claim follow.
The cost analysis, array/edge-counter representation, and Python implementation
remain separate from proving the scalar mathematical recurrence.
