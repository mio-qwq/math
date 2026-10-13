# One unseen final instruction can determine the optimal first action

Status: **WRITTEN_PROOF**, with finite checks reported separately.
Independent review is in progress. No Lean or historical novelty claim
is made. This is the eager ROB model with `B=4,W=3`, forward true edges,
unit execution, next-cycle availability, and maximal in-order retirement.

The information restriction concerns incoming operands: the scheduler
can inspect the incoming true edges of visible instructions, but it is
not given the outgoing edges or hidden future use counts of visible
results. Program length may be known. An observation rule that reveals
the last job's operand through another interface is outside this result.

## 1. Two programs with a common all-but-last prefix

Choose integers `M>=1` and `p in {0,1}`, and put `N=2M+5+p`.
Jobs `0,1,2,3` are roots. Define

`A_0=3`, `B_0=2`,

`A_k=2k+2`, `B_k=2k+3` for `1<=k<=M`.

For every `k>=1`, add the sole incoming edge
`A_(k-1)->A_k` and the sole incoming edge `B_(k-1)->B_k`.
If `p=1`, job `2M+4` is an additional isolated root. The last job is
`z=N-1`. In program `P_A`, its sole predecessor is `A_M`; in program
`P_B`, its sole predecessor is `B_M`.

These programs have identical length and identical incoming edges for
every job except `z`. Their true DAGs consist of two disjoint chains
and two or three isolated roots. Maximum true indegree and outdegree
are both one. The two inputs differ in exactly one hidden operand.

## 2. Exact optima and incompatible optimal first actions

**Theorem 1.** Both programs have optimum `M+2` cycles. Every optimal
schedule of `P_A` must issue jobs `0` and `3` in its first cycle. Every
optimal schedule of `P_B` must issue exactly `{0,1,2}` in its first
cycle. Hence no first action can have an optimal continuation on both.

**Lower bound and first-action necessity.** In `P_A`, the chain
`A_0,...,A_M,z` has `M+2` jobs. In any `M+2`-cycle schedule all of
them must occupy consecutive cycles starting at one. Thus `A_0=3`
issues in cycle one and `A_1=4` in cycle two. Admitting job 4 by cycle
two requires job 0 to have retired after cycle one. Consequently 0
also issues in cycle one.

Likewise, the chain `B_0,...,B_M,z` in `P_B` must begin with `B_0=2`
in cycle one and `B_1=5` in cycle two. Admission of job 5 requires
the first two jobs, 0 and 1, to have retired after cycle one. Width
three therefore forces the first action to be exactly `{0,1,2}`.
This does not contain job 3, so it cannot be optimal for `P_A`.
The reasoning covers idling and underfilled actions as well as
non-delay policies.

**Attaining schedules.** For `P_A`, use first action `{0,1,3}`, then
for `k=1,...,M` issue

`{B_(k-1),A_k}` in cycle `k+1`,

and in cycle `M+2` issue `{B_M,z}` together with the padding root
when `p=1`. For `P_B`, exchange the chain roles in these middle and
last actions: first `{0,1,2}`, then `{A_(k-1),B_k}`, and finally
`{A_M,z}` plus padding.

Here are the window checks. On the `A`-leading schedule, immediately
before middle cycle `k+1` the retired prefix is `2k` for `k=1`, and
`2k+1` for `k>=2`; both jobs in that cycle are within the next four
indices. Their sole predecessors issued earlier. After middle cycle
`M+1`, the only unfinished chain job is `B_M=2M+3`, so the retired
prefix is `2M+3`. The last job has index at most `2M+5`, and is
admitted. The final action has size at most three and its chosen
chain parent is complete.

On the `B`-leading schedule, the retired prefix before cycle two is
3, admitting jobs `A_0=3` and `B_1=5`. Before middle cycle `k+1`
for `k>=2`, it is `2k`, admitting `A_(k-1)=2k` and `B_k=2k+3`.
After middle cycle `M+1`, it is `2M+2`; job `z<=2M+5` is still in
the next four positions. Again both middle jobs and the final chosen
parent satisfy strict earlier-cycle dependencies. Padding is independent
and the final action has at most three jobs. These checks include `M=1`.
Thus both lower bounds are attained. ∎

The `A` program in fact has exactly three optimal possible first actions:
`{0,3}`, `{0,1,3}`, and `{0,2,3}`. Necessity was proved above. For
`{0,3}`, use `{1,2,A_1}` in cycle two; for `{0,2,3}`, use `{1,A_1}`.
Both reach the same clear prefix as the displayed `A`-leading schedule
after cycle two, so the same tail works. This precise statement is
useful when testing policies that are allowed to underissue.

## 3. Arbitrarily long lookahead still cannot ensure exact optimality

**Corollary 2.** For every integer `N>=7`, no first-action rule based
only on `N` and all incoming operands of the first `N-1` jobs can
guarantee an optimal continuation on every `N`-job program at `B=4,W=3`,
even when every true indegree and outdegree is at most one.

**Proof.** Let `M=floor((N-5)/2)>=1` and `p=N-(2M+5) in {0,1}`.
The two inputs above produce identical such observations and require
disjoint sets of optimal first actions. ∎

In particular, fix any integer extra-lookahead budget `L>=0`. Suppose
the initial observation consists of the incoming operands of jobs
`0,...,min(N,4+L)-1`. Choose any `N>=max(7,L+5)`. The last job is not
initially visible, so Corollary 2 applies. Even revealing the entire
remaining input immediately after the first action cannot repair a
first-action failure: the chosen critical chain has already lost a
cycle either at its root or at admission of its second job.

The quantifier is `for every fixed L, there exist indistinguishable
finite inputs`. The corollary does not restrict full-input offline
optimization, and it does not claim a constant multiplicative loss
bounded away from one as `L` tends to infinity.

## 4. Exact performance within the promised two-input family

For fixed `M,p`, suppose the input is promised to be one of `P_A,P_B`
and the last operand is hidden before the first action. Define `K=M+2`.
Every nonoptimal first action on either input needs at least `K+1`
cycles, because makespans are integral. The optimal first-action sets
are disjoint. Thus every deterministic policy loses at least one cycle
on one input, and under the uniform input distribution every randomized
policy has expected completion time at least `K+1/2` on average.
In particular some fixed input has expected time at least `K+1/2`;
no adaptive adversary is being used.

These lower bounds are attained within this two-input family. Pick
the `A`-leading or `B`-leading first action with equal probability and
continue along the corresponding displayed chain schedule. If the
hidden job selects the leading chain, finish in `K`. Otherwise issue
the lagging chain's last job and any padding in cycle `K`, then issue
`z` in cycle `K+1`. At each point this continuation can use observed
readiness, without knowing the last operand until it is revealed.

The exact family minimax ratios are therefore

`1+1/(M+2)` for deterministic policies,

`1+1/[2(M+2)]` for randomized policies against an oblivious input.

These are family-specific upper bounds and lower bounds for any larger
class containing these inputs, not global upper bounds for all DAGs.
One fixed advice bit identifying the hidden parent is both necessary
and sufficient for exact optimality on this promised family; this is
the elementary two-input counting argument, not a new advice technique.

## 5. Verification scope

`lookahead_boundary_check.py` generates both programs for `M=1,...,10`
and both padding values, checks every legal first action (including
the empty one) against an independently encoded completed-state solver,
and replays the two schedules. `LOOKAHEAD_BOUNDARY_CHECK.json` records
the actual run, source hash, Python version, and scope. The universal
statements above are supported by the written proof, not inferred
from that finite range. Independent review is recorded separately.

The saved Python 3.12.14 run passes all 40 programs, 600 legal
first-action checks (including empty actions), and 80 explicit
correct/wrong-leader schedule replays. It also verifies the indegree,
outdegree, all-but-last identity, exact optimal first-action sets,
and the uniform-prior expected lower bound. Runtime is 0.015497 seconds.
