# Full pair lifts and the degree-two/three chain law

`FiniteFreeBarPairLift.lean` constructs a genuine R-bilinear lift of every
pair of elements of the actual noncommutative table algebra into P2.
It proves its full coordinate formula and the three-face identity

`boundary2(L2(x,y)) = x • L1(y) + L1(x*y) + eps(y) • L1(x)`.

The four faces of boundary3 then cancel after boundary2, giving
`boundary2.comp boundary3 = 0` on the entire actual free A-module P3.
All A-valued coefficients and the true left action are retained.
Character-valued Hom maps are not used to separate A coefficients.

Lean 4.34.1 first compilation and independent replay passed with zero
warnings. Ten printed audits use only `propext`, `Classical.choice` and
`Quot.sound`. The verification JSON records the exact source hash and
pinned Mathlib. No `sorry`, added axiom or `native_decide` is used.

This is a general adjacent chain-composition proof, not exactness at P1
or higher degrees, a full projective resolution, or an Ext comparison.
