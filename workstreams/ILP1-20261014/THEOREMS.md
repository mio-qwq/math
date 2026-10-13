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

**Status: WRITTEN_PROOF; fixed-schedule window formula LEAN_VERIFIED in ResourceFootprint.lean. Width cardinality and global saturation minimization below remain written proofs. Not an efficient general optimization theorem.**

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

Thus B_sat as W runs1..4 is (1,4,3,3), and W_sat as B runs1..4 is (1,2,3,2). Both can decrease after increasing, even with original maximum indegree2. This does not contradict monotonicity of T*: changing one resource changes which schedules attain the benchmark. In both decreasing steps of this example, the benchmark remains exactly two cycles.

## R7. Four-job online obstruction

**Status: WRITTEN_PROOF + independently reproduced finite witness; NOVELTY_UNCONFIRMED as an exact ROB instance.**

Set N=4,B=3,W=2. Program A has only edge1->3; program B only edge2->3. The first three visible operations are identical independent roots; even known N cannot distinguish the inputs. To finish in two cycles, job3 must issue in the second cycle and job0 must have retired beforehand. A therefore forces first action {0,1}, while B forces {0,2}. Both have legal two-cycle schedules. Every deterministic online first action fails for at least one fixed input, with duration at least3 and ratio at least3/2. Subsets with fewer than two jobs, or idle actions, cannot finish four jobs in two cycles either.

Oldest-ready chooses {0,1} and needs3 cycles on B. Even original critical-path priority can fail: N=5,E={(1,3),(2,4),(3,4)},B=3,W=2 gives greedy {1,2},{0},{3},{4}, four cycles. The schedule {0,1},{2,3},{4} attains the three-cycle data-chain lower bound. Both traces are replayed in the tests.

## R8. Universal online optimality: exact resource classification

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED; only the four-job arbitrary-policy obstruction is currently LEAN_VERIFIED. NOVELTY_UNCONFIRMED.**

For fixed positive B,W, an online policy optimal for every finite R1 program exists iff W=1 or W>=B. The same classification holds for randomized policies required to attain the optimum in expectation. The information model is precisely MODEL.md: admitted instructions and incoming dependencies are visible; unadmitted future uses are not. N may be known.

Positive directions: W1 takes N nonidle cycles, and W>=B permits all ready jobs to issue, giving augmented-DAG earliest times.

For B>W>=2 set L=ceil((B-W)/(W-1)), so 1<=L<B. Use B initially independent roots and an L-job suffix chain, the first suffix depending on a hidden x in {1,...,B-1}. All initial views and N=B+L agree. Every program has optimum L+1: issue any W roots containing 0,x first, then each chain job with up to W-1 smallest unfinished roots. Before suffix job k (one based), the completed root prefix has length at least min(B,1+(k-1)(W-1))>=k, hence it is admitted. The total root slots W+L(W-1)>=B finish all roots. The true x-plus-chain path supplies the matching lower bound.

A deterministic first action either omits0, blocking suffix admission, or includes0 but misses some x because W<B. Choose that fixed hidden-root input. The chain begins at least one cycle late, so the online duration is at least L+2. This gives strict multiplicative lower bound 1+1/(L+1).

On this hidden-root family the exact randomized minimax ratio is

    1 + (B-W)/((B-1)(L+1)).

Uniform x is hit by any first action containing0 with probability at most (W-1)/(B-1); each failure costs at least one cycle. Choosing0 plus a uniform (W-1)-subset attains the bound, using a single extra root-only cycle if x is missed. The required fixed-length advice before the first decision is exactly ceil(log2(ceil((B-1)/(W-1)))). These are **family-specific** minimax/advice values. Full proofs and exact quantifiers: [ONLINE_LOWER_BOUND.md](subagents/theory/ONLINE_LOWER_BOUND.md), Theorems5–6.

## R9. Hidden subsets and the tight B3,W2 deterministic ratio

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED; general randomized/advice statements not Lean verified. NOVELTY_UNCONFIRMED.**

For q>=1 take N4q,B3q,W2q. First3q jobs are roots. Let F={0,...,q-1}, U={q,...,3q-1}; choose a hidden q-subset A of U. Each suffix job has a distinct parent in A. Every optimum has two cycles and unique first action F union A. With M=binom(2q,q), the exact strict randomized minimax ratio on this family is 3/2-1/(2M), and exactly ceil(log2 M) fixed-length pre-decision advice bits suffice and are necessary. The proof counts compatible first actions and gives an explicit three-cycle continuation for every incorrect guessed subset. See the independent review and theory note for the full argument.

Every work-conserving R1 policy inherits the classical Graham bound 2-1/W on the augmented DAG. The theory note gives the full backward-path counting proof and explicit attribution. Combining W2's upper bound3/2 with R7 proves that the **global strict deterministic online minimax ratio at fixed B3,W2 is exactly3/2**. No additive constant is allowed in this definition. The randomized global value at these fixed resources is only bounded between5/4 and3/2 here.

## R10. Compact exact saturation certificate at unrestricted width

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED; implemented, not Lean verified. Classical algorithmic ingredients.**

Fix N>0,W>=N, and let H=height(E). By R3, B_sat is the least B in1..N with height(E_B)=H. Heights decrease with B, so binary search using the prefix-max recurrence takes O((N+|E|)log N) time. Certificate: an H-cycle schedule at B, an H-vertex chain in E, and, if B>1, an (H+1)-or-longer chain in E_(B-1). The first two establish the unrestricted optimum and attainment; the last excludes all smaller B by edge containment. Certificate size is O(N), independent of the number of schedules. `src/resources.py` constructs and checks these witnesses without full-state enumeration.

## R11. Unbounded exact saturation drops at fixed issue widths

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED + COMPUTATIONALLY_SUPPORTED; not Lean verified; NOVELTY_UNCONFIRMED.**

For every K>=2, define P_K on N=2K jobs: isolated job0, K-1 pair layers {1,2},{3,4},...,{2K-3,2K-2}, then singleton {2K-1}. Add all edges between consecutive nonisolated layers. True indegree and outdegree are at most two. Then

    B_sat(P_K,2)=2K,     B_sat(P_K,3)=3.

Every nonisolated job lies on a K-vertex path. A K-cycle schedule must therefore put each layer in its corresponding cycle. At width2 all first K-1 cycles are full, so job0 must share the final cycle with jobN-1. This attains the height bound at B=N but violates the artificial edge0->N-1 for every B<N. At width3,B3, issue {0,1,2}, then successive pairs, then the final singleton. It takes K cycles. For B<=2 job2 is not initially admitted, although its K-vertex path requires initial issue. These arguments prove both minima.

**Interpretation:** the threshold drop and its ratio are unbounded, but the performance loss at every 2<=B<N and W2 is only one cycle: {0,1},{2},then remaining layers takes K+1 cycles already at B2. Thus the duration ratio is 1+1/K, tending to1. If B_epsilon permits a factor1+epsilon above the unrestricted optimum, its exact values are (N,2,1) for W2 and (3,2,1) for W3 across epsilon intervals [0,1/K),[1/K,1),[1,infinity). No large real-hardware speedup follows.

Independent verification checked216 horizon-K decisions, K2..10, every B and W2,3; the arbitrary-K statement follows from the reviewed proof, not this finite count. Full proofs and review: theory STRUCTURAL_RESULTS §9 and verification SATURATION_REVIEW.

## R12. An exact depth-two issue-width threshold curve

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED + COMPUTATIONALLY_SUPPORTED; not Lean verified; NOVELTY_UNCONFIRMED.**

For m>=2,1<=r<=floor(m/2), use r isolated initial roots, m required roots, then m-r sinks. Partition the required roots into r pairs and m-2r singletons and give each sink one distinct group. N=2m, true indegree<=2,outdegree<=1. For 1<=B<=2m,

    T*(P,B,W)<=2 iff B>=m+r and W>=m+min(r,2m-B).

Every required root must issue first, forcing its last index initially admitted. Admission of the last sink also forces the first2m-B jobs to issue first. Their union with the required roots has exactly m+min(r,2m-B) jobs, proving necessity. Conversely issue that union first: it is admitted, retires the required prefix, and makes all sinks ready. At most m jobs remain, so a second cycle suffices.

Consequently W_sat(P,B)=m+min(r,2m-B) for m+r<=B<=2m. Increasing B from2m-r to2m drops the saturated width by r, which is unbounded. The benchmark stays two cycles. Independent audit:25 programs,5720 horizon-two decisions for m2..10; complete proof in the same review as R11.

## R13. Exact approximate saturation and robust linear window demand

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED + COMPUTATIONALLY_SUPPORTED; not Lean verified; NOVELTY_UNCONFIRMED.**

For K>=1 let Q_K have N=2K jobs: the firstK form a chain and the lastK are independent. For B>=1,W>=2,

    T*(Q_K,B,W)=K+ceil(max(0,K-B+1)/min(B,W)).

If the last chain job issues at cycle c, then c>=K-1. At the start of that cycle retirement is at most K-1, so at most B-1 independent jobs have been admitted, INCLUDING jobs that could issue with the last chain job. At least max(0,K-B+1) independent jobs therefore remain AFTER that cycle and require the asserted extra cycles. For attainment, run the chain every cycle, pairing one independent job in each of its last min(K,B-1) cycles; the ordered window admits each. Then issue the remaining independent suffix in full batches of size min(B,W).

For epsilon>=0 write q=floor(epsilon*K). Since the unrestricted optimum is K,

    B_epsilon(Q_K,W)=max(ceil((K+1)/(q+1)), K+1-q*W).

Proof: the duration condition is K+1<=B+q*min(B,W)=min((q+1)*B,B+q*W). Solving these two integer inequalities gives the formula. For W2 and epsilon<1 it simplifies to max(2,K+1-2q); epsilon>=1 gives1. At W1, the baseline itself is2K and B_epsilon=1 for all nonnegative epsilon. Oversized windows cause no exception.

For fixed W>=2 and epsilon<1/W the threshold is at least (1-W*epsilon)K+1=Omega(N). Hence no universal program-length-independent bound, such as a function of W and epsilon alone, can guarantee this tolerance. True indegree and outdegree are at most one. Independent audit:2020 exact duration/replay comparisons K1..10 including oversized resources,1185 approximate threshold cases. Full proof and scope in verification APPROXIMATE_SATURATION_REVIEW.


### R13 corollary: robust single-slot approximate-window collapse

For fixed integer W>=2 and 1/(W+1)<=epsilon<1/W, the same Q_K family has B_epsilon(Q_K,W)>= (1-W*epsilon)K+1 while B_epsilon(Q_K,W+1)<=W+1. For q=floor(epsilon*K), q>=floor(K/(W+1)), so K+1<=(W+1)(q+1). Both terms of the exact formula at widthW+1 are at mostW+1. The ratio of necessary windows is therefore unbounded as K grows. The left endpoint is included. In particular, fixed epsilon in[1/3,1/2) works for widths2 to3. This does not say every positive tolerance works at every fixed W.

This corollary was first derived in the literature role and then independently checked by theory, verification, formal-DP paper reviewer and the primary agent. It has no Lean or novelty claim. The family's exact B_sat is K+1 for every W>=2; the width-dependent collapse is specifically approximate. Moreover interleaving the same chain with its independent jobs achieves K cycles at B=W=2. Resource thresholds depend on the program's fixed topological ordering, not just the unlabeled DAG; instruction reordering is excluded in R1.


## R14. An oldest-inclusive optimum when B=W+1

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED + COMPUTATIONALLY_SUPPORTED; not Lean verified; NOVELTY_UNCONFIRMED.**

For every positive W and B=W+1, every finite forward-DAG program admits an optimal non-delay schedule that issues the oldest unfinished instruction in every nonterminal cycle. This also holds for optimal continuation from any reachable state.

Choose the lexicographically least program-index time vector among all optimal continuations. It is non-delay: moving a currently ready future job into a vacant issue slot preserves augmented precedence/capacity and strictly improves that vector. If it omits oldest h, its W issued jobs and h exhaust the B-entry window, all unfinished and ready. Retirement cannot advance; next cycle only h is unfinished in the window, so non-delay executes h alone. Swap h with any one issued job x across those two cycles. Both actions remain legal and the completed/retired/admitted state after two cycles is identical. The first changed time coordinate h decreases, a contradiction. The swapped schedule need not remain non-delay: minimization was over ALL optimal schedules, which is essential to this argument.

This is an existence restriction, not arbitrary oldest-inclusive greedy optimality. The four-job B3,W2 online pair still forces a choice of younger job. At B4,W2,E={(1,3),(2,3)}, an optimal two-cycle schedule must omit oldest0 initially, so the hypothesis cannot simply be dropped. Independent restricted-CSP checks cover225 exhaustive small instances plus200 seeded instances and this negative control.

For B3,W2, after choosing the oldest plus any other ready job the optimal continuation returns to a completed-prefix state within at most two cycles. The complete scalar O(N+|E|) recurrence and boundary proof are in theory NARROW_WINDOW_POLICY.md. This simplifies the constant-window DP but does not improve its asymptotic complexity class. The uniform younger-choice online policy is now under investigation; its general5/4 guarantee remains unproved.
