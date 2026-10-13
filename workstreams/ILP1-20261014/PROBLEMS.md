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

   for deterministic policies, while classical list scheduling gives upper bound `2-1/W`. At B3,W2 the deterministic bounds match at 3/2. Its randomized value is still in[5/4,3/2]; R14 oldest-inclusion normalization and the scalar recurrence now support a precise uniform-younger-choice candidate. The sharper exact families do not settle general B,W.

2. **Composable adversaries.** Can the hidden-choice gadgets be repeated at the same B,W while preserving indistinguishability and a linear offline advantage? This is necessary before importing the finite strict ratios into an asymptotic competitive claim with additive constants.

3. **Structured finite-width saturation.** Characterize graph/program classes on which a small optimality certificate avoids full-state enumeration. W2 is already covered by classical Coffman–Graham after reduction. Seek a genuinely stronger bounded-window structure or improved local algorithm, rather than rediscovering that theorem.

4. **Formalize structural resource results and the optimized DP.** Concrete executable time/lane enumeration is now proved sound, complete and optimal for the actual ROB model. Fixed-schedule window footprint is also formalized. Connect an efficient finite-frontier representation to the model; formalize R11–R13. Keep the generic Bellman/search interface, concrete enumeration, optimized DP, and Python correctness distinct.

5. **Full online observations in Lean.** Extend the verified first-action pair to histories, arbitrary B/W and hidden-subset randomized/advice results. The general written theorem currently has more scope than the formal pair.

6. **Robust resource frontiers.** Exact window drops from N to3 at widths2 to3 are now proved, with an explicit one-cycle-loss limitation. The chain-prefix family now gives an exact approximate-saturation curve and an Omega(N) window lower bound for fixed epsilon<1/W. Study tight universal resource trade-offs or further graph classes; do not present these resolved family questions as still open.

## Refuted shortcuts

* Only offset edges `(j-B,j)` model the ROB: false.
* Oldest-ready is universally optimal: false at N4,B3,W2.
* Either original or augmented critical-path priority is universally optimal: false; exact tie-rule witnesses retained.
* The augmented height/work bound is always tight: false; a fan-in-two barrier family has an unbounded additive gap.
* An original ASAP schedule minimizes the window among height-optimal schedules: false at N3 with edge0->1.
* Saturation thresholds inherit makespan monotonicity: false at N4.
* Arbitrary original dependencies preserve the base window's interval-order class: false.

No finite search result is promoted to a general theorem without proof, and no completed proof is promoted to a novelty claim without an adequate literature audit.
