# Exactness at the second free term

`FiniteFreeBarExactTwo.lean` constructs a genuine R-linear contracting
map h2 from P2 to P3 by transferring every A-valued word coefficient
into the first slot of the full trilinear lift.

The preceding contraction h1 satisfies
`h1(x • L1(y)) = L2(x,y)` for arbitrary algebra elements x and y.
This follows from its R-linearity and scalar centrality; h1 is not
assumed A-linear. The full boundary face formulas then give

`boundary3(h2(v)) + h1(boundary2(v)) = v`

on the entire A-valued module P2. A boundary2-closed vector therefore
has the explicit preimage h2(v), proving
`ker boundary2 = range boundary3` for every actual character and q.

Lean 4.34.1 compilation and independent replay passed without warnings.
Nine printed audits use only standard Lean axioms. The verification
JSON fixes the source hash and Mathlib revision. A local elaboration
recursion limit is increased for one definitional equality; no trust
axiom or `native_decide` is introduced.

This proves exactness at P2. Exactness at P3 and above, a complete
projective resolution and an Ext comparison remain open.
