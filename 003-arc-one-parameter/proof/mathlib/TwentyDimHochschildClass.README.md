# A nonzero actual degree-three Hochschild cochain class

`TwentyDimHochschildClass.lean` transfers full-input closure to the installed
twenty-dimensional algebra and constructs the class of its specified
trilinear cochain in `ARCHochschildDegreeThree.H3`.

This quotient uses all R-linear bilinear, trilinear and four-linear cochains
on the actual algebra, with the full four- and five-face Hochschild
differentials in characteristic two. It is the kernel of d3 modulo the
image of d2. Closure is proved on every algebra input, including the two
idempotents. The earlier q^3 separating witness excludes every genuine
bilinear boundary. Consequently the constructed class is nonzero and
this quotient is nontrivial whenever q^3 is nonzero. Over a ring without
zero divisors, q nonzero suffices; in particular this holds over every
characteristic-two field at every nonzero parameter.

The source was compiled and independently replayed with Lean 4.34.1 and
the pinned Mathlib revision. All seven printed audits use only `propext`,
`Classical.choice` and `Quot.sound`. There is no `sorry`, added axiom or
`native_decide`; the verification JSON records the exact source hash.

This is a nonvanishing theorem in the explicitly constructed Hochschild
cochain quotient. No identification with a separate Ext object, all-degree
resolution, stable extension profile or complete ARC counterexample is
proved here. The algebra and cochain data are attributed in
`../../ATTRIBUTION.md`; no historical priority claim is made.
