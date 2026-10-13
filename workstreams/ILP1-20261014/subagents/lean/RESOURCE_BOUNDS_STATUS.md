# Fourth Lean increment

Previous local tip: `c2d47c4da9018f5305517cc5de84e33dcc27e090`.
Added `formal/ResourceBounds.lean` and its exact-scope note.
Seven additional general theorems establish width saturation at B and removal
of window constraints at B>=N. All have actually compiled with only standard
Lean axioms. The executable solver, model, operational bridge, and online pair
sources remain unchanged.

`formal/verify.py` now includes ResourceBounds when present; the fresh combined
author-run receipt has 68 audited declarations. This remains distinct from
the independent parent recompilation and mathematical review.

The initial task's core formal baseline is now present: actual ROB semantics,
optimality existence/certificates, executable exact solver correctness,
resource cap identities, and a universal-policy four-job online obstruction.
Remaining research targets are stronger program-dependent resource thresholds,
structural optimality results, and independent review; the Python solvers
remain outside the Lean implementation-correctness claim.
