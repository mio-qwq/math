# The character module is simple over a field

`CharacterModuleSimple.lean` proves the standard `IsSimpleModule A`
predicate for the actual character module when R is a field and
eps : A → R is an R-algebra character. No characteristic assumption or
commutativity of A is imposed.

For any nonzero module element x and arbitrary target y, the scalar
element of A with value y/x sends x to y. Thus every nonzero vector
has full A-orbit, which proves the actual simple-module criterion.
The nontrivial carrier comes from the field hypothesis.

Lean 4.34.1 compilation and independent replay passed without warnings.
All three printed audits use only `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used; exact
source hashes are in the verification JSON.

This is a simple-module construction and theorem. It supplies no
projective resolution, Ext calculation or all-degree ARC assertion.
