# ROB windows as precedence constraints

Research date: 14 October 2026 (Asia/Singapore). Subagent A, ILP1-20261014.
Baseline: `bf732c32f1b8cef32ebf69cac6fb232a8a5323a3`.

Status of the statements below: **WRITTEN_PROOF**. Historical novelty is
**NOVELTY_UNCONFIRMED**. This note does not claim Lean verification, independent
review, or publication priority. Standard finite-DAG scheduling arguments are
used explicitly; they are not claimed as new results.

## 1. Exact model and schedule convention

Let the program be the ordered set `[N]={1,...,N}` with a set of true dependence
edges `E ⊆ {(i,j):1≤i<j≤N}`. Assume `B,W≥1`. Each instruction has latency one,
can issue at most once, and consumes one of at most `W` issue slots in its cycle.
Results of cycle `c` are available in cycle `c+1`. All operands of a dependence
edge must therefore be produced in strictly earlier cycles. The ROB eagerly
contains the first at most `B` admitted-but-not-retired instructions; admission
is in program order, retirement is in program order and unbounded in bandwidth,
and a completed instruction continues occupying its ROB slot until retirement.
The ROB is filled initially and after each cycle's retirements. No separate
dispatch width, issue latency, or retirement latency is imposed.

A schedule is a map `t:[N]→{1,2,...}`; instruction `j` issues in cycle `t_j`.
Idling is permitted. Its makespan is `max_j t_j`, with makespan zero for `N=0`.
This convention counts issue/completion cycles, and does not append an extra
cycle for observing the final outputs.

Define the augmented DAG

`H_B=( [N], E ∪ F_B )`, where `F_B={(i,j): j−i≥B}`.

In particular **all** earlier indices `i≤j−B` are predecessors of `j`; adding
only the single edge `(j−B,j)` is generally insufficient.

## 2. Schedule equivalence theorem

**Theorem 1.** A schedule `t` can be replayed on this ROB model if and only if

1. `|{j:t_j=c}|≤W` for every cycle `c`;
2. `t_i<t_j` whenever `(i,j)∈E`;
3. `t_i<t_j` whenever `j−i≥B`.

Consequently, the exact ROB optimum equals the usual makespan optimum for
unit-time precedence-constrained tasks on `W` identical issue slots with
precedence DAG `H_B`.

**Proof of necessity.** Items 1 and 2 are issue and data-availability rules.
Before instruction `j>B` can be admitted, at least `j−B` earlier instructions
must have retired: otherwise at least `B+1` admitted instructions, from the
oldest unretired index through `j`, would occupy the ROB. Retirement is in
order, so all of `1,...,j−B` have completed. Since admission for cycle `t_j`
occurs before that cycle issues, they issued in cycles strictly less than
`t_j`. This is item 3. It remains true if `j` was admitted earlier than it
eventually issued.

**Proof of sufficiency.** Replay the instructions assigned to each cycle.
Induct on the cycle number. Suppose all assignments to earlier cycles have
been executed and the ROB has retired the longest completed prefix and filled
again. Let `r` be the length of that prefix. For any instruction `j` assigned
to the current cycle `c`, item 3 says that all indices at most `j−B` have
already completed. Hence `r≥j−B` when `j>B`, and trivially `j≤r+B` when `j≤B`.
Instruction `j` has not completed, so `j>r`. Eager filling therefore puts it in
the current ROB interval `r+1,...,min(N,r+B)`. Item 2 makes it ready; item 1
allows all such instructions to issue together. No two of them are in a
precedence relation because all edge inequalities are strict. The next cycle
continues the induction. Once the last issue cycle completes, every
instruction has completed and all retire. ∎

**Boundary cases.** `B≥N` adds no edges. `B=1` adds the full forward order, so
`T*=N`. `W=1` also gives `T*=N`: the in-order schedule is feasible and the work
bound gives the reverse inequality. `W>B` is equivalent to `W=B` (Theorem 3).
For `N=0`, the empty schedule is feasible with makespan zero; IPC is left
undefined. Negative or zero resource parameters are outside this model.

**Why the single-edge replacement fails.** Take `N=4,B=2,W=2`, no true
dependencies, and
`(t_1,t_2,t_3,t_4)=(2,1,3,2)`. It satisfies `1→3` and `2→4`, but instruction 4
cannot be admitted in cycle 2: instruction 1 has not retired before that
cycle. The missing constraint is `1→4`.

## 3. The exact resource demand of one schedule

For a nonempty schedule satisfying the true data dependencies, define

`b(t)=max {j−i+1 : 1≤i≤j≤N and t_i≥t_j}`

and `w(t)=max_c |{j:t_j=c}|`. The diagonal `i=j` ensures `b(t)≥1`.

**Theorem 2.** Such a schedule is feasible for resources `(B,W)` if and only
if `B≥b(t)` and `W≥w(t)`.

**Proof.** Item 3 of Theorem 1 is equivalently: every pair with `t_i≥t_j` and
`i<j` must have `j−i<B`, that is, `j−i+1≤B`. Taking the maximum and including
diagonal pairs proves the window condition. The issue condition is exactly
the definition of `w(t)`. ∎

Thus `b(t)` is a checkable exact certificate of the window needed by a fixed
schedule. Let `K=T*(P,N,W)` and let `S_K` be the width-`W`, true-dependence
schedules of makespan `K`. After deleting empty cycles, `S_K` is a finite
nonempty set. Then

`B_sat(P,W)=min_{t∈S_K} b(t)`.

This equality is a useful structural schedule certificate, **not** by itself
a polynomial algorithm for finite `W`. The schedule-specific pair `(b(t),w(t))`
also parametrizes the resource pairs feasible at a prescribed makespan:
`T*(P,B,W)≤K` iff some true-dependence schedule with makespan at most `K` has
`b(t)≤B` and `w(t)≤W`.

The earliest-time schedule for `E` alone need not minimize `b(t)` among
height-optimal schedules. For `N=3,E={1→2}`, it is `(1,2,1)`, with footprint 3.
But `(1,2,2)` has the same optimal makespan 2 and footprint 2, so the true
unlimited-width saturation window is 2.

## 4. Unlimited width: a linear-time exact recurrence

Let `p_0=0`. In program order compute

`e_j=1+max( {e_i:(i,j)∈E} ∪ {p_(j−B) if j>B} ∪ {0} )`,

`p_j=max(p_(j−1),e_j)`.

**Theorem 3.** Every antichain in `H_B` is contained in an interval of at most
`B` consecutive program positions. The labels `e_j` are the earliest legal
issue times in `H_B`. With `h_B=max_j e_j`,

`T*(P,B,W)=h_B` for every `W≥B`.

The recurrence takes `O(N+|E|)` time and `O(N)` space, assuming the incoming
true edges are supplied. It never materializes the potentially quadratic
set `F_B`.

**Proof.** If an antichain has smallest index `a` and largest index `z`, then
`z−a<B`; otherwise the artificial edge `a→z` contradicts incomparability.
Every edge of `H_B` points forward, so the standard earliest-time/longest-path
induction applies. The artificial predecessors of `j` have maximum level
`p_(j−B)` when nonempty, which proves the recurrence. Inductively, every
feasible `t` satisfies `t_j≥e_j`; thus `h_B` is a lower bound. Conversely,
the level sets of `e` are antichains and have at most `B` vertices, so `e`
is feasible when `W≥B`. Computing incoming-edge maxima and prefix maxima
has the stated cost. ∎

For arbitrary `W`, this gives the explicit lower bound

`T* ≥ max(h_B, ceil(N/min(B,W)))`.

Neither using the height of `E` nor even replacing it by `h_B` makes the
work/height lower bound universally attainable; see Theorem 7 below.

**Critical-path certificates.** Along with each maximum in the recurrence,
store an attaining predecessor (either a real edge or the index attaining
the prefix maximum). Backtracking from a maximum-level vertex produces a
chain of length `h_B`, every step independently verifiable as a real edge
or as an index gap at least `B`. The levels `e` give a feasible matching
upper certificate when `W≥B`. These are succinct optimality certificates,
requiring no enumeration of schedules.

## 5. Polynomial exact saturation with unrestricted issue width

Assume `N≥1`. Let `H` be the height of the true-dependence DAG `E`, and fix
`W≥N`. The unrestricted-window optimum is `H`.

**Theorem 4.** `B_sat(P,W)` is exactly the least `B∈{1,...,N}` such that the
recurrence of Theorem 3 yields `h_B=H`. It can be computed by binary search
in `O((N+|E|) log N)` time. For a returned value `b>1`, an independently
checkable exact certificate consists of:

* the `H`-cycle earliest schedule for `H_b`;
* a chain of at least `H+1` vertices in `H_(b−1)`.

For `b=1`, the first item and the allowed resource range certify minimality.

**Proof.** Theorem 3 applies for every candidate `B≤N≤W`. As `B` grows,
`F_B` only loses edges, so `h_B` is nonincreasing and never below `H`.
At `B=N` it equals `H`. Binary search on this monotone predicate is exact.
If `b>1`, minimality implies `h_(b−1)>H`, so its longest path supplies the
second certificate. The second certificate excludes every smaller `B`
by edge containment. ∎

There is also an exact graph-only bottleneck formula. For every increasing
sequence `v_0<...<v_H` of `H+1` vertices, define

`d(v)=min {v_(q+1)−v_q : (v_q,v_(q+1))∉E}`.

This minimum is nonempty: otherwise `E` itself would have a chain of `H+1`
vertices. When no sequence of `H+1` vertices exists, define the maximum over
sequences to be zero.

**Theorem 5.** `B_sat(P,W)=1+max_v d(v)` for `W≥N`.

**Proof.** A given increasing sequence of `H+1` vertices is a path in `H_B`
exactly when every consecutive non-`E` pair has index gap at least `B`,
equivalently `B≤d(v)`. A path of at least `H+1` vertices contains such a
sequence by taking its first `H+1` vertices. Therefore `h_B>H` iff some
`v` has `d(v)≥B`. The least integer excluding all such sequences is the
displayed formula. If `H=N`, no sequence exists and the formula gives 1,
as it should. ∎

This bottleneck formula is an exact structural characterization of one
saturation regime. The recurrence/binary-search algorithm is preferred
over explicitly enumerating the sequences in the formula.

## 6. Exact fixed-window state-space bound

Call `D` the set of instructions completed before the current issue cycle,
and let `r` be the length of its largest complete initial prefix. The
terminal state has `r=N`. Otherwise `r+1∉D`.

**Theorem 6.** Every reachable nonterminal completed set has the unique form

`D={1,...,r} ∪ S`, where `S⊆{r+2,...,min(N,r+B)}`.

There are at most

`1 + sum_(r=0)^(N−1) 2^min(B−1,N−r−1) ≤ 1+N·2^(B−1)`

such states. An exact dynamic program over them is fixed-parameter tractable
in `B`, with `O(poly(B)·N·3^B+|E|)` time and
`O(poly(B)·N·2^B+|E|)` space; the polynomial factors account for explicit
bit operations and preprocessing.

**Proof.** Completed sets are ideals of `H_B`. If a completed index
`j>r+B` existed, the edge `(r+1)→j` would force `r+1` to be completed,
a contradiction. Uniqueness follows from the definition of `r` and `S`.
This proves the state count (which may overcount dependency-inconsistent
masks).

At a state, issue any nonempty subset `A` of at most `W` ready unfinished
instructions in `r+1,...,min(N,r+B)`. Normalizing `D∪A` to its new longest
completed prefix gives the successor. Instruction `r+1` is always ready:
all true predecessors have smaller indices and lie in the completed prefix.
Thus a nonterminal state has a successor. Every successor completes more
instructions, so this state graph is acyclic. The recurrence
`V(D)=1+min_A V(D∪A)` with `V([N])=0` consequently computes exactly the
minimum remaining makespan, by induction on the number of unfinished jobs.
Theorem 1 makes both soundness and completeness of its transitions explicit.

For one fixed `r` and a window of length `b≤B`, position `r+1` is unfinished,
whereas each of the remaining `b−1` positions has three possibilities when
counting state/action pairs: already completed, chosen now, or not chosen.
The first position has two possibilities (chosen/not chosen). Hence at most
`2·3^(b−1)` candidate state/action pairs occur for that `r`, before pruning
empty, too-wide, or nonready choices. Checking masks and normalizing adds
polynomial factors in `B`. True predecessors at index at most `j−B` are
already retired whenever `j` is in the ROB. All other relevant predecessors
are in a range of fewer than `B` indices and can be stored as local masks,
with linear processing of the supplied edges. These observations prove
the claimed bounds. ∎

**Non-delay dominance.** There exists an optimal schedule issuing exactly
`min(W,number of ready instructions)` each nonterminal cycle. To see this,
move a ready job into an unused issue slot of an earlier cycle. Its
predecessors have already completed, its successors originally issued after
its later execution and remain valid, and all other precedence inequalities
are preserved. This does not increase the makespan. Repeating cycle by
cycle terminates and yields the claim. Theorem 1 translates this ordinary
precedence-scheduling exchange directly to ROB admission. It does **not**
imply that an arbitrary choice of ready jobs is optimal.

## 7. Exact special class and an unbounded additive lower-bound gap

**Theorem 7 (two-input barrier family).** For each integer `m≥1`, take
`N=3m`, `B=3`, and write each consecutive block as `(a_k,b_k,c_k)`,
where `a_k=3k+1,b_k=3k+2,c_k=3k+3`, `0≤k<m`. The only true edges are,
for `k≥1`,

`b_(k−1)→a_k`, `c_(k−1)→a_k`, and `c_(k−1)→b_k`.

Every instruction has at most two true inputs. The augmented poset `H_3`
is exactly the ordinal sum of `m` antichains of size three. Therefore

`T*(P_m,3,W)=m·ceil(3/min(W,3))`.

In particular, at `W=2`, `T*=2m`, whereas the combined augmented-height
and work bound is only `ceil(3m/2)`. The additive gap grows without bound;
for even `m`, the ratio is exactly `4/3`.

**Proof.** There are no true or artificial edges within a block. Between
two consecutive blocks, the first current instruction has the first
previous instruction as artificial predecessor and the other two as true
predecessors; the second current instruction has the first two previous
instructions as artificial predecessors and the last as true predecessor;
the third current instruction has all three as artificial predecessors.
Thus every previous-block instruction precedes every current-block
instruction. Transitivity gives the same conclusion for nonconsecutive
blocks. All edges point to later blocks, so there is no further within-block
comparison. Each block must finish before the next starts, requires at least
`ceil(3/min(W,3))` cycles, and can be processed in exactly that number.
Summing proves the formula. The height is `m` and the total work is `3m`. ∎

This family proves that even a stronger ROB-aware longest-path bound and
the total work bound fail to characterize optimality for two-input programs.
It does not prove a new approximation lower bound against any named
scheduling algorithm, nor a hardness result.

**Theorem 8 (complete solution for `B=2`).** For any forward dependence DAG,
form a path on `[N]` whose edge `{i,i+1}` is allowed exactly when
`(i,i+1)∉E`. Let `ν` be the maximum matching size in this allowed-edge path.
Then, for `W≥2`,

`T*(P,2,W)=N−ν`.

A maximum matching is obtained greedily by selecting the first allowed
edge, deleting its two endpoints, and continuing. Issuing each matched
adjacent pair together and every unmatched job alone, in program order,
is optimal. The full problem is therefore solvable in `O(N+|E|)` time.

**Proof.** By Theorem 3, any cycle has at most two jobs. If it has two,
their indices must be consecutive; they cannot have a true edge between
them. All double-job cycles therefore constitute a matching in the allowed
path. If their number is `d`, at least `N−d≥N−ν` nonempty cycles are needed.
Conversely, the proposed matching-block schedule respects every forward
edge except potentially an edge internal to a matched pair, and those are
excluded by construction. A dependence path between adjacent indices can
only be their direct edge, because no intermediate index exists. The
matching-block schedule is thus feasible and attains `N−ν` cycles.
For the greedy rule, if the earliest allowed edge has endpoints `i,i+1`,
a maximum matching can be chosen to include it: if its endpoints are
unmatched, add it; otherwise the only possible conflict after all earlier
vertices have been removed is `(i+1,i+2)`, which can be replaced by `(i,i+1)`
without decreasing the matching size. Induct on the remaining suffix. ∎

## 8. Saturation thresholds are not monotone

An independently proposed counterexample from verification subagent C is
`N=4,E={2→4,3→4}` (one-based indices). Its exact makespan table is

| ROB capacity / issue width | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: |
| 1 | 4 | 4 | 4 | 4 |
| 2 | 4 | 3 | 3 | 3 |
| 3 | 4 | 3 | 2 | 2 |
| 4 | 4 | 2 | 2 | 2 |

**Proposition 9.** This table is correct. Consequently, `B_sat(P,W)` for
`W=1,2,3,4` equals `1,4,3,3`, and `W_sat(P,B)` for `B=1,2,3,4` equals
`1,2,3,2`. Neither saturation threshold is necessarily nondecreasing in
the other resource, although the makespan itself is nonincreasing in both.

**Proof.** The row/column with resource one requires four cycles. At `B=2`,
the augmented graph has the chain `1→3→4`, so at least three cycles are
needed; `(1,2) | 3 | 4` attains three when `W≥2`. At `B=3,W=2`, a two-cycle
schedule would need instructions 2 and 3 in the first cycle to make 4
ready, as well as instruction 1 to make 4 admitted. These three jobs
exceed the first-cycle width. The same three-cycle schedule works.
At `B=3,W≥3`, `1,2,3 | 4` attains the two-cycle dependency lower bound.
At `B=4,W≥2`, `2,3 | 1,4` attains the two-cycle lower bound. The threshold
values follow directly from their definitions. ∎

Subagent C reports exhaustive absence of such decreases for `N≤3`; this
note's mathematical conclusion does not require or claim minimality.

## 9. Arbitrarily large saturation-threshold decreases

Proposition 9 extends to unbounded families; the phenomenon is not limited
to a one-entry change in a four-job example.

**Theorem 10 (one extra issue slot can replace an arbitrarily large ROB).**
For every integer `K≥2`, there is a `2K`-instruction program with at most
two true inputs and at most two true consumers per instruction such that

`B_sat(P,2)=2K`, while `B_sat(P,W)=3` for every `W≥3`.

Both unrestricted-window optima equal `K`. Thus increasing width from 2
to 3 can reduce the exact saturation window by an arbitrarily large
additive **and multiplicative** amount, without changing the target
unrestricted-window makespan.

**Construction.** Instruction 1 is isolated. The other instructions form
`K` consecutive layers: the first `K−1` layers have two vertices each,
`L_l={2l,2l+1}` for `1≤l≤K−1`; the final layer is `L_K={2K}`.
Between every two consecutive layers include all forward dependence
edges, and include no other true edges. This is a two-input program.

**Proof.** Every layered job is on a true path of length `K`, and a job
in layer `l` has a path of `l` vertices ending there and a path of `K−l+1`
vertices beginning there. In every schedule of makespan `K`, its issue
time is therefore at least `l` and at most `l`; it must issue in cycle `l`.
There is an unrestricted-window width-2 schedule of length `K`: issue
each layer in its numbered cycle and issue instruction 1 together with
the final singleton. This reaches the path/work lower bound.

At width 2, every one of the first `K−1` cycles of a `K`-cycle schedule
is full with its two layer jobs. Thus instruction 1 must issue in the
last cycle together with instruction `2K`. If `B<2K`, the augmented
edge `1→(2K)` forbids their equal issue times. No smaller window attains
the optimum, proving `B_sat(P,2)=2K`.

At width at least 3 and window 3, issue instruction 1 and the first
layer in cycle 1, then issue each remaining layer in its numbered cycle.
Every earlier layer has retired before the next cycle; the next layer
has at most two consecutive jobs and fits in the ROB. This attains `K`.
If `B≤2`, instruction 3 cannot issue in cycle 1, while its length-`K`
path requires exactly that in every `K`-cycle schedule. Hence the window
cannot be less than 3, proving the second formula. ∎

In fact the full makespan table of this family follows from the same
argument. Resource one gives `2K` cycles. For `B≥2,W≥2`,

* if `B=2`, the optimum is `K+1`;
* if `3≤B<2K` and `W=2`, the optimum is `K+1`;
* if `B≥3,W≥3`, or if `B≥2K,W≥2`, the optimum is `K`.

For the `K+1` upper bound, issue `{1,2}` first, `{3}` second, then the
remaining layers one per cycle; this is legal already at `B=2,W=2`.
The lower bounds excluding `K` were proved above. Consequently
`W_sat(P,1)=1`, `W_sat(P,2)=2`, `W_sat(P,B)=3` for `3≤B<2K`, and
`W_sat(P,B)=2` at `B≥2K`.

**Exact saturation versus near-optimal performance.** The large window
threshold drop does not mean a large running-time gain. For width 2,
every capacity from 2 through `2K−1` already runs in `K+1` cycles, only
one cycle above optimum. The ratio `(K+1)/K` tends to one. To make the
distinction precise, for `epsilon≥0` define

`B_epsilon(P,W)=min{B≥1:T*(P,B,W)≤(1+epsilon)T*(P,N,W)}`.

The exact resource curve above immediately gives

| Relative tolerance | `B_epsilon(P,2)` | `B_epsilon(P,3)` |
| --- | ---: | ---: |
| `0≤epsilon<1/K` | `2K` | `3` |
| `1/K≤epsilon<1` | `2` | `2` |
| `epsilon≥1` | `1` | `1` |

Thus this family establishes a strong discontinuity of **exact** resource
saturation and motivates studying approximate saturation separately. It
does not establish a comparably large IPC gain or a practical hardware
benefit from the larger ROB. This interpretation caveat was independently
raised by the literature/review subagent.

**Theorem 11 (unbounded decrease of saturation width).** Fix integers
`m≥2` and `1≤r≤floor(m/2)`. There is a `2m`-job program with true indegree
at most two and true outdegree at most one such that, for every
`m+r≤B≤2m`,

`W_sat(P,B)=m+min(r,2m−B)`.

In particular, raising the ROB capacity from `m+r` to `2m` reduces the
saturation width from `m+r` to `m`, a decrease of `r`, which is unbounded
over this family. The target makespan remains 2 throughout this range.

**Construction.** There are `r` isolated prefix roots, followed by `m`
required roots `A={r+1,...,r+m}`, followed by `m−r` suffix jobs. Partition
`A` into `r` pairs and `m−2r` singletons. Each suffix job depends on the
one or two roots in one part, and every part is used exactly once.

**Proof.** Each suffix job has an input and cannot issue in cycle 1.
Every root in `A` is the predecessor of a suffix job. Hence a schedule
of makespan 2 must issue all `m` roots of `A` in cycle 1. At `B≥m+r`,
issuing all `m+r` roots in the first cycle and the suffix in the second
is feasible, so the unrestricted effective-width optimum is 2.

For the last job `2m` to be admitted in cycle 2, the first `f=2m−B`
instructions must also issue in cycle 1. In the stated capacity range
`f≤m−r≤m+r`, so these are initial roots. Of these, exactly `min(r,f)`
lie outside `A`. Therefore the first-cycle width must be at least
`m+min(r,f)`. This lower bound also exceeds or equals the total-work
bound `m`.

It is attained by issuing `A` and those first `min(r,f)` isolated roots
in cycle 1. All have been admitted because their indices are at most
`m+r≤B`. The retired prefix is at least `f`: if `f≤r`, its first `f`
isolated roots have issued; if `f>r`, all initial roots have issued.
Thus the entire suffix is admitted and ready in cycle 2. At most `m`
jobs remain, so the same width finishes them. This proves the formula. ∎

For the same program, an additional exact window formula is available
for issue widths at least `m`. Writing the width as `m+s`,

`B_sat(P,m+s)=2m−s` when `0≤s<r`, and
`B_sat(P,m+s)=m+r` when `s≥r`.

Indeed, all required roots must issue first, so the initial window must
include the last root at index `m+r`. When `s<r`, last-job admission
also forces `2m−B≤s`, since only `s` isolated roots can join the `m`
required roots in cycle 1. The corresponding first-cycle union attains
these conditions. When `s≥r`, all initial roots fit in cycle 1 and
capacity `m+r` is sufficient and necessary.

Both families concern **optimal** schedules. These are not the classical
anomalies in which a particular fixed priority list becomes slower when
resources change; the optimal makespan here remains monotone. It is the
minimum resource needed to saturate performance that fails monotonicity.

## 10. Approximate saturation can still require a linear-size window

The layered example shows that exact saturation may be unstable. The next
family proves that allowing a fixed small relative timing loss does not
always remove a large window requirement.

**Theorem 12 (chain prefix and independent suffix).** Let `K≥1`, `N=2K`,
and take the true edges `1→2→...→K`, with all of instructions
`K+1,...,2K` independent of everything. For `W≥2` and `B≥1`,

`T*(P,B,W)=K+ceil(max(0,K−B+1)/min(B,W))`.

Every true indegree and outdegree is at most one. Capacity can be truncated
to `min(B,N)` without changing the result. The unrestricted-window optimum
is `K`, and `B_sat(P,W)=K+1` for every `W≥2`.

**Proof of the lower bound.** The final chain instruction `K` cannot issue
before cycle `K`. Each suffix job with index `j≥K+B` has an augmented edge
`K→j`, so it must issue strictly after instruction `K`. There are
`R=max(0,K−B+1)` such jobs. At most `min(B,W)` instructions fit in any
cycle, so these jobs require at least `ceil(R/min(B,W))` cycles after
the final chain cycle. Add the chain-length lower bound.

**Proof of attainment when `1≤B≤K+1`.** Issue chain instruction `i` in
cycle `i`. For `j=1,...,B−1`, also issue suffix instruction `K+j` in
cycle `K−B+1+j`. These extra issue cycles lie between 1 and `K`.
There is at most one extra suffix job per chain cycle, so the width is
at most two (and when `B=1` there are no extra jobs). The artificial
predecessors of suffix job `K+j` have indices at most `K+j−B`, and all
are chain jobs completed by the preceding cycle; it is therefore admitted.
After cycle `K`, the complete prefix through `K+B−1` retires. The remaining
`K−B+1` suffix jobs are independent, contiguous in program order, and can
be issued in consecutive batches of size `min(B,W)`. This is precisely
the displayed number of cycles. Here the extra issue formula for `j=1`
is `K−B+2`; in particular at `B=K+1` it starts in cycle 1.

**Proof of attainment when `B≥K+1`.** Issue instruction `i` of the chain
and suffix instruction `K+i` together in cycle `i`, for `1≤i≤K`. Before
that cycle the retired prefix has length at least `i−1`, so `K+i` is
in the window because `K+i≤i−1+B`. The width is two and all true
dependencies are respected. This finishes in `K` cycles, as required.
The saturation claim follows because the extra term is zero exactly
when `B≥K+1`. ∎

**Theorem 13 (exact epsilon-saturation curve).** For the same program,
let `epsilon≥0`, put `d=floor(epsilon K)`, and keep `W≥2`. Then

`B_epsilon(P,W)=max( ceil((K+1)/(d+1)), K+1−dW )`.

The right-hand side is automatically an integer between 1 and `K+1`.
For width 2 this simplifies to

`B_epsilon(P,2)=max(2,K+1−2 floor(epsilon K))` if `0≤epsilon<1`,

and `B_epsilon(P,2)=1` if `epsilon≥1`.

**Proof.** By Theorem 12 and integer cycle counts, approximate saturation
is equivalent to

`max(0,K−B+1) ≤ d min(B,W)`.

Since the right-hand side is nonnegative, this is equivalent to
`K+1≤B+d min(B,W)`. The latter right-hand side is
`min((d+1)B, B+dW)`, so both inequalities must hold:

`B≥ceil((K+1)/(d+1))` and `B≥K+1−dW`.

Their maximum is the minimum admissible capacity. The first term is at
least 1, so no separate positivity adjustment is needed; both are at most
`K+1`, which is itself at most `N=2K`. For `W=2` and `d<K`, if
`K+1−2d≥2`, that term also exceeds or equals the ceiling term; otherwise
the ceiling term is 2 because `d<K` and `2(d+1)≥K+1`. Thus the formula
becomes `max(2,K+1−2d)`. If `d≥K`, the ceiling term is 1 and the other
term is at most 1, giving capacity 1. ∎

**Corollary 14 (no length-independent near-optimal window bound).** Fix
`W≥2` and a real tolerance `0≤epsilon<1/W`. For this family,

`B_epsilon(P,W) ≥ (1−W epsilon)K+1`.

Consequently no finite function of just `(W,epsilon)`, independent of
program length, can upper-bound the window needed for a `(1+epsilon)`
approximation to the unrestricted-window optimum on all programs, even
if every true indegree and outdegree is at most one.

**Proof.** Theorem 13 gives
`B_epsilon≥K+1−W floor(epsilon K)≥(1−W epsilon)K+1`.
The coefficient of `K` is positive under the stated hypothesis, and `K`
is arbitrary. ∎

At the especially relevant fixed width 2, every fixed `epsilon<1/2`
therefore needs a window growing linearly with `N=2K` in the worst case.
For example, a ten-percent tolerance gives `B_epsilon≥0.8K+1`.
For this particular family, tolerances at least one half and below one
instead permit capacity 2. No sufficiency claim for **all** programs
at those larger tolerances is made.

This result concerns instruction order fixed by the model: placing the
independent suffix before or among the chain jobs would define a different
program order and can change its ROB requirement. Compiler reordering is
not an allowed optimization here.

**Corollary 15 (unbounded window tradeoff at a fixed positive tolerance).**
Fix an integer `W≥2` and a real tolerance
`1/(W+1)≤epsilon<1/W`. On the same chain-prefix family, for every `K≥1`,

`B_epsilon(P_K,W)≥(1−epsilon W)K+1`, while

`B_epsilon(P_K,W+1)≤min(W+1,2K)`.

Therefore adding a single issue slot can reduce the minimum sufficient
window by an unbounded multiplicative factor even at a fixed positive
relative timing tolerance, with the same unrestricted-window optimum `K`
on both sides. At widths 2 and 3 this applies to every fixed tolerance
`1/3≤epsilon<1/2`.

**Proof.** The first inequality is Corollary 14. Put `m=W+1`. At capacity
and issue width both equal to `m`, Theorem 12 gives

`T*(P_K,m,m)=K+floor(K/m)`.

To verify the floor identity including small cases, write `K=am+r` with
`0≤r<m`. If `a=0`, the extra term in Theorem 12 is zero. Otherwise its
numerator is `K−m+1=(a−1)m+(r+1)`, whose quotient by `m` has ceiling `a`.
Thus the displayed time is at most `(1+1/m)K≤(1+epsilon)K`. Capacities
larger than the whole program can be truncated to `2K`, proving the
second bound. The lower coefficient `1−epsilon W` is strictly positive,
while the upper bound `W+1` is constant. Their ratio is unbounded as
`K` grows. ∎

This corollary was proposed by the literature/review subagent and checked
independently by the theory subagent. It strengthens the exact-saturation
tradeoff without claiming a new priority result or a real-processor speedup.

## 11. Assumption audit and next questions

Theorem 1 critically uses eager unbounded admission after retirement,
in-order retirement, no separate retirement bandwidth, unit latencies,
and strictly next-cycle data availability. It does not apply unchanged
to an issue-queue model where executing a job immediately frees its slot,
to a finite dispatch-width model, to out-of-order retirement, or to
same-cycle dependency chaining. The DAG preserves fixed instruction
identities; no instruction fusion, elimination, or algebraic rewrites occur.

Theorem 4 handles unrestricted issue width only. Extending its simple
longest-path certificate to finite issue width is obstructed by Theorem 7.
Theorem 6 gives an exact parameterized baseline, not a claimed optimal
complexity. Theorem 8 gives a complete narrow-window case; its relation
to the scheduling literature still requires audit.

Priority next steps: independent review of the ROB equivalence; comparison
with bounded lookahead/window and storage-constrained scheduling; formalize
the schedule equivalence and footprint theorem; characterize resource
saturation under additional graph restrictions after Theorems 10–11's
unbounded-decrease families; refine worst-case epsilon-saturation bounds
after Theorems 12–14's linear-window obstruction; seek faster exact methods
for `B=3` and finite `W=2` exploiting the index-local incomparabilities.
