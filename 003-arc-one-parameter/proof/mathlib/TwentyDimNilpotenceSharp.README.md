# A fivefold witness and the exact word threshold

`TwentyDimNilpotenceSharp.lean` proves in the actual algebra that the
ordered kernel word [u,t,u,t,Z] has product q(1+q) times E. Each of its
five factors lies in the established augmentation kernel. The proof
uses five small sparse table products followed by their actual
specialized algebra semantics; there is no long-word enumeration.

When q(1+q) is nonzero, this word has nonzero product. Thus no uniform
word-length vanishing threshold at most five can hold. Combined with
the independently proved fact that every kernel word of length at
least six vanishes, the threshold is exactly six under this condition.
The witness condition is kept explicit over rings with zero divisors.

Lean 4.34.1 compilation and independent replay passed without warnings.
Nine printed audits use at most `propext`, `Classical.choice` and
`Quot.sound`; the small table certificate needs no axioms. No `sorry`,
added axiom or `native_decide` is used. Exact source hashes and pinned
Mathlib are in the verification JSON.

This is an exact threshold for ordered words in the specified
augmentation kernel under the displayed condition. It does not
identify the Jacobson radical, calculate Loewy layers, prove a special
parameter threshold or establish the complete ARC realization.
