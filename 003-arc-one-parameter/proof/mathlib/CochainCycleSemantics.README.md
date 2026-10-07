# A universal scalar internal-coboundary obstruction

`CochainCycleSemantics.lean` proves a universal statement about the actual table, not a test over a finite list of cochains. Let G be any scalar two-cochain and define its internal differential by

`D2(G)(a,b,c) = sum_j B(a,b,j)G(j,c) + sum_j B(b,c,j)G(a,j)`.

The cycle functional `lambda(F) = X^2 F(6,1,17) + F(6,2,17)` annihilates `D2(G)` for every G. This follows from four actual sparse table products. By transporting the frozen encoded cycle-pairing certificate, the same functional takes value `X^3`, which is nonzero, on the f coordinate of the fixed cochain. Thus that coordinate cannot be an internal scalar coboundary; it cannot even agree with one on both displayed radical triples.

Under any commutative characteristic-two specialization, the pairing becomes q³. The obstruction holds whenever q³ is nonzero, and in particular whenever q is nonzero in a ring without zero divisors. Merely assuming q is nonzero in a general ring would not suffice.

All eleven audits compile without warnings and use only the standard three axioms. This proves non-membership in the image of the explicitly defined two-face scalar differential. It does not yet identify that operator with a complete Hochschild/Ext complex or establish a nonzero Ext class.

Replay with `lake env lean CochainCycleSemantics.lean` after its imported semantic modules and frozen `CochainData.olean` are built.
