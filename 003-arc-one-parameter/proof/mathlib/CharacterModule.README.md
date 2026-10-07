# An actual module for every algebra character

`CharacterModule.lean` constructs a distinct module carrier for an actual
R-algebra character eps : A → R. It installs the genuine left A-action
a acting by eps(a) on values, the ordinary R-scalar action, and their
scalar-tower and commuting-action compatibility. All new instances are
on this carrier.

The value map is an R-linear equivalence to R and a bijective semilinear
map through eps. Scalar elements of A act by their original R values,
and every R value occurs in the character image. These results hold for
every commutative ring R and associative R-algebra A, with no
characteristic-two or field assumption.

Lean 4.34.1 compilation and independent replay passed without warnings.
Seven printed audits use at most `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used; hashes
and the pinned Mathlib revision are in the verification JSON.

This file supplies an actual module, not a projective resolution or Ext
comparison. Simplicity under the field hypothesis is proved separately
in `CharacterModuleSimple.lean`.
