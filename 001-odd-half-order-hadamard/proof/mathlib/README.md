# Projection trace obstruction in Mathlib

`ProjectionTrace.lean` proves the actual linear-algebra statement over every characteristic-zero field: a finite-dimensional idempotent endomorphism cannot have twice its trace equal to an odd natural number. The proof obtains the integral trace from the rank of its range in Mathlib; the rank identity is not an added assumption.

This formalizes the trace-integrality step used by the analytical Hadamard argument. It does not yet construct the endomorphism from the matrix blocks or prove their trace formula, and it is not a full formalization of the main rigidity theorem.

`BlockObstruction.lean` goes further: for actual complex `m x m` matrices `A,B`, it proves that the equations `AᴴB=0` and `AAᴴ+BBᴴ=2mI`, together with unit squared moduli of `A`, contradict oddness of `m`. It constructs the projection, computes the Gram trace from the entries, and derives the integer rank obstruction entirely in Lean. The preceding Newton and support arguments constructing these blocks remain outside this file.

The file compiled successfully with Lean 4.34.1 and Mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. Its axiom audit lists only the standard `propext`, `Classical.choice`, and `Quot.sound`, without `sorryAx` or a compiler-trust axiom.

From this directory:

```sh
lake exe cache get Mathlib/LinearAlgebra/Trace.lean Mathlib/LinearAlgebra/Matrix/ConjTranspose.lean Mathlib/Basic/Complex/Basic.lean
lake env lean ProjectionTrace.lean
lake env lean BlockObstruction.lean
```

The package pins Mathlib, the Lean toolchain and transitive dependencies in `lake-manifest.json`. Both source files compiled successfully and use only the standard three axioms listed above. They use the library's established projection/trace theorem and record our application to the Hadamard block obstruction; no priority claim is made about standard library facts.
