# Full coefficient insertion in every degree

`FiniteFreeBarInsertion.lean` defines a genuine R-linear map
`Hn : Pn →ₗ[R] P(n+1)` for every natural number n. The value at the word
with first letter i and tail w is the scalar algebra image of the ith
coordinate of the original A-valued coefficient at w.

The complete finite expansion includes every original word and all
twenty R-coordinates of its coefficient. Coefficients are retained in
the actual noncommutative algebra; no character projection occurs.
At degree zero this is the existing coordinate lift. Since the actual
unit is e+f, insertion of a unit basis coefficient has two first letters.

Compilation and independent replay passed without warnings. Nine
printed audits use only standard axioms; the word decomposition lemma
needs no Classical.choice. Exact hashes and toolchain are in the
verification JSON. Insertion is R-linear; A-linearity is not asserted.
This file alone defines no differential or exactness statement.
