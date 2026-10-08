# Canonical exact-functor transport of the specified Ext constructor

Let F be an exact additive functor between abelian categories with actual
Ext, preserving projective objects. For every given projective resolution
P, every natural degree n and every closed component f, this file proves

```text
Ext.mapExactFunctor(F)(P.extMk(f))
  = (F.mapProjectiveResolution(P)).extMk(F.map(f)).
```

The resolution and cocycle on the right are exactly the actual functor
image of the specified inputs. Both canonical single-complex endpoint
isomorphisms and the full mapping/zero-extension comparison are retained.

The proof first identifies the complete shifted morphism of every mapped
cocycle, in every integer degree. It then proves the shifted square for
the specified resolution cocycle. The actual canonical localized functor
map sends the augmentation and cocycle to their specified mapped
counterparts. Precomposition with the mapped augmentation is an actual
equivalence, so its injectivity cancels the two localized augmentation
inverses. Smallness is transported from HasExt through the actual
augmentation quasi-isomorphisms in the original Ext universes.

This generic theorem supplies the naturality bridge. Specific Ext weights
are computed separately; no dimension, all-degree self-Ext profile,
tensor-square realization or complete ARC theorem follows from this
constructor identity alone.

Actual compilation, independent source replay, printed axiom audits and
the exact source hash are recorded in the companion verification JSON.
Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets ExtMkCanonicalFunctor
```
