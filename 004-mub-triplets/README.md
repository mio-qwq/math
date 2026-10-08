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
- [Exact scope of the symmetry route](four-circulant-route.md) proves that
  existence of a suitably chosen double-anticommutation companion witness
  is equivalent to four-circulantization preserving the displayed triples.
  Sixteen pairs of three-cycles give an exact phase test. The converse
  companion construction is classical Zauner theory, including zero modes.
- [SpectralMomentWeights.lean](proof/SpectralMomentWeights.lean) formalizes
  the exact six-weight reconstruction, with three axiom audits. The matrix
  spectral theorem and the companion/anticommutation bridges remain written.
- [SpectralMatchingSupport.lean](proof/SpectralMatchingSupport.lean)
  proves that actual complex matrix anticommutation with the fixed diagonal
  spectrum is equivalent to support on the opposite-node matching. It has
  three separate audits; unitary monomial phases and the companion
  conjugation bridges are outside that proof.
- [SpectralMatchingUnitary.lean](proof/SpectralMatchingUnitary.lean) completes
  the fixed-node unitary Hermitian phase classification using actual Gram
  products. The forward direction derives unit-modulus partner entries;
  the converse constructs both unitary equations, Hermitian symmetry and
  the anticommutator. Three new audits have a separate independent replay.

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
lake env lean ../../../004-mub-triplets/proof/SpectralMatchingSupport.lean
```

For the import-based phase theorem, from that same Mathlib directory:

```sh
P="../../../004-mub-triplets/proof"
lake env lean --root "$P" -o "$P/SpectralMatchingSupport.olean" "$P/SpectralMatchingSupport.lean"
LEAN_PATH="$(cd "$P" && pwd):${LEAN_PATH:-}" lake env lean "$P/SpectralMatchingUnitary.lean"
```

On PowerShell use the host path-list separator and an absolute import directory:

```powershell
$proofDir = (Resolve-Path '../../../004-mub-triplets/proof').Path
lake env lean --root $proofDir -o (Join-Path $proofDir 'SpectralMatchingSupport.olean') (Join-Path $proofDir 'SpectralMatchingSupport.lean')
$env:LEAN_PATH = $proofDir + [IO.Path]::PathSeparator + $env:LEAN_PATH
lake env lean (Join-Path $proofDir 'SpectralMatchingUnitary.lean')
```

The source-specific [verification record](proof/SpectralMomentWeights.verification.json)
and [actual independent audit output](proof/SpectralMomentWeights.audit.txt)
record the two compiler runs against the same source hash. The proof source
uses neither `sorry`, `native_decide` nor a new axiom. The supporting proof is a
finite linear-system theorem over arbitrary real weights, not a numerical
search or a formal proof of the full MUB conjecture.

The matrix-support source has its own
[verification record](proof/SpectralMatchingSupport.verification.json)
and [actual audit output](proof/SpectralMatchingSupport.audit.txt).
Its premise uses ordinary matrix multiplication, rather than assuming
the desired entrywise support. It supplies an additional fixed-spectrum
interface without asserting unitarity or Hermitian companion existence.

The new phase classification has its own
[verification record](proof/SpectralMatchingUnitary.verification.json)
and [actual independent audit output](proof/SpectralMatchingUnitary.audit.txt).
It concerns an actual matrix B with the fixed reverse matching, not shared
matchings for two coordinate involutions or existence of a complete companion.
The four-circulant converse and phase test remain written matrix proofs with
a [separate full-source review](four-circulant-route.review.json).

The [direct four-circulant character proof](direct-circulant-character.md)
now removes the extra first-character premise in the known symmetry
branch. All four phase-retrieval cases give the exact block product
cancellation, hence both first and cubic characters vanish. The actual
six-column/adjoint character formulas and conditional cubic implications
have a separate six-audit Lean interface; the full Gram-to-cancellation
argument remains written mathematics. General companion circulantization
and the general coupling conjecture remain open.

The [scalar zero-mode obstruction](zero-mode-obstruction.md) has six Lean
audits. The subsequent [actual Gram and inverse proof](gram-block-invertibility.md)
now discharges its mode-bound premise: actual matrix Gram equations give
all four bounds and actual flatness excludes all zero modes. Three more
audited statements factor the actual block determinants and construct four
actual inverse matrices with all eight multiplication equations. No extra
mode bounds, nonzero modes or inverses are assumed. The subsequent
[actual phase retrieval](phase-retrieval-alternatives.md) also formalizes
the cyclic-shift/adjoint reconstruction, including repeated ratios. The full
Gram-to-product-cancellation theorem remains written mathematics.

The [opposite block power proof](mode-power-matching.md) derives matching
Fourier powers of a/e and b/c from the same actual Gram equation, with
three further independently replayed Lean audits. Flatness, block inverses
and a second Gram equation are unnecessary. The subsequent
[correlation and ratio-multiset proof](ratio-multiset-retrieval.md) derives
actual opposite correlations and actual flat-Gram ratio multisets, preserving
all repeated values, with six further independently replayed Lean audits.
The [actual reconstruction proof](phase-retrieval-alternatives.md) now
completes both opposite-block cyclic-shift/adjoint alternatives from the same
actual flat Gram hypotheses, with three further independent Lean audits.
The [connected adjoint-branch proof](adjoint-branch-cancellation.md) now
proves actual product cancellation given either genuine adjoint alternative,
with one further independent audit. The
[actual real-mode product-square theorem](real-mode-product-squares.md) now
formalizes both real-rank cases and their actual flat-triple spectral
identities, with four further independently replayed audits. Phase/shift
normalization of the both-preserving case remains before unconditional
Gram-to-product cancellation.
