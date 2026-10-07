# All-vector associativity of the actual twenty-coordinate multiplication

`TwentyDimAssociativity.lean` closes the combination of the concrete table contractions and the generic bilinear extension. It defines multiplication on `Fin 20 → Polynomial (ZMod 2)` from the actual `tConstants` and proves associativity for **every polynomial vector**, rather than only basis triples.

It then evaluates the same constants through the canonical `ZMod 2` coefficient map into any commutative ring R of characteristic two, at any parameter q in R. Polynomial evaluation preserves finite sums and products, so the specialized constants satisfy the same contraction identities. The resulting multiplication on `Fin 20 → R` is associative for every three vectors, without an assumption that q is nonzero.

The concrete contraction premise is proved, not assumed. Its chain is: fixed exact table certificates and both coefficient bounds; faithful scalar/byte decoding; sparse vector-product interpretation; finite output-label contraction; generic all-vector extension. The four audits list only `propext`, `Classical.choice`, and `Quot.sound`. Independent review and recompilation also passed.

For a general ring this is a **twenty-coordinate module with the defined associative multiplication**. This source does not yet prove its unit or trace laws, install a Mathlib `Algebra` instance, construct Hochschild/Ext objects or establish the complete ARC realization. Specializing identities also does not automatically preserve nonzero witnesses.

After the supplied earlier modules and their prerequisites:

```sh
LEAN_PATH=.:.. lake env lean -o FiniteBilinear.olean FiniteBilinear.lean
LEAN_PATH=.:.. lake env lean -o FiniteTableContraction.olean FiniteTableContraction.lean
LEAN_PATH=.:.. lake env lean TwentyDimAssociativity.lean
```

On Windows keep the semicolon-separated absolute paths from BytePacking's replay instructions. Source hashes and scope are recorded in `TwentyDimAssociativity.verification.json` and `FiniteTableContraction.verification.json`.
