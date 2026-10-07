# The lifted actual module map is not a boundary

`FiniteFreeBarNonboundary.lean` proves that no actual A-linear map from
the degree-two free term to the f-character module precomposes with
the actual degree-three boundary to give the specified lifted
degree-three map, whenever q³ is nonzero.

The quantifier includes all such module maps. The full Hom/cochain
equivalence and its proved differential compatibility turn any
purported preimage into a scalar bilinear boundary of the fixed
cochain, contradicting the independently proved q³ cycle obstruction.
In a ring without zero divisors, q nonzero suffices.

Lean 4.34.1 compilation and independent replay passed without warnings.
Three printed audits use only `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used;
exact hashes and pinned Mathlib are in the verification JSON.

Together with `FiniteFreeBarDegreeFour.lean`, the lifted map is closed
and not a boundary for the displayed actual module maps. An exact
projective resolution and identification with a separate Ext object
are still required before this becomes an Ext nonvanishing theorem.
