# Research queue after the first verified baseline

## Completed or reduced

* Exact R1 legality, finite optimality and operational/time-assignment equivalence.
* Independent operational and time-assignment exact algorithms, certificate checking and reproducible counterexamples.
* Universal online optimality resource dichotomy, with strict model-specific information boundary.
* Saturated-width optimum and unrestricted-width minimal window in polynomial time with short certificates.
* B=W+1 arbitrary-N offline optimum in polynomial time (R21), and the linear perfect-width tiling criterion (R19).
* Actual ROB horizon corridor, sharp candidate count and FPT in c+S (R20), with c=B-W and S=WH-N. Actual strip/count is Lean verified; algorithm/counting sharpness are not.

These do not imply a general efficient optimal finite-width online processor.

## Highest-value next questions

1. **Fixed-resource online loss.** Determine the best strict deterministic/randomized ratio at fixed B,W in the nontrivial regime 1<W<B. Current hidden-chain lower bound is

   `1 + 1/(1+ceil((B-W)/(W-1)))`

   for deterministic policies, while classical list scheduling gives upper bound `2-1/W`. At B3,W2 the deterministic bounds match at 3/2. Its randomized value is now exactly5/4 by the joint potential proof R15, using R14 normalization. The sharper exact families do not settle general B,W.

2. **Resource-parametric composition.** R18 now repeats the B3,W2 four-job gadget with two-input roots and no separator cycles, proving matching factors even with additive constants. Determine when analogous composition preserves the stronger hidden-subset bounds at larger fixed B,W; the already-resolved B3 case must not be relisted as open.

3. **Excess-window complexity and certificates.** R21 supplies polynomial optimum at B=W+1 for arbitrary W, and XP in c=B-W. R25 now gives W[1]-hardness in c for general true DAGs, using a known biclique mechanism. Determine the status for true fan-in<=2; this is not settled by the reduction. The completed polynomial prefix-potential checker is R22. For a height-H/fan-in-d graph with redundant artificial edges, max(0,N-B)<=sum(d^j,j=1..H-1), so naive height-two binary expansion cannot preserve the old construction.

4. **Formalize structural resource results and the optimized DP.** Actual finite/global non-delay normalization is now compiled and independently reviewed. First-clear-prefix macro decomposition and its recurrence are the immediate next steps.  Concrete executable time/lane enumeration is now proved sound, complete and optimal for the actual ROB model. Fixed-schedule window footprint is also formalized. Connect an efficient finite-frontier representation to the model; formalize R11–R13. Keep the generic Bellman/search interface, concrete enumeration, optimized DP, and Python correctness distinct.

5. **Full online observations in Lean.** Connect the sharp5/4 proof and any verified arithmetic kernel to actual ROB traces, randomized policy expectations, oldest normalization and the complete local recurrence. Extend to arbitrary B/W and hidden-subset randomized/advice results. A conditional arithmetic kernel is not a proof of this complete semantics bridge.

6. **Robust resource frontiers.** Exact window drops from N to3 at widths2 to3 are now proved, with an explicit one-cycle-loss limitation. The chain-prefix family now gives an exact approximate-saturation curve and an Omega(N) window lower bound for fixed epsilon<1/W. Study tight universal resource trade-offs or further graph classes; do not present these resolved family questions as still open.

7. **Improve lookahead constants and policies.** R23/R24 determine the optimal excess order Theta(1/(L+1)) at B4,W3, including additive constants. Find better leading constants or exact finite-L minimax values. The random chunk bound1+3/(L+4) is sharp for that policy, but its tight family is trivial for all-ready. A causal non-delay filling wrapper is under investigation; no better universal bound is yet proved.

## Refuted shortcuts

* Only offset edges `(j-B,j)` model the ROB: false.
* Oldest-ready is universally optimal: false at N4,B3,W2.
* Either original or augmented critical-path priority is universally optimal: false; exact tie-rule witnesses retained.
* The augmented height/work bound is always tight: false; a fan-in-two barrier family has an unbounded additive gap.
* An original ASAP schedule minimizes the window among height-optimal schedules: false at N3 with edge0->1.
* Saturation thresholds inherit makespan monotonicity: false at N4.
* Arbitrary original dependencies preserve the base window's interval-order class: false.
* At B=W+1, an optimum can always issue the oldest W-1 ready jobs: false at B4,W3,N5.
* Uniform younger omission has ratio4/3 at B4,W3: false at N9, where E/T*=37/27. The larger-width guess (3-1/W)/2 for this policy is therefore also false. Identify a better information-aware distribution or a stronger all-policy lower bound.
* Append independent dummy jobs to reduce arbitrary N to divisible perfect saturation: false at N5,B4,W3,edge0->1; a sixth job increases the optimum from2 to3.
* Forced segments have length bounded solely by B: false even at B4,W3; an interleaved chain can keep one completed unretired entry for arbitrarily many cycles.

No finite search result is promoted to a general theorem without proof, and no completed proof is promoted to a novelty claim without an adequate literature audit.
