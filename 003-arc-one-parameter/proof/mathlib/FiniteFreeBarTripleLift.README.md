# The full trilinear free-module lift

`FiniteFreeBarTripleLift.lean` constructs the genuine R-trilinear map
`L3 : A →ₗ[R] A →ₗ[R] A →ₗ[R] P3`, with its complete finite coordinate
formula. All three slots range over the installed table algebra.

It proves in the entire A-valued module P2 that

`boundary3(L3(x,y,z)) = x • L2(y,z) + L2(x*y,z) + L2(x,y*z) + eps(z) • L2(x,y)`.

The first face keeps the noncommutative A-action; central R-actions are
used only for scalar coefficients. Equality of the full trilinear maps
is proved by the complete basis in all three input slots. No character
projection or restriction to selected input words is used.

Compilation and independent replay results, six printed standard-axiom
audits and the exact source hash are recorded in the verification JSON.
This file supplies lift semantics; it does not prove higher exactness,
an all-degree resolution or an Ext comparison.
