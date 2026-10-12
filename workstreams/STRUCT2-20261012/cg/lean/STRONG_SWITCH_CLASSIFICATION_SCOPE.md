# Exact strong-switch classification scope

`StrongSwitchClassification.lean` closes the strong-switch membership problem
for the actual synchronized canonical double cover of `CG(n)`, for every odd
`n >= 3`.  It imports the previously proved exhaustive `24*n` automorphism
parametrization rather than assuming a dihedral group presentation.

The proved equivalence is the following.  Write an arbitrary automorphism in
its unique parameter form `(a, positive, swap)`, with `a` modulo `6*n`.
It is strongly switching exactly when

* `positive = true` and `a = 3*n`, with either value of `swap`; or
* `positive = false`, `swap = true`, and `a` is odd.

Thus the file proves necessity and sufficiency of the written list
`r^(3n)`, `r^(3n) tau`, and `r^a f tau` for odd `a`.  In particular there
are no missing strong switches outside the explicit automorphism family.

The proof checks the three defining conditions separately.  Parity formulae
on rotations and reflections prove bipartition reversal.  The half-turn and
every reflection are proved involutive on rings, leaves, and centres.  Direct
adjacency proofs establish nonadjacency for the two valid families.  Conversely,
an odd rotational involution is forced arithmetically to have exponent `3*n`;
an odd reflection without ring interchange sends the explicit ring vertex
`floor(a/2)` to its cyclic successor and therefore fails strongness.

Verification receipt:
`verification/20261013-cg-strong-switches/verification.json`.  The ten-module
Lean 4.34.1 dependency rebuild passed 141 named axiom audits, without errors
or warnings.  Its axiom union is only `propext`, `Classical.choice`, and
`Quot.sound`; there is no `sorryAx`.

The independent literal-original-definition check evaluates all `24*n`
explicit parameters at `n = 3,5,7,9,31,101` (3,744 parameters), obtains
exactly `3*n+2` strong switches each time, and detects three damaged formulae.
It additionally obtains conjugacy class sizes `1,1,3*n` at `n = 3,5,7,9`.
Those finite conjugacy checks are corroboration, not the universal proof.

Not yet claimed by this stage: a universal Lean proof of the three conjugacy
classes, the resulting three fold-isomorphism classes, or the final
exactly-two-TF-cousins theorem.  Those are the next formal layer.  The written
classification already contains their mathematical proof, but its status is
not upgraded by the membership theorem alone.
