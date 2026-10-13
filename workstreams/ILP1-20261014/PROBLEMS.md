# Research queue after the first verified baseline

## Completed or reduced

* Exact R1 legality, finite optimality and operational/time-assignment equivalence.
* Independent operational and time-assignment exact algorithms, certificate checking and reproducible counterexamples.
* Universal online optimality resource dichotomy, with strict model-specific information boundary.
* Saturated-width optimum and unrestricted-width minimal window in polynomial time with short certificates.

These do not imply a general efficient optimal finite-width online processor.

## Highest-value next questions

1. **Fixed-resource online loss.** Determine the best strict deterministic/randomized ratio at fixed B,W in the nontrivial regime 1<W<B. Current hidden-chain lower bound is

   `1 + 1/(1+ceil((B-W)/(W-1)))`

   for deterministic policies, while classical list scheduling gives upper bound `2-1/W`. At B3,W2 the deterministic bounds match at 3/2. Its randomized value is now exactly5/4 by the joint potential proof R15, using R14 normalization. The sharper exact families do not settle general B,W.

2. **Resource-parametric composition.** R18 now repeats the B3,W2 four-job gadget with two-input roots and no separator cycles, proving matching factors even with additive constants. Determine when analogous composition preserves the stronger hidden-subset bounds at larger fixed B,W; the already-resolved B3 case must not be relisted as open.

3. **Structured finite-width saturation.** Characterize graph/program classes on which a small optimality certificate avoids full-state enumeration. W2 is already covered by classical Coffman–Graham after reduction. Seek a genuinely stronger bounded-window structure or improved local algorithm, rather than rediscovering that theorem.

4. **Formalize structural resource results and the optimized DP.** Concrete executable time/lane enumeration is now proved sound, complete and optimal for the actual ROB model. Fixed-schedule window footprint is also formalized. Connect an efficient finite-frontier representation to the model; formalize R11–R13. Keep the generic Bellman/search interface, concrete enumeration, optimized DP, and Python correctness distinct.

5. **Full online observations in Lean.** Connect the sharp5/4 proof and any verified arithmetic kernel to actual ROB traces, randomized policy expectations, oldest normalization and the complete local recurrence. Extend to arbitrary B/W and hidden-subset randomized/advice results. A conditional arithmetic kernel is not a proof of this complete semantics bridge.

6. **Robust resource frontiers.** Exact window drops from N to3 at widths2 to3 are now proved, with an explicit one-cycle-loss limitation. The chain-prefix family now gives an exact approximate-saturation curve and an Omega(N) window lower bound for fixed epsilon<1/W. Study tight universal resource trade-offs or further graph classes; do not present these resolved family questions as still open.

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

No finite search result is promoted to a general theorem without proof, and no completed proof is promoted to a novelty claim without an adequate literature audit.
