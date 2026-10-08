# Actual right-character action on regular-target Ext

[LowerAlgebraRegularRightAction.lean](LowerAlgebraRegularRightAction.lean)
uses actual C-linear regular-module endomorphisms `a ↦ a*c` and genuine
Ext postcomposition to compute the right action on the exceptional
degree-two class.

For every c in the actual lower algebra, the source establishes the
whole installed multiplication formula

```
v*c = lowerCharacter(c) • v + (q * tCoordinate(c)) • z.
```

The specified z is an actual preceding boundary: `ell_0*x = z`.
Its actual `extMk` is zero. Consequently postcomposition with right
multiplication by c acts on the specified nonzero degree-two class by
the scalar `lowerCharacter(c)`. This generator statement uses a
characteristic-two field and `PowerCondition q`, without q-nonzero.
When also `q ≠ 0`, the actual Ext group is spanned by this class, so
the same formula holds for every actual degree-two Ext element.

Together with the preceding K-linear equivalence, this identifies the
action by the right f-character through explicit maps and equalities.
A separate bundled right-C-module equivalence is not constructed.
The underlying mathematical right-simple identification already appears
in the pinned OpenAI manuscript, Section 5, Lemma `res:base`.
See [ATTRIBUTION.md](../../ATTRIBUTION.md). The tensor-dual comparison,
trivial-extension derived triangle, full twenty-dimensional Ext algebra
and complete ARC remain separate.

Compile `LowerAlgebraRegularHom` and `LowerAlgebraRegularExt` first, then:

```powershell
$env:LEAN_PATH=(Get-Location).Path+';'+(Resolve-Path '..').Path
lake env lean LowerAlgebraRegularRightAction.lean
```

The separate verification record reports actual author compilation,
independent replay and the printed axiom audits. Each command must finish
successfully before the next begins.
