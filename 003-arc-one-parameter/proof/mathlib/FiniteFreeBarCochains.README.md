# Actual module Hom maps and full scalar cochains

`FiniteFreeBarCochains.lean` combines the two proved coordinate
equivalences to identify all actual A-linear maps from the degree-two
and degree-three free candidate terms to a character module with all
scalar-valued bilinear and trilinear cochains on the actual algebra.
The equivalences are R-linear and genuinely surjective in both degrees.
Basis-evaluation formulas are proved in both directions.

The specified f-character cochain thereby gives an actual A-linear map
from the degree-three free term into the actual f-character module.
Its two-word weighted pairing is q³, so the map is nonzero whenever
q³ is nonzero. A module-homomorphism structure is constructed rather
than inferred from scalar multilinearity alone.

Lean 4.34.1 compilation and independent replay passed without warnings.
Nine printed audits use only `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used; exact
source hashes and pinned Mathlib are in the verification JSON.

These equivalences are degreewise. No chain differential or its
compatibility, full exactness or Ext comparison is established here.
