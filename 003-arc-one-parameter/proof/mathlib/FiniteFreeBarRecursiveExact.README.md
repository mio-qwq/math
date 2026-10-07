# All-degree chain laws and exactness

`FiniteFreeBarRecursiveExact.lean` proves, for every natural number n,

`D(n).comp D(n+1) = 0` and `ker D(n) = range D(n+1)`.

Here D(n) maps P(n+1) to Pn. The augmentation is also exact at P0.
Every term is the previously proved finite free and projective left
module over the actual table algebra. The coefficient ring is any
commutative ring of characteristic two, q is arbitrary, and the
character is any actual R-algebra homomorphism.

The chain laws follow by induction from the full contraction identity:
the base uses augmentation composed with D(0) equal to zero, and
the successor uses the preceding zero composite. Every closed vector
has the explicit inserted preimage H(n+1)(v). All A-valued coefficients
are retained, and no degree bound or repeated enumeration is needed.

Six printed audits and actual compilation/independent replay records
are in the verification JSON. The source uses no added axiom, sorry
or native_decide. For dependency-ordered replay in this folder:

```powershell
.\verify-cohomology.ps1 -Targets FiniteFreeBarRecursiveExact
```

This establishes exactness of the augmented recursive module family
in every degree. A Mathlib categorical projective-resolution object,
the low-degree comparison with the installed boundaries and the Ext
application have not been constructed by this file. Full ARC remains open.
