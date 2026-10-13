# C66: quantitative continuation, awaiting independent acceptance

This directory studies the precise random variables behind Bychawski
Conjecture 6.6. The fixed-probability limit overlaps an existing public
MathDB proof claim, which is preserved and compared explicitly.

New written results:

- [Second exponential order](SECOND_ORDER.md): full TF expectation at
  `p=1/2`, with coefficients `224*binom(n,3)+528*binom(n,4)` and a
  proved effective `O(n^6*2^(-3n))` error bound.
- [Sparse expectation and twin-free scales](SPARSE_THRESHOLD.md): full
  TF expectation has leading sparse constant 4; twin-freeness has the
  distinct scale 1 and a Poisson critical-window formula.
- [Constant-order threshold refinement](SPARSE_SHIFT.md): for
  `p=(4 log n-K)/n`, full-group expectation tends to one when `K<4`
  and diverges when `K>4`; its boundary is closed by the subsequent note.
- [Constraint-component refinement](COMPONENT_REFINEMENT.md): an exact
  component-excess penalty recovers the discarded `Theta((log n)^2)` scale
  at `K=4`.
- [Critical boundary and the next correction](CRITICAL_BOUNDARY.md): for
  `np=4 log n-4-c(log n)^2/n`, expectation tends to one when `c<8`
  and diverges when `c>=8`. This includes convergence at `K=4`. A finer
  empty-graph obstruction identifies the next coefficient 22 and a positive
  limiting lower bound, whose matching upper bound is proved next.
- [Exact sparse window](EXACT_WINDOW.md): uniformly for
  `n^2*p=4*n*log n-4*n+O((log n)^2)`, the full expectation is
  `1+(n!)^2*(1-p)^binom(n,2)+o(1+(n!)^2*(1-p)^binom(n,2))`.
  At `p=1-(n!)^(-2/binom(n,2))+2*x/n^2`, its limit is `1+exp(-x)`.
  Includes an explicit finite remainder and the matched coefficient-22
  window. The nonempty-conditional expectation tends to one there.
- [Source/overlap report](PRIOR_ART_2026-10-12.md): no first-resolution
  claim for the fixed-p limit, no certification of historical firstness.
  [New source comparison](PRIOR_ART_2026-10-13.md) preserves the same boundary.

[Original-definition checker](check_quantitative.py) and
[actual execution](quantitative_checks.json) supply exact small-support
histograms, an independent graph-row comparison on all graphs through
five vertices, 44,922 rational probability-bound checks, and effective
remainder endpoint certificates. This is definition-level finite evidence,
not a formal universal proof or independent written acceptance.

[Component checker](check_component_refinement.py) separately passes 89,844
exact rational inequalities on full and selected constraint systems at
`n=4,5`, with a size-two damage control. Its receipt is under
`verification/20261013-c66-component-refinement/`.

[Critical structure checker](check_critical_structure.py) checks 16,087
permutation pairs, 96,522 cycle-density bounds, 2,295 exact probabilities,
72 cycle-count comparisons and a four-cycle damage control. These are new
structural checks, not a replay of the earlier graph enumeration.

[Lean component interface](lean/README.md) defines actual original edge
variables and the full equation closure, constructs the component edge list
and proves endpoint/cycle-prefix transport. Its 12 Lean 4.34.1 audits pass;
the overall expectation theorem remains written. Both receipts are under
`verification/20261013-c66-critical-boundary/`.

[Exact-window checker](check_exact_window.py) checks the new singleton and
union-support statements on 15,396 pairs, with 3,984 exact rational
assertions, 80 short-cycle moment/tail comparisons and 1,238 literal-graph
or finite-bound assertions. Two damage controls reject false singleton
rules. The two-module Lean chain adds the actual singleton iff shared
fixed/transposed endpoints, passing 21 audits. Receipts are under
`verification/20261013-c66-exact-window/`; the analytic limit is not Lean.

The new mathematical derivations are written completely, but remain
**pending independent written review**. No human peer review, all-parameter
Lean proof, journal acceptance or main-branch integration is claimed.
The old full/projected/reduced first-order candidate is not reclassified
as accepted because this nearby work has passed its own tests.

Next useful targets: independent semantic acceptance of the exact window,
the unresolved projection interval `2 <= c <= 4`, higher exponential
orders with structural coefficient formulas, and universal formalization
of the selection/component inequality. These are different questions.
