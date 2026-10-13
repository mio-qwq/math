# Results and precise proof status

All indices are zero based; N is finite, every original edge i->j has i<j, and B,W>=1. The model is R1 in MODEL.md. Written proofs in this file do not by themselves assert Lean coverage or historical originality. Formal coverage and independent review are tracked separately in STATUS.md and formal/README.md.

## R1. Existence, state sufficiency and Bellman exactness

**Status: WRITTEN_PROOF; classical foundations, not a novelty claim.**

For any reachable completed set D, eager admission and in-order retirement determine the whole relevant state: r=min(first incomplete index,N) and window [r,min(N,r+B)). Earlier completed jobs have retired; later completed jobs cannot be outside this window because the admitted endpoint only increases. With no in-flight jobs across cycle boundaries and no dynamic latencies, nothing else affects the next legal action.

If unfinished, r is ready since every predecessor has smaller index. Consequently a nonempty legal action exists and increases |D|. Iterating singleton oldest jobs finishes in at most N-|D| cycles. Empty actions can be deleted from a finite schedule: state and readiness are unchanged by an idle cycle, and no absolute-time constraints exist. Hence an optimum can use only nonempty actions.

Set V(all)=0 and, for unfinished D,

    V(D)=1+min { V(D union S): empty != S subset A(D), |S|<=W }.

This recursion is well founded by the number of unfinished jobs. Strong induction on that number proves both directions: every schedule's first nonidle action is enumerated, giving a lower bound by the recurrence; a minimizing first action followed by the induction witness attains it. Thus V(empty)=T*, and following recorded minimizing actions returns a globally optimal schedule. The Python implementation is an unpruned memoized version; recursion depth and finite memory limit its usable instance sizes but not the mathematical recurrence.

**Independent certificate.** Supply a legal K-cycle schedule and integer potential v on all states reachable by nonempty actions, with v(all)=0, v(empty)=K, and v(D)<=1+v(D union S) for every legal nonempty S. Each transition of any schedule satisfies this inequality (idle steps satisfy it trivially). Telescoping gives K<=duration. The supplied schedule proves equality. The checker discovers all successors itself and rejects missing states, rather than trusting the solver's successor list. This is a full-state certificate, not a compact structural certificate.

## R2. Exact static precedence representation

**Status: WRITTEN_PROOF; closely related event-graph representations are prior art.**

Define E_B=E union {(i,j):i+B<=j<N}. A time assignment t is feasible in R1 iff it respects all E_B edges strictly and has at most W jobs at each time.

Necessity: if j is issued in cycle c, it has entered by that cycle. With at most B unretired ordered entries, the entire prefix through j-B must already have retired (when j>=B). Each i<=j-B therefore completed before c, and t(i)<t(j). Ordinary data and width conditions also hold.

Sufficiency: replay time layers. Before t(j), all i with i+B<=j have completed. Therefore the first incomplete index r is at least j-B+1 if j>=B; if j<B then trivially r+B>j. Job j itself is not complete, so r<=j. Hence r<=j<r+B and j has entered. Its data predecessors completed earlier and layer width is <=W. Every requested layer is legal. This proof also accommodates idle cycles.

**Incorrect simplification refuted.** Adding only edges (j-B,j) does not impose all prefix completion requirements. For E=empty,N=4,B=2,W=2, t=(1,0,2,1) satisfies offset edges 0->2,1->3 but violates required 0->3. Operational replay rejects it.

## R3. Monotonicity and an exact saturated-width algorithm

**Status: WRITTEN_PROOF; classical consequences of R2.**

Increasing B deletes artificial edges; increasing W relaxes a layer capacity. Thus T* is nonincreasing separately in B and W. Every E_B-antichain has index span at most B-1, hence at most B jobs. For W>=B, issue each vertex at its earliest precedence-feasible time; every layer is an antichain and respects W. Therefore T*=height(E_B).

With empty maximum -1, compute in original index order

    e(j)=1+max(max_{(i,j) in E} e(i), max_{i<=j-B} e(i)).

The last term is absent if j<B. Prefix maxima make this O(N+|E|) time and O(N+|E|) storage, without materializing quadratic artificial edges. Every feasible t obeys t(j)>=e(j), by induction on j; e itself is feasible when W>=B. For every W, max(height(E_B),ceil(N/min(B,W))) <= T* <= N. Height and workload bounds need not be simultaneously attainable: N=4,E={(1,3),(2,3)},B=3,W=2 has height2 and workload2 but T*=3. In two cycles all three predecessors 0,1,2 of job3 in E_B would have to occupy the first cycle, impossible with W2.

## R4. A parameterized exact algorithm

**Status: WRITTEN_PROOF; straightforward bounded-frontier DP, not claimed novel.**

At a nonterminal state the first incomplete r is absent from D, [0,r) is present, and the only optional completed indices are r+1,...,min(N,r+B)-1. Hence there are at most 1+N*2^(B-1) reachable completed sets (replace B by min(B,N) for N>0).

For a fixed r, each of the other B-1 positions is completed, selected this step, or incomplete and unselected. Index r has two step choices, selected or not. Thus summed over all states, there are at most 2*N*3^(B-1) candidate transitions, before filtering precedence and issue width. This gives time O(N*3^B*poly(N,B,|E|)) and space O(N*2^B*poly(N)) with a direct bit-set implementation. The polynomial factors account for graph checks and non-unit-cost bit operations. This is fixed-parameter tractability in B, not a polynomial bound when B is part of the unrestricted input.

## R5. Exact resources for a fixed schedule

**Status: WRITTEN_PROOF; direct exact characterization, not an efficient general optimization theorem.**

For N>0 and any time assignment satisfying original data precedence, define

    beta(t)=max({1} union {j-i+1: i<j and t(i)>=t(j)}),
    omega(t)=max_c |{j:t(j)=c}|.

R2 gives t feasible under (B,W) iff B>=beta(t) and W>=omega(t). Indeed a pair with t(i)>=t(j) forbids every B<=j-i; conversely B>=beta(t) leaves no artificial-edge violation.

Let U_W be the set of unrestricted-window width-W schedules with minimum duration T*(E,N,W). It is nonempty, and

    B_sat(E,W)=min_{t in U_W} beta(t).

Similarly let H_B be all schedules with E_B precedence and duration height(E_B). Then

    W_sat(E,B)=min_{t in H_B} omega(t).

The minima exist: choose earliest nonnegative optimal times, so all maps lie in a finite time range. These formulas still optimize over schedules. They do not solve P3 in polynomial time. Saturation definitions are restricted to N>0; empty-input minimum positive resources may separately be set to 1 by convention.

## R6. Resource saturation thresholds need not be monotone

**Status: WRITTEN_PROOF + exact certificates; NOVELTY_UNCONFIRMED.**

For N=4,E={(1,3),(2,3)}, the table of optimal times is

| B \\ W | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 4 | 4 |
| 2 | 4 | 3 | 3 | 3 |
| 3 | 4 | 3 | 2 | 2 |
| 4 | 4 | 2 | 2 | 2 |

Proof: W1 or B1 forces four cycles. For B2, artificial edges0->2 and1->3 together with2->3 give a three-job chain0->2->3; schedule {0,1},{2},{3} attains3 for W>=2. For B3,W2 the three augmented predecessors0,1,2 of3 preclude two cycles; the same three-cycle schedule attains3. With B3,W>=3, {0,1,2},{3} attains2. With B4,W>=2, {1,2},{0,3} attains2, which is optimal by data precedence.

Thus B_sat as W runs1..4 is (1,4,3,3), and W_sat as B runs1..4 is (1,2,3,2). Both can decrease after increasing, even with original maximum indegree2. This does not contradict monotonicity of T*: the benchmark optimal time defining saturation itself changes.

## R7. Four-job online obstruction

**Status: WRITTEN_PROOF + independently reproduced finite witness; NOVELTY_UNCONFIRMED as an exact ROB instance.**

Set N=4,B=3,W=2. Program A has only edge1->3; program B only edge2->3. The first three visible operations are identical independent roots; even known N cannot distinguish the inputs. To finish in two cycles, job3 must issue in the second cycle and job0 must have retired beforehand. A therefore forces first action {0,1}, while B forces {0,2}. Both have legal two-cycle schedules. Every deterministic online first action fails for at least one fixed input, with duration at least3 and ratio at least3/2. Subsets with fewer than two jobs, or idle actions, cannot finish four jobs in two cycles either.

Oldest-ready chooses {0,1} and needs3 cycles on B. Even original critical-path priority can fail: N=5,E={(1,3),(2,4),(3,4)},B=3,W=2 gives greedy {1,2},{0},{3},{4}, four cycles. The schedule {0,1},{2,3},{4} attains the three-cycle data-chain lower bound. Both traces are replayed in the tests.

Further general online bounds and proofs are in subagents/theory/ after independent review; see STATUS.md for acceptance status.
