# The actual degree-four boundary and closed module map

`FiniteFreeBarDegreeFour.lean` constructs the actual A-linear map from
the degree-four free term to the degree-three term with all five faces.
For every degree-three A-linear Hom map to the actual character module,
the basis precomposition formula agrees with the full scalar
character differential, including both endpoint faces.

The specified f-character module map precomposed with this actual
degree-four boundary is zero on the entire free term. The proof uses
all word-basis elements and full input-slot linear expansions together
with the previously proved cochain closure. It imposes no radical-input,
field or nonzero-parameter restriction.

Lean 4.34.1 compilation and independent replay passed without warnings.
Six printed audits use only `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used;
exact hashes and pinned Mathlib are in the verification JSON.

Closure of this Hom map does not prove the general adjacent chain
composition is zero or establish exactness. Those statements, a full
projective resolution and the Ext comparison remain open.
