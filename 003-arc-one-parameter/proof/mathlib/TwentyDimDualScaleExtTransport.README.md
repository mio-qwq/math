# Canonical Ext transport along inverse dual restriction

For any commutative characteristic-two ring R, any q in R and any unit H,
let F_H be the actual left-module self-equivalence restricting scalars
along inverse dual scaling. Let S_f be the actual f-character module and
eta_H : F_H(S_f) -> S_f the actual identity-on-elements module isomorphism.

`TwentyDimDualScaleExtTransport.lean` constructs, for every natural n,
the following map on actual Mathlib self-Ext:

```text
Ext^n_A(S_f,S_f) -> Ext^n_A(S_f,S_f)

alpha |-> mk0(eta_H inverse) ; mapExactFunctor(F_H, alpha) ; mk0(eta_H).
```

The semicolons denote Yoneda composition in the displayed order.
The first zero-degree class has source S_f and target F_H(S_f), while
the last has source F_H(S_f) and target S_f. Thus both endpoints are
transported in the correct directions.

The source uses the canonical exact-functor map on Ext, without choosing
a new projective resolution. The module self-equivalence is fully
faithful, exact and preserves projective objects, so the official
projective-preservation theorem makes its Ext map bijective in every
degree. Endpoint transport has an explicit inverse obtained by swapping
the two directions of eta_H. Together they give an R-linear
self-equivalence, also retained as an R-linear map, with zero, addition,
scalar multiplication and bijectivity statements. In particular,

```text
transport_H(alpha) != 0 iff alpha != 0.
```

No field hypothesis or condition on q is needed. Degree n includes zero.
This construction establishes a linear automorphism for each fixed H
and n; compatibility with multiplication of the H parameters is a
separate coherence statement.

The companion verification JSON records actual kernel compilation,
printed axiom audits, an independent replay and the exact source hash.
After its local imports and the pinned Mathlib cache have been prepared,
direct replay from this folder is:

```powershell
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean TwentyDimDualScaleExtTransport.lean
```

The package pins Lean 4.34.1 and Mathlib commit
`d13f23b723b8a846827a245b89c10fc7d3f11612`; imported local sources require
their ignored `.olean` files in dependency order.

The construction does not yet calculate the image of the fixed actual
degree-three class. That calculation requires the exact-functor/extMk
bridge and the specified full resolution comparison. The inverse-input
cochain eigenvalue alone does not supply that Ext equality, whole-space
weights, cohomology dimensions, or the complete ARC realization.
