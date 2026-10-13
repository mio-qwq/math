# Independent review: fixed extra lookahead cannot ensure exact optimality

Reviewer: formal-DP subagent, independent of the theory author.
Review date: 2026-10-13 UTC. No theory-owned files were modified.
Reviewed final commit: `f9c74fc56e96a69772f7106519b3373df49c4ac6`.
`LOOKAHEAD_BOUNDARY.md` SHA-256:
`395e9bc5e110825c3624a66b81ba3b0736971301d243f04d7e3a55cedddd56f2`.

## Verdict

**Accepted as an arbitrary-size written proof under the declared incoming-
operand observation model.** The two exact optima, incompatible first-action
sets, odd/even length extension, and every-fixed-L impossibility have no
remaining index or visibility gap. The final note's stronger, exact
minimax ratios for its promised two-input family are also correct.

These are strict, family-specific ratios. They are not a global upper bound
for all programs or an additive-constant competitive lower bound. No Lean
verification or historical novelty claim is made. The independent finite
CSP checks below supplement, and do not replace, the following proof.

## Independent construction and scheduling proof

Jobs are zero-based; cycles in this proof are numbered from one. Fix M>=1,
p in {0,1}, and N=2M+5+p. The distinct occupied indices are

- isolated jobs 0 and 1;
- chain starts B_0=2 and A_0=3;
- A_k=2k+2 and B_k=2k+3, for 1<=k<=M;
- an isolated job 2M+4 only when p=1;
- the final job z=2M+4+p.

Thus every index from 0 to N-1 is accounted for exactly once. Chain edges
point strictly forward. Attaching z to one chain endpoint adds no fork or
merge: maximum true indegree and outdegree are both one. The two programs
differ only in z's parent, so all earlier incoming operand lists agree.
Window constraints remain resource constraints, not extra true edges.

In P_A the chain A_0,...,A_M,z has K=M+2 jobs. Strict next-cycle availability
forces at least K cycles; attaining K forces its successive jobs into cycles
1,...,K. In particular A_0=3 issues initially and A_1=4 in cycle two.
Admission of 4 at B=4 requires the retired prefix after cycle one to have
length at least one. Hence job 0 also issues initially.

For P_B the same argument forces B_0=2 into cycle one and B_1=5 into cycle
two. Admission of 5 requires retired prefix at least two, so jobs 0 and 1
must both issue initially. Together with B_0 they fill all three issue slots.
The first action is exactly {0,1,2}. This excludes job 3 and is incompatible
with every optimal first action of P_A. The argument does not assume a
non-delay policy and includes initially idle or underfilled actions.

To attain K on P_A, issue {0,1,3}, then {B_(k-1),A_k} in cycle k+1 for
1<=k<=M, then {B_M,z} plus any padding. Before the first middle action the
retired prefix is 2. Before a middle action with k>=2, it is 2k+1; both
required jobs fit within the four admitted entries. After the final middle
action the retired prefix is 2M+3. The remaining job z is at most 2M+5,
so both it and any padding are admitted for the last action. Every true
parent has issued in a strictly earlier cycle.

For P_B, issue {0,1,2}, then {A_(k-1),B_k}, then {A_M,z} plus padding.
The retired prefix before the first middle action is 3. For k>=2 it is
2k, so B_k=2k+3 is admitted exactly at the last permissible index. After
the middle actions it is 2M+2. Even with padding, z=2M+5 is inside that
four-entry window, not at its exclusive upper bound. The final batch has
at most three jobs and its parents are complete. Thus both optima equal K.

This directly covers M=1: the two chains each have two jobs before z, and
the single middle action is present. No formula requiring k>=2 is applied
to that middle action. Padding affects only the final batch and cannot
block its admission or exceed width three.

The complete optimal first-action sets are also as stated. P_A must contain
0 and 3, so only {0,3}, {0,1,3}, and {0,2,3} are possible. The second-cycle
actions {1,2,4} and {1,4} for the two noncanonical choices respectively
reach the same completed prefix 0,...,4 as the canonical schedule. Its tail
therefore supplies optimal continuations. P_B has only {0,1,2}.

## Information and quantifier audit

For every fixed N>=7, setting M=floor((N-5)/2) and p=N-(2M+5) yields
M>=1 and p in {0,1}. The pair has the same known length and agrees on every
incoming operand list for jobs 0,...,N-2. Thus even a first-action rule
given all those lists cannot select an action with an optimal continuation
on both programs.

In the initial actual ROB exactly indices 0,...,3 are admitted. With L
extra incoming-operand positions, the exclusive visible frontier is
min(N,4+L). For N>=max(7,L+5), this is at most N-1, so the final job at
index N-1 is still hidden. Equality `4+L=N-1` does not reveal z: the frontier
is exclusive. L=0 is included, with N=7,M=1,p=0 as one valid pair.

The simpler unpadded construction proposed initially is a valid special
case: choosing M>=max(1,ceil(L/2)) gives `4+L<=2M+4=z` at p=0. The final
padding extension additionally establishes the result for every sufficiently
large specified N, without a parity restriction.

Only this common initial observation is needed. Revealing the whole input
after the first action cannot undo the missed first or second critical-chain
cycle. Later lookahead growth, arbitrary policy memory, and arbitrarily
powerful computation therefore do not evade the argument.

The observation restriction is material: revealing outgoing future uses of
A_M or B_M, the last instruction's operand through another channel, or a
whole-program identifier encoding it would distinguish the pair and is not
covered. All visible instruction metadata and input values may be chosen
identically across the pair; only the hidden last incoming operand changes.
Knowledge of N itself does not distinguish them.

## Randomization, matching family upper bounds, and their limits

Let U_A and U_B denote the disjoint sets of optimal first actions. Any
randomized policy has the same initial action distribution on the two inputs.
The probability of finishing in K on P_A is at most Pr(U_A), and the
corresponding probability on P_B is at most Pr(U_B). Their sum is at most
one. Every other terminating outcome takes at least K+1 cycles; a
nonterminating outcome only strengthens the lower bound.

Averaging over the two **fixed**, equally likely inputs gives expected time
at least K+1/2. Hence some fixed input has expected ratio at least
`1+1/(2K)`. This is an oblivious-input argument, not selection of the hidden
parent after observing the realized random action. For a deterministic
policy one input instead forces at least K+1, giving `1+1/K`.

The promised-family upper bounds are valid. Choose either canonical leading
chain and follow its schedule up to the final batch. By the admission
calculation above, z is visible at the start of that batch. If its parent
is the leading chain, it is ready and finishes in K. If its parent is the
lagging chain, issue that chain's last job and any padding first, then z
alone next cycle. These are legal K+1-cycle continuations. Readiness at
the now-admitted z is sufficient; no earlier knowledge of its hidden parent
is used. One fixed choice proves the deterministic family upper bound;
a fair initial choice gives expectation K+1/2 on each input. The lower and
upper bounds therefore match exactly on this promised pair.

One advice bit identifying the parent selects the optimal canonical schedule.
Zero advice bits cannot overcome the proved indistinguishability. This
elementary necessity/sufficiency claim is correctly restricted to the pair.

The loss remains at most one cycle under these family policies, independent
of M. A fixed additive constant can absorb it. Consequently these inputs
do **not** exclude competitive factor one with an additive constant, and
they do not show a ratio uniformly separated from one as L or N grows.
Their universal content is the failure of exact optimality for every fixed
finite L across arbitrary lengths. The note makes no unjustified global
algorithmic or real-processor conclusion.

## Independent finite checks

`lookahead_pair_check.py` constructs the graph and schedules independently
of the theory implementation. It uses the separately authored
`subagents/verification/constraint_solver.py`, whose variables are execution
times and whose window constraints include all prefix-release edges.
Its direct replay checker separately implements admission and retirement.
The oracle source was read before use; it supports an **exact** fixed first
batch, rather than merely requiring some jobs to be present in that batch.

Actual run, Python 3.12.14:

- M=1,2,3, both padding values, both last-parent choices: 12 programs,
  with N ranging from 7 to 12.
- 216 CSP horizon decisions: infeasibility at K-1, feasibility at K, and
  all 16 subsets of the four initial roots for each program. These include
  15 capacity-valid subsets (including empty) and one over-width rejection.
- 60 direct operational replays of canonical optimal schedules, wrong-leader
  K+1 schedules, unrestricted CSP witnesses, and every optimal fixed-first-
  action witness.
- 33 initial-observation comparisons, covering every L from zero through
  the exact cutoff N-5 for each M/p pair, including equality at the frontier.

All checks passed. The exact optimal first-action sets agreed with the
universal proof. Runtime was 0.009764 seconds. The receipt in
`evidence/lookahead-pair-checks.json` contains both source hashes, UTC time,
all schedules, tested ranges, and actual results. No claim is made to have
rerun the author's M<=10 enumeration, and these small checks are not a
proof about arbitrary lengths or randomized policies.

Reproduction:

```sh
python workstreams/ILP1-20261014/subagents/formal-dp/lookahead_pair_check.py \
  --oracle /absolute/path/to/subagents/verification/constraint_solver.py \
  --output /tmp/lookahead-pair-checks.json
```

This is independent research-agent review, not an academic referee decision.
