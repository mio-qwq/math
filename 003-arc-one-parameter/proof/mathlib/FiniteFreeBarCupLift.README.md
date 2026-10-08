# An actual cup lift in every resolution degree

For any commutative ring R of characteristic two and any parameter q,
this source constructs A-linear maps L(n): P(n+3) -> P(n) on the
specified finite free projective resolution of the actual f-character
module. On every basis word, L(n) retains its first n letters and
multiplies their basis word by the fixed scalar three-cocycle evaluated
on the final three letters. This is a map on the complete term, with
no restriction on the proposed inputs or coefficients.

The constructed maps satisfy the full recursive chain identities

```text
D(n) L(n+1) = L(n) D(n+3),  for every n >= 0,
augmentation L(0) = fCochainHom.
```

The proof uses actual R-linear coefficient insertion and the full
three-cocycle equation. The source also constructs the genuine A-linear
map `cupSixHom = fCochainHom L(3)`. On all six-letter basis words its
value is the product of the cocycle values on the first and last three
letters. Its precomposition with D(6) is zero on all of P7.

Assembly into a whole shifted cochain morphism, identification with a
Yoneda product, and nonvanishing require separate proofs. These chain
identities alone do not establish any higher Ext profile or the complete
ARC realization.

The companion verification JSON records actual compilation, independent
replay of the frozen source, eleven printed axiom audits, and its SHA256.
With the pinned package and dependency artifacts installed:

```powershell
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean FiniteFreeBarCupLift.lean
```
