# Full character-valued cochain differentials

`CharacterHochschildMaps.lean` defines the full four- and five-face
differentials with scalar values in R and endpoint actions given by an
actual R-algebra character eps : A → R. Both endpoint faces are included.
The degree-two, degree-three and degree-four spaces consist of all nested
R-linear maps, and the differentials are R-linear in the cochain.

For every commutative characteristic-two ring R and associative R-algebra
A, d3 composed with d2 is zero. The cancellation theorem already holds
for every arbitrary two-variable scalar function, before multilinearity
is required. The source does not impose a separate characteristic-two
instance on A.

Lean 4.34.1 compilation and an independent replay passed without warnings.
Six printed audits use at most `propext` and `Quot.sound`; no `sorry`,
added axioms, `native_decide` or finite enumeration is used. The accompanying
verification JSON records the pinned Mathlib revision and source hash.

This supplies the character-valued complex relation at degree three.
It does not construct a quotient, apply the formula to a specific
character, construct a bar resolution or identify an Ext group.
