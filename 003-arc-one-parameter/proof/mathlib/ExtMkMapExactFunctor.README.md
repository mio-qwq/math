# Mapping the specified resolution and its actual cocycle

For an additive functor, the actual Hom-complex cocycle maps component by
component. Mapping a single-target cocycle and transporting its target
through the canonical single-complex isomorphism gives the closed
single-target cocycle constructed from the mapped component.

For an exact functor preserving projective objects between abelian
categories, the file keeps the given projective resolution P and its
actual functor image Q = F.mapProjectiveResolution(P). It constructs the
full cochain-complex comparison between mapping P's zero-extension and
zero-extending Q. At every retained degree its component is the two
specified degree identifications, with the first mapped by F. Its
augmentation compatibility holds as equality of complete complex maps,
including the actual single-target comparison.

The mapped resolution cocycle is actually closed. The file also expresses
P.extMk(f) by its exact localized roof: the inverse of P's actual
augmentation, followed by the shifted morphism of the actual
single-target cocycle. The input resolution and cocycle are retained.

These intermediate interfaces support the [canonical
Ext.mapExactFunctor/extMk equality](ExtMkCanonicalFunctor.README.md),
proved in its own source. The [fixed canonical Ext cubed weight](TwentyDimDualScaleExtEigenvalue.README.md)
is a separate application. No complete ARC realization is asserted.

Actual compilation, independent source replay, printed axiom audits and
the exact source hash are recorded in the companion verification JSON.
Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets ExtMkMapExactFunctor
```
