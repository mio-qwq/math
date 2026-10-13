# Repeated finite-lookahead lower bounds and exact family advice

Status: WRITTEN_PROOF and INDEPENDENTLY_REVIEWED. This extension was proposed
by verification subagent C from theory subagent A's single-block construction
in `../theory/LOOKAHEAD_BOUNDARY.md`. A separately reconstructed proof review is
`../theory/REPEATED_LOOKAHEAD_REVIEW.md`, theory commit
`fa9b97b77d544b9590b5e0a8c7a9cabc8f577c42`. No Lean verification or historical
novelty claim is made. The probability and advice arguments are standard;
their exact ROB realization is the object checked here.

## Model and instance family

Fix integers `M>=1`, `q>=1`, and `0<=L<=2M`, with resources `B=4,W=3`.
Let `n0=2M+5`, `K=M+2`, and `N=q n0`. At a cycle boundary whose retired prefix
has length `r`, a policy may inspect all incoming operands of instructions with
indices strictly below `min(N,r+B+L)`. It remembers all previous observations,
knows `N,M,q,L`, and may have arbitrary computation, storage, and randomness.
No outgoing-use oracle, arbitrary future-operand query, or other hidden graph
metadata is provided. This is a precise prefix-lookahead model.

Each block has relative indices `0,...,2M+4`. Its initial four positions are
roots relative to that block. Put

\[
A_0=3,\quad B_0=2,\qquad A_j=2j+2,\quad B_j=2j+3\ (1\le j\le M),
\qquad z=2M+4.
\]

Add edges `A_(j-1)->A_j` and `B_(j-1)->B_j`. A bit `b` chooses exactly one
edge `A_M->z` or `B_M->z`. For each block after the first, each of its first
four jobs has two additional true predecessors: the preceding block's `z`
and the preceding chain leaf that was not selected as that `z`'s parent.
All indices in a block are translated by its start offset.

Thus every true indegree is at most two. The repeated instance is not claimed
to have outdegree at most one; the connecting endpoints can have four outgoing
edges. Unlike a bare concatenation, these connecting edges enforce execution
separation without adding jobs or cycles.

## Exact block separation and offline value

Consider a block starting at `s`. The first root of the next block is at
`s+2M+5`. Its ROB admission requires every job of index at most `s+2M+1` to
have completed in an earlier cycle. These are exactly the early jobs of the
current block, omitting only `A_M,B_M,z`. The next root's true predecessors
include `z` and the unselected leaf; the selected leaf is a predecessor of `z`.
Consequently all three last jobs must also be complete earlier. The same
reasoning applies to all four next roots. Every remaining next-block job is
a descendant of one of those roots. By induction, no job in a later block
can issue until every job of the earlier blocks has completed.

The added predecessors are already satisfied when the next block begins.
There is therefore no extra inter-block cycle. Each block contains a true
chain of `K=M+2` jobs from its selected initial root through its selected
chain to `z`. It takes at least `K` cycles.

If the selected chain is A, the following schedule attains `K`:

\[
\{0,1,A_0\},\quad
\{B_{j-1},A_j\}\ (j=1,\ldots,M),\quad
\{B_M,z\}.
\]

If it is B, exchange the A and B names in the displayed two-chain pattern,
giving first action `{0,1,B_0}` and last action `{A_M,z}`. Each intermediate
pair is admitted and has its predecessors available at cycle start. In the
A-leading case the last unresolved root/leaf determines the retired prefix;
in the B-leading case the completed B leaf may occupy one slot behind the A
leaf, leaving the required two jobs admitted. The direct replay evidence below
checks these boundary cases as well as the written admission argument.

Concatenation gives the exact offline value for every bit vector:

\[
T^*=qK=q(M+2).
\]

To finish an A block in `K` cycles, the entire selected chain must execute
at its earliest possible cycles. In particular `A_0=3` issues first and
`A_1=4` issues second; admission of job 4 forces job 0 to issue first.
Hence the first action must contain `{0,3}`. With capacity three, its exact
possibilities are `{0,3}`, `{0,1,3}`, and `{0,2,3}`. They are all attainable.
The displayed pattern handles `{0,1,3}`. First actions `{0,2,3}` and `{0,3}`
use second actions `{1,A_1}` and `{1,2,A_1}`, respectively, then join that
pattern's clear prefix after job 4.

For a B block, `B_0=2` must issue first and `B_1=5` second. Job 5 admission
forces both jobs 0 and 1 to finish first. Its only optimal first action is
therefore `{0,1,2}`. The A and B optimal first-action sets are disjoint even
when underfull actions are allowed.

## No current-bit leakage before its first decision

Before any job of a block starting at `s` has issued, the retired prefix has
never exceeded `s`. Every earlier observation frontier is therefore at most

\[
s+4+L\le s+2M+4=s+z.
\]

The visible prefix excludes its upper endpoint. The incoming edge of current
`z` has not been visible. The only other edges encoding the current bit are
the next block's new root predecessors, which occur even later. The current
four roots' predecessors reveal only the previous block's bit. Thus the entire
observed history before the current block's first action is independent of its
bit, conditional on previously revealed bits. This includes earlier lookahead
observations, not just the current window snapshot.

Waiting without issuing a current-block job cannot advance this observation
frontier. Future roots may enter a window before a prior block completes, but
the separation lemma prevents them from executing and the frontier bound
still prevents early inspection of the next undecided bit.

## Exact family minimax and additive-constant lower bounds

Choose all `q` bits independently and uniformly before execution, independently
of the policy's random coins. At each block's first decision its bit remains
uniform conditional on the history. No action can be optimal for both bit
values. The probability of a `K`-cycle block is at most one half, while a
nonoptimal first action costs at least one additional integral cycle. Blocks
do not overlap, so every randomized policy has average expected time at least

\[
q\left(K+\tfrac12\right).
\]

Consequently, for every randomized policy, at least one fixed input bit vector
has expected time at least this value. No adversary observes realized random
choices or changes the input during execution.

A matching policy for this promised family independently guesses A or B in
each block and uses that leading-chain pattern. When the guess is correct,
`z` is ready alongside the final lagging leaf and the block costs `K`. When
it is wrong, only the lagging leaf is ready in that cycle and `z` executes
next, costing `K+1`. The policy can distinguish these cases using `z`'s
currently visible readiness; it does not require hidden-bit knowledge when
choosing the first action. For every fixed bit vector its total duration is
`qK+Binomial(q,1/2)`. Thus the exact randomized minimax ratio on this family is

\[
1+\frac1{2K}=1+\frac1{2(M+2)}.
\]

For a deterministic policy, choose a fixed bit vector recursively: at each
block select a bit whose optimal first-action set excludes the action fixed
by the previously determined observation history. The no-leakage property
makes this a single consistent complete input. Every block costs at least
`K+1`. A fixed leading-chain guess attains at most `K+1` per block, proving
the exact deterministic family minimax ratio `1+1/K`.

These are global lower bounds and promised-family matching upper bounds;
they are not claimed global upper bounds for every ROB program at `B=4,W=3`.
For any fixed `L`, choose `M=max(1,ceil(L/2))` and let `q` grow. A randomized
competitive guarantee `E[T]<=rho T*+alpha`, where `alpha` is independent of
the input, is impossible for `rho<1+1/(2K)`: choose
`q>alpha/(K+1/2-rho K)`. The deterministic version uses `K+1-rho K`.
The resulting lower gap is of order `1/(L+1)` and withstands any fixed additive
constant. It does not establish a gap independent of lookahead length.

## Exact fixed-length advice on the family

Exactly `q` advice bits, available before execution, are necessary and sufficient
for a deterministic policy to attain the offline optimum on every member of
this family. Sufficiency follows by revealing the bit vector. For necessity,
if two distinct bit vectors shared an advice message, consider the first block
where they differ. Earlier bits agree, and the full execution/observation
history before that block's first action is identical by the no-leakage proof.
The deterministic policy takes the same first action, while optimality requires
disjoint choices. It cannot be optimal on both. Thus all `2^q` inputs require
different fixed-length messages, needing at least `q` bits.

For the infinitely many lengths `N=q(2M+5)`, this equals `N/(2M+5)` advice
bits. This is an exact promised-family advice theorem, not a statement about
arbitrary query access or variable-length advice conventions.

## Actual computation and a rejected exploratory assumption

Run `python repeated_lookahead_audit.py` from this directory. It uses only the
independent time-variable CSP and direct ROB replay, with exact `Fraction`
averages over all guessed-bit traces. For every `1<=M<=3`, `1<=q<=3`, and every
length-`q` bit vector, the saved run checks:

- 42 programs with exact optimum `q(M+2)`;
- all 15 legal-size first subsets, including empty and underfull actions:
  630 fixed-first-action CSP feasibility checks at that optimum;
- 252 complete guessed-bit trace replays and their exact expected durations;
- 540 cross-block augmented-ancestor conditions establishing total separation;
- 510 comparisons after flipping one current bit, with every `0<=L<=2M`,
  confirming identical visible incoming edges before that block's first issue.

All passed. Runtime was 0.09154280400071002 seconds; exact finish time and source
hashes are saved in `repeated_lookahead_results.json`.

An initial negative-control guess that removing barriers from the two-block
`M=1,AA` instance would strictly improve its optimum was false: the exact value
remains six. That failed expectation is retained in the test comments and
report. However, its optimal six-cycle schedule actually mixes the first
block's final jobs with job 7 of the second block. A separate explicit overlap
trace is legal without connecting edges and illegal with them. Therefore
simple concatenation cannot justify the separation proof, even though this
one sample's optimum happens to equal the sum of block optima.

Finite checks do not prove the arbitrary-size statements. The arguments above,
and theory subagent A's independent review, supply those written proofs.
