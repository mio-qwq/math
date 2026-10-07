# A nonzero class in actual Mathlib Ext cubed

Let R be a commutative ring of characteristic two, q an element of R,
A the actual twenty-coordinate table algebra, and M_f its actual left
f-character module. If q cubed is nonzero, then

`Ext³_A(M_f, M_f)` contains a specified nonzero element.

`FiniteFreeBarExtThree.lean` constructs that element in
`CategoryTheory.Abelian.Ext`, rather than only in a custom Hom quotient.
The element is built from the fixed actual A-linear degree-three map
and the specified all-degree Mathlib projective resolution. The proved
whole-map comparison identifies its degree-three and degree-four
differentials with the previously installed actual boundaries.

The full degree-four closure theorem gives a genuine cocycle. Mathlib's
`ProjectiveResolution.extMk_eq_zero_iff` identifies zero of the actual
Ext class with existence of an arbitrary A-linear map P2 to M_f whose
precomposition with boundary3 is the fixed cocycle. The earlier full
nonboundary theorem excludes every such map when q cubed is nonzero.
The equivalence with that whole-map boundary condition is itself proved
in this source; no comparison with a selected coefficient ansatz is used.

When R has no zero divisors, q nonzero suffices. In particular the
nonvanishing holds over every characteristic-two field at each nonzero
parameter. No assertion about the zero parameter follows from this proof.

Seven printed audits and exact source, toolchain and independent replay
records are in the verification JSON. Dependency-ordered replay is:

```powershell
.\verify-cohomology.ps1 -Targets FiniteFreeBarExtThree
```

This establishes actual Ext³ nonvanishing for the stated character
module. The stable profile, other Ext degrees, required coefficient
module vanishing and complete ARC realization remain separate obligations.
No historical priority or first formalization claim is made.
