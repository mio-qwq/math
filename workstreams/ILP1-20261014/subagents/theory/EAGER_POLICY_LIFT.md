# A causal non-delay lift of any completing prefix-lookahead policy

Status: **WRITTEN_PROOF**; independent review is requested separately.
No Lean or historical novelty claim is made. Completion-set dominance
and filling idle capacity are standard scheduling ideas; the point
checked here is that this transformation also respects the precise
ROB and prefix-information interfaces.

Use the eager, in-order-retiring ROB model with positive `B,W` and
integer `L>=0`. All true edges point forward. At completed set `D`,
write `r(D)` for the first uncompleted index, or `N` after completion.
The scheduler may inspect the incoming operands of jobs

`j < min(N,r(D)+B+L)`.

It can remember already observed metadata. It cannot query the
outgoing hidden uses of a visible job. The scheduling computation
itself consumes no modeled execution cycles.

## 1. Completion inclusion preserves actions and visibility

**Lemma 1.** Suppose `V subset D` are completion sets. Then
`r(V)<=r(D)`. Every query visible at `V` is visible at `D`. If `S`
is a legal next action at `V`, then `S\D` is a ready, admitted set
at `D`, with size at most `W`.

**Proof.** Every job preceding `r(V)` belongs to `V`, hence to `D`.
This proves the prefix inequality, and adding `B+L` proves visibility.
For `j in S\D`, every true parent lies in `V`, hence in `D`. Also
`j<r(V)+B<=r(D)+B`. Since `j` is unfinished in `D`, necessarily
`j>=r(D)`. Thus the retained job is in the real window and ready.
Deleting jobs from `S` cannot exceed the width. ∎

This statement permits completed but unretired holes; neither set is
assumed to be a clear prefix.

## 2. The virtual-controller construction

Let `A` be any policy using this interface. Fix an input and its
random tape such that its virtual execution completes after finitely
many cycles and finitely many computational steps. Run a separate
virtual copy of `A` with completion set `V`, virtual time and virtual
history. Maintain a real completion set `D`, initially equal to `V`.
The real scheduler may use extra observations for filling, but it
does not feed those observations or early completions to the virtual
copy. The copy is given exactly the responses and history of its own
unmodified virtual execution on the fixed input.

For each virtual query, check its virtual frontier and forward the
query to the real observation interface, or return its cached answer.
Lemma 1 makes every forwarded query legal. When the virtual controller
chooses its next action `S`, perform the following steps.

1. Put `R=S\D`. If `R` is empty, advance the virtual action to
   `V union S` without spending a real execution cycle.
2. Otherwise retain all jobs in `R`. Add arbitrary distinct jobs from
   the other currently ready, admitted jobs until the total action
   has size `min(W,number of real ready jobs)`. Issue it in one real
   cycle, then advance the virtual action to `V union S`.
3. Stop immediately when the real program is complete.

All filler readiness is measured before the current real action.
An instruction made ready by that action is available only in the
next real cycle. This is not same-cycle dependency bypass.

**Theorem 2 (causal non-delay domination).** The lifted policy is
causal, every real cycle is non-delay, and for every fixed input and
completing virtual random tape,

`T_lift <= T_A`.

**Proof.** Induct over virtual actions, maintaining `V subset D`.
The queries are legal by Lemma 1. That lemma also proves that every
retained job is ready and admitted, so retaining it and adding other
ready jobs gives a legal action. In the empty case, `S subset D`
already, and the inclusion persists without a real cycle. In the
nonempty case, all of `S` is in the new real completion set, as are
all previously completed virtual jobs. Thus the inclusion persists.

Each actual action is filled to the stated maximum, proving the
non-delay property. Each virtual action consumes at most one real
cycle. When the virtual execution has completed all jobs, inclusion
implies that the real execution has already completed. Thus the real
makespan is no greater than the virtual makespan. Early termination
only strengthens the inequality. ∎

The time comparison couples the same fixed input and the same virtual
random tape. For a randomized policy that terminates almost surely,
it therefore also implies `E[T_lift]<=E[T_A]` whenever these expected
makespans are defined, including the extended nonnegative sense.
No comparison with an input chosen adaptively after observing the
lift's extra actions is asserted.

Consequently one may restrict to non-delay policies when minimizing
the deterministic or oblivious-input randomized competitive ratio
in this information model: each completing policy has a non-delay
dominating counterpart. This is a property of the ideal unit-latency
model, not a hardware implementation claim. In particular, real
register limits, side effects and computation time are not covered.

## 3. Applying the lift to the chunk policy

Keep the original chunk controller and its chosen offset `U` exactly
as in `LOOKAHEAD_UPPER_BOUND.md`. It continues to plan its successive
chunks from virtual clear prefixes. The real execution need not be
at a clear prefix when the virtual controller starts a new chunk.
Lemma 1, not a false assumption that their states coincide, justifies
the block's queries and the retained planned actions.

With the same offset, the lift is never slower. Averaging the same
input-independent uniform offset therefore preserves

`E[T_eager] <= [1+(B-1)/(B+L)] T*`.

This inheritance does not prove a smaller coefficient. The strict
gain shown below concerns one family only.

**Corollary 3 (the previous sharpness family disappears).** On the
two-chain family in `RANDOM_OFFSET_SHARPNESS_REVIEW.md`, with `B>=2`
and `W>=2`, every lifted chunk execution takes the optimum `q(B-1)`
cycles, independently of `L` and `U`.

**Proof.** True cross-block dependencies separate all family blocks.
Within a current block, each of the two chains has at most one ready
job. Therefore at most two jobs are ever ready in a reachable state.
Since the effective width is at least two, a non-delay action is
uniquely the set of all ready jobs. Starting from a clear block, it
issues the two corresponding chain jobs together in every cycle;
their distance is `B-1`, so both are admitted. Induction gives exactly
`B-1` cycles per block, including `B=2`. The chain lower bound matches
this value. Theorem 2 makes the lift non-delay, so it has precisely
this execution. ∎

This example isolates a weakness of the old chunk barriers. It gives
no upper bound below `1+(B-1)/(B+L)` for the lifted policy, and no
global online-optimality statement.

## 4. Callback implementation and evidence boundary

`eager_chunk_lookahead.py` implements the lift for `B=4,W=3` around the
unchanged `chunk_lookahead.run_policy`. It receives only the program
length, lookahead and two callbacks, not the future dependency graph.
The virtual read wrapper checks the virtual `r+4+L` frontier, while
the actual filler observes only actual window jobs. Parent metadata
is cached after its first legal observation. The filler uses the
oldest available jobs after keeping the retained planned action.
No property of this particular tie-break is used in Theorem 2.

The implementation asserts virtual completion inclusion after every
virtual action. An all-completed virtual action is skipped physically;
once the real execution completes, remaining virtual planning is
aborted. The random wrapper makes one uniform offset draw and keeps
it independent of the input, as in the original policy.

The source controller's planning time still occurs in virtual order;
the lift may stop it early. At fixed `B=4,W=3`, finding filler jobs
uses constant many window entries per real cycle. Every incoming
operand set is observed at most once, and caching costs `O(N+|E|)`
with edge lists. The provided Python prototype stores predecessor
bit masks and incurs their actual integer-operation costs.

`eager_chunk_check.py` and its JSON output record finite callback,
non-delay, per-offset dominance, early-completion and family checks.
Those computations check the implementation; they do not replace
the arbitrary-policy induction above. Independent review and actual
Lean coverage must be reported separately.

The saved Python 3.12.14 run checks all 1,100 forward DAGs through five
jobs at `L=0,1,5`, another 54 seeded binary-input graph/lookahead cases
up to 19 jobs, and 12 two-chain family cases. It replays 20,238 fixed
offsets and 3,366 actual seeded random-wrapper calls. The offset checks
include 102,978 legal metadata reads, 66,769 legal non-delay cycles,
2,597 skipped virtual cycles and 4,904 strict improvements over the
original controller. Every tested two-chain execution is optimal.
The saved elapsed time is 2.772980 seconds; source hashes and the
exact finite scope are in `EAGER_CHUNK_CHECK.json`.
