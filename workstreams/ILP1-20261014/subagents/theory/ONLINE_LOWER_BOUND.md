# Hidden successor sets: exact online minimax family

Date: 14 October 2026. ILP1-20261014, theory subagent A.

Status: **WRITTEN_PROOF**, **NOVELTY_UNCONFIRMED**. This construction extends
the four-instruction indistinguishability pair first supplied during this
session by independent verification subagent C. It has not, at drafting,
been Lean-verified or checked against all online-scheduling literature.
The result is a lower bound for the precise observation model below and
an exact minimax calculation on an explicit family, not an assertion of
the global competitive ratio for arbitrary programs.

## 1. Observation model

Use the eager ROB model of `STRUCTURAL_RESULTS.md`. An online scheduler may
know `N,B,W`, the entire mathematical family of possible programs, its own
past choices, and all instructions and operands currently admitted to its
ROB. It cannot inspect operand identities of unadmitted future instructions,
nor receive information about future successor lists from another source.
All jobs have unit latency, one issue slot, no side effects and at most one
true data-dependence predecessor in the construction. Admission and retirement
are eager and unbounded apart from capacity `B`; results become ready only
in the following cycle.

This information restriction is essential. A scheduler supplied with the
complete outgoing edges of its current jobs would already know the hidden
set, and the indistinguishability proof would not apply.

The scheduler may randomize. For randomized statements the program is fixed
before observing the scheduler's random choices (an oblivious adversary).
Ratio means expected algorithmic makespan divided by the offline optimum.

## 2. Program family

Fix `q≥1`. Set

`N=4q`, `B=3q`, `W=2q`.

The first `3q` instructions are mutually independent roots. Divide them into

* `F={1,...,q}`, the prefix which must retire to admit the entire program;
* `U={q+1,...,3q}`, the set of `2q` possible hidden predecessors.

Choose any `q`-element subset `A⊆U`, and write its elements increasingly as
`a_1<...<a_q`. For `r=1,...,q`, instruction `3q+r` has the single true
predecessor `a_r`. Denote the resulting program by `P_A`. There are

`M=binomial(2q,q)`

possible programs. All have identical initially visible instructions,
resource parameters, instruction counts and maximum input arity. Only
the operand identities of the unadmitted suffix differ.

## 3. Unique first action of every two-cycle schedule

**Lemma 1.** Every `P_A` has offline optimum exactly 2. A complete schedule
of length 2 must issue exactly `F∪A` in its first cycle.

**Proof.** The work bound is `N/W=2`, so fewer than two cycles are impossible.
If the schedule finishes in two cycles, every suffix instruction must issue
in the second cycle, because none is initially admitted. For the last
instruction `4q` to be admitted by that cycle, the first `4q−B=q`
instructions must have retired after the first cycle; thus every member
of `F` issued in cycle 1. Every member of `A` must also issue in cycle 1
so that all suffix operands are ready. The disjoint union `F∪A` has
`2q=W` members, so it is the entire first issue action.

Conversely, issue `F∪A` in cycle 1. Prefix `F` then retires, opening at least
`q` ROB slots; eager filling admits all `q` suffix instructions for cycle 2.
Every suffix predecessor is complete. Exactly `q` initial roots and `q`
suffix jobs remain, so all issue together in cycle 2. This is a legal
two-cycle schedule. ∎

The lemma concerns the first *cycle*, not merely the first nonempty issue
action. An idle first cycle cannot finish by cycle 2, since all `4q` jobs
need two full-width cycles.

## 4. Deterministic lower bound

**Theorem 2.** For each `q≥1`, every deterministic online scheduler has some
`P_A` on which its makespan is at least 3, and hence its competitive ratio
is at least `3/2`.

**Proof.** The initially visible states of all `P_A` are identical, so the
scheduler's first-cycle issue action `S` is the same on all of them.
By Lemma 1, it permits a two-cycle completion for at most one choice of
`A`: this requires `S=F∪A`. Since `M≥2`, choose any other `A`. The makespan
is an integer and cannot be 2, so it is at least 3, while offline optimum
is 2. ∎

This is a fixed-program indistinguishability argument, not an online
adversary changing the program after seeing an individual execution.
For each deterministic algorithm, its fixed first action determines a
single adverse program that can be selected in advance.

## 5. Randomized lower bound and exact minimax value

**Theorem 3.** For every randomized online scheduler, some fixed `P_A`
satisfies

`E[T_online(P_A)] / T*(P_A) ≥ 3/2 − 1/(2 binomial(2q,q))`.

For the finite family `{P_A}`, this lower bound is attained by an explicit
randomized scheduler, so it is its exact minimax expected ratio. In
particular, as `q` varies, no universal randomized competitive ratio
strictly below `3/2` is possible in this observation model.

**Proof of the lower bound.** Temporarily draw `A` uniformly from its `M`
possible values, independently of all scheduler randomness. Fix any
realization of that randomness. The scheduler's first action is now fixed
and compatible with a two-cycle schedule for at most one `A` by Lemma 1.
Thus the probability of a two-cycle completion is at most `1/M`, whether
or not the scheduler actually completes in two cycles whenever it could.
Every other completion takes at least three cycles. The expected makespan,
averaged over `A` and the algorithm's randomness, is therefore at least
`2/M+3(1−1/M)=3−1/M`. At least one fixed `A` has expectation at least this
average. Divide by its offline optimum 2.

**Attaining scheduler.** Choose a uniformly random `q`-subset `A'⊆U`, and
issue `F∪A'` in cycle 1. All suffix jobs are then admitted. If `A'=A`,
Lemma 1's second cycle finishes in 2. Otherwise, in cycle 2 issue all
`q` initial roots not already completed, together with every suffix job
whose predecessor lies in `A'`. There are at most `q` such suffix jobs,
so the total issue count is at most `2q=W`. In cycle 3 issue the remaining
suffix jobs, all now ready. Since `A'≠A` and both sets have size `q`, some
suffix predecessor was absent from `A'`, so three cycles are necessary
and sufficient. Every fixed `A` is matched with probability exactly `1/M`,
giving expected makespan exactly `3−1/M`.

Finally, `binomial(2q,q)≥2^q`: partition the `2q` elements into `q` pairs
and choose one from each pair to obtain `2^q` distinct `q`-subsets.
Hence the correction term tends to zero, proving the global lower-bound
statement. This final statement supplies no matching global upper bound. ∎

For example, `q=1` recovers the four-job pair and expected ratio `5/4`.
At `q=2` the exact family minimax ratio is `17/12`; at `q=3` it is `59/40`.

## 6. Exact advice requirement for always attaining the offline optimum

Suppose a deterministic online scheduler receives a fixed-length binary
advice message before its first cycle. The advice may depend on the entire
program; all other observation restrictions remain in force.

**Corollary 4.** Attaining the offline optimum on every member of this family
requires and is achievable with

`ceil(log2 binomial(2q,q))`

advice bits.

**Proof.** If the message has `b` bits, it has at most `2^b` possible values.
For each fixed message, the initially observed state is identical across
the family, so the first action is fixed and can be optimal for at most
one `A`. Covering all `M` programs requires `2^b≥M`. Conversely, a message
encoding the index of `A` among the `M` possible subsets specifies the
unique first action `F∪A`, followed by Lemma 1's optimal second cycle. ∎

This is an exact advice count for this explicit family and a prescribed
fixed-length advice model. It is not a count for all instruction programs
or for variable-length, timing-dependent, or nondeterministic advice.

## 7. Exact resource dichotomy for universal deterministic optimality

The following general construction was proposed independently by the main
research agent and reviewed by subagent A. It covers every constrained
resource pair, whereas the binomial family above supplies stronger ratios
at selected resource pairs.

**Theorem 5.** Fix positive integers `B,W`. There is a deterministic online
scheduler attaining the offline optimum for **every** finite forward-DAG
program if and only if

`W=1` or `W≥B`.

For the negative direction it suffices to consider programs whose true
dependency graph consists of one directed path and isolated vertices;
every true indegree and outdegree is at most one.

**Proof of sufficiency.** At `W=1`, issue any ready job whenever unfinished
jobs remain. The oldest unfinished instruction is always ready, so there
are exactly `N` nonempty cycles, which is optimal by the work bound.
At `W≥B`, issue every currently ready instruction. Induction on the cycle
shows this is the earliest-level schedule of `H_B`: a job whose real and
artificial predecessors completed in earlier cycles is both admitted and
ready, by the schedule-equivalence theorem. Its makespan is therefore the
height of `H_B`, the exact optimum from Theorem 3 of the structural note.
Neither policy needs unseen instructions.

**Proof of necessity.** Suppose `B>W≥2` and put
`L=ceil((B−W)/(W−1))≥1`. Use `N=B+L` instructions. The first `B` are
independent roots. Choose a hidden index `x∈{2,...,B}`. The `L` suffix
instructions form a directed chain, with `x→(B+1)` as its first true edge.
The initially visible state is independent of `x`.

For every `x`, offline optimum equals `L+1`: the path consisting of `x`
followed by the `L` suffix jobs has that many vertices. An attaining
schedule issues any `W` roots in cycle 1 including `1` and `x`. In each of cycles
`2,...,L+1`, issue the next chain job, together with up to `W−1` smallest
unfinished initial roots. Before the `k`th chain job, instruction `B+k`,
the completed initial prefix has length at least
`min(B,1+(k−1)(W−1))`: this holds initially with `k=1`, and each subsequent
cycle completes the first `W−1` still-missing roots unless fewer remain.
Also `L≤B−W<B`, since
`W−1≥1` and the numerator is a positive integer. Therefore this prefix
length is at least `k` for all `1≤k≤L`, proving that job `B+k` is admitted.
Its dependency is complete from the previous cycle. The available root
slots total `W+L(W−1)≥B`, so every root has completed by cycle `L+1`.
The chain completes in that cycle as well, proving the claimed optimum.

Now take any deterministic online policy and inspect its fixed first
action `S` in the common initial state. If `1∉S`, the first suffix job
cannot be admitted for cycle 2, regardless of `x`. If `1∈S`, then
`|S|≤W<B` guarantees some `x∈{2,...,B}` is absent from `S`; fix that
program. Its first suffix job has an unavailable operand in cycle 2.
In either case the suffix chain starts no earlier than cycle 3 and
finishes no earlier than cycle `L+2`. The policy is not universally
optimal. ∎

This theorem is a yes/no characterization of **universal** optimality
over all programs at fixed resources. It does not say that all programs
incur an online loss when `B>W≥2`; many still have online-optimal policies.
The negative case gives the explicit ratio bound

`1 + 1/(1+ceil((B−W)/(W−1)))`.

In particular it gives `3/2` whenever `W<B≤2W−1`, using just `N=B+1`
instructions in that regime. It does not replace the stronger randomized
binomial-family statement above.

**Theorem 6 (exact chain-family minimax and advice).** Fix `B>W≥2` and the
single-hidden-root chain family just used, with
`L=ceil((B−W)/(W−1))`. Its exact deterministic minimax ratio is
`(L+2)/(L+1)`. Its exact randomized minimax expected ratio against fixed
programs is

`1 + (B−W)/((B−1)(L+1))`.

Attaining the offline optimum on every program with fixed-length advice
available before cycle 1 requires and is achievable with

`ceil(log2 ceil((B−1)/(W−1)))`

bits. Consequently, the universal optimality dichotomy of Theorem 5 also
holds for randomized schedulers when optimality is measured in expectation.

**Proof.** A first action can permit the optimal chain start in cycle 2
only if it contains both root 1 and the hidden root `x`. It therefore
covers at most `W−1` of the `B−1` possible hidden indices. Under a uniform
hidden index, the probability of an optimal-length completion is at most
`(W−1)/(B−1)`, for any fixed or randomized first action. Every failure
takes at least one extra cycle. Averaging, as in Theorem 3, proves the
randomized lower bound on some fixed input. Theorem 5 already proves the
deterministic lower bound.

To attain the bounds, first issue root 1 and any `W−1` additional roots
(chosen uniformly among such subsets for the randomized version). The
first suffix job is now admitted, revealing `x`. If `x` was issued,
the schedule in Theorem 5 finishes in `L+1`: explicitly, before its `k`th
chain job the completed initial prefix has length at least
`min(B,1+(k−1)(W−1))≥k`, because root 1 completed first and each intervening
cycle issues up to `W−1` smallest unfinished roots. This proves admission
even when the random first subset contains no other early prefix root.
Otherwise, use cycle 2 to
issue `x` and fill any remaining slots with the smallest unfinished
initial roots; then in cycles `3,...,L+2` issue the next chain job and
up to `W−1` smallest unfinished initial roots. The same prefix-growth
argument proves admission. Root throughput is more than sufficient,
since `W+L(W−1)≥B` already held even without the extra root-only cycle.
The dependency chain forces exactly `L+2` cycles in this missed case.
For each fixed hidden index the randomized choice hits it with probability
exactly `(W−1)/(B−1)`, proving equality of the expected bound; the
deterministic worst case misses some index and also attains its bound.

Each advice message fixes a first action covering at most `W−1` hidden
indices, so at least `ceil((B−1)/(W−1))` distinct messages are necessary.
Partition the possible indices into that many groups, each of size at
most `W−1`; advice identifies the group containing `x`. Issue root 1 and
all roots in that group, padding with other roots to width `W`, then
apply the optimal continuation just proved. This attains the message
count and hence its binary fixed-length encoding bound. Finally the
randomized loss displayed above is strictly positive for `B>W`, whereas
the positive cases of Theorem 5 are deterministic and therefore also
randomized policies. ∎

## 8. Classical global upper bound and an exact narrow-window ratio

The upper bound below is the unit-time specialization of Graham's classical
list-scheduling analysis, applied to the augmented DAG. It is included to
close a global lower/upper-bound pair in one ROB parameter regime, not as
a new approximation theorem. Primary bibliographic sources are R. L.
Graham, *Bounds for Certain Multiprocessing Anomalies*, Bell System
Technical Journal 45 (1966), 1563–1581,
[DOI](https://doi.org/10.1002/j.1538-7305.1966.tb01709.x), and its sequel
*Bounds on Multiprocessing Timing Anomalies* (1969),
[author-hosted scan](https://fanchung.ucsd.edu/ron/papers/69_02_multiprocessing.pdf).
The original theorem numbering is not asserted here; the specialized
argument is provided in full.

Call a policy non-delay if it issues `min(W,number of currently ready jobs)`
in every unfinished cycle, with any choice among ready jobs.

**Theorem 7 (classical list-scheduling bound in the ROB model).** For a
nonempty program and any non-delay policy, writing `h_B` for the height of
the augmented DAG,

`T_policy ≤ floor((N+(W−1)h_B)/W) ≤ (2−1/W)T*`.

The policy may be online and need not know the unseen true dependencies.

**Proof.** By the schedule-equivalence theorem, ready ROB jobs are exactly
unfinished jobs all of whose augmented-DAG predecessors have completed.
Thus the ROB policy produces an ordinary non-delay schedule of `H_B`.
Choose a job issued in its last cycle and repeatedly choose an incoming
predecessor issued latest, stopping at a source. Reverse this path to obtain
`v_1,...,v_ell`, with `ell≤h_B`, whose issue times strictly increase.

Before `v_1` issues, it is ready from cycle 1. Between the issue cycle of
`v_k` and that of `v_(k+1)`, every predecessor of `v_(k+1)` has already
completed by the end of `v_k`'s cycle, by the choice of latest predecessor. In every cycle
strictly between those two issue times the next path job is therefore ready
but not issued. Non-delay then forces that cycle to contain `W` jobs.
Every cycle without a path job is of one of these kinds, because the last
path job occurs in the final cycle. Consequently, the `T_policy−ell`
cycles without path jobs are full, while the `ell` path-job cycles each
contain at least one job. Therefore

`N≥W(T_policy−ell)+ell`.

Rearrange, use `ell≤h_B`, and use integer makespans to obtain the first
bound. Finally `N/W≤T*` and `h_B≤T*`; substituting those two lower bounds
gives `T_policy≤(2−1/W)T*`. ∎

**Corollary 8 (global deterministic minimax at `B=3,W=2`).** Over every
finite nonempty program in the stated observation model, the smallest
worst-case ratio achievable by any deterministic online scheduler is
exactly `3/2`. Every non-delay online scheduler attains this global upper
bound. The same equality holds if inputs are restricted to true dependency
graphs consisting of disjoint edges and isolated vertices.

**Proof.** Theorem 7 gives the `3/2` upper bound for all programs, and its
policies require only currently visible readiness. The `q=1` binomial
family has `B=3,W=2` and forces every deterministic policy to incur ratio
at least `3/2`, by Theorem 2. Those two examples already consist of one
true edge and isolated vertices. ∎

This exact ratio is an application of a classical upper bound plus the
model-specific indistinguishability pair. Historical novelty remains
unconfirmed. No matching global randomized ratio is proved: the family
lower bound at these fixed resources is `5/4`, while Theorem 7 supplies
the general `3/2` upper bound.

## 9. Research scope and follow-up

The binomial family uses extremely shallow true dependency graphs: disjoint edges
and isolated vertices, with true indegree and outdegree at most one.
The single-hidden-root family instead has a path of `L+1` vertices and
isolated roots, retaining true indegree and outdegree at most one. The
limited ROB observation, and the need to complete the prefix that opens
the window, produce the online obstruction. Offline optimality itself is
trivial for this family; its value is separating offline resource bounds
from what finite observation can guarantee.

Before any originality claim, compare this construction with hidden-successor
DAG scheduling, revelation models for precedence tasks, online scheduling
with bounded lookahead, and scheduling advice-complexity results. A theorem
for a stronger observation model could invalidate an overbroad claim even
when every proof above is correct for the stated model. Independent review
and actual Lean formalization remain separate requirements.
