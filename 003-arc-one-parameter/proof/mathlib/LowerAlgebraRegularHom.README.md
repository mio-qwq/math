# Actual regular-target Hom complex over the lower algebra

[LowerAlgebraRegularHom.lean](LowerAlgebraRegularHom.lean) computes the
whole Hom complex of the specified lower-algebra resolution. Here
`C` is the actual lower subalgebra of the installed table algebra.

Evaluation at the actual idempotents gives coefficient-ring linear
equivalences

```
Hom_C(Ce,C) ≃ eC,     Hom_C(Cf,C) ≃ fC.
```

The right corners `eC` and `fC` are constructed as R-submodules, with
respective bases `(e,x,y,z,u,v)` and `(f,t,j,n)`. Their definition does
not assert that they are left C-submodules. The inverse evaluation maps
send a corner element `b` to the C-linear map `a ↦ a*b`.
Precomposition with the actual right multiplication maps becomes actual
left multiplication, giving

```
fC --u*--> eC --ell_0*--> eC --ell_1*--> eC --> ...
```

The source proves complete coordinate formulas on every input and every
natural index. The first map is injective, and the next kernel equals
its image, over every characteristic-two field and every q. Under
`q ≠ 0` and the stated nonzero factors, all subsequent kernels equal
the preceding images except at degree two. At that degree every cycle
has the form `ell_0*b + lambda*v`, and its v-coordinate determines
lambda. The specified v is not a boundary, including when q is zero.

The mathematical calculation is already in the pinned OpenAI manuscript,
Section 5, Lemma `res:base`. This source supplies actual Lean corners,
evaluation equivalences, whole maps and proofs; it does not claim a new
discovery of that calculation. See [ATTRIBUTION.md](../../ATTRIBUTION.md).
Actual Ext comparison is in [the following source](LowerAlgebraRegularExt.README.md).

After compiling `LowerAlgebraCategoricalResolution` and its dependencies,
run sequentially in this pinned Mathlib package:

```powershell
$env:LEAN_PATH=(Get-Location).Path+';'+(Resolve-Path '..').Path
lake env lean -o LowerAlgebraRegularHom.olean LowerAlgebraRegularHom.lean
```

The separate verification record gives the frozen source hash, actual
author compilation, non-author replay and 33 printed axiom audits.
