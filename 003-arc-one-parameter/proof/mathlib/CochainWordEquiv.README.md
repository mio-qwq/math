# Full scalar cochains and word coefficients

`CochainWordEquiv.lean` gives R-linear equivalences between all scalar
bilinear and trilinear cochains on the actual table algebra and all
scalar functions on its degree-two and degree-three basis words.

Repeated actual basis extension supplies mutually inverse maps for
arbitrary pair/triple coefficients. Ordered words are packed with
`Fin.cons`; unpacking covers every word, without enumeration. Forward
maps evaluate on the actual coordinate basis. Inverse maps on arbitrary
algebra inputs are the full finite twofold or threefold coordinate
contractions. No selected coefficient subspace is imposed.

Lean 4.34.1 compilation and independent replay passed without warnings.
Ten printed audits use at most `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used; exact
source hashes and pinned Mathlib are in the verification JSON.

These are degreewise full-space equivalences, without a statement about
bar differentials, exactness, a projective resolution or Ext.
