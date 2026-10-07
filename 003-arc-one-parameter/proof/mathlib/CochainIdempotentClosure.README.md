# Full-input closure of the attributed cochain

`CochainIdempotentClosure.lean` proves that the actual five-face differential
of the specified cochain is zero on every four twenty-coordinate vectors,
over any commutative characteristic-two ring and at every parameter q.

The proof checks the corner support of 8,000 input triples, the 2,400
normalization entries involving the two idempotents, and their 80 left/right
table actions. These use kernel `decide`. Corner compatibility makes each
of the four idempotent-input formulas cancel. Every remaining basis input
belongs to the eighteen-label span, where the previously frozen 104,976
closure certificate applies. Four-linearity then gives all-vector closure.
No new 20^4 closure enumeration is used.

The source was compiled and independently replayed with Lean 4.34.1 and the
pinned Mathlib revision. Eleven printed audits use at most `propext`,
`Classical.choice` and `Quot.sound`; there is no `sorry`, added axiom or
`native_decide`. See the accompanying verification JSON for its source hash.

Closure does not require q to be nonzero. This file proves no nonzero
cohomology class or Ext identification; the actual-algebra quotient
application is in `TwentyDimHochschildClass.lean`. The finite data retain
the provenance recorded in `../../ATTRIBUTION.md`.
