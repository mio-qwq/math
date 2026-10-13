# A chunk policy and the order of the bounded-lookahead loss

Status: **WRITTEN_PROOF**; independent review and finite implementation
checks are separate. Historical novelty is unconfirmed; no Lean claim
is made. Use the eager ROB model, positive `B,W`, and forward true DAGs.
One may replace `W` by its effective value `min(W,B)` throughout.

At a boundary whose retired prefix has length `r`, the policy sees the
incoming operands of jobs with indices strictly below
`min(N,r+B+L)`, where `L>=0` is a fixed integer. This is prefix lookahead,
not arbitrary queries about future jobs. Program length may be known.

## 1. An implementable online chunk policy

Set `Q=B+L`. Partition the program into consecutive blocks of `Q`
jobs, except for a possibly shorter last block. Execute these blocks
one at a time. At a block's start, every earlier job is complete, so
the state is the clear prefix at that block's first index. The entire
block lies in the visible prefix of length `B+L`. Remove its incoming
edges from earlier blocks, since those predecessors are already complete,
and compute an offline optimal schedule of the resulting block with
the original `B,W`. Execute that schedule completely, then proceed
to the next block.

All decisions use already visible operands. Computing an optimal block
is a finite exact subproblem; this is an information bound regardless
of its worst-case computational cost. At `B=W+1`, the polynomial
prefix-macro solver in `FORCED_SEGMENT_DP.md` computes each block.

Future jobs can be admitted while a block is executing, but this policy
does not issue them early. That voluntary restriction is legal. Removing
the block-end truncation does not prevent the block's own jobs from
being admitted, and all external predecessors are already complete.

## 2. Restricting a global schedule to one block

**Lemma 1 (projection).** Restrict any legal global schedule to jobs
of a consecutive block, deleting all other issued jobs and all cycles
that become empty. The result is a legal schedule of that block,
with earlier-block predecessors treated as initially complete.

**Proof.** Retain the order of nonempty projected cycles. Every true
edge with both endpoints in the block still has its source in a strictly
earlier projected cycle: neither endpoint's cycle was deleted. Every
artificial ROB edge between block jobs is also preserved, because
index differences are unchanged by renumbering a consecutive interval.
Recall that these edges include every pair `i<j` with `j-i>=B`.
Cycle widths only decrease. The established exact equivalence between
this augmented precedence model and eager ROB schedules proves legality.

Equivalently, in direct operational terms, fully completing all jobs
before the block can only advance the retired prefix relative to the
original execution. A retained uncompleted job remains at or after
that new prefix and below its enlarged admission frontier. Removing
later jobs never removes an earlier predecessor of a block job.
Deleting empty projected cycles preserves next-cycle dependencies. ∎

## 3. Counting the cost of block boundaries

Fix a global optimal schedule of length `T*`. For each block `j`, let
`a_j` count its nonempty projected cycles. By Lemma 1, the block's
optimum is at most `a_j`, so

`T_chunk <= sum_j a_j`.

All jobs issued in a single cycle lie in one window of `B` consecutive
indices, and therefore have span at most `B-1`. Since `Q>=B`, a cycle
can touch at most two consecutive blocks. A cycle contributing to two
projections is exactly a cycle issuing jobs on both sides of one block
boundary. Thus

`sum_j a_j <= T* + sum_c x_c`,

where `x_c` counts cycles crossing boundary `c`. Empty original cycles,
if any, only make this an inequality rather than an equality.

**Lemma 2 (one boundary).** For every cut between indices `c-1` and
`c`, at most `B-1` cycles issue jobs on both sides of that cut.

**Proof.** Such a cycle issues some `i<c` and some `j>=c`. Their
common-window span bound gives `i>=j-B+1>=c-B+1`. Choose one issued
job on the earlier side. It lies among the at most `B-1` jobs
`max(0,c-B+1),...,c-1`. Different cycles choose different jobs because
a job issues only once. This is an injection of crossing cycles into
those earlier jobs. ∎

**Theorem 3 (chunk guarantee).** For every nonempty program,

`T_chunk <= T* + (B-1) floor((N-1)/(B+L))`

`<= [1+W(B-1)/(B+L)] T*`.

**Proof.** There are exactly `floor((N-1)/Q)` internal block boundaries.
Apply Lemma 2 at each boundary and the projection inequality. Then
`floor((N-1)/Q)<=N/Q` and the work bound `N<=WT*` give the second
inequality. ∎

If `N=0`, both makespans are zero. If `N<=B+L`, there is one block
and the policy is exactly optimal. For `B=1`, the boundary term is
zero, as expected for a serial window. Unit latency and strict
dependency cycles are preserved throughout; no same-cycle bypass
is introduced by projection or by the chunk algorithm.

The additive boundary term is not claimed to be the best possible
for every program, nor is the competitive-ratio constant asserted
optimal. The guarantee uses no maximum-indegree assumption.

## 4. A stronger randomized bound by shifting the block boundaries

The verification agent proposed the following improvement; the theory
agent independently checked its probability, causality and boundary
arguments. Sample `U` uniformly from `1,...,Q` before executing the
program, independently of its contents. Use an initial block of length
`U`, followed by blocks of length `Q` and a possibly shorter final block.
Each block is still no longer than the visible `B+L` prefix, so the
same exact block-planning policy is causal.

**Theorem 4 (random offset).** Against every fixed input,

`E[T_offset] <= T* + (1/Q) sum_t span(A_t)`

`<= [1+(B-1)/(B+L)] T*`,

where `A_t` are the actions of any fixed global optimal schedule,
`span(A_t)=max(A_t)-min(A_t)` for nonempty actions, and empty actions
have span zero.

**Proof.** Fix the input and one of its optimal schedules before
averaging over `U`. For each choice of offset, project this same
schedule into the resulting blocks as in Lemma 1. A nonempty action
has span at most `B-1<Q`. The grid boundaries are `U,U+Q,U+2Q,...`,
excluding boundaries at or beyond `N`. The action is split exactly
when one boundary lies at an integer position `c` with
`min(A_t)<c<=max(A_t)`.

There are exactly `span(A_t)` such integer positions, each in
`1,...,N-1`. Each position has exactly one corresponding offset
`U in {1,...,Q}`; residue zero corresponds to `U=Q`. Distinct such
positions have distinct residues, because their total span is below
`Q`. Thus the action's split probability is precisely `span(A_t)/Q`,
and it can cross at most one boundary. The first and last partial
blocks do not change this calculation.

The sum of projected cycle counts exceeds the original count by
one for each split action. Each block optimum is no greater than
its projection length. Linearity of expectation proves the first
inequality; `span(A_t)<=B-1` proves the second. Empty cycles, if
present, only weaken the comparison. ∎

The adversary is oblivious: its input is fixed independently of the
offset draw. No assertion is made for an adversary that observes `U`
and then selects the hidden program. The deterministic bound in
Theorem 3 remains valid separately; randomizing the offset does not
replace its stronger additive boundary formula on each fixed partition.

## 5. Matching order at `B=4,W=3`

Let `rho_det(L)` and `rho_rand(L)` be the infimal competitive ratios
for deterministic and randomized policies in this prefix-lookahead
model. Ratios here may include an arbitrary finite additive constant
independent of the input. The randomized guarantee is against fixed
oblivious inputs. One may restrict the input class to true indegree
at most two; the statements below still hold.

Set `M=max(1,ceil(L/2))`. The independently reviewed repeated family
in `REPEATED_LOOKAHEAD_REVIEW.md` gives

`rho_det(L) >= 1+1/(M+2)`,

`rho_rand(L) >= 1+1/[2(M+2)]`.

These lower bounds explicitly survive additive constants because
the number of separated blocks can grow without bound at fixed `L`.
The two chunk policies give the upper bounds

`rho_det(L) <= 1+9/(L+4)`,

`rho_rand(L) <= 1+3/(L+4)`.

Consequently, as integer `L` tends to infinity,

`rho_det(L)-1 = Theta(1/L)` and
`rho_rand(L)-1 = Theta(1/L)`.

This determines the order of the optimal information loss, not its
leading constant or exact value at any finite `L`. It also explains
how two apparently different statements coexist: no finite lookahead
is universally exact, but increasing finite lookahead brings the
best guaranteed ratio arbitrarily close to one.

## 6. Causal implementation and evidence scope

`chunk_lookahead.py` implements the policy at `B=4,W=3` through callbacks
`read_parents(job)` and `issue(action)`. It receives only `N,L` and
these interfaces, reads precisely the current block's operands, and
uses the polynomial one-extra-entry solver for that block. It cannot
consult a future instruction through a supplied full-program argument.
An optional `initial_chunk_size` selects a shifted partition. The
wrapper `run_random_policy` draws this size once uniformly from
`1,...,4+L` using an injectable random generator; its default is
`SystemRandom`. The remaining computation is unchanged.

If `E_j` is the block's internal edge count, the macro solver costs
`O(Q_j min(4,Q_j)(Q_j+E_j))` for that block. Summing yields the
conservative total planning bound `O(Q(N+|E|))` at these fixed resources,
including reading incoming edges. The policy can release a block's
planning state after execution; it does not require knowledge of
outgoing hidden dependencies. This is a scheduling interface, not
an implementation claim about a physical processor.

These are indexed edge-list planning bounds. The Python callback
prototype uses integer predecessor masks and additionally pays their
ordinary bit-conversion costs; it does not treat arbitrarily long
integers as unit-cost input objects.

The checker supplies an environment that rejects any read outside
the actual current `r+4+L` frontier and any illegal ROB action. It
also compares against the independent completed-state optimum and
checks the additive boundary inequality. Actual run metadata is saved
in `CHUNK_LOOKAHEAD_CHECK.json`; finite tests are not the proof of the
general projection or asymptotic result.

The saved Python 3.12.14 run passes 4,400 exhaustive small-graph/lookahead
cases, 100 seeded random cases up to 30 jobs, and 60 hidden-family cases.
Every operand access is checked against the actual evolving observation
frontier. The report was regenerated after adding the offset interface,
so its current runtime and source hash are authoritative. A separate
`RANDOM_OFFSET_CHECK.json` records exact enumeration of offsets and
the stronger expectation inequality, not a Monte Carlo estimate.

The exact-offset run checks 4,400 exhaustive program/lookahead pairs
through five jobs using all 26,400 associated offsets, plus 27 seeded
larger cases and 216 offsets. It also makes 4,427 actual seeded calls
to the random wrapper and checks their selected partition against the
enumerated values. All causal checks and the refined span-sum inequality
pass; the recorded runtime is 1.626537 seconds.
