# Full low-degree comparison for the recursive resolution

`FiniteFreeBarRecursiveLowDegrees.lean` proves equalities of the entire
actual A-linear maps, where D(n) maps P(n+1) to Pn:

`D(1) = boundary2`, `D(2) = boundary3`, and `D(3) = boundary4`.

The coefficient ring is any commutative characteristic-two ring, q is
arbitrary, and the character is any actual R-algebra homomorphism. These
are identities on the complete A-valued free terms. No character projection
is used to infer equality of A-valued coefficients.

The general R-linear insertion equals the previously proved first and
second R-linear contractions. In degree two it sends x times the full
pair lift of y,z to the full triple lift of x,y,z. The recursive basis
formulas then give the installed three-, four- and five-face boundaries.

Seven printed axiom audits and exact source hashes are recorded in the
verification JSON. Dependency-ordered replay in this folder is:

```powershell
.\verify-cohomology.ps1 -Targets FiniteFreeBarRecursiveLowDegrees
```

This file supplies the comparison needed to transport the fixed cocycle
to the all-degree resolution. The actual categorical resolution and Ext
interpretation are in their separate sources.
