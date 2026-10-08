# Scalar endomorphisms and an actual square-zero splitting

For every scalar r, including zero and nonunits, `rho(q,r)` fixes the
lower ten coordinates and multiplies the upper ten by r. These are actual
R-algebra homomorphisms on the installed table algebra over every
commutative characteristic-two ring. Composition multiplies the scalars;
the scalar one gives the identity, and units recover the existing
dual-scaling automorphisms.

The scalar zero gives an actual idempotent projection. Its image is a
subalgebra consisting exactly of vectors with upper coordinates zero.
Its two-sided kernel consists exactly of vectors with lower coordinates
zero, and any two kernel elements have product zero. The source constructs
a genuine R-linear equivalence between the algebra and the product of its
image and kernel, together with the split multiplication formula.

The proofs reuse the established multiplication-support law and include
all vectors. No new table enumeration is performed. Identification of the
kernel with the lower algebra's dual bimodule is supplied subsequently
by [the explicit dual extension construction](TwentyDimTrivialExtension.README.md).
The full self-Ext profile and complete ARC realization remain separate.

Author compilation and an independent replay of the frozen source passed
with zero warnings. Its 23 printed audits use only subsets of the standard
axioms propext, Classical.choice and Quot.sound; the weight definition
uses none. The verification JSON binds the exact source SHA256.

With the pinned package and dependency artifacts installed, run in this
directory:

```powershell
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean TwentyDimDualScaleEndomorphism.lean
```
