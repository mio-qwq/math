# A specified all-degree lower-algebra resolution and actual self-Ext vanishing

[LowerAlgebraCategoricalResolution.lean](LowerAlgebraCategoricalResolution.lean)
constructs an actual Mathlib `ProjectiveResolution` of the lower
f-character object. Its terms and maps are the specified actual corners
and multiplication maps:

```
... -> Ce --ell_1--> Ce --ell_0--> Ce --u--> Cf -> s -> 0
```

The hypothesis is a field K of characteristic two with
1+q^(n+1)≠0 for every natural n. No q≠0 hypothesis is required for
this resolution or its positive self-Ext vanishing.

The source includes the augmented kernel/image equality, explicit
augmentation preimages, categorical exactness in every positive degree,
projectivity of every specified term and an augmentation
quasi-isomorphism. This includes degree-zero homology, rather than
assembling only an acyclic positive tail.

For every n, every element of actual Mathlib Ext_C^(n+1)(s,s) equals zero.
The proof uses `extMk_surjective` for this specified projective resolution:
every actual Ext element is represented by a cocycle on Ce, and every
C-linear map Ce→s is zero by the preceding source. It is an assertion
about genuine Ext, not just a custom cochain quotient.

This does not compute Ext_C(s,C) or identify its right-module action.
The regular-target Hom computation, the tensor-dual comparison, the
trivial-extension derived triangle and the complete polynomial
Ext algebra of the twenty-dimensional algebra remain separate. The
previously published nonzero actual Yoneda square is retained; this
source does not prove all higher powers nonzero or complete ARC.

The mathematical resolution follows the C-corner calculation in the
pinned upstream preprint, Section 5, Lemma `res:base`; see [ATTRIBUTION.md](../../ATTRIBUTION.md).
These files implement it over the actual installed algebra.

With the pinned package and its dependencies installed, compile in order:

```powershell
$env:LEAN_PATH=(Get-Location).Path+';'+(Resolve-Path '..').Path
lake env lean -o LowerAlgebraResolution.olean LowerAlgebraResolution.lean
lake env lean -o LowerAlgebraProjective.olean LowerAlgebraProjective.lean
lake env lean LowerAlgebraCategoricalResolution.lean
```

Run the commands sequentially and stop if any command fails. The separate
verification records state the actual compilation, independent replay,
source hashes and printed axiom audits for each source.
