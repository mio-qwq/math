# Four-linear extension of the five-face formula

`FiniteHochschild.lean` defines the five-face expression using the actual finite bilinear multiplication and trilinear evaluation. It proves linearity in each of its four inputs, expands four finite weighted sums, and deduces that vanishing on selected basis quadruples implies vanishing on their entire finite span.

This is a general commutative-semiring theorem; no associativity, radical closure or cochain-complex hypothesis is needed for this extension argument. The formula is unsigned. In characteristic two its signs agree with the degree-three Hochschild differential.

All four printed audits use standard axioms and compilation passed without warnings. The generic file assumes basis vanishing when using its final extension theorem; the actual table premise is supplied separately by `TwentyDimCochain.lean`.
