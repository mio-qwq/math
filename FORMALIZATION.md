# Formalization status

The Lean files are pinned to Lean `4.34.1`. The currently published files import only its bundled `Std` library. All statements below have been compiled locally, and their axiom lists are printed by their source files. None uses `sorry`, an added axiom, or `native_decide`.

| File | Exact formal statement | Boundary |
| --- | --- | --- |
| [001/proof/Parity.lean](001-odd-half-order-hadamard/proof/Parity.lean) | Oddness, support multiplicity and cleared projection-trace equations are incompatible | Does not construct the complex projection or prove its trace formula |
| [001/proof/Examples.lean](001-odd-half-order-hadamard/proof/Examples.lean) | Cubic six-by-six row/column difference counts, their squares, Fourier-four opposite-root counts and fourth-root phase invariants | Exponent certificates; no formal bridge to complex matrices or the general rigidity theorem |
| [002/proof/SingleConflict.lean](002-weighted-rectangular-pruning/proof/SingleConflict.lean) | For every four natural-number costs, cover and pruning feasibility have the stated exact criterion; the scaled nonproduct example fails both | The full arbitrary rectangular rank argument and arbitrary real weights are not formalized |
| [003/proof/FiniteCore.lean](003-arc-one-parameter/proof/FiniteCore.lean) | All 1,000 basis triples of the explicit ten-dimensional table have equal encoded products, with output and coefficient bounds and two radical products | Fixed bit-polynomial table identities; the interpretation as a field algebra and the complete ARC realization are not formalized |

Replay from the repository root:

```sh
lean 001-odd-half-order-hadamard/proof/Parity.lean
lean 001-odd-half-order-hadamard/proof/Examples.lean
lean 002-weighted-rectangular-pruning/proof/SingleConflict.lean
lean 003-arc-one-parameter/proof/FiniteCore.lean
```

The proofs certify the propositions stated in these files. A formal proof of a supporting certificate is a formalization contribution, but it is not a formal proof of every theorem in the surrounding papers. Mathematical provenance and the specific formalization work are identified separately in the notes. No claim of first formalization or historical priority is made.
