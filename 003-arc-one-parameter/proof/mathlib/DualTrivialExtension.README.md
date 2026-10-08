# The dual-action trivial extension

`DualTrivialExtension.lean` constructs the genuine extension of any ring
algebra `A` over a commutative ring `R` by its module dual `Module.Dual R A`.
Its multiplication is

\[
 (a,\phi)(b,\psi)=(ab,a\psi+\phi b),\qquad
 (a\psi)(c)=\psi(ca),\quad (\phi b)(c)=\phi(bc).
\]

Lean proves associativity, both unit actions of `(1,0)`, distributivity,
zero products and compatibility with coordinatewise scalar multiplication.
`Carrier R A` has actual `Ring`, `Module R` and `Algebra R` instances using
this multiplication. The carrier has its own type so it does not inherit
componentwise multiplication from a product type.

The linear trace is `λ(a,φ) = φ(1)`, and `tracePairing` is the actual bilinear
map `(x,y) ↦ λ(x*y)`. Lean proves

\[
 \lambda((a,\phi)(b,\psi))=\psi(a)+\phi(b),
\]

hence symmetry. `trace_nondegenerate` states the exact dual-separation
hypothesis on `A`; `trace_nondegenerate_of_free` and
`tracePairing_nondegenerate` discharge it whenever `A` is a free `R`-module.
There is no assumption of characteristic two in this generic construction.

Given any finite basis `b` of `A`, `carrierBasis b` is the genuine basis
consisting of the original vectors and their coordinate duals. The theorem
`tracePairing_basis` identifies its trace Gram matrix with the permutation
that exchanges these two groups. Under `StrongRankCondition R`,
`carrier_finrank` proves that the rank is twice the number of original basis
labels.

## Provenance and boundaries

The motivating construction and trace are in OpenAI family 199,
`03-algebra.tex`, at commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
That file's SHA-256 is
`f3da85912c346824c1532feb9b410e169a0b520e8261ebbea2a95e8527908af5`.
See `../../ATTRIBUTION.md`. These generic formal proofs use Mathlib's
linear maps, duals and bases. No priority or novelty claim is made.

This file does not identify the concrete twenty-label ARC table with this
extension, identify its radical, construct a Hochschild complex or prove
the complete ARC realization. It supplies an actual algebra and symmetric
nondegenerate trace for a future comparison map; finite packed trace checks
alone do not supply that comparison.

## Replay

From the pinned Mathlib package directory:

```sh
lake exe cache get Mathlib.LinearAlgebra.Dual.Basis Mathlib.Algebra.Algebra.Bilinear Mathlib.LinearAlgebra.FreeModule.Basic Mathlib.LinearAlgebra.Basis.Prod Mathlib.LinearAlgebra.Dimension.Constructions
lake env lean -o DualTrivialExtension.olean DualTrivialExtension.lean
```

Lean is `4.34.1`; Mathlib is
`d13f23b723b8a846827a245b89c10fc7d3f11612` with the unchanged manifest.
Compilation exited 0 without warnings. The thirteen printed audits contain
only `propext`, `Classical.choice` and `Quot.sound` (some omit choice).
The matching verification JSON fixes the source hash and exact scope.
No `sorry`, additional axiom, `native_decide` or new enumeration is used.

## Independent replay provenance

The source and original verification/audit records above are retained from
the contributed structural proof. A separate actual independent replay on
8 October 2026 accepted the identical source bytes with exit zero, no
warnings or errors, and the printed standard-axiom audits. See the
[selected replay record](SelectedStructuralReplay.verification.json) and
[scope and reproduction note](../../structural-bridge-replay.md).
Previously verified local prerequisites were reused in that replay;
earlier prerequisite runs are not recounted as fresh checks.
