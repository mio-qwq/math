# Semilinear dual scaling on the specified free complex

Let R be any commutative ring of characteristic two, let q be any element
of R, and let H be a unit of R. No field, nonzero parameter or absence of
zero divisors is required. Write A for the actual twenty-coordinate table
algebra at q and h for `dualScale q H`. The first ten coordinates are
fixed; the last ten are multiplied by H.

For a basis label i, put κ_H(i) = 1 when i < 10 and κ_H(i) = H otherwise.
For a complete n-letter word w, define

`μ_H(w) = ∏ j : Fin n, κ_H(w j)`.

The empty product is one. The product uses every letter, and its head/tail
identity is `μ_H(i::w) = κ_H(i) * μ_H(w)`. On the actual free left
A-module `Pn = (Fin n → Fin 20) → A`, the source defines

`T_n^H(v)(w) = μ_H(w) • h(v(w))`.

This transforms the complete A-valued left coefficient at every word.
It is a genuine R-linear map because h fixes the scalar algebra map. Its
actual A-semilinearity is

`T_n^H(a • v) = h(a) • T_n^H(v)`.

It does not apply a character to the coefficient in this formula. On the
specified A-basis it sends `e_w` to `μ_H(w) • e_w`; on a basis-letter
coefficient it sends `cb_i • e_w` to
`(κ_H(i) * μ_H(w)) • (cb_i • e_w)`.

The full-coordinate insertion `I_n : Pn →ₗ[R] P(n+1)` obeys

`T_(n+1)^H(I_n(v)) = I_n(T_n^H(v))`.

The proof compares actual coordinate values: h multiplies the inserted
coordinate by its head-letter weight, while the complete word weight
splits into that head weight and the tail product. The scalar left
coefficient of insertion is fixed by h.

For the specified recursive boundary `D_n : P(n+1) →ₗ[A] Pn` with the
actual f-character augmentation, every natural number n satisfies

`T_n^H(D_n(v)) = D_n(T_(n+1)^H(v))`.

In degree zero, h commutes with the f-character defect because the
f-character is fixed by h. The successor proof uses the complete
A-basis formula

`D_(n+1)(e_(i::w)) = cb_i • e_w + I_n(D_n(cb_i • e_w))`.

Insertion naturality, the preceding-degree identity and the head/tail
weight product give the next identity on each basis word. The full
A-basis expansion and A-semilinearity extend it to every vector, with
arbitrary noncommutative left coefficients. There is no finite degree
cutoff or new multiplication/cochain enumeration. The actual f-character
augmentation also satisfies `augmentation(T_0^H(v)) = augmentation(v)`,
with the underlying identity on its character-module target.

The convention in this source is **forward H**. To map the original
complex into the module complex obtained by restricting scalars along
h⁻¹, instantiate these formulas with H⁻¹. Then
`T_n^(H⁻¹)(a • v) = h⁻¹(a) • T_n^(H⁻¹)(v)` is exactly the A-linearity
required by that twisted target. A categorical comparison is a separate
source; the semilinear identities here do not calculate the canonical
Ext functor map or the eigenvalue of any Ext class. No all-degree
self-Ext dimension/profile or complete ARC statement follows from this
file alone.

The source prints ten axiom audits. Actual compilation, independent
replay, the exact source hash and the fixed Lean/Mathlib versions are
recorded in the companion verification JSON before publication. With
the local dependencies already built, a direct replay from this folder is

```powershell
$env:PATH = 'C:\Users\Administrator\.elan\bin;' + $env:PATH
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean FiniteFreeBarDualScaleSemilinear.lean
```
