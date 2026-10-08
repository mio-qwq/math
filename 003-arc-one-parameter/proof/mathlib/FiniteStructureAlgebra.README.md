# Finite multiplication from structure constants

`FiniteStructureAlgebra.lean` supplies the generic unit and algebra-instance
layer above the published `FiniteBilinear.lean` and `FiniteBilinearUnit.lean`.
Let `R` be any commutative
semiring, let `ι` be any finite decidable index type, and let
`C : ι → ι → (ι → R)` be structure constants. The product is

\[
 (u v)_\ell=\sum_i\sum_j u_i v_j C_{ij\ell}.
\]

Lean proves that this product is associative on **every vector** if and only
if all structure constants satisfy

\[
 \sum_m C_{ijm} C_{mk\ell}=\sum_m C_{jkm} C_{im\ell}
 \qquad (i,j,k,\ell\in\iota).
\]

The sufficient associativity direction reuses `FiniteBilinear.mul_associative`
through `product_eq_mul`; the converse evaluates on coordinate basis vectors.
The two unit actions now reuse the published finite unit contractions through
the same product identification. The new construction bundles those results
into actual typeclass instances, a genuine basis and exact rank.
These results place no bound on scalar coefficients or polynomial degrees
and perform no finite enumeration. They apply to `R = Polynomial (ZMod 2)`.

`LeftUnitConstants` and `RightUnitConstants` alias the published two unit
equations on basis vectors. Lean transports both to our product. `Laws C` bundles these
equations with the associativity condition and the unit vector.
`Carrier L` then has an actual `Semiring`, coordinatewise `Module R`, and
`Algebra R` instance. Its multiplication is the product above, its one is
the supplied unit vector, and its scalar map is `r ↦ r • L.unit`.
The separate carrier avoids inheriting pointwise multiplication on functions.
Over a commutative ring it also has an actual `Ring` instance.
`carrierBasis` is a genuine basis of the carrier as an `R`-module; the carrier
is both free and finite, and `carrier_basis_mul` recovers `C` exactly.
With `StrongRankCondition R`, Lean proves
`Module.finrank R (Carrier L) = Fintype.card ι`.

## Scope and provenance

These are generic formalization results. They do not assert that any
particular ARC table meets `Laws C`. That next step must use the genuine
table basis semantics and the published finite certificates. Polynomial
specialization, arbitrary-field evaluation, radical identification,
Hochschild cohomology and the complete ARC realization remain separate.

The motivating basis-to-vector step is stated in OpenAI family 199,
`03-algebra.tex`, at upstream commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`; that source file has SHA-256
`f3da85912c346824c1532feb9b410e169a0b520e8261ebbea2a95e8527908af5`.
See `../../ATTRIBUTION.md`. The code here is an independent generic proof
using Mathlib's finite sums and module infrastructure; no claim of novelty,
historical priority or full ARC verification is made.

## Replay

Use this directory's unchanged `lean-toolchain` and `lake-manifest.json`:

```sh
lake exe cache get Mathlib.LinearAlgebra.StdBasis Mathlib.LinearAlgebra.Dimension.Constructions Mathlib.Algebra.Algebra.Defs
LEAN_PATH=. lake env lean -o FiniteBilinear.olean FiniteBilinear.lean
LEAN_PATH=. lake env lean -o FiniteBilinearUnit.olean FiniteBilinearUnit.lean
LEAN_PATH=. lake env lean -o FiniteStructureAlgebra.olean FiniteStructureAlgebra.lean
```

The fixed versions are Lean `4.34.1` and Mathlib
`d13f23b723b8a846827a245b89c10fc7d3f11612`.
The matching verification JSON records the source hash, actual compilation
exit code and audited declarations. All printed audits use only `propext`,
`Classical.choice` and `Quot.sound`; the source has no `sorry`, added axioms,
or `native_decide`.

## Independent replay provenance

The source and original verification/audit records above are retained from
the contributed structural proof. A separate actual independent replay on
8 October 2026 accepted the identical source bytes with exit zero, no
warnings or errors, and the printed standard-axiom audits. See the
[selected replay record](SelectedStructuralReplay.verification.json) and
[scope and reproduction note](../../structural-bridge-replay.md).
Previously verified local prerequisites were reused in that replay;
earlier prerequisite runs are not recounted as fresh checks.
