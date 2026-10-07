# Formalization status

The Lean files are pinned to Lean `4.34.1`. Most use its bundled `Std` library; the isolated `001/proof/mathlib` package pins Mathlib as well. All statements below have been compiled locally, and their axiom lists are printed by their source files. None uses `sorry`, an added axiom, or `native_decide`.

| File | Exact formal statement | Boundary |
| --- | --- | --- |
| [001/proof/Parity.lean](001-odd-half-order-hadamard/proof/Parity.lean) | Oddness, support multiplicity and cleared projection-trace equations are incompatible | Does not construct the complex projection or prove its trace formula |
| [001/proof/Examples.lean](001-odd-half-order-hadamard/proof/Examples.lean) | Cubic six-by-six row/column difference counts, their squares, Fourier-four opposite-root counts and fourth-root phase invariants | Exponent certificates; no formal bridge to complex matrices or the general rigidity theorem |
| [001/proof/Support.lean](001-odd-half-order-hadamard/proof/Support.lean) | Four-phase collapse and the odd support-count obstruction for every phase system satisfying the explicit cancellation laws | The complex-ratio and Newton-identity hypotheses are not yet connected to this abstract statement |
| [001/proof/mathlib/ProjectionTrace.lean](001-odd-half-order-hadamard/proof/mathlib/ProjectionTrace.lean) | Every finite-dimensional idempotent over a characteristic-zero field has integral trace, excluding the odd half-trace equation | Uses pinned Mathlib; construction from the Hadamard blocks is still separate |
| [002/proof/SingleConflict.lean](002-weighted-rectangular-pruning/proof/SingleConflict.lean) | For every four natural-number costs, cover and pruning feasibility have the stated exact criterion; the scaled nonproduct example fails both | The full arbitrary rectangular rank argument and arbitrary real weights are not formalized |
| [003/proof/FiniteCore.lean](003-arc-one-parameter/proof/FiniteCore.lean) | All 1,000 basis triples of the explicit ten-dimensional table have equal encoded products, with output and coefficient bounds and two radical products | Fixed bit-polynomial table identities; the interpretation as a field algebra and the complete ARC realization are not formalized |
| [003/proof/FiniteCoreT.lean](003-arc-one-parameter/proof/FiniteCoreT.lean) | All 8,000 twenty-dimensional basis triples, both coefficient bounds, the dual recurrences, unit actions and all 400 trace pairings | Same fixed bit-polynomial scope; not the complete ARC realization |

Replay from the repository root:

```sh
lean 001-odd-half-order-hadamard/proof/Parity.lean
lean 001-odd-half-order-hadamard/proof/Examples.lean
lean 001-odd-half-order-hadamard/proof/Support.lean
lean 002-weighted-rectangular-pruning/proof/SingleConflict.lean
lean 003-arc-one-parameter/proof/FiniteCore.lean
```

To compile `FiniteCoreT.lean`, first build its imported module. In PowerShell:

```powershell
$env:LEAN_PATH = (Resolve-Path '003-arc-one-parameter/proof').Path
lean -o 003-arc-one-parameter/proof/FiniteCore.olean 003-arc-one-parameter/proof/FiniteCore.lean
lean 003-arc-one-parameter/proof/FiniteCoreT.lean
```

The proofs certify the propositions stated in these files. A formal proof of a supporting certificate is a formalization contribution, but it is not a formal proof of every theorem in the surrounding papers. Mathematical provenance and the specific formalization work are identified separately in the notes. No claim of first formalization or historical priority is made.
