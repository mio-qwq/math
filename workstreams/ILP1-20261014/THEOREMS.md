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

Every work-conserving R1 policy inherits the classical Graham bound 2-1/W on the augmented DAG. The theory note gives the full backward-path counting proof and explicit attribution. Combining W2's upper bound3/2 with R7 proves that the **global strict deterministic online minimax ratio at fixed B3,W2 is exactly3/2**. No additive constant is allowed in this definition. The initial randomized interval[5/4,3/2] at these resources is now closed by R15 below: the exact strict randomized value is5/4.

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

For B3,W2, after choosing the oldest plus any other ready job the optimal continuation returns to a completed-prefix state within at most two cycles. The complete scalar O(N+|E|) recurrence and boundary proof are in theory NARROW_WINDOW_POLICY.md. This simplifies the constant-window DP but does not improve its asymptotic complexity class. The uniform younger-choice online policy is proved sharply5/4 in R15 below.


## R15. Sharp randomized scheduling at B=3,W=2

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED + COMPUTATIONALLY_SUPPORTED; conditional scalar induction kernel LEAN_VERIFIED, full ROB/random-policy theorem not Lean verified; NOVELTY_UNCONFIRMED.**

Define R to include the oldest unfinished operation. If all three entries are unfinished and ready, uniformly and independently choose one of the two younger operations; otherwise issue all ready operations. For every fixed finite forward-DAG program, with N instructions, offline optimum F and policy expected time E,

    4E <= N+3F <= 5F.

Therefore the global strict randomized online minimax ratio at these fixed resources is exactly5/4, against an oblivious adversary choosing the complete program in advance. For the empty program the undivided inequality remains true but no ratio is defined.

**General proof.** R14 reduces optimal and policy values to the same completed-prefix scalar recursion, with a minimum for F and an average for E. Let F_i,E_i,n_i be the remaining optimal time, expected time and number of jobs at suffix i; empty suffixes have zero values. Completing one extra prefix job never hurts and doing it alone costs one cycle, so F_i-F_(i+1) is0 or1. Define K_i=3F_i+n_i-4E_i. Descending strong induction jointly proves K_i>=0 and, for a nonempty suffix with F_i=F_(i+1), K_i+K_(i+1)>=1.

Forced macros have nonnegative K increments. Randomized macros have targets p=i+2,q=i+ell, where ell=3 or4, and x=F_p-F_q. The exact K increments above the average of the two tail potentials are -1/2 for(ell,x)=(3,0),1 for(3,1),0 for(4,0)or(4,2), and3/2 for(4,1). The negative row is canceled by the later adjacent-equality invariant. To prove that invariant at i, the forced-singleton case has unequal F; all other forced cases and x1 have K_i>=1. Each remaining randomized case forces either a fixed pair or a good x1 random state at i+1, giving K_(i+1)>=1. The delicate(4,0)case follows from excluding the suboptimal adjacent-pair branch at suffix i+2, forcing a four-job alternative and then two consecutive unit F decreases. All existence, tail and edge implications are given in the complete proof [RANDOMIZED_FIVE_QUARTERS.md](subagents/theory/RANDOMIZED_FIVE_QUARTERS.md), §3, and independently reconstructed in two review reports. No numerical search is used in that induction.

At i=0, K_i>=0 is the first displayed bound; width two gives N<=2F. The four-job pair of R7 has E=5/2,F=2 under R. For every randomized policy, its probabilities of choosing the two distinct uniquely optimal first actions sum to at most1. One fixed program thus has miss probability at least1/2 and expected duration at least5/2. This proves the matching lower bound without an adaptive adversary.

Finite support: all2,796,203 effective local-edge graphs throughN12 were searched exactly. Independent time-variable CSP optima and direct operational policy expectations checked683 nonempty graphs plusempty,3869 suffix occurrences and1232 equal-adjacent cases. They also checked every difficult proof classification. These data are supporting evidence, not the general proof. The equivalent three-quarter guarantee for double-issue cycles is not automatically a theorem about arbitrary online matching models.

`formal/UniformYoungerPotential.lean` verifies the finite joint strong induction and all five local min/mean identities over a common positive integer scale. Ten new declaration audits were actually recompiled by the primary agent. The explicit `MacroShape` interface contains local equations and structural successor classifications; connecting those assumptions to every actual ROB instance, constructing the probability/scale semantics, and the separate work bound remain unformalized. No full-policy Lean claim follows from this conditional kernel.

## R16. A unified hidden-subset family at shallow true depth

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED + COMPUTATIONALLY_SUPPORTED; not Lean verified; NOVELTY_UNCONFIRMED.**

Fix W>=2,1<=m<=W-1,W<B<=2W-m,d>=1 and W-m<=dm. Let N=B+m. The first B jobs are roots, F={0,...,m-1},U={m,...,B-1}. A hidden A subset U of size W-m is partitioned among the m suffix jobs, with each part of size at most d supplying its incoming edges. Empty parts are allowed. True indegree<=d,outdegree<=1,depth<=2.

Every member has optimum two and unique two-cycle first action F union A. The last suffix job's admission requires all F first; all parents require all A first; their union fills width W. Conversely the remaining B-W roots plus m sinks fit the second cycle since B-W+m<=W.

With M=binom(B-m,W-m), the exact promised-family deterministic ratio is3/2, randomized ratio3/2-1/(2M), and fixed-length advice for always-optimal deterministic scheduling is ceil(log2 M) bits before the first decision. Initial observations agree and the M required actions are distinct, giving the counting lower bounds. For attainment, uniformly guess A', issue F union A', then all ready jobs. A correct guess takes two cycles. Otherwise all remaining roots and currently ready sinks fit cycle two, and all blocked sinks fit cycle three. Encoding A gives the advice upper bound. These are family upper bounds and unrestricted-model lower bounds, not unrestricted-model upper bounds.

At B=W+1, M=W+1-m. For W=2q,m=q,d=1, the true graph contains q disjoint edges, yet the randomized lower bound is3/2-1/(2(q+1)), approaching3/2 as the resources grow. At B4,W3,m1,d2 it is4/3. This already prevents extending the B3,W2 value5/4 uniformly to all B=W+1. Proof and reviews: theory ONE_EXTRA_ENTRY_FAMILY and verification WINDOW_PLUS_ONE_FAMILY_REVIEW. Independent checks cover77 single-omission programs/10675 first actions/419 policy replays and51 further unified-family programs/1927 first actions/761 replays.

## R17. Limits of stronger oldest-first and uniform-omission rules

**Status: REFUTED conjectures, exact counterexamples; independent numerical verification; no novelty claim.**

Requiring the oldest W-1 jobs in every full-ready action is already suboptimal at N5,B4,W3,E={(2,4),(3,4)}. Optimum2 uses {0,2,3};{1,4}; including0,1 first forces3 cycles. The valid single-oldest normalization R14 is unaffected.

The policy that always includes oldest and uniformly omits one younger job when all B=W+1 jobs are ready does not have ratio4/3 at B4,W3. On N9,E={(1,4),(2,4),(2,5),(5,8)}, optimum3 uses {0,1,2};{3,4,5};{6,7,8}. The policy has duration3 with probability1/9,4 with probability2/3,and5 with probability2/9. Thus E=37/9 and E/T*=37/27>4/3. Exact independent CSP and operational probability-tree checks agree. The prior exhaustive N<=8 search contains no smaller counterexample to this specific policy, in the effective local-edge graph encoding. This refutes a policy guarantee, not the possibility that another online policy achieves4/3.

In fact no fixed younger-rank probability vector, independent of length, operands, position and history, can guarantee4/3. The three N5 hidden-pair programs force all three omission probabilities to be1/3 if that bound is to hold, but the N9 example then violates it. The four-input minimax within this restricted fixed-vector class is (13+sqrt(73))/16; see theory WIDER_POLICY_COUNTEREXAMPLE §4. This is not a lower bound above4/3 for fully adaptive online policies.

## R18. The same sharp ratios with an additive constant

**Status: WRITTEN_PROOF + INDEPENDENTLY_REVIEWED; general random observation/probability argument not Lean verified; NOVELTY_UNCONFIRMED.**

At fixed B3,W2, the optimal randomized factor remains5/4 and the deterministic factor remains3/2 in the definition E[T(P)]<=cT*(P)+alpha, with fixed finite input-independent alpha. This is not inferred just from the earlier finite witness.

For q>=1 concatenate q four-job blocks (a_k,b_k,c_k,d_k)=(4k,4k+1,4k+2,4k+3), each with hidden parent b_k or c_k for d_k. Give each of the three roots of the next block two true predecessors c_k,d_k. Every true indegree is at most two. Window edges automatically supply the missing a_k,b_k precedences, so every instruction of a new block must wait for the entire preceding block to finish. There are no extra separator instructions or cycles. Issuing a_k and the hidden parent, then the remaining two jobs, proves T*=2q.

Under independent uniform hidden bits chosen in advance, each block's d_k remains unadmitted at its first decision. Its bit is still uniform conditioned on all previous history and policy random state. The two distinct successful first batches have total probability at most1, hence expected duration at least5/2 per block. Some fixed length4q input has E[T]>=5q/2. Letting q grow rules out c<5/4 even with alpha. For deterministic policies, recursively select the missed hidden parent per block; this specifies one fixed input with T>=3q. Existing strict upper bounds match both. Full proof: [REPEATED_GADGETS.md](REPEATED_GADGETS.md); independent theory and verification reviews saved separately. `formal/RepeatedGadgets.lean` now verifies the exact true graph (indegree<=2), arbitrary-q block separation, hidden-job admission barrier, forced first jobs in a two-cycle block, the explicit schedule, and actual-model optimum2q including q0. This is a closed structural theorem, not a conditional DP interface; its probability/online semantics extension remains unformalized. Product-distribution/direct-sum methods are classical.
