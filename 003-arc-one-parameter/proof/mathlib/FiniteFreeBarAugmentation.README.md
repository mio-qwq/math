# An actual right-end projective presentation

`FiniteFreeBarAugmentation.lean` constructs the actual A-linear
augmentation of the degree-zero free term to the character module and
the degree-one A-linear boundary. A basis letter b is sent to
b minus the scalar element with value eps(b).

The augmentation is surjective and kills the degree-one boundary.
Every element in its kernel has an explicit boundary preimage: lift
its actual R-coordinates to scalar elements of A in the degree-one
free term. The lifted boundary is the original algebra element minus
its scalar character value. Hence the augmentation kernel equals the
boundary image, proving exactness at degree zero. All maps retain the
noncommutative left A-action; the auxiliary defect is only R-linear.

The two terms are actual free/projective left modules from
`FiniteFreeBarModules.lean`. These results hold at every parameter over
every commutative characteristic-two ring and for every actual
R-algebra character, without a field or nonzero-parameter condition.

Lean 4.34.1 compilation and independent replay passed without warnings.
Ten printed audits use at most `propext`, `Classical.choice` and
`Quot.sound`. No `sorry`, added axiom or `native_decide` is used; exact
hashes are in the verification JSON.

This is a right-end projective presentation. Exactness at degree one,
higher differentials, a full projective resolution and the Ext
comparison remain open.
