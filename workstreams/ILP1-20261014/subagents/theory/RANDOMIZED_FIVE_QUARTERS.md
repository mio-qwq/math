# A sharp randomized bound for a three-entry ROB

Authoring role: ILP1 theory subagent A. Status at this checkpoint:
**WRITTEN_PROOF**, **NOVELTY_UNCONFIRMED**. Independent review is in
the verification agent's commit
`8566370336bd87985b5a3296725c70b426450e3e`, which independently accepts
the arbitrary-size proof; thus this note is also
**INDEPENDENTLY_REVIEWED**. This file does not claim Lean verification. The preceding
finite experiment is supporting evidence, not the proof below.

## 1. Model, policy, and statement

Use the eager, unit-latency ROB model of `NARROW_WINDOW_POLICY.md`:
instructions have indices `1,...,N`, every true dependency points forward,
the window contains at most `B=3` entered but unretired instructions,
retirement is in program order with unlimited bandwidth at each cycle end,
and at most `W=2` instructions issue per cycle. Results are first usable in
the next cycle. An online policy sees admitted instructions and their
operands, but no unadmitted instructions or future successor lists.

Define policy **R** to issue the oldest unfinished instruction every cycle.
If all three window entries are unfinished and ready, it chooses one of
the two younger instructions uniformly, independently of previous choices.
In every other state it issues all ready instructions. The oldest
unfinished instruction is always ready in this model.

**Theorem 1.** For every finite forward-dependency program with `N`
instructions, let `F` be its offline optimal makespan and let `E` be the
expected makespan of R. Then

`4E <= N+3F <= 5F`.

Equivalently, the expected number of two-instruction cycles of R is at
least three quarters of the maximum possible number of such cycles.
For `N=0`, both makespans are zero. For every nonempty program,
`E/F <= 5/4`.

**Corollary 2.** Against an oblivious adversary choosing a complete
program in advance, the global randomized online minimax ratio at
`B=3,W=2` is exactly `5/4`.

The lower bound uses the established four-instruction pair with roots
`1,2,3` and sole edge `2->4` or `3->4`. Each program has optimum two.
Their unique first actions attaining two cycles are respectively
`{1,2}` and `{1,3}`. Their initial observations agree. Averaging over
these two fixed programs, any randomized online policy has probability
at most one half of finishing in two cycles, so its average expected
makespan is at least `5/2`. One of the programs therefore has expected
ratio at least `5/4`. This argument does not require an adversary that
observes the policy's realized random bits.

The upper bound concerns this ideal model. It makes no assertion about
multi-cycle execution, finite retirement bandwidth, real instruction
latencies, memory effects, or hardware implementation costs.

## 2. Clear-prefix values and their recurrence

A clear-prefix state at index `i` has exactly jobs `1,...,i-1` completed.
Let `F_i` be its optimal remaining makespan, `E_i` the expected remaining
makespan of R, and `n_i=max(0,N-i+1)` its number of unfinished jobs. Set
`F_i=E_i=n_i=0` for `i>N`.

The oldest-inclusive normalization theorem in
`NARROW_WINDOW_POLICY.md` proves that an optimal non-delay schedule
issuing the oldest job every cycle exists when `B=W+1`. Thus its scalar
recurrence applies here. We restate all cases needed in the proof.

At a nonempty clear-prefix state write
`a=i`, `b=i+1`, `c=i+2`, `d=i+3`, omitting jobs beyond `N`.
Job `b` is ready exactly when it exists and edge `a->b` is absent.
Job `c` is ready exactly when it exists and edges `a->c,b->c` are absent.

If only `a` is ready, the next clear-prefix state is `i+1` after one
cycle. If the only ready younger job is `b`, it is `i+2` after one cycle.
If the action is `{a,c}`, the following cycle issues `b`, together
with `d` exactly when `d` exists and edge `b->d` is absent. This returns
to clear-prefix state `i+ell` after two cycles, where

`ell=4` if `d` exists and `b->d` is absent, and `ell=3` otherwise.

When both younger jobs are ready, the two macro-actions are therefore

`(cost 1, target p=i+2)` and `(cost 2, target q=i+ell)`.

The optimal recurrence takes the minimum of their costs plus tail values;
R takes their arithmetic mean. When just one macro-action is available,
both values use that same macro-action. No further random choice occurs
inside the two-cycle macro-action: one entry is already completed there.

We also use the elementary monotonicity

`F_i-F_(i+1) in {0,1}` for every nonempty suffix.

For the lower inequality, completing an additional prefix instruction
cannot harm any continuation: simulate a schedule, omitting that already
completed instruction, and earlier retirement can only admit jobs sooner.
For the upper inequality, issue oldest `i` alone, then follow an optimal
continuation from `i+1`. Consequently `0<=F_p-F_q<=q-p` whenever `p<q`.

## 3. The joint invariant

Define the real-valued potential

`K_i = 3F_i+n_i-4E_i`.

We prove simultaneously by descending induction on `i`:

1. `K_i>=0` for every suffix, including empty suffixes.
2. If `i<=N` and `F_i=F_(i+1)`, then `K_i+K_(i+1)>=1`.

The nonempty restriction in the second statement is essential: two
empty suffixes both have zero value and zero potential. For `i=N`,
`F_i=E_i=1`, `n_i=1`, so `K_i=0`, and the second antecedent is false.
Empty suffixes provide the zero boundary values.

For a forced macro-action of length `ell` and cycle cost `a`, substitution
gives `K_i=3a+ell-4a+K_(i+ell)=ell-a+K_(i+ell)`.
The four possibilities `(ell,a)=(1,1),(2,1),(3,2),(4,2)` have respective
potential increments `0,1,1,2`.

At a state with both younger jobs ready, put
`x=F_p-F_q`, with targets `p=i+2`, `q=i+ell` as above. The one-step
monotonicity gives `x in {0,1}` for `ell=3` and `x in {0,1,2}` for
`ell=4`. Direct substitution of the minimum for `F_i` and the average
for `E_i` gives:

| Macro length `ell` | Tail difference `x` | `K_i` |
| --- | --- | --- |
| 3 | 0 | `(K_p+K_q)/2-1/2` |
| 3 | 1 | `(K_p+K_q)/2+1` |
| 4 | 0 or 2 | `(K_p+K_q)/2` |
| 4 | 1 | `(K_p+K_q)/2+3/2` |

### 3.1. Nonnegativity at the new index

Every forced case has a nonnegative increment. Every randomized case
except `ell=3,x=0` has a nonnegative increment. In that exceptional case,
`p` is a nonempty suffix and `q=p+1`, with `F_p=F_q`. The second induction
hypothesis gives `K_p+K_q>=1`, canceling the negative half. Thus `K_i>=0`.

### 3.2. The adjacent-equality invariant at the new index

Assume `i<=N` and `F_i=F_(i+1)`. A forced singleton `a` is impossible,
because it would give `F_i=1+F_(i+1)`. Every other forced case gives
`K_i>=1`. The randomized cases with `x=1` also give `K_i>=1`.
Together with tail nonnegativity, these cases prove the required sum.
Only the following three randomized cases remain. In them all of
`a,b,c` are present and ready; in particular the edges among these
three jobs are absent.

**Case `ell=3,x=0`.** Here `F_c=F_d`. Job `d` must exist: otherwise
`F_d=0` but the nonempty suffix beginning at `c` has positive value.
Therefore `ell=3` means edge `b->d` exists. At the clear-prefix state
beginning at `b`, the only ready younger job is `c`; the fixed action
is `{b,c}` and `K_b=1+K_d>=1`. Together with the already proved
`K_a>=0`, this establishes the desired sum.

**Case `ell=4,x=2`.** Here `F_c=F_d+1=F_e+2`, where `e=i+4`
denotes the next clear-prefix index (and could initially be beyond `N`).
If edge `c->d` were absent, issuing `{c,d}` from the clear-prefix
state `c` would give the feasible bound `F_c<=1+F_e`, a contradiction.
Thus `c->d` exists. At state `b`, edge `b->d` is absent by `ell=4`,
but `d` is blocked by `c->d`; only younger job `c` is ready.
Consequently `K_b=1+K_d>=1`. The already proved `K_a>=0` completes
the adjacent sum.

**Case `ell=4,x=0`.** Now `F_c=F_e`. If edge `c->d` exists, the
same fixed action at `b` gives `K_b>=1`, so suppose it is absent.
At state `c`, the macro-action issuing `{c,d}` costs `1+F_e`,
strictly exceeding `F_c=F_e`. The exact recurrence therefore forces
the alternative `{c,e}` to be ready and optimal. In particular, job
`e` exists, both edges `c->e,d->e` are absent, and its two-cycle
macro-action has some target `u in {e+1,e+2}` satisfying

`2+F_u=F_e`.

The one-step difference bound rules out `u=e+1`. Hence `u=e+2`,
and `F_e-F_(e+1)=F_(e+1)-F_(e+2)=1`.
Monotonicity and `F_c=F_e` also give `F_d=F_e`.

At state `b`, all of `b,c,d` are ready because `b->d` and `c->d`
are absent. Its second macro-action, beginning with `{b,d}`, also
issues `e` in its second cycle because `c->e` is absent. Its two
targets are consequently `d` and `e+1`, and their optimal-value
difference is

`F_d-F_(e+1)=F_e-F_(e+1)=1`.

This is the good randomized case `ell=4,x=1` at `b`, giving
`K_b>=3/2`. Again `K_a>=0` completes the sum. This exhausts the
cases and establishes both induction statements for every finite `N`.

## 4. Consequences and scope

At the initial state, `K_1>=0` is exactly `4E<=N+3F`.
The width-two work lower bound gives `N<=2F`, hence `4E<=5F`.
Every non-delay width-two schedule has `T=N-M`, where `M` is its
number of two-instruction cycles. Substitution gives
`E[M_R]>=3(N-F)/4`, the stated pairing guarantee.

The four-job indistinguishability pair supplies equality: each member
has `N=4,F=2`, while R has `E=5/2`. The proof establishes a global
guarantee over arbitrary program lengths and all forward dependency
graphs under the model. It does not rely on the finite exhaustive
experiment, on an independence assumption between different macro-states,
or on the program belonging to the lower-bound family.

The linear-combination potential and adjacent-equality invariant above
are the actual arbitrary-size proof obligations. No novelty is claimed
for generic dynamic programming, matching reformulations, or the
two-input graph reduction; relevant precedence-scheduling and randomized
matching literature remains under review.
