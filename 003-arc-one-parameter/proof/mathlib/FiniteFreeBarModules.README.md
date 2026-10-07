# Actual finite free candidate bar terms

`FiniteFreeBarModules.lean` defines, in every degree n, the actual left
module of algebra-valued functions on n-letter words in the twenty
basis labels. The action is left multiplication in the installed
noncommutative table algebra.

The standard coordinate basis gives free, finite and projective module
instances. The same object is projective in `ModuleCat`. The displayed
basis has cardinal 20^n, including the single basis element at n = 0.
This is the cardinal of the exhibited basis, with no assertion about
an invariant rank over an arbitrary ring.

Lean 4.34.1 compilation and independent replay passed without warnings.
Eight printed audits use at most `propext`, `Classical.choice` and
`Quot.sound`; no `sorry`, added axiom or `native_decide` is used.
Exact source hashes are in the verification JSON.

These are degreewise candidate free left-module terms. No differential,
augmentation, exactness, projective resolution, tensor identification
or Ext comparison is constructed in this source.
