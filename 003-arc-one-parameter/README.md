# Exact ARC core certificate and a conditional one-parameter note

This directory contains two verified components and one explicitly conditional
application:

1. An exact polynomial certificate for the finite algebra and 179-entry
   Hochschild cochain in OpenAI family 199. The checker verifies associativity,
   the symmetric form, every radical four-word, the twisted boundary identity,
   and the explicit nonzero cycle pairing. These are identities over
   `F_2[q]`, not numerical specializations.
2. A proved abstract extension-spectrum theorem. Under the stable-profile and
   twist-action hypotheses stated in [paper.md](paper.md), the converted
   module's positive self-Ext groups have an exact multiplicative-order
   classification, including a rational generating function.
3. A **conditional application** to the upstream ARC construction: replacing
   its independent parameters by `q=t, H_1=1, H_2=t` would give a construction
   over `F_2(t)`. This application still depends on the upstream infinite
   homological realization; the finite checker does **not** verify that
   realization or prove the complete ARC counterexample.

The note does not claim mathematical priority or a newly established
unconditional counterexample to Auslander--Reiten.

[Lean kernel certificates](proof/README.md) now cover the explicit algebra tables, trace pairing, cycle, boundary data and all 104976 radical four-word closure identities. The formalization scope and remaining semantic bridges are stated there separately from the Python certificate. The final universally quantified closure theorem depends only on standard `propext`; no certificate uses `sorry`, added axioms or `native_decide`.

The additional [Mathlib semantic layers](proof/mathlib/README.md) connect the scalar codes, byte packing and sparse products to genuine polynomial vectors. The actual twenty-coordinate multiplication is associative and has the two-sided unit e+f on **all** vectors, including every specialization in an arbitrary commutative characteristic-two ring. Its trace pairing has an exact dual-coordinate formula, is symmetric and left/right nondegenerate, and satisfies invariance and cyclic trace identities. The multiplication is now packaged as a genuine unital `Ring` and `Algebra R`, with an explicit 20-element basis and dimension 20 over every characteristic-two field. The homological realization remains separate; these results do not establish the complete ARC counterexample.

## Reproduce the exact certificate

Further formalized structure includes [perfect trace duality on the actual algebra](proof/mathlib/TwentyDimFrobenius.README.md), [full-input cochain closure](proof/mathlib/CochainIdempotentClosure.README.md), and a [nonzero degree-three Hochschild cochain class](proof/mathlib/TwentyDimHochschildClass.README.md) in the actual cycles-modulo-boundaries quotient. The nonzero witness is q³, so this conclusion requires q³ to remain nonzero; over characteristic-two fields, q nonzero suffices. Both endpoint faces and all multilinear cochains are included. A comparison with Ext and the complete homological realization remain open.

The [actual algebra characters](proof/mathlib/TwentyDimCharacters.README.md)
and [independent scalar boundary obstruction](proof/mathlib/TwentyDimCharacterClass.README.md)
also give a nonzero degree-three class in the full f-character cochain
quotient when q³ is nonzero. The scalar proof excludes every actual
scalar-valued bilinear boundary and includes both endpoint actions.
The fixed class now has an actual module Ext interpretation through the
specified projective resolution described below.

The actual character module, degreewise projective left terms and full
Hom/cochain equivalences are now constructed. The displayed degree-three
module map is [closed for the actual degree-four boundary](proof/mathlib/FiniteFreeBarDegreeFour.README.md)
and [not a degree-two module-map boundary](proof/mathlib/FiniteFreeBarNonboundary.README.md)
when q³ is nonzero. All adjacent chain laws through P4 are proved, and
the map defines a [nonzero class in the actual module-Hom quotient](proof/mathlib/FiniteFreeBarHomologyThree.README.md).
The installed presentation is exact at P0, P1 and P2. An actual recursive
finite free family now has
[all-degree chain laws and exactness](proof/mathlib/FiniteFreeBarRecursiveExact.README.md).
Its [whole-map low-degree comparison](proof/mathlib/FiniteFreeBarRecursiveLowDegrees.README.md)
and [actual Mathlib projective resolution](proof/mathlib/FiniteFreeBarProjectiveResolution.README.md)
now give a [nonzero actual Ext cubed class](proof/mathlib/FiniteFreeBarExtThree.README.md)
for the actual f-character module whenever q cubed is nonzero. This
proves the stated character-module Ext nonvanishing using every actual
A-linear degree-two map. The stable two-cone profile, converted module
and remaining homological realization required for complete ARC remain open.

Over every characteristic-two field, the actual table algebra is also
[self-injective](proof/mathlib/TwentyDimSelfInjective.README.md) for every
parameter, including zero. Consequently
[all positive actual Ext groups into its left regular module vanish](proof/mathlib/TwentyDimExtIntoAlgebra.README.md)
for every source module. This coefficient-module vanishing is separate
from the self-Ext profile and converted objects in the conditional ARC application.

The [actual unit dual-scaling automorphism](proof/mathlib/TwentyDimDualScale.README.md)
fixes the e/f characters over every commutative characteristic-two ring.
The fixed scalar f-cochain has a
[full five-term coordinate formula](proof/mathlib/TwentyDimFCharacterSparse.README.md)
and its [inverse-input pullback has inverse-unit eigenvalue](proof/mathlib/TwentyDimDualScaleCochain.README.md).
These whole-cochain identities preserve full closure and nonboundary.
Identifying this eigenvalue with the canonical module-functor action on
the actual Ext class still needs the generic naturality bridge below.

The [full semilinear scaling](proof/mathlib/FiniteFreeBarDualScaleSemilinear.README.md)
commutes with every specified recursive differential. Its inverse instance
gives the [actual all-degree chain comparison](proof/mathlib/FiniteFreeBarDualScaleComparison.README.md)
into the inverse-restricted specified resolution, including its
augmentation and quasi-isomorphism. The
[actual inverse-restriction module equivalence](proof/mathlib/TwentyDimDualScaleModule.README.md)
also defines [canonical R-linear self-Ext transport in every degree](proof/mathlib/TwentyDimDualScaleExtTransport.README.md).
The [whole mapped module cocycle and its actual represented Ext cubed
class](proof/mathlib/FiniteFreeBarDualScaleCocycle.README.md) now have
inverse-unit weight after the two character endpoints are transported.
The represented class is nonzero whenever q cubed is nonzero.
[Scalar compatibility and the natural comparison for zero-extended
complexes](proof/mathlib/ExtMkExactFunctor.README.md) supply general interfaces.
Identifying the represented class with canonical functor transport still
requires a generic exact-functor/extMk naturality theorem; that remaining
equality is not asserted by these results.

Python 3.9 or later, standard library only:

```console
python checker/verify.py
python checker/verify.py --output results/verification.json
```

Expected coverage: `8000` basis triples, `104976` radical four-words,
`15250` composable four-words, `324` radical input pairs, `179` nonzero
cochain entries; cycle pairing `q^3 f`.

The [saved result](results/verification.json) states the verification scope and
records SHA-256 of the [fixed input](data/arc-core.json). Both flags concerning
verification of the complete ARC realization are deliberately `false`.

## Files and provenance

- [paper.md](paper.md): definitions, proof of the abstract spectrum formula,
  proof interpretation of the finite certificate, conditional specialization,
  and remaining verification gap.
- [checker/verify.py](checker/verify.py): new standalone exact checker.
- [data/arc-core.json](data/arc-core.json): finite data transcribed from
  OpenAI's algebra and cochain tables, with source hashes.
- [ATTRIBUTION.md](ATTRIBUTION.md): exact upstream version and license.

Upstream source is pinned to commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
