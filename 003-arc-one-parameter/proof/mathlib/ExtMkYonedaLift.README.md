# Actual Yoneda composition from a specified shifted resolution lift

This generic theorem works in an abelian category with actual Mathlib
Ext in the supplied universe. It retains the given projective resolutions
P of X and Q of Y, their actual augmentations, and closed components
f:P(a)->Y, g:Q(b)->Z and h:P(c)->Z with a+b=c.

A supplied whole shifted complex morphism L:P'->Q'[a] must satisfy two
explicit equalities: composing with the shifted augmentation of Q gives
the whole single-target cocycle of f, and composing with the whole
shifted cocycle of g gives that of h. Under these hypotheses,

```text
P.extMk(f).comp(Q.extMk(g)) = P.extMk(h) in Ext(X,Z,c).
```

The source proves that passing actual shifted morphisms to small
localized shifted Hom preserves composition. It then cancels the
actual Q augmentation against its localization inverse in the middle
roof. The complete comparison retains shifts, endpoints and the
original Ext universe; the necessary smallness instances are transported
through the actual augmentation quasi-isomorphisms.

The complete lift and its two equalities are mathematical hypotheses.
This source does not construct a particular bar cup-product lift, identify
the fixed class's square with a particular six-cocycle, or prove any
higher-power nonvanishing, self-Ext profile or complete ARC.

Actual compilation, independent source replay, three printed axiom audits
and the exact source hash are recorded in the companion verification JSON.
Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets ExtMkYonedaLift
```
