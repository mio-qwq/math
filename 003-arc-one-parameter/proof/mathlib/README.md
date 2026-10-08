# Genuine scalar polynomial semantics

`BitPolynomial.lean` connects the exact scalar operations imported from the frozen `../FiniteCore.lean` to `Polynomial (ZMod 2)` for **every natural-number code**, rather than a bounded test range.

The decoder assigns bit `i` to the coefficient of `X^i`. Lean proves:

- the decoder is injective;
- decoding XOR is polynomial addition;
- decoding twice a code is multiplication by `X`;
- with sufficient fuel, `pMulAux` is genuine polynomial multiplication;
- `decode (pMul a b) = decode a * decode b` without a bound on either input;
- consequently the encoded scalar multiplication is associative and commutative on all natural numbers.

All six printed axiom audits report only `propext`, `Classical.choice` and `Quot.sound`. The source compiled successfully with Lean 4.34.1 and the pinned Mathlib commit, without `sorry`, added axioms or `native_decide`.

This completes the **scalar** semantic bridge. It does not yet decode the eight-bit packed vectors, identify the finite multiplication table with a formal algebra instance, construct a Hochschild complex, or establish arbitrary-field Ext or the complete ARC realization. The eight Std certificates keep their original, separately documented scope. Associativity of the scalar polynomial operation also does not by itself prove associativity of the twenty-dimensional table.

The additional [BytePacking bridge](BytePacking.README.md) now supplies generic eight-bit coordinate extraction, coordinatewise XOR addition, and the exact interpretation of a single packed coefficient under its explicit `<256` bound. It does not yet interpret all table sums or construct an algebra instance; those are subsequent layers.

[TermSemantics](TermSemantics.README.md) supplies the next generic layer: arbitrary sparse-list sums, scaled sums and left/right triple products become actual polynomial vectors, with the necessary bounds on every composed coefficient. A formal finite algebra instance and the complete homological construction remain separate.

Further compiled layers are [actual table-basis associativity](TableBasisSemantics.README.md), [specialization in any commutative characteristic-two ring](ScalarEvaluation.README.md), and [generic all-vector associativity from finite structure constants](FiniteBilinear.README.md). The last theorem requires its explicit contraction premise; connecting the concrete table and installing an algebra instance remain subsequent work.

The [concrete finite contraction bridge](FiniteTableContraction.README.md) and [all-vector theorem](TwentyDimAssociativity.README.md) close that premise for the actual twenty-label table. Its defined multiplication is associative on all polynomial vectors, and on all vectors after specialization in any commutative characteristic-two ring.

The [concrete unit](TwentyDimUnit.README.md) and [trace pairing](TracePairSemantics.README.md) establish the two-sided identity, exact trace formula, symmetry and left/right nondegeneracy on all those vectors. The [general bilinear laws](FiniteBilinearLaws.README.md) supply distributivity and scalar compatibility, while [trace invariance](TraceInvariance.README.md) adds linearity and cyclic triple products.

The [actual algebra](TwentyDimAlgebra.README.md) now packages the proved multiplication as a genuine unital `Ring` and `Algebra R`, with a 20-element basis and dimension 20 over every characteristic-two field. These algebra interfaces support the cochain and actual module Ext layers below; the complete ARC realization remains open.

[Perfect trace duality](TwentyDimFrobenius.README.md) now gives an explicit linear equivalence from the actual algebra to its full R-linear dual. The [cochain basis bridge](CochainBasisSemantics.README.md) and [specialization](CochainSpecialization.README.md) turn the five-term radical-basis certificate into genuine polynomial and ring identities. The [cycle obstruction](CochainCycleSemantics.README.md) excludes every internal scalar coboundary when the q³ witness is nonzero. [Generic trilinear evaluation](FiniteTrilinear.README.md) provides the next interface for arbitrary-vector extension. These cochain statements do not yet construct a complete Hochschild or Ext complex.

The [four-linear extension](FiniteHochschild.README.md) and [actual vector cochain](TwentyDimCochain.README.md) prove the five-face identity on arbitrary vectors in the eighteen-label span. The [full-boundary obstruction](CochainFullBoundary.README.md) also accounts for both outer multiplication faces and excludes every vector-valued basis boundary when q³ is nonzero. The remaining gap is the correspondence with a complete complex and its cohomology objects, not merely checking the displayed scalar or vector identities.

[Low-degree differential composition](HochschildLowDegrees.README.md) now proves the full degree-three formula annihilates the full degree-two formula on every associative characteristic-two ring, with actual bilinear-to-trilinear packaging.

The [actual-algebra cochain](TwentyDimCochainAlgebra.README.md) is now a genuine trilinear map, with its span closure and failure to be any actual bilinear coboundary proved. The [coordinate augmentation](TwentyDimAugmentation.README.md) identifies the eighteen-label span with the kernel of a surjective ring map to R × R and proves its ambient multiplication closure.

[Characteristic two of the actual algebra](TwentyDimCharacteristic.README.md), [linear cochain differentials](HochschildCochainMaps.README.md), and the [cycles-modulo-boundaries construction](LowDegreeCohomology.README.md) support an explicit [degree-three Hochschild cochain quotient](HochschildDegreeThree.README.md). [Full-input closure](CochainIdempotentClosure.README.md) now includes both idempotents and all twenty-coordinate vectors. The [actual cochain class](TwentyDimHochschildClass.README.md) is nonzero in this full quotient whenever q³ is nonzero; over a field or a ring without zero divisors, q nonzero suffices. This does not identify a separate Ext construction or prove the complete ARC realization.

[Character-valued differentials](CharacterHochschildMaps.README.md) provide the full degree-three complex relation for every actual R-algebra character. The [actual e/f characters](TwentyDimCharacters.README.md), [full character quotient](CharacterHochschildDegreeThree.README.md), and [scalar boundary obstruction](TwentyDimCharacterClass.README.md) now give a nonzero f-character degree-three class whenever q³ is nonzero. All scalar-valued bilinear boundaries are excluded independently; no vector-to-scalar nonboundary inference is used. The homological comparison remains open.

The [positive-degree filtration](TwentyDimNilpotence.README.md) also proves
that every ordered word of at least six augmentation-kernel elements
vanishes, at every parameter over every commutative characteristic-two
ring. This is a uniform upper bound, without a sharpness or Jacobson
radical identification claim.

A [fivefold actual witness](TwentyDimNilpotenceSharp.README.md) has product
q(1+q)E, with every factor in the augmentation kernel. When q(1+q) is
nonzero, no uniform threshold at most five holds, so the word-length
vanishing threshold is exactly six. Special parameter thresholds and
Jacobson-radical identification remain separate.

The [actual character module](CharacterModule.README.md) retains compatible
R and A actions and is [simple when R is a field](CharacterModuleSimple.README.md).
The [degreewise free candidate terms](FiniteFreeBarModules.README.md) are
projective as actual left modules and in `ModuleCat`. Their
[full Hom/word-value equivalence](FiniteFreeBarHom.README.md) uses the actual
character action on coefficients. No bar differential, exactness or Ext
comparison follows merely from these degreewise constructions.

The [complete scalar cochain/word equivalences](CochainWordEquiv.README.md)
now give [actual Hom/cochain equivalences in degrees two and three](FiniteFreeBarCochains.README.md),
including a genuine A-linear lift of the fixed f-character cochain with
its q³ pairing. The [actual augmentation presentation](FiniteFreeBarAugmentation.README.md)
is surjective and exact at degree zero with an explicit kernel lift.
Full exactness in higher degrees remains open.

The actual [degree-two](FiniteFreeBarDegreeTwo.README.md),
[degree-three](FiniteFreeBarDegreeThree.README.md) and
[degree-four](FiniteFreeBarDegreeFour.README.md) boundaries now retain the
full A-linear left action and character endpoints. The degree-three
Hom precomposition agrees with the full scalar cochain differential.
The fixed lifted module map is
[closed and not a boundary](FiniteFreeBarNonboundary.README.md) when q³
is nonzero. The degree-one/degree-two adjacent chain composition is zero.
The [full bilinear pair lift](FiniteFreeBarPairLift.README.md) now proves
the degree-two/degree-three composition is zero in the entire A-valued
free module as well. The [full trilinear lift](FiniteFreeBarTripleLift.README.md)
now gives the [degree-three/four chain law](FiniteFreeBarComposition34.README.md).
Thus the actual Hom maps define an
[actual degree-three cycles/boundaries quotient with a nonzero class](FiniteFreeBarHomologyThree.README.md)
when q³ is nonzero. The explicit R-linear contraction also proves
[exactness at P1](FiniteFreeBarExactOne.README.md), including an actual
preimage for every closed vector. The next contraction proves
[exactness at P2](FiniteFreeBarExactTwo.README.md), retaining the full
A-valued coefficients.

The [all-degree coefficient insertion](FiniteFreeBarInsertion.README.md)
now defines a [recursive A-linear differential family](FiniteFreeBarRecursive.README.md).
The [full contraction identities](FiniteFreeBarRecursiveContraction.README.md)
prove its [chain laws and exactness in every degree](FiniteFreeBarRecursiveExact.README.md),
including exactness at the character augmentation. Every recursive term
is the actual finite free/projective left module. The
[whole-map low-degree equality](FiniteFreeBarRecursiveLowDegrees.README.md)
and [actual Mathlib projective resolution](FiniteFreeBarProjectiveResolution.README.md)
now retain exactly these terms, differentials and augmentation. They
interpret the fixed f-character cocycle as a
[nonzero element of actual Ext cubed](FiniteFreeBarExtThree.README.md)
when q cubed is nonzero. The zero criterion covers every actual A-linear
degree-two map. The stable profile, remaining Ext vanishing and complete
ARC realization remain separate obligations.

The actual table algebra is now proved
[self-injective over every characteristic-two field](TwentyDimSelfInjective.README.md),
for any q including zero, by an explicit extension of arbitrary A-linear
maps using its perfect symmetrizing trace. Its actual left regular
module is consequently an injective object, and
[every positive actual Ext group into it vanishes](TwentyDimExtIntoAlgebra.README.md)
for every source module. The full self-Ext profile and converted ARC
objects still require their own proofs.

For every unit H, [dual-summand scaling](TwentyDimDualScale.README.md)
is now an actual algebra automorphism with its inverse and fixed
characters proved over every commutative characteristic-two ring.
The fixed f-character cochain has an
[explicit whole-input five-term formula](TwentyDimFCharacterSparse.README.md),
and [inverse-input pullback scales it by H inverse](TwentyDimDualScaleCochain.README.md).
Full closure and exclusion of every scalar bilinear boundary are retained.
This cochain calculation does not yet identify the canonical functor
action on the actual Ext class or prove the full Ext profile.

[Full coefficient semilinear scaling](FiniteFreeBarDualScaleSemilinear.README.md)
commutes with every actual recursive differential and the augmentation.
Together with the [actual inverse-restriction module equivalence](TwentyDimDualScaleModule.README.md),
it gives an [all-degree comparison of the specified resolution](FiniteFreeBarDualScaleComparison.README.md)
with its actual functor image, as a genuine chain map and quasi-isomorphism.
The [canonical transported Ext map](TwentyDimDualScaleExtTransport.README.md)
is an R-linear self-equivalence in every degree. The
[actual class represented by the mapped specified cocycle](FiniteFreeBarDualScaleCocycle.README.md)
has inverse-unit weight after its two endpoints are transported, and is
nonzero when q cubed is nonzero. The full module morphism equality retains
arbitrary left coefficients. The
[generic scalar and zero-extension interfaces](ExtMkExactFunctor.README.md)
are also proved. Identifying this represented class with the canonical
functor image still requires the exact-functor/extMk naturality bridge.
The [specified resolution, mapped cocycle and exact localized roof
interfaces](ExtMkMapExactFunctor.README.md) establish the complete
augmentation square and the whole single-target cocycle comparison
needed for that remaining identification.

## Replay

To replay the full dependency chain for the nonzero actual cochain class,
including the Std closure sources on a fresh checkout, use:

```powershell
& '003-arc-one-parameter/proof/mathlib/verify-cohomology.ps1' -FetchCache
```

`-PlanOnly` displays the dependency order without compiling. The default
target is `TwentyDimHochschildClass`. Use `-Targets TwentyDimCharacterClass`
for the full scalar-character result. `-Targets` selects local modules
with their imported source dependencies. `-UseExistingStd` explicitly
reuses existing Std artifacts, including the large closure blocks, and
reports that their sources are not rechecked. Sources in the Mathlib
package are compiled one at a time; failures stop the script. Location and
`LEAN_PATH` are restored. A plan check is not itself a compilation result.

The generic [unit extension](FiniteBilinearUnit.README.md) now proves that left and right basis contractions suffice for a unit on all vectors, over every commutative semiring.

For the complete published semantic chain through the algebra and dimension theorem, use the dependency-ordered PowerShell script from any directory:

```powershell
& '003-arc-one-parameter/proof/mathlib/verify-semantics.ps1' -FetchCache
```

The path above is relative to the repository root. The script compiles the three required Std modules and all fourteen semantic modules, stops on the first failed command, and restores the caller's location and `LEAN_PATH`. Dependencies must be installed in this pinned Lake package; `-FetchCache` obtains the Mathlib imports. Omit that switch when they are already cached. `-UseExistingStd` explicitly reuses the three existing Std artifacts and reports that their sources were not rechecked in that run. The much larger radical closure certificate remains available through `../verify.ps1` and is not part of this algebra replay.

From this directory, obtain the selectively cached Mathlib modules and compile the imported Std source:

```sh
lake exe cache get Mathlib.Algebra.Polynomial.Coeff Mathlib.Data.ZMod.Basic Mathlib.Tactic.Ring
lean -o ../FiniteCore.olean ../FiniteCore.lean
LEAN_PATH=.. lake env lean BitPolynomial.lean
```

PowerShell equivalent for the last step:

```powershell
$previousLeanPath = $env:LEAN_PATH
try {
    $env:LEAN_PATH = (Resolve-Path '..').Path
    lake env lean BitPolynomial.lean
    if ($LASTEXITCODE -ne 0) { throw 'Lean rejected the scalar bridge.' }
} finally {
    $env:LEAN_PATH = $previousLeanPath
}
```

The package pins Mathlib, Lean and transitive dependency revisions. `.olean` and `.lake` outputs remain ignored. The bit-polynomial source data are attributed in `../../ATTRIBUTION.md`; this bridge is an additional proof about our publicly defined checker operations, using Mathlib's established polynomial and binary-digit facts. No historical priority claim is made.
