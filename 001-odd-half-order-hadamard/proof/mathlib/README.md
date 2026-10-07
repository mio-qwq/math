# Projection trace obstruction in Mathlib

`ProjectionTrace.lean` proves the actual linear-algebra statement over every characteristic-zero field: a finite-dimensional idempotent endomorphism cannot have twice its trace equal to an odd natural number. The proof obtains the integral trace from the rank of its range in Mathlib; the rank identity is not an added assumption.

This formalizes the trace-integrality step used by the analytical Hadamard argument. It does not yet construct the endomorphism from the matrix blocks or prove their trace formula, and it is not a full formalization of the main rigidity theorem.

The file compiled successfully with Lean 4.34.1 and Mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. Its axiom audit lists only the standard `propext`, `Classical.choice`, and `Quot.sound`, without `sorryAx` or a compiler-trust axiom.

From this directory:

```sh
lake update
lake exe cache get Mathlib/LinearAlgebra/Trace.lean
lake env lean ProjectionTrace.lean
```

The package pins Mathlib and the Lean toolchain. The source uses the library's established projection/trace theorem and records our application to the odd trace obstruction; it makes no priority claim about that standard linear-algebra fact.
