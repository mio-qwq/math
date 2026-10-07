# All actual A-linear maps to the character module

`FiniteFreeBarHom.lean` constructs an R-linear equivalence between all
A-linear maps from each degree-n free candidate term to an actual
character module and all scalar functions on its word basis.

The forward map evaluates an A-linear map on each actual basis vector
and takes its module value. The inverse sends any free-module vector v
to the sum of eps(v at w) times the prescribed scalar value at w.
This uses the actual character A-action. Every scalar function is
allowed, and the maps are proved mutually inverse. The f-character
application uses the installed algebra augmentation and actual module.

Lean 4.34.1 compilation and independent replay passed without warnings.
Six printed audits use at most `propext`, `Classical.choice` and
`Quot.sound`; no `sorry`, added axiom or `native_decide` is used.
Exact source hashes are in the verification JSON.

This proves a full Hom/word-value correspondence. It does not yet
identify scalar multilinear cochains, transport a bar differential,
prove exactness or establish an Ext comparison.
