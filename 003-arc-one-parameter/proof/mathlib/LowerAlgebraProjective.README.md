# Projectivity over the actual lower algebra

[LowerAlgebraProjective.lean](LowerAlgebraProjective.lean) proves that
the actual left corners Ce and Cf are projective over C, for every
commutative coefficient ring of characteristic two and every q.

The maps a↦ae and a↦af are specified C-linear retractions from the
regular C-module onto the corners. Their composites with the actual
inclusions are identities, so the split-summand theorem proves
module-theoretic and categorical projectivity. The coefficient-ring
bases in the preceding source are not used as substitutes for C-bases.

The source restricts the installed f-character along the actual
subalgebra inclusion. Its character module has the actual C-action,
and Cf maps onto it by its f coordinate. The e idempotent acts as zero
on this module. Since Ce is generated over C by the actual element e,
every C-linear map from Ce into this character module is zero.

The carrier named `Simple` is a character-module wrapper. This file
does not assert simplicity over arbitrary commutative rings.
[The next source](LowerAlgebraCategoricalResolution.README.md) retains
these projective corners and augmentation in a genuine all-degree
resolution over fields satisfying the indicated power conditions.
