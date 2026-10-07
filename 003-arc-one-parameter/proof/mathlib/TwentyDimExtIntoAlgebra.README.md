# All positive actual Ext groups into the regular algebra vanish

For every characteristic-two field k, every parameter q, every actual
left A-module M in the stated module category, and every positive
integer n, where A is the actual table algebra,

`Ext^n_A(M, A) = 0`.

`TwentyDimExtIntoAlgebra.lean` states this as every element of actual
`CategoryTheory.Abelian.Ext` being zero, and as the corresponding Ext
type being a subsingleton. It includes the zero parameter and all
source modules, without a finite-dimensional hypothesis on M.

The target is exactly the actual left regular module, whose action
is multiplication in A. The source imports the explicitly proved
algebraic self-injectivity, transfers it to categorical injectivity
in `ModuleCat`, and applies Mathlib's actual positive-degree Ext
vanishing theorem for injective targets. Injectivity is a proved
result of this family, rather than an additional hypothesis.

Six printed audits and exact source/compilation/independent replay
records are in the verification JSON. Dependency-ordered replay is:

```powershell
.\verify-cohomology.ps1 -Targets TwentyDimExtIntoAlgebra
```

This proves coefficient-module Ext vanishing for the actual table
algebra. It does not compute the self-Ext groups of M or establish
the tensor-square, converted module and stable-profile statements
required by the complete ARC application.
