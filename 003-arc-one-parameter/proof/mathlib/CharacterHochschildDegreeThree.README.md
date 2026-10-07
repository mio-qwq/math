# The full degree-three character cochain quotient

`CharacterHochschildDegreeThree.lean` constructs degree-three cycles modulo
the full degree-two boundaries for any actual R-algebra character A → R,
over a commutative characteristic-two ring R and associative R-algebra A.
The spaces contain all scalar-valued multilinear maps, and both endpoint
faces are included in the differentials.

The quotient is ker(d3) modulo the image of d2 within that kernel.
`classOf_eq_zero_iff` proves that a closed cochain's class vanishes exactly
when it is the full differential of some scalar-valued bilinear map.
`classOf_ne_zero` supplies the corresponding nonzero-class criterion.

Lean 4.34.1 compilation and independent replay passed without warnings.
All three printed audits use only `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used.
The verification JSON records the exact source hash and pinned Mathlib.

This generic quotient is not an Ext identification or a projective bar
resolution. A particular cochain still needs full closure and exclusion
of every scalar boundary before the nonzero-class criterion applies.
