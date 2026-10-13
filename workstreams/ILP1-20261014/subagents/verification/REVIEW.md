# Independent mathematical review

Reviewer role: independent verification subagent C. Date: 2026-10-14 Singapore.
The reviewer wrote a time-assignment solver independently of the primary
completed-set dynamic program. The theoretical claims below originated in the
main/theory research work or emerged from explicit counterexample search.

## Scope and status

All jobs have unit latency, forward true dependencies, no same-cycle dependency
execution, and no control-flow or memory uncertainty. The ROB fills eagerly,
retires an unlimited completed prefix after each cycle, and retains blocked
completed jobs. Online observation includes the admitted prefix and history,
but no future operands, outgoing fanout information, or equivalent future hints.
The scheduler may know `N`, `B`, `W`, and the promised input family.

The reviewed conclusions have a written proof and independent mathematical
review in this model. The accompanying program checks are finite evidence.
No Lean verification, historical originality, publication acceptance, or real
processor performance is asserted by this review.

## Exact prefix-precedence characterization

For a completed schedule let `t_j` be the cycle in which job `j` executes.
Besides data precedences and the per-cycle width bound, ROB legality is exactly

`t_i < t_j` for every `i < j` with `j - i >= B`.

Necessity: to admit job `j` by its issue cycle, at least `j-B+1` jobs must already
have retired (zero-based indexing). Hence all jobs `0..j-B` completed strictly
earlier. Sufficiency: at the beginning of cycle `t_j`, those jobs are complete,
so retirement has advanced to at least `j-B+1`. Eager filling therefore admits
`j`; original predecessors are also complete. This applies simultaneously to
all jobs in each cycle, so the capacity bound completes a valid replay.

The strict inequality is essential: completion and retirement in the current
cycle only affect admission for the following cycle. Finite exhaustive replay
found no mismatch in 264,121 parameter/time-map cases.

Adding only the single edge `(j-B,j)` is insufficient. For `N=4,B=2,W=1`, no data
edges, the sequence `[[1],[3],[0],[2]]` satisfies edges `(0,2),(1,3)` but attempts
to issue unadmitted job `3` in the second cycle. Every prefix edge is needed
unless replaced by an actually equivalent transitive representation.

## Explicit local-policy counterexamples

Ties are always resolved by smaller program index. Critical path means longest
remaining path in the stated DAG. All examples have original indegree at most
two. Schedules below use zero-based job indices.

| Policy | N,B,W | Original edges | Policy schedule | Optimal schedule |
|---|---|---|---|---|
| Oldest ready | 4,3,2 | `(2,3)` | `[0,1];[2];[3]` | `[0,2];[1,3]` |
| Original-DAG critical path | 5,3,2 | `(1,3),(2,4),(3,4)` | `[1,2];[0];[3];[4]` | `[0,1];[2,3];[4]` |
| Augmented-DAG critical path | 6,6,2 | `(2,3),(0,4),(2,4),(1,5),(2,5)` | `[0,1];[2];[3,4];[5]` | `[0,2];[1,3];[4,5]` |

The first failure has the smallest `N` among searched forward DAGs; original
critical-path and augmented critical-path failures have the smallest `N` within
the exhaustively searched indegree-at-most-two class. These statements concern
the specified tie rule; they do not exclude every tie-breaking variant.

## Both saturation thresholds can decrease

For `N=4` with edges `(1,3),(2,3)`, exact times are:

| B \ W | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| 1 | 4 | 4 | 4 | 4 |
| 2 | 4 | 3 | 3 | 3 |
| 3 | 4 | 3 | 2 | 2 |
| 4 | 4 | 2 | 2 | 2 |

Thus `B_sat(P,W)` is `[1,4,3,3]` across widths, while `W_sat(P,B)` is
`[1,2,3,2]` across windows. Neither threshold inherits monotonicity from the
underlying duration function. This does not contradict that increasing either
resource cannot increase the optimum duration. All `N<4` forward DAGs were
checked, so four is the smallest size for these decreases.

The only nontrivial cell is `B=3,W=2`: a two-cycle schedule would have to issue
both parents `1,2` initially, leaving `0` incomplete and job `3` unadmitted in
cycle two. Three cycles suffice. At `B=4,W=2`, `[1,2];[0,3]` uses two cycles.
At `B=3,W=3`, `[0,1,2];[3]` uses two cycles. Other entries follow directly from
the unit-capacity lower bound or from these explicit dependencies.

## Online impossibility at every 1 < W < B

Take `N=2B`. The first `B` jobs are roots. The last `B` jobs form a chain whose
first job depends on hidden root `x`, where `1 <= x < B`. The visible initial
program is identical for all choices of `x`.

Every instance has optimum `B+1`: the root-to-suffix chain supplies a lower bound.
Issue `{0,x}` initially. In each following cycle issue the next chain job and,
while any initial root remains, the smallest unfinished initial root. Width two
suffices. Before the `k`-th suffix job must issue, the retired prefix has advanced
far enough to admit it; after all initial roots complete, the contiguous completed
chain prefix supplies the required retirements. This attains the lower bound.

Any schedule attaining `B+1` must issue both `0` and `x` initially. Otherwise the
first suffix job cannot both be admitted and have its operand ready in cycle one
(the second cycle), and the suffix chain then finishes no earlier than `B+2`.
A first action of size at most `W<B` either omits `0` or, when containing `0`,
omits at least one candidate `x`. Therefore no deterministic online policy is
optimal for every member of the family. The same argument rules out an
almost-surely always-optimal randomized policy because the required-action
intersection is empty. This is an existence impossibility, not a general exact
competitive ratio.

Boundary classification: for `W=1`, continuously executing one ready job gives
exactly `N` cycles, optimal by capacity. For `W>=B`, executing all ready window
jobs realizes the earliest-level schedule of the augmented precedence DAG and
is optimal by its critical-path lower bound. Consequently a universally optimal
online policy exists exactly in these two boundary resource regimes.

Independent finite check: all `3<=B<=8`, `2<=W<B`, all hidden parents and every
first action of size at most `W`; 112 programs and 11,036 action tests.

### Sharpening: a shorter chain and larger lower bound

The chain length can be reduced from `B` to

`L = ceil((B-W)/(W-1))`, with `N=B+L`.

For all `B>W>=2`, each instance then has optimum `L+1`. The dependency chain
including its hidden root has `L+1` vertices, proving the lower bound. To attain
it, issue `W` roots initially, containing the prefix `0..W-2` and hidden root
`x` (add another root if `x` already lies in that prefix). In each of the next
`L` cycles issue the next suffix job and up to `W-1` smallest unfinished roots.
The inequality `B <= W+L(W-1)` guarantees that all roots finish. Before suffix
job number `k` must execute, the completed initial prefix has length at least
`min(B,k(W-1))`. Because `k<=L<=B-W<=B-2`, this is at least `k`, exactly what
the ROB admission of index `B+k-1` requires. Dependence latency is one cycle.

As before, every common first action misses either `0` or some hidden `x`,
forcing the chain to start no earlier than the third cycle and giving duration
at least `L+2`. Thus every deterministic online policy at these resources has
competitive ratio at least

`1 + 1/(1+ceil((B-W)/(W-1)))`.

This recovers `3/2` throughout `W<B<=2W-1`. The result is a lower bound, not an
exact global competitive ratio. Its programs still have original indegree and
outdegree at most one. The shorter construction strictly strengthens the long
chain's ratio guarantee at many parameter pairs.

Independent finite check: all `3<=B<=10, 2<=W<B`, 240 programs and 75,352 first
actions including idle/underfull actions. The explicit schedule was replayed
for every program. All 60,506 first actions missing `0` or `x` were excluded
at horizon `L+1`. For every full first action the constrained optimum was
`L+1` when it contains `0,x`, and `L+2` otherwise. No counterexample to the
general proof was found.

## Binomial family: randomized loss and first-decision advice

Let `q>=1`, `N=4q`, `B=3q`, and `W=2q`. The initial `3q` jobs are roots. Choose
`A` to be a `q`-subset of `{q,...,3q-1}`. Each of the last `q` jobs depends on a
distinct root from `A`. There are `M=binom(2q,q)` indistinguishable initial inputs.

Each instance has optimum two, and its unique optimal first action is

`F_A = {0,...,q-1} union A`.

Indeed, all suffix jobs can only execute in cycle one. The last suffix job's
admission requires the first `q` roots completed initially, and suffix operand
availability requires all `A` completed initially. These are `2q` distinct jobs,
filling the entire first cycle. Conversely this action admits all suffix jobs
and satisfies every suffix dependency, so the second cycle executes the rest.

For any full first action, finish the remaining `q` initial roots in the second
cycle together with every admitted ready suffix job, then finish the remaining
suffix in the third cycle. This respects width `2q` and proves that every wrong
full first action has optimal continuation duration exactly three.

For a uniform fixed input `A`, independent of the scheduler's random bits, any
randomized first action matches `F_A` with probability at most `1/M`. Hence some
input has expected ratio at least `3/2 - 1/(2M)`. Choosing a uniform random
`F_A` and the three-cycle continuation attains this ratio for every family input.
This proves the exact minimax expected ratio **for this family only**; it tends
to `3/2` as `q` grows and supplies a lower bound for the larger problem class.

For deterministic guaranteed-optimal scheduling with a fixed-length advice
string available before the first decision, the advice must distinguish all `M`
different required first actions. The necessary and sufficient number of bits
is `ceil(log2 M)` when `q` and this family are known. This does not claim an
advice characterization for arbitrary programs or variable-length protocols.

Independent finite check: all `1<=q<=4`, all 98 programs, and 36,426 full first
actions; direct replay also checked the explicit continuation for every action.

## A corrected intermediate claim

For the simpler family `N=2W,B=W+1` with all `W-1` suffix jobs depending on the
same root `x`, the condition "first action contains `0` and `x`" is insufficient
when `W>=3`. To admit the entire suffix by the second cycle, the first action
must contain **all** roots `0..W-2` as well as `x`. Example `W=3,x=2`, first action
`{0,2,3}` leaves root `1` blocking admission of the last job. This was caught by
the independent assignment search and corrected before publication. Choosing
`x=W-1` versus `x=W` still gives a valid two-program indistinguishability pair.

## Not covered

The review does not prove root-register semantic translation, a machine-checked
algorithm correctness theorem, all details of any later Lean development, or
novelty. It does not cover finite retirement bandwidth, non-eager dispatch,
same-cycle dependence forwarding, multi-cycle instructions, branch prediction,
memory effects, bounded rename resources beyond the declared ROB, or a scheduler
that can inspect future outgoing dependencies. Existing scheduling theory may
already imply part or all of these results; literature review is separate.
