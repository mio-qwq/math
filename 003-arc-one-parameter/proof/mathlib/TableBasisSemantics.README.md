# Table associativity in genuine polynomial vectors

`TableBasisSemantics.lean` transports the frozen ten-label and twenty-label associativity certificates into `Nat → Polynomial (ZMod 2)`, using the generic left/right product interpretation from `TermSemantics`.

Both independently verified composed-coefficient bounds are required. The left bound controls each actually packed product in the left expression; the right bound separately controls the right expression. With those bounds, the packed equality gives an actual polynomial-vector equality. No new enumeration is performed.

The resulting theorems hold for every `Fin 10` and `Fin 20` basis triple. They prove the intended sparse basis-product expressions, rather than only an equality of natural-number codes. Extending this to a defined multiplication on all finite vectors requires the finite contraction step and bilinear extension; this source alone does not install an algebra instance or establish the full ARC realization.

All three axiom audits report only the standard three axioms. Compilation succeeded without warnings, and the source hash is recorded in `TableBasisSemantics.verification.json`.

Build `../FiniteCoreT.olean` after `../FiniteCore.olean` using the original Std instructions, and keep both local module directories on `LEAN_PATH`. After the earlier Mathlib bridge prerequisites:

```sh
LEAN_PATH=.:.. lake env lean -o TermSemantics.olean TermSemantics.lean
LEAN_PATH=.:.. lake env lean TableBasisSemantics.lean
```

On Windows use the semicolon-separated paths from the BytePacking README.
