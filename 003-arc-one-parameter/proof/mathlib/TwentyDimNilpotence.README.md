# Sixfold vanishing in the actual augmentation kernel

`TwentyDimNilpotence.lean` proves that every ordered list of at least six
actual algebra elements in the e/f augmentation kernel has product zero.
In particular, every kernel element has sixth power zero. The conclusion
holds over every commutative characteristic-two ring at every parameter q,
without a field or nonzero-parameter assumption.

The proof uses the positive grading recorded in the attributed upstream
algebra note. The two idempotent labels have degree zero, every other
label has positive degree, and all degrees are at most five. Kernel
`decide` checks homogeneity for the 400 multiplication-table pairs, the
20 degree bounds and the 20 zero-degree label classifications. Genuine
polynomial support and specialization then give a multiplicative
filtration on arbitrary algebra elements. An ordinary list induction
puts a length-n kernel word in filtration n, which vanishes for n at
least six. No long-word enumeration is used.

Lean 4.34.1 compilation and independent replay passed without warnings.
Ten printed audits use at most `propext`, `Classical.choice` and
`Quot.sound`; the first two finite certificates need no axioms.
No `sorry`, added axioms or `native_decide` are used. Exact source hashes
and the pinned Mathlib revision are recorded in the verification JSON.

This proves a uniform sixfold upper bound. It does not prove that this
bound is sharp at any parameter, identify the Jacobson radical or the
Loewy layers, or construct the full ARC homological realization.
See `../../ATTRIBUTION.md` for the upstream source and license.
