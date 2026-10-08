# Scalar compatibility and mapping zero-extended complexes

In every linear abelian category with actual Ext, the specified
projective-resolution constructor satisfies

```text
P.extMk(r * f) = r * P.extMk(f).
```

The scalar action is the installed Ext module action. The proof uses
actual target composition and the official `extMk_comp_mk₀` theorem.

For every functor preserving zero morphisms and every embedding of
complex shapes, the file also constructs a genuine natural complex
isomorphism

```text
F.map(K.extend e) ≅ (F.map K).extend e.
```

Outside the original support it uses the canonical mapped zero-object
isomorphism. Within support its components are the two actual degree
identifications, with the first mapped by F. Differential commutation
and naturality are proved for the full complexes.

These interfaces support the [general canonical exact-functor/extMk
naturality theorem](ExtMkCanonicalFunctor.README.md), proved in its own
source with the full resolution, cocycle and endpoint comparisons.

Actual compilation, independent source replay, printed axiom audits and
the exact source hash are recorded in the companion verification JSON.
Dependency-ordered reproduction from this directory is:

```powershell
.\verify-cohomology.ps1 -Targets ExtMkExactFunctor
```
