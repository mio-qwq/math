# The degree-three Hochschild cochain quotient

`HochschildDegreeThree.lean` applies the cycles-modulo-boundaries construction to the actual full Hochschild cochain maps C²→C³→C⁴ in characteristic two. Its `H3 R A` is the module of trilinear cocycles modulo full bilinear coboundaries.

A class is zero exactly when the cochain is an actual bilinear coboundary. Consequently any fully closed cochain with the proved non-boundary property gives a nonzero class. All three audits compile without warnings and use standard axioms.

This constructs the degree-three cochain quotient explicitly. It does not construct an all-degree resolution or prove an isomorphism with a separately defined Ext group. In particular, applying it to the fixed table cochain still requires closure on all algebra inputs, not just on the augmentation kernel.
