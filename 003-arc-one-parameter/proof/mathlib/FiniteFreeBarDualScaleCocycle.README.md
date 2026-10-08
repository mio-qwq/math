# The mapped specified cocycle and its genuine Ext cubed class

Let R be any commutative characteristic-two ring, q any parameter and H
any unit. Write P for the specified all-degree free resolution of the
actual f-character module S, F_H for inverse dual-scaling restriction,
Q for F_H.mapProjectiveResolution(P), and eta for the underlying-identity
isomorphism F_H(S) to S.

The complete A-linear comparison in degree three satisfies

```text
Psi_3 ; F_H.map(fCocycle) ; eta.hom = H_inverse * fCocycle.
```

This is equality of whole actual module morphisms, proved on the full
free A-basis, with arbitrary left coefficients retained. The three-letter
word weight is derived from the whole-cochain pullback identity without
another support enumeration.

The mapped cocycle is actually closed on Q. Its actual Mathlib Ext cubed
class is constructed with Q.extMk. Using the complete resolution
comparison lifting eta.inv and official extMk naturality in both
arguments gives

```text
Ext.mk0(eta.inv) ; Q.extMk(F_H.map(fCocycle)) ; Ext.mk0(eta.hom)
  = H_inverse * fExtThree.
```

Consequently this represented class is nonzero whenever q cubed is
nonzero. No field or no-zero-divisors hypothesis is required.

The represented mapped-resolution class has not yet been identified with
canonical Ext.mapExactFunctor(F_H)(fExtThree). That final generic
exact-functor/extMk naturality bridge is still open. These theorems do not
assert the canonical fixed-class eigenvalue, a dimension or full self-Ext
profile, the tensor-square construction or complete ARC.

Actual compilation, independent source replay, printed axiom audits and
the exact source hash are recorded in the companion verification JSON.
Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets FiniteFreeBarDualScaleCocycle
```
