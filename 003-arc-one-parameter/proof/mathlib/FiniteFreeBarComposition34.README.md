# The full degree-three/four chain law

`FiniteFreeBarComposition34.lean` proves
`boundary3.comp boundary4 = 0` on the whole actual free A-module P4.
The coefficient ring is any commutative ring of characteristic two,
the parameter q is arbitrary, and eps is any actual R-algebra character.

The five degree-four faces are rewritten as genuine trilinear lifts.
Applying the proved four-face degree-three formula gives twenty terms
that cancel in ten pairs. Associativity, the central R-action,
character multiplicativity and characteristic two suffice. Every
A-valued coefficient is retained throughout; A need not be commutative.
The arbitrary-input identity then extends across the complete A-basis
of P4, without enumerating its 160000 words.

Compilation and independent replay results, six standard-axiom audits
and the exact source hash are in the verification JSON. This completes
the adjacent chain laws through P4. Higher exactness, a complete
projective resolution and an Ext comparison remain separate tasks.
