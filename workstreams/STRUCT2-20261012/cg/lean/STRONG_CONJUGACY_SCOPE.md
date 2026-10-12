# Universal conjugacy and fold-class scope

`StrongConjugacy.lean` completes the next formal layer for every odd `n >= 3`.
It uses the actual coordinate actions and the exhaustive `24*n` parametrization;
no abstract dihedral presentation or finite catalogue is assumed.

The file proves:

* both half-turn strong switches commute with every actual automorphism and
  hence each is a singleton conjugacy class;
* every odd reflected ring-swap is conjugate to exponent one, using the
  explicit rotation by `floor(a/2)`;
* the two half-turn classes and reflected class are pairwise nonconjugate;
* every actual strong switch belongs to one of exactly those three classes;
* the existing universal theorem “folds are isomorphic iff their switches are
  conjugate” converts these into exactly three pairwise nonisomorphic fold
  classes;
* the swapped half-turn is pointwise the original CG deck, leaving exactly
  two nonoriginal fold classes.  This is packaged as
  `exactly_two_cousin_folds`.

The certificate is a theorem about all actual strongly switching automorphisms
and their folds.  The standard converse saying that every finite simple graph
with this connected canonical double cover arises from such a switch remains
the written argument in `cg/independent/INDEPENDENT_RECONSTRUCTION.md`; it has
not been repackaged as a new arbitrary-base Lean interface in this stage.

The finite original-definition checker from the preceding stage already
independently obtains class sizes `1,1,3*n` for `n=3,5,7,9`.  Those checks are
corroboration only; the new conjugacy theorem is symbolic for every odd
`n>=3`.

Verification is recorded in
`verification/20261013-cg-strong-conjugacy/verification.json`.  A clean
eleven-module rebuild with the official Lean 4.34.1 release passed 157 named
axiom audits without errors or warnings.  The axiom union is only `propext`,
`Classical.choice`, and `Quot.sound`; there is no `sorryAx`.  The companion
literal-definition run again checked 3,744 explicit parameters and all three
damage controls, without rerunning an automorphism search.
