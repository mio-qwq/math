# Independent review of repeated bounded-lookahead obstructions

Construction proposed by the verification agent after the theory agent's
single-block `LOOKAHEAD_BOUNDARY.md`. This note independently reconstructs
the block barrier, information argument, and exact family bounds.
Decision: **ACCEPTED as a written proof**. No Lean, historical originality,
or unperformed computational check is claimed here.

## 1. Family and precise observation model

Fix integers `M>=1`, `0<=L<=2M`, and `q>=1`. Let

`n0=2M+5`, `K=M+2`, `B=4`, `W=3`.

Use `q` consecutive copies of the unpadded two-chain block from
`LOOKAHEAD_BOUNDARY.md`, with total length `N=q n0`. In block `k`,
its four root positions are `a=0,1,2,3` relative to that block;
`A_0=3,B_0=2`, `A_j=2j+2,B_j=2j+3`, and `z=2M+4`.
A bit `b_k in {A,B}` chooses whether `z` depends on `A_M` or `B_M`.
All stated indices in this paragraph are relative to block `k`.

For every block after the first, give each of its four root positions
two true predecessors from the preceding block: the preceding `z`
and the preceding chain leaf **not** selected as that `z`'s parent.
All other incoming edges are the original within-block chain edges.
Every true indegree is at most two. The repeated family no longer has
maximum true outdegree one; the single-block theorem retains that
stronger restriction.

At a cycle boundary with retired prefix `r`, the policy may inspect
incoming operands of jobs with index strictly below
`min(N,r+B+L)`. It retains all previous observations, may know `N,M,q`,
and may use arbitrary computation, memory and internal randomness.
It receives no outgoing-use oracle or other description of hidden
operands. This is a prefix lookahead model, not a budget of arbitrary
future-operand queries.

## 2. Exact block separation without extra jobs

**Lemma 1.** Every job in block `k+1` must issue strictly after every
job in block `k` completes.

**Proof.** Write `s` for the start of block `k`. The first root in
the next block has index `s+n0=s+2M+5`. Its artificial ROB predecessors
include every previous index at most `s+2M+1`, because their distance
is at least `B=4`. This covers all but the last three jobs of block
`k`, including the isolated roots 0 and 1. The last three are
`A_M,B_M,z`. The next root has `z` and the unselected leaf as true
predecessors; the selected leaf is itself a predecessor of `z`.
Thus these last three jobs also precede the next root.

Every other root in block `k+1` has at least the same early artificial
predecessors and the same two true parents, so the argument applies
to all four roots. Every remaining job in the next block is a
descendant of one of its chain roots. Transitivity proves the claim. ∎

The extra parents are all already complete when a block starts, so
they add no cycle to the single-block schedules. Concatenating the
correct `K`-cycle schedules is legal. Conversely, separation and the
chosen critical chain of length `K` in each block imply a lower bound
of `qK`. Therefore every bit vector has exact offline optimum

`T*=qK`.

This is separation of actual execution, not just program order. Future
root entries may be admitted before the preceding block finishes, but
their true/ROB predecessors prevent their issue.

## 3. Why a block's bit is still hidden at its first decision

Let `s` be the current block's start. Before any job in that block
has issued, the retired prefix has never exceeded `s`. Consequently
every earlier observation frontier is at most

`s+4+L <= s+2M+4`,

which is the index of the current `z`, excluded from the visible
prefix. The current bit appears in the incoming edge of this `z`
and in the root metadata of the next block. Those next roots occur
even later. Hence neither form of the current bit has been visible
before the first action in the current block. The current roots'
incoming edges encode only the preceding bit, and provide no information
about the current one.

By Lemma 1, that first action occurs after the previous block completes,
so its possible job choices and the single-block lower-bound argument
are exactly as before. To finish this block in `K` cycles, an `A`
block requires first action containing relative jobs 0 and 3, whereas
a `B` block requires first action exactly `{0,1,2}`. The optimal
first-action sets are disjoint. This remains true for underissuing
policies; idle time between blocks can only increase total makespan.

## 4. Randomized and deterministic bounds, including additive constants

Give the `q` bits the independent uniform product distribution. Conditional
on all observations and private random choices before a block's first
action, its bit remains uniform by Section 3. No action can be optimal
for both choices. The expected duration of that block is at least
`K+1/2`, since a nonoptimal first action costs at least one whole cycle.
Block durations are disjoint by Lemma 1; idle gaps only add time. Thus

`E[T] >= q(K+1/2)`.

For every randomized policy there is a **fixed** bit vector whose
expected cost is at least this average. This is an oblivious-input
argument, not an adversary choosing bits after observing realized
random choices.

The bound is attained within the promised family: independently guess
the leading chain with probability one half in each block, use its
first action and two-chain continuation, and issue `z` one cycle later
if the guess is wrong. Each correct block takes `K` and each wrong
block `K+1`, for expected total `q(K+1/2)` on every fixed input.
The exact randomized family minimax ratio is therefore

`1+1/(2K) = 1+1/[2(M+2)]`.

For a deterministic policy, construct a fixed bit string sequentially.
At each block, its first action is determined by the already fixed
past and cannot depend on the current bit. Choose a bit for which
that action is nonoptimal. This defines a single complete input
without changing anything the policy had already observed. Every
block then takes at least `K+1`. A fixed leading-chain guess supplies
the matching family upper bound, so the deterministic family minimax
ratio is exactly `1+1/K`.

Now allow a competitive guarantee `E[T] <= rho T*+alpha`, where
`alpha` is any input-independent finite constant. If
`rho<1+1/(2K)`, take

`q > alpha / (K+1/2-rho K)`

(or any sufficiently large positive integer when `alpha<=0`). The
averaging bound contradicts that guarantee on some fixed input.
The deterministic statement follows in the same way with `K+1`.
For each fixed `L`, choosing `M=max(1,ceil(L/2))` therefore gives a
strict lower bound above one even with additive constants. Its gap
is of order `1/(L+1)`; this does not prove a lookahead-independent
constant gap.

## 5. Fixed-length advice for exact optimality

On this promised family, exactly `q` advice bits available before
execution are necessary and sufficient for deterministic optimality
on every input. Sufficiency is the explicit bit vector.

For necessity, suppose two different bit vectors receive the same
advice, and consider their first differing bit. Previous block bits
agree. Before the first action in the differing block, the policy's
full observation and execution histories are identical by Section 3;
even metadata encoding the differing bit has not been visible. It
therefore takes the same action on both inputs, although those inputs
have disjoint optimal first actions. It cannot attain `qK` on both.
All `2^q` bit vectors consequently need distinct advice messages,
requiring at least `q` bits at fixed length.

This is the standard first-divergence counting technique. The review
claims the stated ROB construction and its consequences, not novelty
of the probability or advice lower-bound methods.

## Review limits

The construction assumes the exact eager ROB, unlimited in-order
retirement and next-cycle dependency semantics. The extra observation
frontier is explicitly a prefix bound. The fixed-family upper bounds
do not establish global upper bounds for all programs at these resources.
Independent computational checks are being saved by the construction's
author, the verification agent; none are reported as performed in this
review. Formalization and literature assessment remain separate tasks.
