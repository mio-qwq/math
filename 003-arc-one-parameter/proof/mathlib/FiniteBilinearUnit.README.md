# Units from finite structure constants

`FiniteBilinearUnit.lean` extends basis unit identities to every vector over any commutative semiring and finite coordinate type. It uses the multiplication defined in `FiniteBilinear.lean`.

If contracting the first index of the structure constants with a vector E gives the identity matrix, E is a left unit. The corresponding second-index identity gives a right unit. The combined theorem proves both laws, without requiring associativity, characteristic two, or any enumeration.

All five printed theorem audits contain only `propext`, `Classical.choice`, and `Quot.sound`. The source compiled with Lean 4.34.1 and the pinned Mathlib revision. The concrete ARC unit is a separate application of these generic contraction hypotheses.

From this directory, with its path in `LEAN_PATH`, replay:

```sh
lake env lean -o FiniteBilinear.olean FiniteBilinear.lean
lake env lean FiniteBilinearUnit.lean
```
