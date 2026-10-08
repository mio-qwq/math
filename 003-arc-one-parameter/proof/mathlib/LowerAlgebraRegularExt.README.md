# The actual exceptional regular-target Ext group

[LowerAlgebraRegularExt.lean](LowerAlgebraRegularExt.lean) applies the
preceding actual Hom calculation to the actual Mathlib
`ProjectiveResolution` of the lower f-character object s. Let K be a
characteristic-two field and assume

```
PowerCondition q := for every n : Nat, 1 + q^(n+1) ≠ 0.
```

The specified map represented by v is a closed actual C-linear map on
the degree-two term. Its `extMk` is a genuine nonzero element of
`Ext_C²(s,C)`. Every element in degrees zero and one is zero. These
statements do not require q to be nonzero.

If additionally `q ≠ 0`, every actual Ext element in every degree
other than two is zero, and every degree-two element is a unique scalar
multiple of the specified class. The source constructs an actual
K-linear equivalence

```
K ≃ₗ[K] Ext_C²(s,C),     lambda ↦ lambda • regularExtTwo,
```

and proves `Module.finrank K Ext_C²(s,C) = 1`. These assertions quantify
actual Mathlib Ext elements. They follow from `extMk_surjective` and the
actual boundary criterion on the specified resolution, rather than an
assumed comparison with a custom cochain quotient. The q-nonzero
assumption is retained for the complete regular-target profile.

The mathematical regular-target profile is already in the pinned OpenAI
manuscript, Section 5, Lemma `res:base`. This is its verified Lean
implementation over the actual installed objects, with the assumptions
of each statement explicit. See [ATTRIBUTION.md](../../ATTRIBUTION.md).
The right-character action is treated in
[a separate source](LowerAlgebraRegularRightAction.README.md). The
trivial-extension derived triangle, tensor-dual comparison, full Ext
algebra of the twenty-dimensional algebra and complete ARC realization
remain separate obligations.

After compiling `LowerAlgebraRegularHom` and its dependencies, run:

```powershell
$env:LEAN_PATH=(Get-Location).Path+';'+(Resolve-Path '..').Path
lake env lean -o LowerAlgebraRegularExt.olean LowerAlgebraRegularExt.lean
```

The verification record gives actual author compilation, independent
non-author replay and 14 printed axiom audits on the same frozen source.
