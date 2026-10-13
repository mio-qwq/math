# Independent review: a sharp randomized bound at B=3, W=2

Reviewing role: verification subagent C, 2026-10-13 UTC. The theory subagent
proposed the potential and supplied `RANDOMIZED_FIVE_QUARTERS.md`. This review
independently reconstructs its general argument, checks its fragile local
implications, and tests the new invariants with independently computed values.
It does not claim novelty or Lean verification.

**Verdict:** the written proof is accepted under the precise eager ROB semantics.
For a fixed finite forward DAG, the oldest-inclusive policy which chooses each
younger instruction with probability one half when all three entries are ready
satisfies

`4 E[T] <= N + 3 T* <= 5 T*`.

Together with the previously reviewed four-job indistinguishability pair, this
establishes the global randomized online ratio `5/4` against an **oblivious**
adversary selecting a complete program in advance. An adversary adapting the
future program to the realized random choices is outside this conclusion.

## 1. Dependencies of the argument

Use zero-based job indices. Let `F_i` be the optimum for the clear-prefix state
where all jobs before `i`, and no later jobs, are complete. Let `E_i` be this
policy's expected remaining time, and let `n_i=max(0,N-i)`. All three quantities
are zero at indices at least `N`.

The proof uses the separately reviewed oldest-inclusive normalization theorem
at `B=W+1`. Its exact `B=3,W=2` recurrence is as follows. At a nonempty suffix,
write `a=i,b=i+1,c=i+2,d=i+3`. A one-cycle action `{a,b}` reaches suffix `i+2`.
An action `{a,c}` has a forced second cycle: issue `b`, also issuing `d` if it
exists and the edge `b -> d` is absent. It reaches `i+ell` in two cycles, with
`ell=4` in that case and `ell=3` otherwise. If only one younger job is ready,
the corresponding macro is forced; if neither is ready, issue `a` alone.
If both are ready, `F_i` is the minimum of these two macro costs and `E_i` is
their average. The second cycle of the latter macro contains an already
completed entry, so there is no hidden additional random choice.

For each nonempty suffix,

`0 <= F_i - F_(i+1) <= 1`.

For the lower inequality, restrict a feasible issue-time assignment to the
remaining suffix. All true and artificial ROB precedences among remaining
jobs are preserved, as is capacity. For the upper inequality, issue `i` alone
and then follow an optimal suffix schedule. The values are integers.

The inference to the original ROB model depends on the previously reviewed
time-assignment/operational equivalence. It would not automatically survive
finite retirement bandwidth or different same-cycle forwarding semantics.

## 2. A joint invariant that closes

Set `K_i=3F_i+n_i-4E_i`. Strong descending induction proves:

1. `K_i >= 0`, including the empty boundary.
2. For `i<N`, if `F_i=F_(i+1)`, then `K_i+K_(i+1) >= 1`.

The nonempty condition in item 2 is essential. Two empty tails have equal
values and zero potentials, so extending item 2 to them would be false.

A forced macro of length `ell` and cost `t` gives
`K_i=ell-t+K_(i+ell)`. The possibilities `(ell,t)` are `(1,1)`, `(2,1)`,
`(3,2)`, and `(4,2)`, so the increments are `0,1,1,2` respectively.

For a two-choice state, put `p=i+2`, `q=i+ell`, and `x=F_p-F_q`.
The following identities result by substitution, not by an approximation:

| Length ell | Difference x | K_i minus (K_p+K_q)/2 |
| --- | --- | --- |
| 3 | 0 | -1/2 |
| 3 | 1 | 1 |
| 4 | 0 or 2 | 0 |
| 4 | 1 | 3/2 |

Monotonicity excludes every other `x`. To prove item 1 at `i`, only the
`ell=3,x=0` row needs more than tail nonnegativity. There `q=p+1`, `p` is
nonempty, and the two tail values agree. Item 2 at `p` supplies a tail
potential sum of at least one, exactly canceling the negative half.

For item 2 at `i`, a forced singleton is impossible under its antecedent:
it has `F_i=1+F_(i+1)`. Every other forced macro gives `K_i>=1`.
Every random row with `x=1` also gives `K_i>=1`. For the other rows,
the following local facts show `K_(i+1)>=1`. Item 1 at `i` was already
established, so these facts suffice without circular induction.

**Length three, difference zero.** Job `d` must exist because `F_c=F_d`
and `c` is nonempty. Thus the edge `b -> d` is present. At suffix `b`,
only younger job `c` is ready, forcing `{b,c}` and giving
`K_b=1+K_d>=1`.

**Length four, difference two.** Job `d` exists. If `c -> d` were absent,
one could issue `{c,d}` from suffix `c`, proving `F_c<=1+F_(i+4)`.
This contradicts the assumed difference two. Hence that edge is present,
and again the suffix at `b` forces `{b,c}`, giving `K_b>=1`.

**Length four, difference zero.** Write `e=i+4`. If `c -> d` is present,
the preceding forced-pair argument applies. Suppose it is absent. Since
`F_c=F_e`, the `{c,d}` branch of cost `1+F_e` cannot be optimal. The exact
recurrence then forces the alternative `{c,e}` to exist, be ready, and
have optimal cost `2+F_u=F_e` for a target `u` in `{e+1,e+2}`. In
particular, `c -> e` and `d -> e` are absent. The adjacent-value bound
rules out `u=e+1`. Therefore `u=e+2`, with

`F_e-F_(e+1)=F_(e+1)-F_(e+2)=1`.

Also `F_d=F_e` by monotonicity between `c` and `e`. At suffix `b`, all
three jobs `b,c,d` are ready. Its second macro starts with `{b,d}` and
also issues `e` next cycle because `c -> e` is absent. Thus its targets
are `d` and `e+1`, whose values differ by exactly one. The good
length-four row applies at `b` and gives `K_b>=3/2`.

This exhausts all cases. All induction hypotheses used have larger
indices. The smallest nonempty suffix has `K=0` and unequal adjacent
values, so the base case is valid. The arbitrary-size induction is
independent of the finite tests below.

## 3. Sharpness and quantifiers

At `i=0`, item 1 states `4E_0<=N+3F_0`. The width-two work bound
`N<=2F_0` gives `E_0<=5F_0/4`. For a nonempty program, division by
`F_0>0` is justified. For the empty program the unnormalized inequality
still holds, while an IPC or ratio is not being assigned.

The four-job pair has either sole edge `1 -> 3` or sole edge `2 -> 3`,
using zero-based indices. Both optima equal two, and their visible
first three jobs are identical. Their only optimal first actions are
`{0,1}` and `{0,2}` respectively. For any randomized online first
action, the probabilities of these two distinct actions sum to at most
one. On at least one fixed input, the probability of failing to finish
in two cycles is at least one half; every such run costs at least three.
Its expected makespan is at least `5/2`. This lower bound allows arbitrary
randomized first subsets, including underfull or empty actions.

The stated policy attains `5/2` on each input. The proof applies to all
finite forward DAGs under the model, not merely to this pair, a bounded
number of jobs, or indegree-two inputs. It is a bound from the initial
empty processor (and from clear-prefix states), not a claim that the
same suffix potential handles arbitrary partly completed windows.

## 4. Independent finite checks

`randomized_bound_audit.py` computes every suffix optimum with the independent
time-variable CSP. Expected policy costs come from a direct ROB completed-set
recursion; it does not call the scalar recurrence or any theory/root solver.
Only after those independent values are available does the audit test the
scalar identities, joint invariants, and every delicate local implication.

The real run checked all 683 nonempty effective graphs through `N=6`, plus
the empty graph. It checked 3,869 nonempty suffix occurrences and 1,232
adjacent equal-value cases. Every proof classification occurs, including
the difficult length-four, difference-zero case without edge `c -> d`.
There are 684 distinct CSP inputs after cache deduplication. All assertions
passed, and the maximum observed expected ratio is exactly `5/4`.

The smallest difficult-case witness found is `N=6`, with sole edge `4 -> 5`.
At the initial state its suffix optimum vector is `[3,3,2,2,2,1,0]` and
its expected value is `15/4`. The exact output, local witnesses, runtime,
Python version, and source hashes are in `randomized_bound_results.json`.
These finite results check the semantics and arithmetic; they are not a
substitute for the general proof in section 2.

Status: **WRITTEN_PROOF**, **INDEPENDENTLY_REVIEWED**;
**NOVELTY_UNCONFIRMED**; **not LEAN_VERIFIED by this subagent**.
