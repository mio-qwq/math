# The specified actual Mathlib projective resolution

`FiniteFreeBarProjectiveResolution.lean` constructs a genuine
`CategoryTheory.ProjectiveResolution` of the actual left character module
in `ModuleCat (TableAlgebra q)`.

Let R be any commutative characteristic-two ring, q any element of R,
and eps any actual R-algebra homomorphism from the table algebra to R.
The n-th term is exactly the previously exhibited finite free module
Pn, with one A-basis vector for each n-letter word on twenty labels.
The adjacent differential is exactly `recursiveBoundary q eps n`.
The degree-zero augmentation is exactly the specified character
augmentation. Component equalities are formalized explicitly.

Every positive degree is exact by the full kernel/next-range theorem.
At degree zero, exactness and surjectivity of the actual augmentation
prove the remaining quasi-isomorphism condition. Every specified term
is projective, and the actual module category is abelian. These give
the full Mathlib structure, including its genuine homology and
augmentation quasi-isomorphism fields.

The construction retains the specified terms and maps throughout.
The contraction used to prove exactness is R-linear; it is not assumed
to be an A-linear chain homotopy. An automatically selected resolution
is not substituted for this one.

Eleven printed axiom audits and exact compilation/replay records are
in the verification JSON. Dependency-ordered replay in this folder is:

```powershell
.\verify-cohomology.ps1 -Targets FiniteFreeBarProjectiveResolution
```

This is a full projective resolution of the actual character module.
The low-degree comparison and actual Ext class are separate sources;
the complete ARC homological realization remains open.
