# Actual algebra characters and scalar cochain projection

`TwentyDimCharacters.lean` packages the e and f coordinate augmentations as
actual R-algebra homomorphisms to R, including their scalar compatibility,
basis values and distinct values on the two idempotents.

Composing the full actual algebra cochain with the f character gives the
scalar-valued trilinear map `actualfSimpleP`. Ring-homomorphic projection
transfers the full five-face formula to the character endpoint actions.
It is closed on all four algebra inputs, and the two specified basis
triples have weighted pairing q³. Thus q³ nonzero makes this cochain
itself nonzero.

Lean 4.34.1 compilation and independent replay passed without warnings.
Eight printed audits use at most `propext`, `Classical.choice` and
`Quot.sound`; there is no `sorry`, added axiom or `native_decide`.
The source hash and pinned Mathlib revision are recorded in the JSON.

The scalar cochain being nonzero does not alone prove its cohomology
class is nonzero. That requires excluding every scalar bilinear boundary
in a further file. No simple-module instance, projective resolution or
Ext identification is constructed here. The underlying data keep their
provenance in `../../ATTRIBUTION.md`.
