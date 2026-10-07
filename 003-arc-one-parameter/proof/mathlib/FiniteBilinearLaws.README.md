# Additive and scalar multiplication laws

`FiniteBilinearLaws.lean` proves distributivity, both zero laws, scalar compatibility in each argument, and simultaneous scalar multiplication for finite structure-constant multiplication. The results hold over every commutative semiring and finite coordinate type. They do not require associativity or unit assumptions.

It also packages multiplication by a fixed vector as actual left and right linear maps. These laws support subsequent construction of a ring and algebra from the actual table. All nine printed audits use only the standard three axioms, and the source compiled without warnings.

After compiling `FiniteBilinear.lean`, run `lake env lean FiniteBilinearLaws.lean` with this directory in `LEAN_PATH`. Its additional Mathlib imports are `Mathlib.Algebra.Module.LinearMap.Defs` and `Mathlib.Algebra.Module.Pi`.
