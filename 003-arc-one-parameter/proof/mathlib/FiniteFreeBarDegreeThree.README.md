# The actual degree-three boundary and full cochain compatibility

`FiniteFreeBarDegreeThree.lean` constructs the actual A-linear map from
the degree-three free term to the degree-two term with all four faces.
The endpoints use left multiplication and the actual character;
both interior products use the full specialized structure constants.

For every actual A-linear degree-two map to the character module,
precomposing by this boundary corresponds exactly to the full
character-valued cochain d2 under the proved Hom/cochain equivalences.
The equality holds in the complete scalar trilinear cochain module,
on all algebra inputs. The inverse compatibility is also proved for
every scalar bilinear cochain.

Lean 4.34.1 compilation and independent replay passed without warnings.
Seven printed audits use only `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used;
exact hashes and pinned Mathlib are in the verification JSON.

This file does not prove the preceding chain boundary composed with
this map is zero. Character-valued Hom maps do not separate all
algebra coefficients, so their compatibility alone cannot prove that
chain identity. Higher exactness, a full resolution and Ext remain open.
