# The specified resolution and its actual inverse-restriction comparison

Let R be a commutative characteristic-two ring, q an arbitrary parameter
and H a unit. Write A for the installed twenty-coordinate algebra,
P for the specified all-degree free resolution of the f-character
module, and F_H for restriction of A-scalars along h_H inverse.

`FiniteFreeBarDualScaleComparison.lean` uses the inverse instance of the
full semilinear scaling formula. In degree n the underlying function is

```text
Psi_n(v)(w) = (product of the H-inverse weights of all letters of w)
             times h_H_inverse(v(w)).
```

Its source is P_n and its target is F_H(P_n). The complete coefficient
semilinearity is precisely A-linearity for this restricted target. The
all-degree boundary commutation gives a genuine categorical chain map.
Its target resolution is `F_H.mapProjectiveResolution P`, keeping the
specified original terms, maps and augmentation under the actual functor.

The zero-degree augmentation square lifts the inverse of the actual
identity-on-elements character isomorphism F_H(S_f) to S_f. It gives an
actual `ProjectiveResolution.Hom`. Since both augmentations are
quasi-isomorphisms and the endpoint is an isomorphism, the complete
comparison is a quasi-isomorphism by the two-out-of-three theorem.

The generic identification of `Ext.mapExactFunctor` with the class
represented by `extMk` on the mapped resolution is a separate proof
obligation. This comparison alone does not compute the canonical action
on the fixed Ext cubed class or prove any all-degree self-Ext profile or
complete ARC statement.

Actual compilation, axiom audits, independent replay and the exact source
hash are recorded in the companion verification JSON. Dependency-ordered
reproduction from this folder is:

```powershell
.\verify-cohomology.ps1 -Targets FiniteFreeBarDualScaleComparison
```
