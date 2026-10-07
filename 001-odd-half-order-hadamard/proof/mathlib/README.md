# Projection trace obstruction in Mathlib

`ProjectionTrace.lean` proves the actual linear-algebra statement over every characteristic-zero field: a finite-dimensional idempotent endomorphism cannot have twice its trace equal to an odd natural number. The proof obtains the integral trace from the rank of its range in Mathlib; the rank identity is not an added assumption.

This formalizes the trace-integrality step used by the analytical Hadamard argument. It does not yet construct the endomorphism from the matrix blocks or prove their trace formula, and it is not a full formalization of the main rigidity theorem.

`BlockObstruction.lean` goes further: for actual complex `m x m` matrices `A,B`, it proves that the equations `AᴴB=0` and `AAᴴ+BBᴴ=2mI`, together with unit squared moduli of `A`, contradict oddness of `m`. It constructs the projection, computes the Gram trace from the entries, and derives the integer rank obstruction entirely in Lean. The preceding Newton and support arguments constructing these blocks remain outside this file.

The file compiled successfully with Lean 4.34.1 and Mathlib commit `d13f23b723b8a846827a245b89c10fc7d3f11612`. Its axiom audit lists only the standard `propext`, `Classical.choice`, and `Quot.sound`, without `sorryAx` or a compiler-trust axiom.

`BlockRanks.lean` proves the exact rank statement for every positive block size under the same Gram equations: `2 * A.rank = m` and `2 * B.rank = m`. Only `A` needs unit squared moduli; the total Gram trace supplies the trace of `BBᴴ`. Both determinants are then zero. An intermediate theorem replaces the unit-modulus assumption by the single explicit Gram trace equation. No rank identity is assumed: the proof constructs the projection and relates its range to the actual matrix rank. This file compiled successfully and its five axiom audits list only the same standard three axioms.

`ComplexSupport.lean` connects the abstract `../Support.lean` cancellation argument to actual nonzero complex values. Under the explicit at-most-two-values hypothesis, both nonconstant phases equal `-1`; the actual value `1` has multiplicity `2*t`, excluding an odd required multiplicity. It also handles the row-ratio form with an inverse phase. See [the exact scope and replay instructions](ComplexSupport.md); deriving these hypotheses from the original Hadamard matrix remains separate.

From this directory:

```sh
lake exe cache get Mathlib/LinearAlgebra/Trace.lean Mathlib/LinearAlgebra/Matrix/ConjTranspose.lean Mathlib/LinearAlgebra/Matrix/Rank.lean Mathlib/Basic/Complex/Basic.lean Mathlib/Algebra/Ring/Commute.lean
lake env lean ProjectionTrace.lean
lake env lean BlockObstruction.lean
lake env lean BlockRanks.lean
lean -o ../Support.olean ../Support.lean
LEAN_PATH=.. lake env lean ComplexSupport.lean
```

For PowerShell, set `$env:LEAN_PATH = (Resolve-Path '..').Path` before the final command and omit its `LEAN_PATH=..` prefix, restoring the previous value afterward.

The package pins Mathlib, the Lean toolchain and transitive dependencies in `lake-manifest.json`. All four source files compiled successfully and use only the standard three axioms listed above. They use the library's established field, projection and trace theorems and record our application to the Hadamard phase and block obstructions; no priority claim is made about standard library facts.
