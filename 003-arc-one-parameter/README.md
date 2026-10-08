# ARC core certificate and finite resonant Yoneda and Tate algebras

The [finite realization note](finite-resonant-realization.md) constructs
actual finite triangular modules realizing the previously conditional
positive multiplication theorem over characteristic-two fields with an
infinite-order base parameter. It fixes one OpenAI two-cone target,
reconstructs its maps for arbitrary nonzero twists, and proves both
branch actions on all positive classes. Finite twist-ratio order d gives
the Veronese positive algebra plus epsilon times its positive ideal;
the epsilon ideal squares to zero and has no constant term. This is a
complete written construction proof, not a complete Lean formalization.
For finite d the module has nonzero self-Ext and is not an ARC
counterexample. Prior field-extension conclusions remain attributed.

The [full Tate algebra calculation](finite-resonant-tate-algebra.md)
now determines every integer degree and every product for this same
finite module when the twist ratio has order d>1 (necessarily odd).
Its negative diagonal part is the dual polynomial contraction module
M, with the usual Veronese local cohomology description. The complete
algebra is (R plus M) plus epsilon(R_+ plus M) plus k omega:
M and the epsilon ideal square to zero, and the exceptional degree-minus-one
omega annihilates every non-scalar homogeneous summand. Tate degree zero
is the stable scalar ring k. The proof checks both negative branch
actions and excludes hidden products at the exceptional seam; it
remains written mathematics, with the d=1 secondary products and
the complete Lean realization open.

The [scalar endomorphism construction](proof/mathlib/TwentyDimDualScaleEndomorphism.README.md)
now includes every scalar, with zero giving an actual lower-subalgebra
projection. Its actual two-sided upper kernel is square-zero, and a genuine
R-linear image/kernel splitting is constructed. This structural result
is extended by an [explicit dual construction](proof/mathlib/TwentyDimTrivialExtension.README.md):
the actual kernel is R-linearly equivalent to the lower algebra's dual
with both lower multiplication actions intertwined. The whole algebra's
split coordinates have an explicit inverse, unit and complete mixed
multiplication formula. A
[specified lower-algebra projective resolution](proof/mathlib/LowerAlgebraCategoricalResolution.README.md)
now retains the actual Cf term in degree zero, Ce in every positive
degree, right multiplication by u and ell_n, and the actual character
augmentation. Its all-degree exactness, projectivity and augmentation
quasi-isomorphism give vanishing of every positive actual self-Ext of
this lower f-character over characteristic-two fields with every
1+q^m nonzero for positive m. The subsequent
[actual regular-target Ext calculation](proof/mathlib/LowerAlgebraRegularExt.README.md)
now proves Ext_C(s,C) vanishes outside degree two, where it has a
specified K-linear parametrization and dimension one, additionally
assuming q nonzero. The
[genuine right action](proof/mathlib/LowerAlgebraRegularRightAction.README.md)
is the lower f-character action on every actual degree-two class.
These lower-algebra mathematical conclusions already appear in the
OpenAI manuscript and Tang's October 2026 discussion draft; see
[the precise provenance comparison](ATTRIBUTION.md). The implementation
here supplies actual Lean objects and proofs. The derived triangle and
full twenty-dimensional self-Ext profile remain open.

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
The general naturality theorem below now identifies this eigenvalue with
the canonical module-functor action on the fixed actual Ext class.

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
The
[specified-resolution and actual cocycle mapping interfaces](proof/mathlib/ExtMkMapExactFunctor.README.md)
now retain the complete augmentation square and exact localized extMk
roof, including every supported degree.

The [general canonical exact-functor/extMk naturality theorem](proof/mathlib/ExtMkCanonicalFunctor.README.md)
closes that identification for every degree, given resolution and closed
cocycle. Therefore the [actual canonical action on the fixed Ext cubed
class](proof/mathlib/TwentyDimDualScaleExtEigenvalue.README.md) has inverse-unit
weight, as does every scalar multiple of that class. Its image is nonzero
when q cubed is nonzero. This computes the fixed class and its scalar
multiples; it does not prove a dimension, all-degree self-Ext profile,
tensor-square realization or complete ARC.

The [actual graded Yoneda compatibility](proof/mathlib/TwentyDimDualScaleYoneda.README.md)
proves that canonical transport preserves composition in every pair of
degrees and fixes the degree-zero identity. The recursively defined
m-fold power of the fixed Ext cubed class lies in actual Ext^(3*m) and
has weight (H inverse)^m, as do its scalar multiples with the appropriate
scalar factor. The second power is proved nonzero below when q^4 is
nonzero; powers with m at least three and the all-degree self-Ext profile
remain separate.

The [actual f-character object is neither projective nor injective](proof/mathlib/TwentyDimCharacterHomologicalObstruction.README.md)
when q cubed is nonzero, using its nonzero actual third self-Ext class.
This retains arbitrary commutative characteristic-two coefficient rings;
q nonzero suffices without zero divisors. Infinite homological dimension
and nonprojectivity of the final converted ARC object remain separate.

The [all-degree actual word lift](proof/mathlib/FiniteFreeBarWordLift.README.md)
preserves every tensor coordinate and supplies a general nonboundary
test for arbitrary character Hom maps. With zero adjacent products and
zero endpoint character values, every possible preceding Hom kills the
boundary of the lifted word. Its first A-coefficient is retained before
evaluation. This alone gives no cup-product closure or higher Yoneda
nonvanishing.

The [generic actual Yoneda constructor comparison](proof/mathlib/ExtMkYonedaLift.README.md)
identifies products of specified extMk cocycles when a whole shifted
resolution lift and two full cocycle equalities are supplied. It cancels
the actual middle augmentation inverse and preserves the given Ext
universe. Constructing a particular cup-product lift and satisfying those
hypotheses remain separate from this generic theorem.

The [constructed all-degree cup lift](proof/mathlib/FiniteFreeBarCupLift.README.md)
now gives actual A-linear maps P(n+3) -> P(n) satisfying every recursive
chain identity and the augmentation identity for the fixed cocycle. Its
degree-six cup Hom is closed on all of P7. A
[six-letter witness](proof/mathlib/TwentyDimCupSquareWitness.README.md)
evaluates this Hom to q^4 and excludes every preceding A-linear Hom
boundary. Consequently its actual Ext^6 class is nonzero when q^4 is
nonzero, in particular when q is nonzero over a field or a ring without
zero divisors. The [constructed whole shifted lift](proof/mathlib/FiniteFreeBarCupShift.README.md)
now proves the actual Yoneda product identity, and the
[nonzero square theorem](proof/mathlib/TwentyDimYonedaSquare.README.md)
identifies the class with the square of fExtThree and with its defined
second power. No all-power nonvanishing or complete ARC realization
follows from this result.

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

The [resonant Yoneda-algebra note](resonant-yoneda-algebra.md) determines
the positive multiplication under explicit polynomial and branch
bimodule action hypotheses. For finite twist-ratio order d, adjoining
only the actual scalar degree-zero identity gives
`R + epsilon R_+`, where R is the dth Veronese of k[x,y], |x|=|y|=3,
|epsilon|=1 and epsilon squared is zero. The epsilon summand has no
constant term, so it introduces no Ext^1 class. The proof uses an actual
square-zero DG ideal, unique graded lifts and both branch actions;
dimensions alone do not determine this algebra. This is a written
conditional theorem with independent proof reviews, not a new Lean
verification of the concrete ARC realization or the whole Tate algebra.

- [paper.md](paper.md): definitions, proof of the abstract spectrum formula,
  proof interpretation of the finite certificate, conditional specialization,
  and remaining verification gap.
- [resonant-yoneda-algebra.md](resonant-yoneda-algebra.md): the complete
  positive multiplication proof, its additional hypotheses and exact
  degree-zero/realization boundaries.
- [finite-resonant-realization.md](finite-resonant-realization.md): finite
  objects satisfying those hypotheses, actual two-sided branch actions,
  and the F_4(t) order-three example, with separate written/Lean scope.
- [finite-resonant-tate-algebra.md](finite-resonant-tate-algebra.md): the
  full integer-graded Tate algebra of that same finite module for d>1,
  including both mixed actions, the omega seam and local cohomology model.
- [checker/verify.py](checker/verify.py): new standalone exact checker.
- [data/arc-core.json](data/arc-core.json): finite data transcribed from
  OpenAI's algebra and cochain tables, with source hashes.
- [ATTRIBUTION.md](ATTRIBUTION.md): exact upstream version and license.

Upstream source is pinned to commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
