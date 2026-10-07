# A genuine twenty-coordinate algebra

`TwentyDimAlgebra.lean` installs the actual table multiplication on a distinct wrapper type `TableAlgebra q`. For every commutative ring R of characteristic two and parameter q, this type is a unital `Ring` and an `Algebra R`. Its multiplication is exactly `specializedMul q`, its unit is exactly `specializedUnit q`, and its scalar map sends r to r times that unit.

The ring laws use the proved all-vector associativity, unit and bilinear identities. The wrapper keeps this multiplication distinct from the pointwise multiplication on the coordinate function space. No commutativity of the table algebra is asserted.

The file constructs a linear equivalence with `Fin 20 → R`, a basis indexed by `Fin 20`, and finite/free module instances. Over every characteristic-two field K it proves `Module.finrank K (TableAlgebra q) = 20`, with no restriction on q.

All eight printed audits use only `propext`, `Classical.choice`, and `Quot.sound`. Independent compilation passed without warnings. This is an actual library algebra instance, but it does not construct the Hochschild complex, Ext groups or the complete ARC realization. Trace laws are proved on its coordinate multiplication in the separate trace files.

Replay after `TwentyDimUnit.olean` and `FiniteBilinearLaws.olean` with `lake env lean TwentyDimAlgebra.lean`. Additional Mathlib imports are listed at the top of the source.
