# Specialized five-term identities

`CochainSpecialization.lean` maps the actual polynomial cochain constants and five-term contractions through the existing `specialize q` ring homomorphism. The algebra constants remain the already proved `specializedConstants q`.

Every radical-basis five-term identity therefore holds over every commutative characteristic-two ring, for every parameter q. No field, nonzero parameter or absence of zero divisors is assumed for these identities. All three printed audits use standard axioms; compilation passed without warnings.

The scope remains basis closure. A full cochain complex, arbitrary radical-vector closure and the Ext interpretation require further arguments. Replay after the two imported local modules with `lake env lean CochainSpecialization.lean`.
