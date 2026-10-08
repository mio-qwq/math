# A constructed whole shifted lift and actual Yoneda square

For every commutative characteristic-two ring and parameter q, the
all-degree suffix maps of `FiniteFreeBarCupLift` are assembled into an
actual degree-three cocycle on the specified zero-extended cochain
resolution. The negative-degree components use the complete A-linear
maps with both actual term comparison isomorphisms; the remaining
components are zero. The full differential equation includes the shift
sign and is proved in characteristic two.

The resulting whole shifted morphism U has two proved identities:

```text
U followed by the augmentation = the fixed degree-three cocycle,
U followed by the shifted fixed cocycle = the degree-six cup cocycle.
```

These are equalities of morphisms of complete complexes. Combining them
with the generic localized Yoneda lift comparison gives

```text
fExtThree(q) composed with fExtThree(q) = extMk(cupSixHom(q)).
```

The proof retains the actual augmentation inverse, shift comparisons and
specified projective resolution. The companion `TwentyDimYonedaSquare`
adds nonvanishing from the independently proved q^4 witness. This source
alone makes no nonvanishing, dimension, all-power or complete ARC claim.

The verification JSON records actual compilation and independent replay
of the frozen source, twelve axiom audits and its SHA256. With the pinned
package and dependency artifacts installed:

```powershell
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean FiniteFreeBarCupShift.lean
```
