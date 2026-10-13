# Third Lean increment

Prior local increments:

- `ada228db8a794f1c0404ff591eac9fa64b024a99`: model and operational equivalence.
- `e0f1f8710bb1d84d65c615f920912d0ef884cb37`: deterministic online pair.

The new `formal/ExactEnumeration.lean` compiles and proves an executable
bounded-slot enumerator sound, complete, and globally optimal for all finite
forward-dependence programs with positive window and width. It returns an
actual issue-time schedule. Twelve new printed audits use only standard
Lean axioms. Three actual `#eval` executions are recorded in the build log.

The previous model, operational and online source files remain unchanged.
`formal/verify.py` now includes the new module when present; previous run
receipts remain preserved as historical source-specific records. The fresh
combined run is in `evidence/exact-enumeration/` (61 declarations).

The Python solver implementations remain independently tested rather than
Lean-certified. The enumerator is exponential and is not an algorithmic
novelty claim. Next formal target: derive width saturation at `W=B` directly
from the canonical ROB interval, using position-minus-retired-index lanes.
