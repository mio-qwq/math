# Hidden omission with only one extra ROB entry

Status: **WRITTEN_PROOF**, **NOVELTY_UNCONFIRMED**. This note follows
the sharp `B=3,W=2` randomized bound and asks whether its two-choice
structure extends to `B=W+1`. The first stronger normalization fails;
the resulting obstruction yields a larger family of information lower bounds.
Independent review and finite checks of the unified family are saved
in verification commit `71d0ba7509ac193ae4686f41d37dc1eefc636ea9`;
the family theorem is **INDEPENDENTLY_REVIEWED**. No Lean verification
is claimed here.

## 1. Refuted stronger normalization

Consider the statement: when `B=W+1`, there is always an optimal
non-delay schedule that, whenever every window entry is ready, includes
the oldest `W-1` entries in the next action.

**Counterexample.** Let `B=4,W=3,N=5`, with only true edges
`3->5` and `4->5` (one-based indices). Jobs `1,2,3,4` are initially
ready. The optimum is two, witnessed by

`{1,3,4}; {2,5}`.

Any first action including the oldest two jobs `1,2` can issue at most
one of `3,4`. Thus job `5` cannot issue before cycle three. The restricted
optimum is exactly three, for example

`{1,2,3}; {4}; {5}`.

This is minimum in program length for these resources. For `N<=4`, a
choice between different full-width actions exists only when all four
instructions are initially ready; then the whole program is independent,
and every three-plus-one schedule has optimum two. In all other states
there are at most three ready instructions, so non-delay fixes the action.
The valid theorem that only the *single* oldest instruction can always
be included is unaffected.

## 2. A parameterized family

Fix integers `W>=2` and `1<=m<=W-1`. Set

`B=W+1`, `N=B+m`, `F={1,...,m}`,
`C={m+1,...,W+1}`, and `c=|C|=W+1-m>=2`.

The first `B` instructions are roots. For each hidden parameter `x in C`,
partition the `W-m` roots of `C\{x}` among the `m` suffix instructions
`B+1,...,B+m`, and make the assigned roots exactly that instruction's
true predecessors. Each pool root is used once. Empty parts are allowed
and mean that the suffix instruction has no true predecessor; it may
still read an initial SSA input. There are no other edges.

If a maximum true indegree `d>=1` is required, a partition with every
part of size at most `d` exists whenever

`W-m <= dm`.

All true outdegrees are at most one, and every true dependency path has
at most two vertices. In particular, the family does not use a hidden
long critical chain. All programs have identical initial observations
under the declared model: the same `N,B,W` and the same `B` admitted roots.
Their differences occur only in unadmitted operand lists.

**Theorem 1.** Each member has offline optimum two. Its unique first
action permitting completion in two cycles is

`A_x = F union (C\{x}) = {1,...,B}\{x}`.

**Proof.** To finish in two cycles, the final suffix instruction `B+m`
must enter the ROB at the start of cycle two. That requires all of the
first `m` roots to retire at the end of cycle one. Thus all of `F` must
issue in the first action. Every root in `C\{x}` is a predecessor of
some suffix instruction, so all those roots must also issue in cycle one.
Their union has exactly `m+(W-m)=W` members and exhausts the issue width;
the first action is forced to equal `A_x`.

Conversely, issuing `A_x` completes the entire prefix `F`, admits all
suffix instructions next cycle, and satisfies all their true dependencies.
The remaining jobs are `x` and the `m` suffix instructions, at most
`m+1<=W` jobs; issue them together in cycle two. Since `N>W`, one cycle
is impossible. ∎

**Theorem 2.** Over this finite family, with the program chosen before
the policy's random bits are realized, the exact randomized online
minimax ratio is

`3/2 - 1/(2c) = 3/2 - 1/[2(W+1-m)]`.

The exact deterministic minimax ratio over the same family is `3/2`.

**Proof of lower bounds.** Before issuing, the policy's observation and
hence its first-action distribution are identical on all `c` inputs.
The required first actions `A_x` are pairwise distinct. Averaging
uniformly over `x`, the chance of selecting the required action is at
most `1/c`, even if the policy sometimes idles or uses fewer than `W`
slots. By Theorem 1, all other first actions require at least three
cycles. The average expected makespan is therefore at least
`2/c+3(1-1/c)=3-1/c`, and some fixed input achieves at least this value.
Divide by the common optimum two. For a deterministic policy, at least
one required first action is missed because `c>=2`, giving three cycles.

**Attaining policy on this family.** Choose `y` uniformly from `C`,
issue all initial roots except `y`, and thereafter issue all ready jobs.
The policy is given the promised family parameters (equivalently it can
recover `m=N-B` from the known total length). This is a family upper bound,
not an assumption that a general online policy sees unadmitted operands.
All of `F` completes in cycle one, so the entire suffix is admitted at
the start of cycle two. If `y=x`, completion occurs in two cycles. If
`y!=x`, the unexecuted root `y` is a predecessor of exactly one suffix
instruction. At cycle two issue `y` and every other suffix instruction;
all are ready, and their number is at most `m<=W`. The one blocked
child issues in cycle three. Thus every fixed input has expected time
exactly `3-1/c`. A fixed choice of `y` gives a deterministic policy with
worst-case time exactly three. ∎

This is an exact minimax calculation for the explicit family. The lower
bounds apply to the global program class containing the family. The
attaining policy above is not asserted to provide the same upper bound
on all programs with these resources.

## 3. Consequences for bounded-input instructions

Taking `m=ceil(W/(d+1))` is valid for every `W>=2,d>=1`; it lies in
`[1,W-1]` and satisfies the indegree condition. Therefore every randomized
online policy has global worst-case expected ratio at least

`3/2 - 1/[2(W+1-ceil(W/(d+1)))]`

on forward programs with true indegree at most `d` and outdegree at
most one, at resources `B=W+1`.

For the particularly simple choice `W=2q`, `B=2q+1`, `m=q`, `d=1`,
the true graph consists of exactly `q` disjoint edges and isolated roots.
The randomized lower bound becomes

`3/2 - 1/[2(q+1)]`,

which tends to `3/2` while the window exceeds issue width by only one.
Thus the `5/4` randomized ratio at `B=3,W=2` does not extend as a uniform
ratio to all capacities `B=W+1`, even for true disjoint-edge graphs.

At `W=3,B=4,m=1,d=2`, the three programs make their last instruction
depend on each possible pair from roots `2,3,4`. Their exact family
ratio is `4/3`; the first program-length counterexample above is one
member. This already separates width three from the proven width-two
global randomized value.

The model with `B<=W` still has a universally optimal policy issuing
every ready instruction. There is no contradiction: the present result
is a worst-case information cost after increasing the number of visible
unfinished entries past the number that can be issued at once. It does
not assert that an individual program's offline optimum worsens when
the window is enlarged.

## 4. Unified hidden-cover family

The main agent proposed the following extension after independently
reviewing the one-extra-entry construction. The theory subagent checked
the proof below. It includes both this note's family and the earlier
binomial family in `ONLINE_LOWER_BOUND.md`, so their information-counting
arguments are instances of one statement.

Fix integer parameters

`W>=2`, `1<=m<=W-1`, `W<B<=2W-m`, `d>=1`, and `W-m<=dm`.

Set `N=B+m`, let the first `B` instructions be roots, let
`F={1,...,m}` and `U={m+1,...,B}`, and put `r=W-m`.
For every hidden subset `A subset U` of size `r`, partition `A` into
`m` parts of size at most `d`. The `m` suffix instructions have these
parts as their true predecessor sets. As before, every root in `A`
is used once and empty parts are allowed. A fixed canonical partition
rule can be used so there is one program for each `A`. The number of
programs is

`M=binomial(B-m,W-m)`.

**Theorem 3.** In this family every program has optimum two and unique
two-cycle first action `F union A`. The exact deterministic family
minimax ratio is `3/2`, the exact randomized family minimax ratio is
`3/2-1/(2M)`, and the number of fixed-length advice bits sufficient and
necessary for an always-optimal deterministic family policy is
`ceil(log_2 M)`. Advice is supplied before the first action; the family
parameters are known to the policy.

**Proof.** To admit the last suffix instruction for cycle two, all of
`F` must finish in cycle one. To make every suffix dependency ready,
all of `A` must finish in cycle one. Their disjoint union has exactly
`m+r=W` jobs, forcing the first action. Conversely, this action leaves
`B-W` roots and all `m` suffix instructions for cycle two. Their number
is `B-W+m<=W`, so the required two-cycle schedule exists.

The initial observations are identical and the `M` required first
actions are distinct. Thus the same uniform-input argument gives
randomized expected time at least `3-1/M` on some fixed input, and
every deterministic policy misses a required first action on some
input. There are at least two inputs because `B>W` and `W-m>=1`.

For the matching upper bound within the family, guess `A'` uniformly
among the `M` possibilities, issue `F union A'`, and then issue every
ready instruction. All suffix instructions are admitted next cycle.
When `A'=A`, completion takes two cycles. When `A'!=A`, at least one
true parent is missing, so at least one suffix instruction is blocked.
All `B-W` remaining roots and every currently ready suffix instruction
fit into the second cycle, because even their upper bound
`B-W+m` is at most `W`. After this action, the blocked suffix
instructions are ready and number at most `m<=W-1`; issue them in
cycle three. Hence every wrong guess completes in exactly three cycles,
and every fixed input has expected time `3-1/M`. A fixed guess proves
the deterministic upper bound three.

Finally, two different inputs require different first actions under
identical observations. Any fixed-length advice scheme that always
selects the correct action needs at least `M` messages, or
`ceil(log_2 M)` bits. Encoding `A` uses exactly that many bits and
selects the optimal two-cycle schedule. This is the standard
distinguishability-counting argument, not a new advice-complexity method. ∎

The earlier binomial family is obtained by
`W=2q,B=3q,m=q,d=1`, giving `M=binomial(2q,q)`.
The single-omission family above is obtained by `B=W+1`, for which
`M=binomial(W+1-m,W-m)=W+1-m`.
The condition `B<=2W-m` is necessary for these two-cycle witnesses
simply because `N=B+m<=2W` is the width-two-cycle work bound.

These are family minimax equalities and global lower bounds. No global
upper bound for arbitrary `B=W+1,W>=3` programs follows from them.
