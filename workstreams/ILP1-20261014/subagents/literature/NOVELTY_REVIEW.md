# Independent novelty and mathematical-scope review

Reviewer: literature subagent D, 2026-10-13 UTC. Sources are keyed to
`LITERATURE_REVIEW.md`. This review is independent of the originating theory
agent. Written arguments below were checked here, but no Lean compilation or
solver experiment was performed by this reviewer.

## Claim inventory

| Candidate | Correctness assessment here | Prior-art assessment | Permitted presentation |
|---|---|---|---|
| Finite optimum, Bellman recurrence, exhaustive certificates | Standard finite optimization foundations | Classical; not original | Reproducible baseline and formalization |
| R1 equals a DAG with all edges `i→j` for `j-i≥B` | Written proof below checked | FIFO event edges already explicit in L04 | Specialized elimination theorem; novelty unconfirmed |
| Unlimited-width optimum equals augmented DAG height | Follows from reduction and ASAP | Classical longest-path scheduling | Corollary |
| Two-wide offline polynomial optimum | Follows from reduction plus L05 | Classical Coffman–Graham | Corollary; not a new scheduling algorithm |
| Fixed-schedule minimal window formula | Direct exact consequence, checked | Equivalent bounded-reordering formulations not exhaustively ruled out | Structural characterization; novelty unconfirmed |
| Unlimited-width window saturation by binary search | Direct algorithmic consequence | Standard monotonicity plus DAG longest paths | Useful corollary; not a major novelty claim |
| Universal online optimality iff `W=1` or `B≤W` | Independent written review passes | R1-specific statement not located; L12/L14/L15 supply close methodology | Candidate theorem, novelty unconfirmed |
| Hidden-subset family with exact randomized minimax/advice | Counting proof checked below | Standard indistinguishability, averaging and advice techniques | Exact family result; novelty unconfirmed |
| Any work-conserving R1 policy is `(2-1/W)` competitive | Classical transfer if ready-set equivalence is proved | L11 | Corollary, not a new constant |
| FPT in ROB capacity via finite frontier | Plausible and elementary; implementation not reviewed here | General frontier-DP literature needs deeper audit | Do not claim first parameterized algorithm |

The strongest present opportunity is a precise online information/resource
classification, supported by a small exact family and explicit observation
semantics. Its short proof is a virtue, but importance and originality require
comparison beyond a first search. No item here is claimed as academically novel
or publication-ready.

## R1 reduction: independent semantic check

Use one-based instruction indices, positive integer `B,W`, a forward data DAG
`E`, and integer issue cycles `t_j≥0`. A job completes at the end of its issue
cycle. At cycle `c`, the retired prefix contains exactly those initial jobs all
completed in earlier cycles. Eager admission fills through `min(N,r+B)` where
`r` is that prefix length. No completion frees an entry before in-order retirement.

Define `E_B = E ∪ {(i,j): 1≤i<j≤N and j-i≥B}`. Then a time assignment is R1
feasible exactly when each slot contains at most `W` jobs and every edge of
`E_B` has `t_i<t_j`.

Necessity: if `j` is admitted when it issues, at least `j-B` instructions are
already retired. Every `i≤j-B` therefore completed in an earlier cycle.
Data precedences and the issue bound give the remaining conditions.

Sufficiency: process the proposed assignment by increasing cycle, admitting
eagerly and retiring maximally. For a job `j` assigned to the current cycle,
every `i≤j-B` has already completed by the added edges. Thus the retired prefix
is at least `j-B`, so `j` is present. Its original predecessors also completed
earlier, and the proposed slot fits width `W`. This inductively realizes every
assigned job at its proposed cycle, including assignments with idle cycles.

This proof specializes the known retirement-to-entry event constraint by
eliminating admission/retirement events. L04 does not explicitly state the
complete feasible-schedule equivalence above. That distinction supports the
value of a formal semantic bridge; it does not establish a new resource-modeling
idea. Edges only from `j-B` to `j` on execution nodes are insufficient: they
omit older incomplete jobs that prevent retirement of `j-B`.

This argument depends on unlimited prefix retirement, refill before the next
cycle, unit latency, no same-cycle dependency bypass, and capacity counting
finished-but-unretired jobs. Changing those clauses requires a separate model.

## Resource formula and its limits

For a fixed precedence-feasible time assignment define

`b(t) = max({1} ∪ {j-i+1 : i<j and t_i≥t_j})`.

Then the assignment fits exactly the capacities `B≥b(t)`. Indeed, the added
edge condition fails precisely when a pair has `j-i≥B` but `t_i≥t_j`.
Both reversed pairs and same-cycle pairs matter. The default value 1 is a
positive-capacity convention, including the empty set of pairs.

For finite width, minimizing `b(t)` over all unrestricted-window optimal
assignments characterizes saturation but still contains a scheduling
optimization problem. Calling that expression an efficient closed-form
solution would be misleading.

For width at least the window capacity, all currently ready jobs can issue.
The optimum is augmented height. With `h_j` measured in vertices, compute

`h_j = 1 + max({0} ∪ {h_i : (i,j)∈E} ∪ {h_i : i≤j-B})`.

A prefix-maximum array handles the last set without materializing quadratically
many resource edges. One height query takes `O(N+|E|)` time, and monotonicity
allows the least `B` matching the no-window height to be found in
`O((N+|E|) log N)` time for nonempty input. These are classical algorithmic
ingredients applied to the reduction, not evidence of a new general scheduling
algorithm.

The base window order can be represented by equal-length intervals. Arbitrary
original dependencies need not preserve interval-order structure: if `B≥4`,
four consecutive instructions can induce only `1→3` and `2→4`, the forbidden
`2+2` pattern. Consequently, a general claim “the augmented DAG is an interval
order” is false. L08's optimality theorem cannot be applied without a class
membership proof.

## Online universal-optimality dichotomy: independent proof review

Fix positive integers `B,W`. “Universal” means one policy is optimal for every
finite forward program, with no bound on `N`. The policy may know `N,B,W`, all
admitted instructions and their incoming dependencies, and complete history.
It does not see instructions or operands beyond the admitted prefix and gets
no successor oracle about those instructions. This information restriction must
be defined at the level of observations, not merely described as hardware-like.

**Claim.** Such a deterministic policy exists if and only if `W=1` or `B≤W`.

For `W=1`, every non-idling policy executes one job each unfinished cycle and
takes `N` cycles. A ready job always exists: the earliest unfinished job is in
the window and all its forward predecessors have completed. For `B≤W`, issue
every ready job. This is ASAP on `E_B`; induction on the DAG gives the earliest
possible completion of every vertex, hence optimal makespan.

For necessity let `B>W≥2`, now use zero-based indices, and construct `2B` jobs.
Jobs `0,…,B-1` are roots. Jobs `B,…,2B-1` form a chain, with an additional edge
`x→B` for a chosen `x∈{1,…,B-1}`. The initial observation and total length are
identical for every possible `x`.

Let `A` be the policy's first issue set. If `0∉A`, no root retires in cycle 0,
so job `B` is not present in cycle 1. If `0∈A`, then `|A|≤W<B` leaves a positive
root `x` unissued; choose that input. Job `B` cannot execute in cycle 1 because
`x` was not completed in cycle 0. In either case the length-`B` suffix starts
no earlier than cycle 2 and makespan is at least `B+2`.

Offline, issue exactly `{0,x}` in cycle 0. Then issue the next chain job and,
while one remains, the least-index unfinished root each cycle. Root-prefix
retirement advances at least one position per such cycle, admitting the next
chain job in time. Once all roots retire, the entire suffix fits in capacity
`B`. The schedule finishes in `B+1`, which is also the lower bound from
`x→B→…→2B-1`. Every job has original indegree and outdegree at most one.

The construction disproves universal optimality even when `N` is known. It
does not address a class restricted to `N≤B`, when the entire input is visible.
It is a strict instance ratio lower bound `(B+2)/(B+1)`; without a repeatable
construction it should not be advertised as a lower bound in definitions that
permit an arbitrary additive constant in competitive analysis.

The independence argument also rules out a randomized policy that achieves
the optimum almost surely on every input: each input forces inclusion of
`{0,x}` in the first action almost surely, and the finite intersection would
force all `B` roots into a width-`W` action. This does not by itself give a
sharp expected competitive ratio.

Status of this review: `WRITTEN_PROOF`, `INDEPENDENTLY_REVIEWED` for the displayed
mathematical argument, `NOVELTY_UNCONFIRMED`; no claim of Lean coverage. L12,
L14 and L15 explain why the adversarial method is prior art. No exact R1
resource dichotomy was identified within this search's coverage.

## Hidden-subset family: randomized minimax and advice

This separately checks the stronger construction supplied by the theory agent.
Let `q≥1`, `N=4q`, `B=3q`, `W=2q`. The first `3q` instructions are roots. Fix a
hidden subset `A` of size `q` from root indices `q,…,3q-1`. The last `q`
instructions each have one parent, bijectively the elements of `A` (use sorted
order to make the family canonical). There are `C=binomial(2q,q)` programs.

Each program has optimum 2. A two-cycle schedule must execute all of the prefix
`Q={0,…,q-1}` in its first cycle: retiring fewer than `q` roots would prevent
admission of all `q` suffix jobs for cycle 2. It must also execute every parent
in `A` in cycle 1. Since `|Q∪A|=2q`, the unique successful first action is
`Q∪A`. Issuing that set, then the remaining `q` roots and `q` suffix jobs,
achieves 2.

For any randomized policy, the probabilities of these `C` distinct first
actions sum to at most 1. Some fixed input therefore has success probability
at most `1/C`; its expected cycles are at least `3-1/C`. Uniformly choosing
one of these canonical actions attains this bound: after a wrong choice,
execute all remaining roots in cycle 2 and all still blocked suffix jobs in
cycle 3. Thus the exact minimax expected instance ratio *on this family* is
`3/2-1/(2C)`. This is an oblivious fixed-input lower bound, not an adversary
that sees private random bits. The deterministic value is `3/2`.

For deterministic advice with a fixed-length binary message available before
the first decision, exact optimality on this family needs and suffices with
`ceil(log2 C)` bits. Distinct inputs require distinct first actions, so a message
cannot serve two inputs; sending an index of `A` suffices. This statement does
not silently count future-arriving advice, variable-length unframed messages,
or advice per instruction. Its counting technique is standard (L16), while
the R1 family requires its own novelty audit. The result is not an exact
minimax theorem for all R1 programs with those resource values.

## September 2026 claim: reproducible inspection boundary

Observed `openai/math` main commit from real `git ls-remote`:
`1581d4cbdd69a0faf34b2089614fe2a814316a6a`. Three key files were re-fetched at
that exact commit, returning these Git blob SHAs:

| Path | Observed blob SHA |
|---|---|
| `lean/OAI/Computability/Scheduling/Main.lean` | `e1bde8078ff07f7508b9677830b1d8d52e0acb51` |
| `lean/ComparatorChallenges/ThreeMachine.json` | `f43edce328e71ef23b19fedfbf92a0a17755f1c7` |
| `preprints/A-polynomial-time-algorithm-for-three-machine-unit-job-scheduling-September-24-2026/build/paper.tex` | `00a3e5fed881652cd68cc6a522602f6a66e5a3ab` |

The public challenge specification uses explicit graph encoding including the
job list, strict edge times, slot occupancy at most three and uniform machine
quantifiers. This rules out a few obvious misreadings but is not a complete
semantic/kernel audit. The endpoint's proof invokes `Algorithm.output_correct`
and a uniform request-machine bound. Neither those dependencies nor the
manuscript's structural decomposition were reconstructed here.

Do not conclude failure from the challenge's intentional placeholder, or success
from the endpoint file alone. A subsequent audit should pin the toolchain,
build the actual module, run the documented comparator on its configuration,
print axioms of the resulting theorem, inspect all definition bridges, and
independently review the nontrivial combinatorial structural lemmas. Until then,
our theorems should avoid relying on the claimed three-machine polynomial
algorithm. The accurate chronology is “historically open; September 2026 claim
with released formal artifact awaiting this workstream's independent audit.”

## Research priorities after this review

1. Formalize online observation equivalence and the exact universal-optimality
   dichotomy, keeping the quantifier over all program lengths explicit.
2. Determine whether hidden-subset gadgets can be composed while preserving
   fixed resources and an additive lower bound. This is needed for asymptotic
   competitive-ratio claims with an additive constant.
3. Audit future-information guarantees beyond one initial decision: advice
   rate, lookahead measured in admitted instructions, and randomized guarantees.
4. Search architecture and scheduling literatures for the exact fixed-schedule
   displacement formula and ordered-frontier DP, before calling either new.
5. Inspect the complete L07 artifact independently if three-wide complexity
   becomes necessary. This is a substantial separate audit, not a source-check
   footnote.
