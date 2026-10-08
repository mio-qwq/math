# Actual lower-algebra corners and exact right maps

[LowerAlgebraResolution.lean](LowerAlgebraResolution.lean) uses the actual
lower-image subalgebra C of the installed twenty-coordinate algebra.
It constructs the genuine left C-submodules Ce={a | ae=a} and Cf={a | af=a},
their coefficient-ring bases and coordinate equivalences. The basis orders
are (e,x,y,z,t,j) and (f,u,v,n), of sizes six and four.

The C-linear maps are actual right multiplication, not assumed matrices.
For coordinates a=(a0,a1,a2,a3,a4,a5) in Ce they satisfy

```
a*u     = (0, a0, a1+a2, (1+q)*a4)                       in Cf
a*ell_n = (0, a0, q^n*a0, q^(n+1)*a1+a2, 0,
           (1+q^(n+2))*a4)                              in Ce
ell_n   = x + q^n*y
```

These whole-vector identities hold over every commutative ring of
characteristic two. The installed idempotent-support theorems and three
sparse lower multiplication columns are reused; no new full associativity
or cochain-closure enumeration is involved.

Over a field of characteristic two, the source proves

- ker(rightU)=range(rightEll_0) if 1+q and 1+q² are nonzero;
- ker(rightEll_n)=range(rightEll_(n+1)) if 1+q^(n+2) and 1+q^(n+3) are nonzero.

Every kernel element has a specified preimage. For example, for the second
identity its preimage in Ce coordinates is
(a1,0,a3,0,a5/(1+q^(n+3)),0). The proof quantifies over every n and every
actual corner vector. It does not need q itself to be nonzero.

[LowerAlgebraProjective.lean](LowerAlgebraProjective.lean) supplies actual
C-projectivity and the character augmentation.
[LowerAlgebraCategoricalResolution.lean](LowerAlgebraCategoricalResolution.lean)
assembles the specified maps as a categorical projective resolution.
The regular-target Hom cohomology and the trivial-extension derived
triangle are separate obligations.
