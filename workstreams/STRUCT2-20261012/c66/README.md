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
- [Source/overlap report](PRIOR_ART_2026-10-12.md): no first-resolution
  claim for the fixed-p limit, no certification of historical firstness.

[Original-definition checker](check_quantitative.py) and
[actual execution](quantitative_checks.json) supply exact small-support
histograms, an independent graph-row comparison on all graphs through
five vertices, 44,922 rational probability-bound checks, and effective
remainder endpoint certificates. This is definition-level finite evidence,
not a formal universal proof or independent written acceptance.

The new mathematical derivations are written completely, but remain
**pending independent written review**. No human peer review, all-parameter
Lean proof, journal acceptance or main-branch integration is claimed.
The old full/projected/reduced first-order candidate is not reclassified
as accepted because this nearby work has passed its own tests.

Next useful targets: the full-group critical window near `4 log(n)/n`,
the unresolved projection interval `2 <= c <= 4`, higher exponential
orders with structural coefficient formulas, and universal formalization
of the selection/component inequality. These are different questions.
