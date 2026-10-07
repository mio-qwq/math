# The cochain on the actual algebra

`TwentyDimCochainAlgebra.lean` packages the fixed table cochain as three nested R-linear maps on `TableAlgebra q`. Its basis values are exactly the attributed cochain constants. The actual algebra's five-face differential vanishes on every four elements in the eighteen-label span.

The file also proves a coordinate expansion for every element and every bilinear map. Using these expansions, the full actual-algebra degree-two differential on basis inputs is identified with the previously defined four-face coordinate boundary, including both outer multiplications.

When q³ is nonzero, no genuine R-bilinear cochain has this trilinear map as its full coboundary. It cannot even match on the two cycle triples. A nonzero q in a ring without zero divisors suffices. These are statements about the installed algebra and actual linear maps, not just unconstrained coordinate arrays.

All eight audits compiled without warnings and use standard axioms. Closure remains proved on the eighteen-label span. Full-input closure, relative balancing, identification with a standard cohomology object, and the complete ARC realization remain separate.
