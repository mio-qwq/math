# An explicit split dual square-zero description of the actual algebra

Write C for the actual image subalgebra of the zero-scalar projection and
J for its actual upper kernel, viewed as an R-submodule. Over every
commutative characteristic-two ring, the source constructs

```text
J ≃ₗ[R] (C →ₗ[R] R),        A ≃ₗ[R] C × (C →ₗ[R] R).
```

The forward functional is trace against lower inputs. Its explicit inverse
extends a functional through the lower projection and applies the already
proved perfect trace inverse. The source proves that this inverse actually
lies in J and proves both inverse identities. Neither a field assumption
nor a dimension comparison is used.

Actual left and right multiplication by C are R-linear maps on J. The
equivalence intertwines them with the two dual actions:

```text
phi(c*x)(b) = phi(x)(b*c),
phi(x*c)(b) = phi(x)(c*b).
```

The order matters because C is noncommutative. For the whole algebra,
E(a)=(pi(a),phi(a)) has inverse E⁻¹(c,f)=c+dualInverse(f), sends the unit
to (1,0), and satisfies the complete multiplication formula

```text
E(a*b).1 = E(a).1 * E(b).1,
E(a*b).2(t) = E(b).2(t*E(a).1) + E(a).2(E(b).1*t).
```

Thus the actual algebra is described explicitly as a split extension by
the lower algebra's dual, with square-zero dual multiplication and both
mixed actions. The source gives these actual maps and formulas; it does
not package a separate Mathlib `TrivSqZeroExt` algebra equivalence. It also
does not construct the lower algebra's minimal resolutions or the derived
triangle required for the full self-Ext profile and ARC realization.

The verification JSON records actual compilation and independent replay
of the frozen source, zero warnings, 22 standard-axiom audits and SHA256.
With the pinned package and dependency artifacts installed, run here:

```powershell
$env:LEAN_PATH = (Get-Location).Path + ';' + (Resolve-Path '..').Path
lake env lean TwentyDimTrivialExtension.lean
```
