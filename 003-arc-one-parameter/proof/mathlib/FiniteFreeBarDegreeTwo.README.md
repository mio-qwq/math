# The actual degree-two chain boundary

`FiniteFreeBarDegreeTwo.lean` constructs an actual A-linear map from the
degree-two free term to the degree-one term. Its three basis faces are
left multiplication, the complete coordinate lift of the product of
the two basis letters, and the right character coefficient.

The preceding degree-one boundary composed with this map is zero,
using character multiplicativity, scalar centrality and characteristic
two. Both source and target retain the genuine noncommutative left
A-action. For every A-linear map from the degree-one term to the
actual character module, precomposition has the full three-face scalar
formula on all ordered basis pairs.

Lean 4.34.1 compilation and independent replay passed without warnings.
Nine printed audits use only `propext`, `Classical.choice` and `Quot.sound`.
No `sorry`, added axiom or `native_decide` is used; exact source hashes
and pinned Mathlib are in the verification JSON.

This proves a chain-composition law and a Hom face formula. It does
not prove exactness at degree one, higher chain-composition laws, a
full projective resolution or an Ext comparison.
