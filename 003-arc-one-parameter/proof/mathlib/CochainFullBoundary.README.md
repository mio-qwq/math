# Excluding full vector-valued boundaries

`CochainFullBoundary.lean` strengthens the internal scalar obstruction to the complete four-face basis boundary of an arbitrary vector-valued two-cochain G. Both outer faces use the actual table multiplication; the two inner faces use its actual structure constants.

The f coordinate of the outer faces vanishes on the cycle inputs `(6,1,17)` and `(6,2,17)`. This is proved from two small sets of twenty kernel-checked sparse output-label facts. Projecting the full boundary to f therefore gives exactly the scalar internal differential already annihilated by the cycle functional.

Consequently the fixed vector-valued P cannot be a full boundary. More strongly, no boundary can agree with it on both cycle triples, even without imposing conditions on the other triples. This holds over F₂[X] and after any commutative characteristic-two specialization with q³ nonzero; a nonzero q in a ring without zero divisors suffices.

All eight audits compile without warnings and use standard axioms. No large closure enumeration is repeated. The conclusion is non-membership in the image of the displayed full basis-boundary formula. Identifying this with a specific Hochschild or Ext cohomology object still requires the complex correspondence.
