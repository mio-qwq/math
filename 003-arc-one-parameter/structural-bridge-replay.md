# Actual dual-extension and Jacobson bridges: selected replay

Eight contributed source modules now close two specific structural interfaces
of the actual twenty-coordinate algebra. Their identical source bytes passed
an independently executed Lean 4.34.1 replay on 8 October 2026, with zero
warnings, zero errors, and 77 printed audits using only `propext`,
`Classical.choice` and `Quot.sound`. The
[machine-readable record](proof/mathlib/SelectedStructuralReplay.verification.json)
contains observed compiler times, source hashes and separate fresh audit hashes.
The original contributor records remain distinguishable from this new replay.

## Mathematical statements

For every commutative characteristic-two ring R and every q, including q=0,
[the bundled comparison](proof/mathlib/TwentyDimDualIsomorphism.README.md) is
an actual R-algebra equivalence from TableAlgebra(q) to C(q) plus its R-linear
dual, with multiplication

    (a,f)(b,g) = (ab, c ↦ g(ca)+f(bc)).

The ten-coordinate core has its actual unit and multiplication. The comparison
uses the full coordinate dual, preserves the complete product and unit, and
identifies evaluation at the core unit with the original trace. Its target is
the genuine custom `CoreDualExtension`, rather than a claim that the carrier
is literally Mathlib's `TrivSqZeroExt`.

For the actual surjection ε:TableAlgebra(q)→R×R,
[the radical bridge](proof/mathlib/TwentyDimAugmentationJacobson.README.md) proves

    J(TableAlgebra(q)) = ε⁻¹(J(R×R)).

Under the additional `[IsSemisimpleRing R]`, this is exactly ker ε: coordinates
0 and 8 vanish. The entire radical has six-factor word vanishing under that
coefficient hypothesis. The general-ring preimage formula must not be replaced
by the zero-coordinate formula without an appropriate coefficient assumption.
The proof concerns a whole nil ideal, rather than asserting that every
individual nilpotent element of a noncommutative ring lies in its radical.

The underlying trivial-extension description and the field radical statement
are prior mathematics in [OpenAI's original source](https://github.com/openai/math/blob/adc7f1241b42e322a6451854ab7e4b4c146bf78a/preprints/An-explicit-counterexample-to-the-Auslander-Reiten-conjecture-September-23-2026/build/03-algebra.tex),
Lemma `alg:T`. These implementations close formal interfaces and allow the
stated general coefficient rings. They establish neither literature-wide
novelty nor a new unconditional ARC counterexample. See [attribution](ATTRIBUTION.md).

## Replay scope and reproduction

The three radical modules are `SquareZeroJacobson`, `NilIdealJacobson`,
`TwentyDimAugmentationJacobson` (3, 4 and 8 audits). The five structural modules
are `DualTrivialExtension`, `FiniteStructureAlgebra`, `TwentyDimDualCorrespondence`,
`TwentyDimCoreAlgebra`, `TwentyDimDualIsomorphism` (13, 12, 11, 9 and 17 audits).
Previously verified published prerequisite objects were reused unchanged;
the large frozen certificates were not rerun or credited as fresh checks.
The eight newly replayed sources introduce no new finite enumeration.
This scope does not extend to unselected contributed exceptional-parameter
certificates or their complete ideal-power and socle dependency graph.

The replay used the existing pinned package at
`002-weighted-rectangular-pruning/proof/mathlib`, Lean 4.34.1 and Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`. Its actual manifest hash is in
the fresh record. Contributor manifest hashes describe the contributor's
original environment and are preserved as original evidence.

From this directory's `proof/mathlib` package, inspect or reproduce the local
dependency closure with the existing script:

```powershell
./verify-cohomology.ps1 -Targets TwentyDimAugmentationJacobson,TwentyDimDualIsomorphism -PlanOnly
./verify-cohomology.ps1 -Targets TwentyDimAugmentationJacobson,TwentyDimDualIsomorphism -FetchCache -UseExistingStd
```

The second command recompiles the full imported local Mathlib source closure
and explicitly reuses existing Std objects; it is broader than the eight-source
replay reported here. Running without `-UseExistingStd` also rebuilds imported
Std sources. A package-specific dependency cache is required; a missing pinned
Mathlib object is an environment failure, not a verified counterexample.

The trivial-extension derived triangle, the full twenty-dimensional self-Ext
profile, tensor-square realization and complete ARC remain separate Lean gaps.
No original-algebra-linear or multiplicative filtration splitting is supplied.
