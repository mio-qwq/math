# MUB triplets: complete companion compatibility

This direction studies public structural conjectures about actual
six-dimensional MUB triplets, with precise literature and proof boundaries.
It does not announce a solution of the maximum-number problem.

- [Literature and overlap review](LITERATURE.md) distinguishes the 2026
  journal conjectures, subsequent proof claims, and actual OpenAI Lean scope.
- [Spectral companion criterion](spectral-companion.md) proves in writing
  an equivalence between a complete third basis and one Hermitian observable
  with a fixed simple spectrum and five uniform diagonal power moments.
- The same note proves a conditional branch: a double anticommutation
  witness gives four circulant blocks; one first-character zero then forces
  both cubic-character zeros. Existence of that additional witness in
  general is unproved.
- [Fixed-companion witness criterion](fixed-companion-witness.md) decides
  that additional condition by a shared monomial pairing. An exact genuine
  triplet has a fixed companion for which the condition fails, while an
  alternative companion works. Diagonal reflection product alone is
  insufficient at repeated eigenvalues.
- [SpectralMomentWeights.lean](proof/SpectralMomentWeights.lean) formalizes
  the exact six-weight reconstruction, with three axiom audits. The matrix
  spectral theorem and the companion/anticommutation bridges remain written.

The methods use standard spectral interpolation, MUB observables and
Fourier diagonalization. Originality of the reformulation is not established.
Known theorems and conditional reductions are kept separate from the public
coupling target. The current concrete missing step is to control compatible
spectral witnesses without assuming the two anticommutation equations.

## Reproduce the supporting Lean proof

Use the pinned Lean 4.34.1 and Mathlib package shared with 002. From the
repository root, after obtaining that package's pinned dependencies:

```sh
cd 002-weighted-rectangular-pruning/proof/mathlib
lake env lean ../../../004-mub-triplets/proof/SpectralMomentWeights.lean
```

The source-specific [verification record](proof/SpectralMomentWeights.verification.json)
and [actual independent audit output](proof/SpectralMomentWeights.audit.txt)
record the two compiler runs against the same source hash. The proof source
uses neither `sorry`, `native_decide` nor a new axiom. The supporting proof is a
finite linear-system theorem over arbitrary real weights, not a numerical
search or a formal proof of the full MUB conjecture.
